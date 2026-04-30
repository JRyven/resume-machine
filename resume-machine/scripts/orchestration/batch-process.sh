#!/bin/bash

# Batch Process v2 - relocated to scripts/orchestration/

cd /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/ || exit 1

script_dir=$(cd "$(dirname "$0")" && pwd)

AUTO_TEMPLATE=false
DRY_RUN=false
SKIP_EXTRACT=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --auto-template)
      AUTO_TEMPLATE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --skip-extract)
      SKIP_EXTRACT=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

load_config() {
  local config_file="${1:-resume-machine/config.yaml}"
  if [ -f "$config_file" ]; then
    awk -F': ' '
      /^[[:space:]]*input_dir:/ {print "INPUT_DIR=" $2}
      /^[[:space:]]*output_dir:/ {print "OUTPUT_DIR=" $2}
      /^[[:space:]]*queue_file:/ {print "QUEUE_FILE=" $2}
      /^[[:space:]]*role_templates_dir:/ {print "ROLE_TEMPLATES_DIR=" $2}
      /^[[:space:]]*unique_data_file:/ {print "UNIQUE_DATA_FILE=" $2}
      /^[[:space:]]*candidate_name:/ {print "CANDIDATE_NAME=" $2}
      /^[[:space:]]*theme:/ {print "THEME=" $2}
    ' "$config_file" 2>/dev/null | while IFS= read -r line; do
      if [ -n "$line" ]; then
        export "$line"
      fi
    done
  fi
}

load_config

if [ -z "$INPUT_DIR" ]; then
  INPUT_DIR="$(pwd)/jobbankjobs/2026/02/22"
fi

if [ -z "$SKIP_EXTRACT" ]; then
  echo "Running extract-html-data.js with INPUT_DIR=$INPUT_DIR..."
  if ! node "$script_dir/../data_processing/extract-html-data.js" "$INPUT_DIR"; then
    echo "Error: Failed to run extract-html-data.js."
    exit 1
  fi
else
  echo "SKIP_EXTRACT set; skipping extract-html-data.js"
fi

if [ ! -f "resume-machine/resume-machine-queue.json" ]; then
  echo "Error: resume-machine/resume-machine-queue.json not found. Extraction failed."
  exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "Installing jq..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install jq || exit 1
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y jq || exit 1
    else
        echo "Error: Unsupported OS. Please install jq manually."
        exit 1
    fi
fi

echo "Running batch processing workflow (v2 with adapter)..."

json_file="resume-machine/resume-machine-queue.json"

if ! content=$(cat "$json_file" 2>/dev/null); then
  echo "Error: Failed to read $json_file."
  exit 1
fi

if [ -z "$content" ] || [ "$(echo "$content" | jq -e '.' >/dev/null 2>&1; echo $?)" != "0" ]; then
  echo "Error: $json_file is empty or not valid JSON."
  exit 1
fi

echo "Resume machine queue summary (current raw file):"
echo "$content" | jq -r '.[] | "- Title: " + (.title // "") + " | Company: " + (.company // "") + " | role-template: " + ((.["role-template"] // "(auto)") ) + " | cover-letter: " + ((.["cover-letter"] // false) | tostring) + " | generated: " + ((.generated // false) | tostring)'

if [ "$AUTO_TEMPLATE" != "true" ]; then
  read -p "Review the queue above. Press ENTER to proceed with adapter-assisted template selection (or Ctrl+C to abort)..."
fi

tmpqueue=$(mktemp)
echo "$content" | jq 'map(.["role-template"] = (.["role-template"] // "auto") | .generated = (.["generated"] // false) | .["cover-letter"] = (.["cover-letter"] // false))' > "$tmpqueue" && mv "$tmpqueue" "$json_file"

content=$(cat "$json_file")
entries=()
while IFS= read -r line; do
  entries+=("$line")
done < <(echo "$content" | jq -c '.[]')

run_correlator_if_available() {
  local job_json_path="$1"
  local correlation_output_path="$2"

  if [ ! -f "$job_json_path" ]; then
    return 1
  fi

  if [ -f "$correlation_output_path" ]; then
    return 0
  fi

  echo "  Running correlator for job JSON..."
  python "$script_dir/../data_processing/py_skill_job_correlator.py" "$job_json_path" > "$correlation_output_path" 2>/dev/null
  return $?
}

get_template_from_adapter() {
  local correlation_file="$1"

  if [ ! -f "$correlation_file" ]; then
    echo ""
    return 1
  fi

  echo "  Running adapter for template inference..."
  local template_json=$(python "$script_dir/../template_management/py_adapter_correlator_to_template.py" "$correlation_file" 2>/dev/null)

  if [ $? -eq 0 ] && [ -n "$template_json" ]; then
    echo "$template_json"
    return 0
  fi

  return 1
}

display_adapter_recommendation() {
  local template_json="$1"
  local title="$2"

  if [ -z "$template_json" ]; then
    return
  fi

  echo ""
  echo "  ╭─ Adapter Recommendation ─────────────────────────"
  echo "  │ Job: $title"
  echo "  │ Domain:    $(echo "$template_json" | jq -r '.domain_inference // "unknown"')"
  echo "  │ Languages: $(echo "$template_json" | jq -r '.featured_languages // "unknown"')"
  echo "  │ Highlights:"
  for i in {1..3}; do
    highlight=$(echo "$template_json" | jq -r ".highlight_${i} // \"\"" | sed 's/<[^>]*>//g' | cut -c1-70)
    if [ -n "$highlight" ]; then
      echo "  │   • $highlight"
    fi
  done
  echo "  ╰────────────────────────────────────────────────────"
  echo ""
}

for i in "${!entries[@]}"; do
  entry="${entries[$i]}"
  title=$(echo "$entry" | jq -r '.title')
  company=$(echo "$entry" | jq -r '.company')
  generated=$(echo "$entry" | jq -r '.generated')
  role_template=$(echo "$entry" | jq -r '."role-template"')
  cover_flag=$(echo "$entry" | jq -r '."cover-letter"')
  template_data=""

  if [ "$generated" = "true" ]; then
    echo "Skipping already-generated entry: $company - $title"
    continue
  fi

  echo ""
  echo "╔═══════════════════════════════════════════════════════════════╗"
  echo "║ Processing: $company — $title"
  echo "╚═══════════════════════════════════════════════════════════════╝"

  if [ "$role_template" = "auto" ]; then
    echo "Template mode: auto (adapter-driven)"

    correlation_file=""
    title_lower=$(echo "$title" | tr '[:upper:]' '[:lower:]')
    first_word=$(echo "$title_lower" | awk '{print $1}')

    for cf in $(find jobbankjobs -name "*correlation*.json" -type f 2>/dev/null); do
      job_title=$(jq -r '.metadata.job_title // ""' "$cf" 2>/dev/null | tr '[:upper:]' '[:lower:]')
      if echo "$job_title" | grep -q "$first_word"; then
        correlation_file="$cf"
        break
      fi
    done

    if [ -z "$correlation_file" ]; then
      echo "⚠ No correlation found; using default template"
      role_template="default"
    else
      template_data=$(get_template_from_adapter "$correlation_file")

      if [ $? -eq 0 ] && [ -n "$template_data" ]; then
        display_adapter_recommendation "$template_data" "$title"

        adapter_domain=$(echo "$template_data" | jq -r '.domain_inference // "default"')
        role_template="$adapter_domain"
        echo "✓ Using adapter-inferred template: $role_template"
      else
        echo "⚠ Adapter failed; using default template"
        role_template="default"
      fi
    fi
  else
    echo "Template mode: manual ($role_template)"
  fi

  basename=$(python "$script_dir/../utilities/naming_utils.py" "$company" "$title")
  company_doc=$(python "$script_dir/../utilities/naming_utils.py" sanitize "$company")
  title_doc=$(python "$script_dir/../utilities/naming_utils.py" sanitize "$title")
  company_file="$basename"
  title_file="$basename"

  role_file_src="resume-machine/role-based-templates/resume.${role_template}.json"
  unique_dest="resume-machine/role-based-templates/default/resume.unique-data.json"
  mkdir -p "$(dirname "$unique_dest")"
  default_role_file="resume-machine/role-based-templates/resume.defaults.json"
  if [ -f "$role_file_src" ]; then
    tmpl="$role_file_src"
  elif [ -f "$default_role_file" ]; then
    tmpl="$default_role_file"
  else
    tmpl=""
  fi

  if [ -n "$tmpl" ]; then
    tmpfile=$(mktemp)
    cover_json=$(jq -c '.cover_letter_content // null' resume-machine/resume.unique-data.json 2>/dev/null || echo null)
    if [ "$cover_flag" = "true" ] && [ "$cover_json" != "null" ]; then
      jq --arg hc "$company_doc" --arg hp "$title_doc" --argjson cover "$cover_json" '.hiring_company=$hc | .hiring_position=$hp | .cover_letter_content = $cover' "$tmpl" > "$tmpfile" && mv "$tmpfile" "$unique_dest"
    else
      jq --arg hc "$company_doc" --arg hp "$title_doc" '.hiring_company=$hc | .hiring_position=$hp | .cover_letter_content = ""' "$tmpl" > "$tmpfile" && mv "$tmpfile" "$unique_dest"
    fi
  else
    cat > "$unique_dest" <<EOF
{
  "hiring_company": "${company_doc}",
  "hiring_position": "${title_doc}"
}
EOF
  fi

  if [ -n "$template_data" ]; then
    if echo "$template_data" | jq . > /dev/null 2>&1; then
      tmpfile=$(mktemp)
      jq --argjson adapter "$template_data" '. += $adapter' "$unique_dest" > "$tmpfile" && mv "$tmpfile" "$unique_dest"
      echo "  ✓ Merged adapter template: $(echo "$template_data" | jq -r '.domain_inference // "N/A"')"
    else
      echo "  ⚠ Adapter template invalid JSON; skipping merge"
    fi
  fi

  if ! node "$script_dir/preprocess-resume.js"; then
    echo "Error: Failed to run preprocess-resume.js."
    continue
  fi

  pdf_name="resume-machine/artifacts/resume-James-Valeii-${company_file}-${title_file}.pdf"

  if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY RUN] Would generate: $pdf_name"
  else
    if resumed export resume.json -t valeii-professional -o "$pdf_name"; then
      echo "✓ Generated: $pdf_name"
      tmpqueue=$(mktemp)
      jq '.['"$i"'].generated = true' "$json_file" > "$tmpqueue" && mv "$tmpqueue" "$json_file"
    else
      echo "Error: Failed to generate PDF for $company - $title."
      continue
    fi
  fi
done

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║ Batch processing completed!"
echo "╚═══════════════════════════════════════════════════════════════╝"

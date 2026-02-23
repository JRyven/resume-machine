#!/bin/bash

# Ensure script runs from project root
cd /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/ || exit 1

# Resolve script directory
script_dir=$(cd "$(dirname "$0")" && pwd)

# Input directory for HTML extraction (can be overridden by environment)
# Default targets the specific jobbankjobs date folder; change here to use another folder.
INPUT_DIR="${INPUT_DIR:-$(pwd)/jobbankjobs/2026/02/22}"

if [ -z "$SKIP_EXTRACT" ]; then
  echo "Running extract-html-data.js with INPUT_DIR=$INPUT_DIR..."
  if ! node "$script_dir/extract-html-data.js" "$INPUT_DIR"; then
    echo "Error: Failed to run extract-html-data.js."
    exit 1
  fi
else
  echo "SKIP_EXTRACT set; skipping extract-html-data.js"
fi

# Check if the extraction was successful by verifying the output file exists
if [ ! -f "resume-machine/resume-machine-queue.json" ]; then
  echo "Error: resume-machine/resume-machine-queue.json not found. Extraction failed."
  exit 1
fi

# Ensure jq is installed
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

echo "Running batch processing workflow..."

json_file="resume-machine/resume-machine-queue.json"

# Read JSON data (robustly read whole file and check contents)
if ! content=$(cat "$json_file" 2>/dev/null); then
  echo "Error: Failed to read $json_file."
  exit 1
fi

if [ -z "$content" ] || [ "$(echo "$content" | jq -e '.' >/dev/null 2>&1; echo $?)" != "0" ]; then
  echo "Error: $json_file is empty or not valid JSON."
  exit 1
fi

# Show queue summary and require operator review of role-template before proceeding
echo "Resume machine queue summary (current raw file):"
echo "$content" | jq -r '.[] | "- Title: " + (.title // "") + " | Company: " + (.company // "") + " | role-template: " + ((.["role-template"] // "(missing)") ) + " | cover-letter: " + ((.["cover-letter"] // false) | tostring) + " | generated: " + ((.generated // false) | tostring)'

read -p "Please review resume-machine/resume-machine-queue.json and update 'role-template' for entries as needed. Ready to proceed? (Y/N) " yn
case "$yn" in
  [Yy]* ) ;;
  * ) echo "Aborted by user."; exit 1;;
esac

# Now normalize entries: ensure queue entries have required fields (`role-template`, `generated`, `cover-letter`) with defaults
tmpqueue=$(mktemp)
echo "$content" | jq 'map(.["role-template"] = (.["role-template"] // "default") | .generated = (.generated // false) | .["cover-letter"] = (.["cover-letter"] // false))' > "$tmpqueue" && mv "$tmpqueue" "$json_file"

# Reload content and entries after normalization
content=$(cat "$json_file")
entries=()
while IFS= read -r line; do
  entries+=("$line")
done < <(echo "$content" | jq -c '.[]')

# Iterate over each entry and process it
for i in "${!entries[@]}"; do
  entry="${entries[$i]}"
  title=$(echo "$entry" | jq -r '.title')
  company=$(echo "$entry" | jq -r '.company')
  generated=$(echo "$entry" | jq -r '.generated')
  role_template=$(echo "$entry" | jq -r '."role-template"')
  cover_flag=$(echo "$entry" | jq -r '."cover-letter"')

  if [ "$generated" = "true" ]; then
    echo "Skipping already-generated entry: $company - $title"
    continue
  fi

  # Sanitize company and title using the JS helper in this scripts folder (portable)
  _sanitized_lines=()
  while IFS= read -r line; do
    _sanitized_lines+=("$line")
  done < <(node "$script_dir/sanitize.js" "$company" "$title")
  company_doc="${_sanitized_lines[0]:-}"
  title_doc="${_sanitized_lines[1]:-}"
  company_file="${_sanitized_lines[2]:-}"
  title_file="${_sanitized_lines[3]:-}"

  # Copy role-based template into resume.unique-data.json and inject company/title
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
    # prepare cover content: read default cover content (object) from resume.unique-data.json
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

  # Run preprocess-resume.js (in this scripts folder)
  if ! node "$script_dir/preprocess-resume.js"; then
    echo "Error: Failed to run preprocess-resume.js."
    exit 1
  fi

  # Generate PDF
  pdf_name="artifacts/resume-James-Valeii-${company_file}-${title_file}.pdf"
  if resumed export resume.json -t valeii-professional -o "$pdf_name"; then
    # mark this entry as generated=true in the queue
    tmpqueue=$(mktemp)
    jq '.['"$i"'].generated = true' "$json_file" > "$tmpqueue" && mv "$tmpqueue" "$json_file"
  else
    echo "Error: Failed to generate PDF for $company - $title."
    exit 1
  fi
done

echo "Batch processing completed successfully."

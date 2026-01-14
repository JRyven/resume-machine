#!/bin/bash

# Navigate to project root
cd /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/ || exit 1

# Step 1: Extract data from HTML files using Puppeteer
echo "Running extract-html-data.js..."
if ! node scripts/extract-html-data.js; then
  echo "Error: Failed to run extract-html-data.js."
  exit 1
fi

# Check if the extraction was successful by verifying the output file exists
if [ ! -f "preprocess-batch-export-resume.json" ]; then
  echo "Error: preprocess-batch-export-resume.json not found. Extraction failed."
  exit 1
fi

# Step 2: Install jq (if it's not already installed)
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

# Step 3: Process the extracted data and generate PDFs
echo "Running batch processing workflow..."

# Path to JSON file
json_file="preprocess-batch-export-resume.json"

# Read JSON data (robustly read whole file and check contents)
if ! content=$(cat "$json_file" 2>/dev/null); then
  echo "Error: Failed to read $json_file."
  exit 1
fi

if [ -z "$content" ] || [ "$(echo "$content" | jq -e '.' >/dev/null 2>&1; echo $?)" != "0" ]; then
  echo "Error: $json_file is empty or not valid JSON."
  exit 1
fi

entries=()
while IFS= read -r line; do
  entries+=("$line")
done < <(echo "$content" | jq -c '.[]')

# Iterate over each entry and process it
for entry in "${entries[@]}"; do
  title=$(echo "$entry" | jq -r '.title')
  company=$(echo "$entry" | jq -r '.company')

    # Sanitize company and title for document and filename using JS helper
    readarray -t _sanitized_lines < <(node scripts/sanitize.js "$company" "$title")
    company_doc="${_sanitized_lines[0]:-}"
    title_doc="${_sanitized_lines[1]:-}"
    company_file="${_sanitized_lines[2]:-}"
    title_file="${_sanitized_lines[3]:-}"

  # Configure resume.defaults.json with sanitized, title-cased values for use inside documents
  cat > resume.defaults.json <<EOF
{
  "hiring_company": "${company_doc}",
  "hiring_position": "${title_doc}"
}
EOF

  # Run preprocess-resume.js
  if ! node scripts/preprocess-resume.js; then
    echo "Error: Failed to run preprocess-resume.js."
    exit 1
  fi

  # Generate PDF (use sanitized filename-safe values)
  pdf_name="artifacts/resume-${company_file}-${title_file}.pdf"
  resumed export resume.json -t valeii-professional -o "$pdf_name" || {
    echo "Error: Failed to generate PDF for $company - $title."
    exit 1
  }
done

echo "Batch processing completed successfully."

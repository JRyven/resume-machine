#!/bin/bash
# Integration example: How to use the adapter in batch-process.sh
#
# This shows how to inject the adapter into the existing batch processing
# workflow to automate template selection based on skill-job correlation.
#
# To use:
#   1. Review this file
#   2. Copy the relevant sections into batch-process.sh
#   3. Adjust paths/naming as needed

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1: Import and add adapter logic after job extraction
# ════════════════════════════════════════════════════════════════════════════════

# In batch-process.sh, after running extract-html-data.js, for each queue entry:

# Pseudocode in batch-process.sh:
# ```bash
# for i in "${!entries[@]}"; do
#   entry="${entries[$i]}"
#   title=$(echo "$entry" | jq -r '.title')
#   company=$(echo "$entry" | jq -r '.company')
#   generated=$(echo "$entry" | jq -r '.generated')
#   
#   if [ "$generated" = "true" ]; then
#     continue
#   fi
#   
#   # ── NEW: Adapter section ───────────────────────────────────────────────────
#   # Check if we have a corresponding job JSON file
#   job_json_file=$(find jobbankjobs -name "*${title}*" -type f 2>/dev/null | head -1)
#   
#   # If job JSON exists, run correlator and adapter
#   if [ -n "$job_json_file" ]; then
#     # Run correlator to generate correlation data
#     correlation_file="${job_json_file%.json}_correlation.json"
#     if [ ! -f "$correlation_file" ]; then
#       python resume-machine/scripts/py_skill_job_correlator.py "" "$job_json_file" > "$correlation_file"
#     fi
#     
#     # Run adapter to generate template
#     if [ -f "$correlation_file" ]; then
#       template_json=$(python resume-machine/scripts/py_adapter_correlator_to_template.py "$correlation_file")
#       
#       # Merge template into resume.unique-data.json
#       # Assuming jq is available (already required in batch-process.sh)
#       unique_dest="resume-machine/role-based-templates/default/resume.unique-data.json"
#       if [ -n "$template_json" ]; then
#         tmpfile=$(mktemp)
#         # Read existing defaults
#         defaults=$(jq -c '.cover_letter_content // null' "$unique_dest" 2>/dev/null || echo null)
#         # Merge template with defaults
#         jq --argjson template "$template_json" \
#            --arg company "$company" \
#            --arg title "$title" \
#            --argjson cover "$defaults" \
#            '.hiring_company = $company |
#             .hiring_position = $title |
#             .cover_letter_content = (if $cover != null then $cover else "" end) |
#             . += $template' \
#           "resume-machine/role-based-templates/resume.defaults.json" \
#           > "$tmpfile" && mv "$tmpfile" "$unique_dest"
#       fi
#     fi
#   fi
#   # ── END: Adapter section ───────────────────────────────────────────────────
#   
#   # ... rest of existing batch-process.sh logic (preprocess, PDF export, etc.)
# done
# ```

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2: Standalone orchestration (simpler alternative)
# ════════════════════════════════════════════════════════════════════════════════

# If you prefer a simpler approach, use the orchestration script directly:
# 
# Loop through correlation files and process each:
# ```bash
# for correlation_file in jobbankjobs/**/*correlation*.json; do
#   echo "Processing: $correlation_file"
#   python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py "$correlation_file"
# done
# ```

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3: Example workflow (from command line)
# ════════════════════════════════════════════════════════════════════════════════

# Step 1: Extract job postings (existing flow)
# node resume-machine/scripts/extract-html-data.js jobbankjobs/2026/04/05

# Step 2: Run skill-job correlations (existing)
# python resume-machine/scripts/py_skill_job_correlator.py

# Step 3: For each correlation, run adapter → orchestration (NEW)
correlation_file="jobbankjobs/2026/04/05/correlation_software_developer_kanata.json"

# Option A: Dry-run preview
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py "$correlation_file" --dry-run

# Option B: Actually generate resume + PDF
# python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py "$correlation_file"

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 4: Error handling & validation
# ════════════════════════════════════════════════════════════════════════════════

validate_adapter_output() {
  local correlation_file="$1"
  
  if [ ! -f "$correlation_file" ]; then
    echo "ERROR: Correlation file not found: $correlation_file"
    return 1
  fi
  
  # Run adapter and validate output is valid JSON
  local output=$(python resume-machine/scripts/py_adapter_correlator_to_template.py "$correlation_file" 2>&1)
  local exit_code=$?
  
  if [ $exit_code -ne 0 ]; then
    echo "ERROR: Adapter failed: $output"
    return 1
  fi
  
  # Validate JSON
  echo "$output" | jq . > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "ERROR: Adapter output is not valid JSON"
    return 1
  fi
  
  echo "✓ Validation passed"
  return 0
}

# Usage:
validate_adapter_output "jobbankjobs/2026/04/05/correlation_software_developer_kanata.json"

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5: Metrics & logging
# ════════════════════════════════════════════════════════════════════════════════

log_adapter_execution() {
  local correlation_file="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  local adapter_output=$(python resume-machine/scripts/py_adapter_correlator_to_template.py "$correlation_file")
  
  # Log to structured JSON
  cat >> logs/adapter-executions.json <<EOF
{
  "timestamp": "$timestamp",
  "correlation_file": "$correlation_file",
  "domain_inference": "$(echo "$adapter_output" | jq -r '.domain_inference')",
  "featured_languages": "$(echo "$adapter_output" | jq -r '.featured_languages')",
  "job_title": "$(echo "$adapter_output" | jq -r '.job_title')"
}
EOF
}

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 6: Parallel processing (for multiple correlations)
# ════════════════════════════════════════════════════════════════════════════════

# Process multiple correlation files in parallel (using GNU parallel or xargs)
# This speeds up batch operations:

# Using xargs:
# find jobbankjobs -name "*correlation*.json" | \
#   xargs -I {} -P 4 \
#   python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py {}

# Or using GNU parallel:
# find jobbankjobs -name "*correlation*.json" | \
#   parallel -j 4 \
#   python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py {}

# ════════════════════════════════════════════════════════════════════════════════
# NOTES
# ════════════════════════════════════════════════════════════════════════════════
#
# 1. The adapter reads correlation JSON and infers the best domain
# 2. It generates domain-specific highlights based on LEAD_STRENGTH skills
# 3. Template data is merged with resume defaults before preprocessing
# 4. The existing pipeline handles the rest: preprocess → resume.json → PDF
#
# 5. To extend with new domains:
#    - Add domain pattern to py_adapter_correlator_to_template.py
#    - Update DOMAIN_PATTERNS dict
#    - Optional: add resume.{domain}.json template file
#
# 6. Integration points:
#    - Direct: Use in batch-process.sh within job loop
#    - Orchestrated: Run separately after all correlations complete
#    - Standalone: Use py_orchestrate_correlation_to_pdf.py directly

# Resume Machine - Orchestration Script

This repository contains the tools to automatically generate PDF resumes from job correlation data using the resume-machine workflow.

## Orchestration Script

The `py_orchestrate_correlation_to_pdf.py` script automates the complete workflow from correlation JSON to PDF generation:

1. Runs the adapter to infer domain + template data from correlation JSON
2. Merges the template data into `resume.unique-data.json`
3. Runs `preprocess-resume.js` to produce `resume.json`
4. Exports PDF via `resumed` CLI

### Usage

```bash
# Generate PDF from correlation file
python scripts/py_orchestrate_correlation_to_pdf.py <correlation_file.json>

# Dry run to preview steps without generating PDF
python scripts/py_orchestrate_correlation_to_pdf.py <correlation_file.json> --dry-run

# Specify candidate name and template
python scripts/py_orchestrate_correlation_to_pdf.py <correlation_file.json> --name "John Doe" --template "my-template"

# Using environment variables (fallbacks)
export RESUME_NAME="John Doe"
export RESUME_THEME="my-template"
python scripts/py_orchestrate_correlation_to_pdf.py <correlation_file.json>
```

### Features

- **End-to-end automation**: Complete workflow from correlation to PDF
- **Dry-run mode**: Preview steps without generating PDF
- **Flexible naming**: Custom candidate names and templates
- **Environment variable support**: Fallbacks for name and template
- **Error handling**: Graceful error handling and reporting

### Requirements

- Python 3.6+
- Node.js
- `resumed` CLI tool installed
- `py_adapter_correlator_to_template.py` and `preprocess-resume.js` scripts

### Example

```bash
python scripts/py_orchestrate_correlation_to_pdf.py jobbankjobs/2026/04/05/correlation_web_developer_saint_antoine_abbe.json
```

This will generate a PDF at `artifacts/resume-James Valeil-web-developer-saint-antoine-abbe-.pdf`.

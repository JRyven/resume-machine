# JSON Resume Theme: Valeii Professional

A minimal, ATS-friendly theme for JSON Resume, optimized for professional use with clean typography and layout.

 **Typography**: Uses only web-safe, ATS-friendly fonts: Arial, Helvetica, sans-serif for headings; Calibri, Arial, sans-serif for body text.

 **ATS-Ready Fonts**: No custom or local fonts required; all fonts are web-safe and render consistently across platforms.
- **Layout**: Clean, professional design with proper spacing
- **ATS-Friendly**: Structured for applicant tracking systems
- **Minimal Noise**: Focus on content without distractions
- **Offline Ready**: Uses local fonts for consistent rendering without external dependencies

## Font Requirements

## Font Requirements

This theme includes specialized Noto fonts locally for offline rendering and CI/CD stability:

## Font Usage

This theme uses only web-safe, ATS-friendly fonts:

- **Headings (h1, h2, h3):** Helvetica, Arial, sans-serif
- **Body text (p, li, etc):** Calibri, Arial, sans-serif
- **Meta/italic text:** Times New Roman, Times, serif (for .italic class)

No custom or local fonts are required. All fonts are available by default on major operating systems and browsers, ensuring consistent rendering and maximum compatibility with applicant tracking systems (ATS).

Fonts are loaded via CSS `@font-face` declarations and do not require internet access.

## Installation

### Via NPM (Global)
```bash
npm install -g valeii-professional
```

### In Monorepo
This theme is included in the JSON Resume monorepo at `packages/themes/jsonresume-theme-valeii-professional/`.

## Usage

### With resumed CLI
```bash
resumed export resume.json -t valeii-professional -o output.pdf
```

### In JSON Resume Registry
Select "valeii-professional" from the theme dropdown in the web editor.

## Development

### Building
```bash
pnpm turbo run build --filter=jsonresume-theme-valeii-professional
```

### Testing
Test with sample resume data:
```bash
resumed export resume-machine/artifacts/resume.json -t valeii-professional -o test.pdf
```

## Schema Support

Renders the following JSON Resume fields:
- `basics`: name, label, email, phone, location.city, summary
- `work[]`: company, position, startDate, endDate, highlights[]
- `skills[]`: name, keywords[]

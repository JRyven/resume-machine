dz# JSON Resume Theme: Valeii Professional

A minimal, ATS-friendly theme for JSON Resume, optimized for professional use with clean typography and layout.

## Features

- **Typography**: Noto Serif Display font family (local fonts included)
- **Layout**: Clean, professional design with proper spacing
- **ATS-Friendly**: Structured for applicant tracking systems
- **Minimal Noise**: Focus on content without distractions
- **Offline Ready**: Uses local fonts for consistent rendering without external dependencies

## Font Requirements

## Font Requirements

This theme includes specialized Noto fonts locally for offline rendering and CI/CD stability:

- `fonts/Noto_Serif_Hentaigana/static/NotoSerifHentaigana-Medium.ttf` (Headers - h1, h2, h3)
- `fonts/Noto_Sans_Cypro_Minoan/NotoSansCyproMinoan-Regular.ttf` (Body text - p elements)
- `fonts/Noto_Serif_Display/static/NotoSerifDisplay-Italic.ttf` (Meta text - dates, contact info)

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
resumed export artifacts/resume.json -t valeii-professional -o test.pdf
```

## Schema Support

Renders the following JSON Resume fields:
- `basics`: name, label, email, phone, location.city, summary
- `work[]`: company, position, startDate, endDate, highlights[]
- `skills[]`: name, keywords[]

## License

MIT

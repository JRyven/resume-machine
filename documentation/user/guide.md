---
project_name: JSON Resume
title: User Guide
description: How to use the JSON Resume platform to create, edit, and export professional resumes.
last_updated: 2025-12-18
cleardoc_version: 2.3.0
keywords: [user-guide, resume, json-resume, themes, export]
---

# User Guide

This guide helps you get started with the JSON Resume platform. Learn to create professional resumes using JSON data and customizable themes.


## Launch

To preview your theme edits locally in the browser (http://localhost:3001):

1. **Install dependencies (if not done):**
```bash
pnpm install
```

2. **Build your theme (if you made changes):**
```bash
pnpm turbo run build --filter=valeii-professional
```

3. **Start the registry app:**
```bash
pnpm turbo run dev --filter=registry
```

or, if you have a script:
```bash
pnpm dev --filter=registry
```

4. **Open your browser and go to:**
[http://localhost:3001](http://localhost:3001)

You can now preview your resume and theme changes live. Any edits to your theme will require a rebuild and a browser refresh to see updates.

## Generate PDF Resume
```
resumed artifacts/resume.json --theme ./themes/valeii-professional -o artifacts/baseline-valeii-professional.pdf
```

---

## Getting Started

### Accessing the Platform

- **Online:** Visit [registry.jsonresume.org](https://registry.jsonresume.org) for the hosted version.
- **Local Development:** For contributors, clone the repo and run `pnpm turbo dev --filter=registry` to start locally at http://localhost:3001.

### Account Setup

1. Sign up or log in using GitHub, Google, or email.
2. Verify your email if required.
3. Access your dashboard to manage resumes.

---

## Creating a Resume

### Using the Editor

1. Navigate to the editor from your dashboard.
2. Fill in sections: Basics (name, contact), Work Experience, Education, Skills, etc.
3. Use the JSON editor for advanced users or import existing JSON Resume data.
4. Save drafts automatically.

### Resume Structure

Follow the JSON Resume schema:

- **Basics:** Name, label, email, phone, location, profiles.
- **Work:** Position, company, dates, highlights.
- **Education:** Institution, area, dates.
- **Skills:** Name, level, keywords.
- **Projects, Awards, Publications:** As needed.

---

## Choosing Themes

### Available Themes

Select from 50+ themes like Professional, Modern Classic, and Creative Studio. Each theme renders your resume differently.

### Customizing Themes

- Preview themes before selecting.
- Some themes support custom colors or layouts via theme options.
- For developers: Create new themes in `packages/themes/` following the theme API.

### Theme Recommendations

- **ATS-Friendly:** Professional, Modern Classic for applicant tracking systems.
- **Creative:** Coastal Creative, Writers Portfolio for design roles.
- **Minimal:** Nordic Minimal, Flat for clean looks.

---

### Advanced Theming

To modify or clone the CV template (the valeii-professional theme), you'll work with the theme files in the monorepo's themes directory. Here's how:

#### Modifying the Existing Template

Primary File to Edit: index.js

This file contains the render function that generates the HTML template. It uses resume data to build sections like header, experience, and skills. Edit this to change styling, layout, or content rendering.

#### Supporting Files:

- package.json - Update name/version if needed
- README.md - Update documentation

#### Cloning and Modifying the Template

To create a new theme based on valeii-professional:

1. Copy the Theme Directory:

```
cp -r packages/themes/jsonresume-theme-valeii-professional packages/themes/jsonresume-theme-your-new-name
```

2. Update Package Details:
- Edit package.json:
    - Change "name" to "jsonresume-theme-your-new-name"
    - Update "description" and "version"

3. Modify the Template:
- Edit index.js to customize the HTML/CSS output
- Update README.md with new theme details

4. Integrate into the App:
- Add the new theme to themeConfig.js (import and add to THEMES object)
- Rebuild: pnpm build

5. Test the New Theme:

```
resumed export artifacts/resume.json -t your-new-name -o test.pdf
```

#### Key Template Structure
The index.js file builds HTML with:

- Header Section: Name, contact info, summary
- Experience Section: Work history with dates and highlights
- Skills Section: Categorized skills as inline tags
- Styling: Embedded CSS with EB Garamond fonts and responsive design

For major changes, reference the JSON Resume theme API or existing themes in themes. Let me know if you need help with specific modifications!

---

## Exporting Resumes

### Export Formats

- **PDF:** High-quality, printable version.
- **HTML:** Web-friendly, embeddable.
- **JSON:** Raw data for backup or reuse.

### Export Steps

1. Select your resume in the dashboard.
2. Choose a theme.
3. Click "Export" and select format.
4. Download or share the link.

### PDF Rendering

Uses Puppeteer for accurate PDF generation. Ensure your resume data is valid JSON Resume format.

---

## Troubleshooting

### Common Issues

**Resume not rendering:**

- Validate JSON against the schema at [jsonresume.org/schema](https://jsonresume.org/schema).
- Check for missing required fields.

**Theme not loading:**

- Ensure theme is selected correctly.
- For custom themes, verify installation.

**Export failing:**

- Check browser console for errors.
- Try a different theme or format.

**Login issues:**

- Clear cookies and try again.
- Use a different authentication method.

### Getting Help

- Check the [FAQ](#faq) below.
- Report issues at [GitHub Issues](https://github.com/jsonresume/registry/issues).
- Join the community on [Discord](https://discord.gg/jsonresume).

---

## FAQ

**Q: What is JSON Resume?**
A: A standard for resume data in JSON format, making resumes portable and themeable.

**Q: Can I import my LinkedIn profile?**
A: Not directly, but you can manually enter data or use third-party tools to convert.

**Q: Are resumes private?**
A: Public resumes are shareable; private ones are only visible to you.

**Q: How do I contribute a theme?**
A: Follow the theme development guide in the docs, then submit a PR.

**Q: Is the platform free?**
A: Yes, open-source and free to use.

---

## Related Documentation

- [README](../../README.md): Project overview.
- [Schema](https://jsonresume.org/schema): JSON Resume specification.
- [Theme Development](../development/themes.md): For creating custom themes.

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

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating a Resume](#creating-a-resume)
3. [Choosing Themes](#choosing-themes)
4. [Exporting Resumes](#exporting-resumes)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

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

2. [Step 2]
3. [Step 3]

**Expected Result:** Describe what should happen after completing the task.

### Best Practices

- **[Practice 1]:** Explanation
- **[Practice 2]:** Explanation
- **[Practice 3]:** Explanation

---

## Troubleshooting

### Common Issues

#### Issue 1: [Problem Description]

**Symptoms:** How to identify this issue.

**Solution:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Prevention:** How to avoid this issue in the future.

#### Issue 2: [Problem Description]

**Symptoms:** How to identify this issue.

**Solution:**

1. [Step 1]
2. [Step 2]
3. [Step 3]

**Prevention:** How to avoid this issue in the future.

### Error Messages

**Error: [Error Message]**

- **Cause:** Explanation of what causes this error
- **Solution:** Steps to resolve the error

---

## FAQ

**Q: [Common Question]**
A: [Answer]

**Q: [Common Question]**
A: [Answer]

**Q: [Common Question]**
A: [Answer]

---

## Support

### Getting Help

- **Documentation:** Start with this guide and the [README](../../README.md)
- **Issue Tracker:** Report bugs or request features at [ISSUE_TRACKER_URL]
- **Community:** Join discussions at [COMMUNITY_URL]
- **Email:** Contact support at [SUPPORT_EMAIL]

### Reporting Bugs

When reporting bugs, please include:

1. Application version
2. Operating system and version
3. Steps to reproduce the issue
4. Expected vs. actual behavior
5. Screenshots or error messages (if applicable)

---

## Related Documentation

- [README](../../README.md): Project overview and quick start
- [Development Guide](../development/abstract.md): For contributors and developers

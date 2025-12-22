// Minimal theme renderer for resumed. Returns a simple, ATS-friendly HTML.
export const render = function(resume, options) {
  const basics = resume.basics || {};
  const name = basics.name || '';
  const label = basics.label || '';
  const email = (basics.email) ? `<a href="mailto:${basics.email}">${basics.email}</a>` : '';
  const phone = basics.phone || '';
  const location = basics.location ? (basics.location.city || '') : '';

  const summary = resume.basics && resume.basics.summary ? resume.basics.summary : '';

  const experience = (resume.work || []).map(w => {
    const title = w.position || '';
    const company = w.company || '';
    const start = w.startDate || '';
    const end = w.endDate || 'Present';
    const bullets = (w.highlights || [])
      .map(h => `<li>${h}</li>`).join('');
    return `<section class="work"><h3>${title} — ${company}</h3><time>${start} — ${end}</time><ul>${bullets}</ul></section>`;
  }).join('');

  const skills = (resume.skills || []).map(s => `<li>${s.name}: ${(s.keywords||[]).join(', ')}</li>`).join('');

  const html = `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>${name} — Resume</title>
  <style>
    /* Local Noto fonts */
    @font-face {
      font-family: 'Headers - Noto Serif Hentaigana';
      src: url('fonts/Noto_Serif_Hentaigana/static/NotoSerifHentaigana-Medium.ttf') format('truetype');
      font-weight: 500;
      font-style: normal;
      font-display: swap;
    }

    @font-face {
      font-family: 'Body - Noto Sans Cypro Minoan';
      src: url('fonts/Noto_Sans_Cypro_Minoan/NotoSansCyproMinoan-Regular.ttf') format('truetype');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }

    @font-face {
      font-family: 'Italic - Noto Serif Display';
      src: url('fonts/Noto_Serif_Display/static/NotoSerifDisplay-Italic.ttf') format('truetype');
      font-weight: 400;
      font-style: italic;
      font-display: swap;
    }

    body {
      font-family: 'Body - Noto Sans Cypro Minoan', sans-serif;
      color: #111;
      margin: 36px;
      line-height: 1.35;
    }

    h1, h2, h3 {
      font-family: 'Headers - Noto Serif Hentaigana', serif;
    }

    p {
      font-family: 'Body - Noto Sans Cypro Minoan', sans-serif;
    }

    time, .meta, .contact {
      font-family: 'Italic - Noto Serif Display', serif;
      font-style: italic;
    }

    header {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 12px;
    }

    .head-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }

    h1 {
      font-size: 30px;
      margin: 0;
    }

    .meta {
      font-size: 12px;
      color: #333;
      margin-top: 6px;
    }

    .summary {
      background: transparent;
      border-left: 3px solid #eee;
      padding-left: 12px;
      margin-top: 8px;
      color: #222;
    }

    main {
      margin-top: 10px;
    }

    h2 {
      font-size: 14px;
      margin: 18px 0 6px 0;
      color: #111;
      letter-spacing: 0.2px;
    }

    section {
      margin-top: 6px;
    }

    .work h3 {
      font-size: 15px;
      margin: 0;
    }

    time {
      display: block;
      font-size: 12px;
      color: #666;
      margin-bottom: 6px;
    }

    ul {
      margin: 6px 0 0 18px;
    }

    li {
      margin-bottom: 6px;
    }

    .skills-list {
      display: block;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .skills-list li {
      display: inline-block;
      background: #f3f3f3;
      padding: 4px 8px;
      margin: 4px;
      border-radius: 4px;
      font-size: 12px;
    }

    .contact {
      font-size: 12px;
      color: #333;
    }

    @media print {
        @page {
            margin: 20mm 15mm;
        }

        body {
            margin: 0;
        }

        h2 {
            page-break-after: avoid;
        }
    }
  </style>
</head>
<body>
  <header>
    <div class="head-top">
      <div>
        <h1>${name}</h1>
        <div class="contact">${label}${label?'<br/>':''}${email}${phone?'<br/>':''}${phone}${location?'<br/>':''}${location}</div>
      </div>
    </div>
    ${summary?`<div class="summary"><strong>Summary</strong><p style="margin:6px 0 0 0">${summary}</p></div>`:''}
  </header>

  <main>
    <h2>Experience</h2>
    ${experience || '<p>No experience provided.</p>'}

    <h2>Skills</h2>
    ${skills ? `<ul class="skills-list">${skills}</ul>` : '<p>No skills listed.</p>'}
  </main>
</body>
</html>`;

  return html;
};

// HELPER AND CONSTANTS

// STYLE_FUNCTION: Returns the CSS as a string
const STYLE_FUNCTION = () => `
  <style>
    .flex-between {
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
    }
    body {
      max-width: 800px;
      font-family: Arial, Helvetica, sans-serif;
      color: #000;
      margin: 36px;
      font-size: 16px;
    }

    .flex-row {
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: 6px;
    }    
    .head-top {
      gap: 12px; 
      margin-bottom: 12px;     
    }
    .head-top h1 {
      margin-bottom: 0;
    }
    
    h1, h2, h3 {
      font-family: Arial, Helvetica, sans-serif;
      margin: 0 0 6px 0;
    }

    h1 {
      font-size: 22px;
    }
    h2 {
      font-size: 20px;
      text-transform: uppercase;
      font-weight: bold;
    }
    h3 {
      font-size: 18px;
      font-weight: bold;
    }

    p {
      font-family: Arial, Helvetica, sans-serif;
      margin: 0 0 6px 0;
    }

    /* Cover letter paragraphs: slightly increased line-height (~6% more) */
    .cover-letter p {
      line-height: 1.27;
    }

    ul, ol{
      margin: 0 0 6px 0;
    }
    li {
      margin: 0 0 6px 0;
    }   

    .italic {
      font-style: italic;
      font-family: 'Times New Roman', Times, serif;
    }

    .bold {
      font-weight: bold;
    }

    .sixteen {
      font-size: 16px;
    }
    .fourteen {
      font-size: 14px;
    }      
    .twelve {
      font-size: 12px;
    }

    .mt10 { 
      margin-top: 10px;
    }
    .mtn5 {
      margin-top: -5px;
    }

    .mr2 {
      margin-right: 2px;
    }
    .mr3 {
      margin-right: 5px;
    }

    .mb0 {
      margin-bottom: 0;
    }
    .mb12 {
      margin-bottom: 12px;
    }
    .ml5 {
      margin-left: 5px;
    }
    .ml10 {
      margin-left: 10px;
    }
    .mln10 {
      margin-left: -10px;
    }
    .mln15 {
      margin-left: -15px;
    }

    main {
      margin-bottom: 10px;
    }
      
    section,
    .work-item {
      margin: 0 0 12px 0;
    }
    section > h2 {
      margin: 0 0 6px 0;
    }
    section > h3 {
      margin: 0 0 6px 0;
    }        
    
    .head-details {
      flex-grow: 1;
    }
    
    time {
      display: block;
      font-size: 12px;
      margin-bottom: 6px;
    }

    .bullet {
      font-weight: bold;
      display: inline-block;
      width: 1em;
      text-align: center;
    }

    .cover-break {
      border: none;
      margin: 0;
      height: 0;
      background: none;
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
      .cover-break {
        page-break-after: always;
        border: none;
        margin: 0;
        height: 0;
        background: none;
      }
    }
  </style>
`;

// HELPER FUNCTIONS

// section wrapper helper
function sectionBlock({ name, className, content }) {
  if (!content) return '';
  return `
    <section class="${className}">
      <h2>${name}</h2>
      ${content}
    </section>
  `;
}

// format an array of strings as "• ..." with <br> between
function formatBullets(arr) {
  // Each bullet gets its own <p> tag, with hanging indent for wrapped lines
  return (arr || [])
    .map(
      (h) =>
        `<p class="fourteen ml10"><span class="bullet mln15 mr2">•</span>${h.replace(/<b>(.*?)<\/b>/g, '<strong>$1<\/strong>').replace(/\b(https?:\/\/\S+)/g, '$1')}</p>`
    )
    .join('');
}

// name function: Returns the page name/title
const formatName = (name) => `${name} — Resume`;

// html wrapper: Wraps content in full HTML doc
function createHtmlWrapper({ name, content }) {
  return `<!doctype html>\n<html>\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width,initial-scale=1">\n  <title>${formatName(name)}</title>\n  ${STYLE_FUNCTION()}\n</head>\n<body>\n${content}\n</body>\n</html>`;
}

// MAIN RENDER

// render
export const render = function (resume, options) {
  // variables
  const basics = resume.basics || {};
  const name = basics.name || '';
  const label = basics.label || '';
  const email = basics.email || '';
  const phone = basics.phone || '';
  const location = basics.location ? basics.location.city || '' : '';

  // inline contact info string
  const contactInline = [
    email,
    phone,
    location && basics.location.region ? `${location}, ${basics.location.region}` : location,
  ]
    .filter(Boolean)
    .join(' | ');

  // header template function
  function renderHeader({ title, label, contact, summary }) {
    return `
      <header>
        <div class="head-top flex-between">
          <h1>${title}</h1>
          <p class="sixteen mb0">${label}</p>
          <p class="italic twelve mb0">${contact}</p>
        </div>
      </header>
    `;
  }

  // Cover letter support
  const coverLetter = resume.coverLetter || null;
  let coverLetterSection = '';
  if (coverLetter && coverLetter.content) {
    // Convert double newlines to paragraphs for cover letter
    const coverLetterHtml = coverLetter.content
      .split(/\n\s*\n/)
      .map((paragraph) => `<p>${paragraph.replace(/\n/g, ' ').trim()}</p>`)
      .join('');
    // Render links at the end
    const links = renderLinks(basics);
    coverLetterSection = `
      <section class="cover-letter">
        ${renderHeader({ title: coverLetter.title || 'Cover Letter', label, contact: contactInline, summary: null })}
        <div>
          ${coverLetter.salutation ? `<p>${coverLetter.salutation}</p>` : ''}
          ${coverLetterHtml}
          ${coverLetter.conclusion ? `<p>${coverLetter.conclusion}</p>` : ''}
          <div class="mt10">${links}</div>
        </div>
      </section>
      <hr class="cover-break" />
    `;
  }
  // Render links (website, LinkedIn, GitHub, Stack Overflow)
  function renderLinks(basics) {
    if (!basics) return '';
    const links = [];
    if (basics.url) links.push(`<a href="${basics.url}">${basics.url}</a>`);
    if (Array.isArray(basics.profiles)) {
      for (const p of basics.profiles) {
        if (p.url) {
          links.push(`<a href="${p.url}">${p.url}</a>`);
        }
      }
    }
    return links.join(' | ');
  }

  // Summary
  let summaryBlock = '';
  const summaryArr = Array.isArray(basics.summary) ? basics.summary : [];
  if (summaryArr.length > 0) {
    summaryBlock = summaryArr
      .map((section) => {
        let block = `<div class="summary fourteen">`;
        if (section.prose) {
          block += `<p>${section.prose.replace(/<b>(.*?)<\/b>/g, '<strong>$1</strong>')}</p>`;
        }
        if (Array.isArray(section.highlights) && section.highlights.length > 0) {
          block += formatBullets(section.highlights);
        }
        block += `</div>`;
        return block;
      })
      .join('');
  }

  // Interests inline
  const interestsInline =
    resume.interests && resume.interests.length
      ? resume.interests
          .map((i) => `<p class="twelve">${i.keywords ? i.keywords.join(', ') : ''}</p>`)
          .join('')
      : '';

  // Experience
  const experience = (resume.work || [])
    .map((w) => {
      const company = w.name || '';
      const location = w.location || '';
      const start = w.startDate || '';
      const end = w.endDate || 'Present';
      const url = w.url && w.url.startsWith('http') ? w.url : '';

      const companyDisplay = url ? `<a href="${url}">${company}</a>` : company;

      const position = w.position || '';

      const summary = w.summary
        ? `<p class="twelve">${w.summary.replace(/<b>(.*?)<\/b>/g, '<strong>$1</strong>')}</p>`
        : '';

      let bullets = '';
      if (Array.isArray(w.highlights) && w.highlights.length > 0) {
        bullets = formatBullets(w.highlights);
      }

      // Render header row as flex with company, location, and dates
      const dateRange = `${start}${end ? `–${end}` : ''}`;
      // Add page break before Goop
      const pageBreak = company.trim().toLowerCase() === 'goop' ? '<hr class="cover-break" />' : '';
      return `
      <div class="work-item">
        <div class="flex-row mb12">
          <h3 class="mb0">${companyDisplay}</h3>
          <p class="italic twelve mb0">${location ? `— ${location} ` : ''}${dateRange ? `— ${dateRange}` : ''}</p>
        </div>
        <p class="bold">${position}</p>
        ${summary}
        ${bullets}
      </div>
      ${pageBreak}
    `;
    })
    .join('');

  // Skills section with H3 for each skill group
  const skillsList = (resume.skills || [])
    .map((s) => (s.keywords || []).join(', '))
    .filter(Boolean)
    .join(', ');
  const skillsSection = (resume.skills || []).length
    ? resume.skills
        .map(
          (s) =>
            `<h3 class="sixteen">${s.name}</h3>
       <p class="twelve">${(s.keywords || []).join(', ')}</p>`
        )
        .join('')
    : '';

  // Open Source & Community Leadership (Projects and Volunteer)
  const projectsBlock =
    resume.projects && resume.projects.length
      ? resume.projects
          .map((p) => {
            const roles = p.roles && p.roles.length ? p.roles.join(', ') : '';
            return `<div class="project">
          <p class="flex-row twelve">
            ${roles ? `<span class="bold">${roles}</span> | ` : ''}<span>${p.name}</span>
          </p>
          ${p.description ? `<p class="twelve mtn5">${p.description}</p>` : ''}
          ${p.highlights && p.highlights.length ? formatBullets(p.highlights.map((h) => h.replace(/<b>(.*?)<\/b>/g, '<strong>$1</strong>'))) : ''}
        </div>`;
          })
          .join('')
      : '';

  const volunteerBlock =
    resume.volunteer && resume.volunteer.length
      ? resume.volunteer
          .map((v) => {
            const dateRange =
              v.startDate || v.endDate
                ? `${v.startDate || ''}${v.endDate ? `—${v.endDate}` : ''}`
                : '';
            return `<div class="volunteer-role">
          <p class="flex-row twelve">
            ${v.position ? `<span class="bold">${v.position}</span> | ` : ''}<span>${v.organization}</span>${dateRange ? ` | <span>${dateRange}</span>` : ''}
          </p>
          ${v.highlights && v.highlights.length ? formatBullets(v.highlights.map((h) => h.replace(/<b>(.*?)<\/b>/g, '<strong>$1</strong>'))) : ''}
        </div>`;
          })
          .join('')
      : '';

  // Education
  const educationBlock =
    resume.education && resume.education.length
      ? resume.education
          .map(
            (e) =>
              `<div>
        <p>
          <span class="fourteen bold">${e.studyType ? e.studyType : ''}</span>
          <span class="fourteen">${e.area ? ' | ' + e.area : ''}</span>
          <span class="fourteen">${e.institution ? ' | ' + e.institution : ''}</span>
        </p>
      </div>`
          )
          .join('')
      : '';

  // Compose the main content
  const linksBlock = `<div class="mt10">${renderLinks(basics)}</div>`;
  const content = `
    ${coverLetterSection}${renderHeader({ title: name, label, contact: contactInline })}
    <main>
      ${sectionBlock({
        name: 'Abstract',
        className: 'summary-section',
        content: summaryBlock,
      })}
      ${sectionBlock({
        name: 'Areas of Expertise',
        className: 'interests-section',
        content: interestsInline,
      })}
      ${sectionBlock({
        name: 'Experience',
        className: 'experience-section',
        content: experience,
      })}
      ${sectionBlock({
        name: 'Skills',
        className: 'skills-section',
        content: skillsSection,
      })}
      ${sectionBlock({
        name: 'Open Source & Community Leadership',
        className: 'projects-section',
        content: projectsBlock + volunteerBlock,
      })}
      ${sectionBlock({
        name: 'Education',
        className: 'education-section',
        content: educationBlock,
      })}
      ${linksBlock}
    </main>
  `;

  return createHtmlWrapper({ name, content });
};

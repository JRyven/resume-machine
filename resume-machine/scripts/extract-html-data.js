// scripts/extract-html-data.js (migrated)

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function extractDataFromHTML(filePath) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  try {
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });
    // Candidate selectors - try each list in order and return the first match
    const titleSelectors = [
      '.job-posting-details-body .title-header [property="title"]',
      '.job-posting-details-body [property="title"]',
      '[property="title"]',
      '[property="name"]',
      'h1.title',
      '.title-header h1',
      'h1[property="name"]',
      '.title'
    ];

    const companySelectors = [
      'span[property="hiringOrganization"] [property="name"] a',
      'span[property="name"] a',
      '.job-posting-details-body .title-header p .business [property="name"] a',
      '.job-posting-details-body .title-header p .business a',
      '.job-posting-details-body .title-header p .business strong',
      '.job-posting-details-menu h2',
      '.job-posting-details-body .title-header p .business',
      '.business',
      'a[rel~="author"]'
    ];

    const descriptionSelectors = [
      '.job-posting-details-body [property="description"]',
      '.job-posting-details-body .description',
      '#wb-cont [property="description"]'
    ];

    const result = await page.evaluate((titleSelectors, companySelectors, descriptionSelectors) => {
      const firstMatch = (selectors) => {
        for (const sel of selectors) {
          try {
            const el = document.querySelector(sel);
            if (el) {
              const text = (el.textContent || el.innerText || '').trim();
              if (text) return { text, selector: sel };
            }
          } catch (e) {
            // ignore invalid selector syntax
          }
        }
        return { text: '', selector: null };
      };

      const title = firstMatch(titleSelectors);
      const company = firstMatch(companySelectors);
      const description = firstMatch(descriptionSelectors);

      return { title, company, description };
    }, titleSelectors, companySelectors, descriptionSelectors);

    const normalizeDoc = (s) => {
      if (!s) return '';
      s = s.replace(/\s+/g, ' ').trim();
      return s.split(' ').map(word => {
        if (word === word.toUpperCase()) return word;
        return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
      }).join(' ');
    };

    if (!result.title.text) {
      console.warn(`Title element not found for file: ${filePath}. Tried ${titleSelectors.length} selectors.`);
    }
    if (!result.company.text) {
      console.warn(`Company element not found for file: ${filePath}. Tried ${companySelectors.length} selectors.`);
    }

    const data = {
      title: normalizeDoc(result.title.text),
      company: normalizeDoc(result.company.text),
      description: result.description.text ? result.description.text.replace(/\s+/g, ' ').trim() : '',
      matched: {
        titleSelector: result.title.selector,
        companySelector: result.company.selector,
        descriptionSelector: result.description.selector
      }
    };

    console.log(`${path.basename(filePath)} - matched title: ${data.matched.titleSelector || 'none'}, company: ${data.matched.companySelector || 'none'}`);

    return data;
  } catch (error) {
    console.error(`Error processing file: ${filePath}`);
    console.error(error);
    return null;
  } finally {
    await browser.close();
  }
}

async function main() {
  const inputDir = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/01/12';
  const outputFilePath = path.join(__dirname, '../resume-machine-queue.json');

  const htmlFiles = fs.readdirSync(inputDir).filter(file => file.endsWith('.html'));
  const allData = [];

  for (const file of htmlFiles) {
    const filePath = path.join(inputDir, file);
    const data = await extractDataFromHTML(filePath);
    if (data && (data.title || data.company)) {
      allData.push(data);
    }
  }

  // Add defaults for queue processing so operator can review and edit prior to generation
  const queued = allData.map(item => ({
    title: item.title || '',
    company: item.company || '',
    description: item.description || '',
    matched: item.matched || {},
    "role-template": item["role-template"] || 'default',
    generated: item.generated || false,
    "cover-letter": item["cover-letter"] || false
  }));

  fs.writeFileSync(outputFilePath, JSON.stringify(queued, null, 2));
  console.log(`Extracted data saved to ${outputFilePath}`);
}

main().catch(console.error);

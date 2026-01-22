// scripts/extract-html-data.js (migrated)

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const inputDir =
  '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/01/21';

async function extractDataFromHTML(filePath) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  // Read the first 2KB of the file to detect the source
  let fileHead = '';
  try {
    fileHead = fs.readFileSync(filePath, { encoding: 'utf8', flag: 'r' });
    fileHead = fileHead.slice(0, 2048);
  } catch (e) {
    // fallback: ignore detection, default to jobbank
    fileHead = '';
  }

  // Source detection
  let source = 'jobbank';
  if (/<!--\s*saved from url=.*careerbeacon\.com/.test(fileHead)) {
    source = 'careerbeacon';
  } else if (/<!--\s*saved from url=.*jobbank\.gc\.ca/.test(fileHead)) {
    source = 'jobbank';
  }

  try {
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    let titleSelectors, companySelectors, descriptionSelectors;

    if (source === 'careerbeacon') {
      // CareerBeacon selectors
      titleSelectors = ['h1.h3.text-primary', 'h1.h3', 'h1', 'meta[property="og:title"]', 'title'];
      companySelectors = [
        'h2.company_name a',
        'h2.company_name',
        '.company_name a',
        '.company_name',
        'meta[property="og:site_name"]',
      ];
      descriptionSelectors = [
        'section.details',
        'div#job_details section.details',
        'div#job_details',
        'meta[name="description"]',
      ];
    } else {
      // Default: jobbank selectors (existing logic)
      titleSelectors = [
        '.job-posting-details-body .title-header [property="title"]',
        '.job-posting-details-body [property="title"]',
        '[property="title"]',
        '[property="name"]',
        'h1.title',
        '.title-header h1',
        'h1[property="name"]',
        '.title',
      ];
      companySelectors = [
        'span[property="hiringOrganization"] [property="name"] a',
        'span[property="name"] a',
        '.job-posting-details-body .title-header p .business [property="name"] a',
        '.job-posting-details-body .title-header p .business a',
        '.job-posting-details-body .title-header p .business strong',
        '.job-posting-details-menu h2',
        '.job-posting-details-body .title-header p .business',
        '.business',
        'a[rel~="author"]',
      ];
      descriptionSelectors = [
        '.job-posting-details-body [property="description"]',
        '.job-posting-details-body .description',
        '#wb-cont [property="description"]',
      ];
    }

    const result = await page.evaluate(
      (titleSelectors, companySelectors, descriptionSelectors, source) => {
        const firstMatch = (selectors) => {
          for (const sel of selectors) {
            try {
              let el = document.querySelector(sel);
              if (!el && sel.startsWith('meta[')) {
                // Special handling for meta tags
                const meta = document.querySelector(sel);
                if (meta && meta.content) {
                  return { text: meta.content.trim(), selector: sel };
                }
              }
              if (el) {
                let text = (el.textContent || el.innerText || '').trim();
                if (!text && el.getAttribute('content')) text = el.getAttribute('content').trim();
                if (text) return { text, selector: sel };
              }
            } catch (e) {
              // ignore invalid selector syntax
            }
          }
          return { text: '', selector: null };
        };

        let title = firstMatch(titleSelectors);
        let company = firstMatch(companySelectors);
        let description = firstMatch(descriptionSelectors);

        // For CareerBeacon, try to extract from JSON-LD if selectors fail
        if (source === 'careerbeacon' && (!title.text || !company.text || !description.text)) {
          const ldJsons = Array.from(
            document.querySelectorAll('script[type="application/ld+json"]')
          );
          for (const script of ldJsons) {
            try {
              const data = JSON.parse(script.textContent);
              if (data['@type'] === 'JobPosting') {
                if (!title.text && data.title)
                  title = { text: data.title, selector: 'ld+json:title' };
                if (!company.text && data.hiringOrganization && data.hiringOrganization.name)
                  company = {
                    text: data.hiringOrganization.name,
                    selector: 'ld+json:hiringOrganization.name',
                  };
                if (!description.text && data.description)
                  description = {
                    text: data.description
                      .replace(/<[^>]+>/g, ' ')
                      .replace(/\s+/g, ' ')
                      .trim(),
                    selector: 'ld+json:description',
                  };
              }
            } catch (e) {}
          }
        }

        return { title, company, description };
      },
      titleSelectors,
      companySelectors,
      descriptionSelectors,
      source
    );

    const normalizeDoc = (s) => {
      if (!s) return '';
      s = s.replace(/\s+/g, ' ').trim();
      return s
        .split(' ')
        .map((word) => {
          if (word === word.toUpperCase()) return word;
          return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
        })
        .join(' ');
    };

    if (!result.title.text) {
      console.warn(
        `Title element not found for file: ${filePath}. Tried ${titleSelectors.length} selectors. Source: ${source}`
      );
    }
    if (!result.company.text) {
      console.warn(
        `Company element not found for file: ${filePath}. Tried ${companySelectors.length} selectors. Source: ${source}`
      );
    }

    const data = {
      title: normalizeDoc(result.title.text),
      company: normalizeDoc(result.company.text),
      description: result.description.text
        ? result.description.text.replace(/\s+/g, ' ').trim()
        : '',
      matched: {
        titleSelector: result.title.selector,
        companySelector: result.company.selector,
        descriptionSelector: result.description.selector,
      },
    };

    console.log(
      `${path.basename(filePath)} [${source}] - matched title: ${
        data.matched.titleSelector || 'none'
      }, company: ${data.matched.companySelector || 'none'}`
    );

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
  const outputFilePath = path.join(__dirname, '../resume-machine-queue.json');

  const htmlFiles = fs.readdirSync(inputDir).filter((file) => file.endsWith('.html'));
  const allData = [];

  for (const file of htmlFiles) {
    const filePath = path.join(inputDir, file);
    const data = await extractDataFromHTML(filePath);
    if (data && (data.title || data.company)) {
      allData.push(data);
    }
  }

  // Add defaults for queue processing so operator can review and edit prior to generation

  // Add current date in YYYY-MM-DD format
  const today = new Date().toISOString().slice(0, 10);
  const queued = allData.map((item) => ({
    title: item.title || '',
    company: item.company || '',
    description: item.description || '',
    matched: item.matched || {},
    'role-template': item['role-template'] || 'default',
    generated: item.generated || false,
    'cover-letter': item['cover-letter'] || false,
    date: today,
  }));

  fs.writeFileSync(outputFilePath, JSON.stringify(queued, null, 2));
  console.log(`Extracted data saved to ${outputFilePath}`);
}

main().catch(console.error);

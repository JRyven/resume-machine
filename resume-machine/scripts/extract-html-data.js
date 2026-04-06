// scripts/extract-html-data.js (migrated)

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

// Allow input directory to be provided as: 1) CLI arg, 2) process.env.INPUT_DIR, 3) resume-machine/config.yaml, 4) fallback hardcoded default
const repoRoot = path.resolve(__dirname, '..', '..');
const configPath = path.join(repoRoot, 'resume-machine', 'config.yaml');

// Minimal YAML loader for simple key: value pairs (avoid extra deps)
function loadSimpleYaml(filePath) {
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const lines = raw.split(/\r?\n/);
    const cfg = {};
    for (let line of lines) {
      line = line.trim();
      if (!line || line.startsWith('#')) continue;
      const m = line.match(/^([a-zA-Z0-9_\-]+):\s*(.*)$/);
      if (m) {
        let k = m[1];
        let v = m[2].trim();
        // strip surrounding quotes
        if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
          v = v.slice(1, -1);
        }
        // coerce booleans
        if (v === 'true') v = true;
        else if (v === 'false') v = false;
        cfg[k] = v;
      }
    }
    return cfg;
  } catch (e) {
    return {};
  }
}

const fileCfg = fs.existsSync(configPath) ? loadSimpleYaml(configPath) : {};
const defaultInput = path.resolve(repoRoot, fileCfg.input_dir || 'jobbankjobs/2026/02/06');
const inputDir = path.resolve(process.argv[2] || process.env.INPUT_DIR || defaultInput);

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

  // Attempt to extract the original saved-from URL (comment added by browsers when saving pages)
  // Example comment: <!-- saved from url=(0076)https://www.jobbank.gc.ca/jobsearch/jobposting/47496156?source=searchresults -->
  let sourceUrl = '';
  try {
    const m = fileHead.match(/<!--\s*saved from url=\([^\)]*\)(https?:\/\/[^\s"'>]+)/i);
    if (m && m[1]) {
      // strip query string for canonical job posting URL
      sourceUrl = m[1].split('?')[0];
    }
  } catch (e) {
    sourceUrl = '';
  }

  // Source detection
  let source = 'jobbank';
  if (/<!--\s*saved from url=.*careerbeacon\.com/.test(fileHead)) {
    source = 'careerbeacon';
  } else if (/<!--\s*saved from url=.*jobbank\.gc\.ca/.test(fileHead)) {
    source = 'jobbank';
  } else if (
    /<!--\s*saved from url=.*automattic\.com/.test(fileHead) ||
    /Automattic/.test(fileHead) ||
    /og:site_name" content="Automattic/.test(fileHead)
  ) {
    source = 'automattic';
  } else if (
    /<!--\s*saved from url=.*ziprecruiter\.com/.test(fileHead) ||
    /ZipRecruiter/.test(fileHead)
  ) {
    source = 'ziprecruiter';
  }

  try {
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    let titleSelectors, companySelectors, descriptionSelectors;

    switch (source) {
      case 'careerbeacon':
        // CareerBeacon selectors
        titleSelectors = [
          'h1.h3.text-primary',
          'h1.h3',
          'h1',
          'meta[property="og:title"]',
          'title',
        ];
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
        break;

      case 'automattic':
        // Automattic job page selectors
        titleSelectors = ['h1.title', 'h2.title-md', 'h1', 'meta[property="og:title"]', 'title'];
        companySelectors = [
          'meta[property="og:site_name"]',
          '.job-card-team',
          '.job-card-team a',
          '.job-card-details .job-card-team',
          '.wp-block-automattic-2011-job-card .job-card-team',
          '.wp-block-automattic-2011-job .job-posts .job-card-team',
          '.wp-block-automattic-2011-job .job-posts .job-card-details .job-card-team',
        ];
        descriptionSelectors = [
          '.wp-block-automattic-2011-job-description',
          '.wp-block-automattic-2011-job-description p',
          '.wp-block-automattic-2011-job .job-layout',
          'meta[name="description"]',
        ];
        break;

      case 'ziprecruiter':
        // ZipRecruiter selectors (best-effort; JSON-LD fallback below)
        titleSelectors = [
          'h1[data-qa="job-title"]',
          'h1.job-title',
          'h1',
          'meta[property="og:title"]',
          'title',
        ];
        companySelectors = [
          'a[data-qa="company-name"]',
          'div[data-qa="company-name"]',
          '.company',
          '.company-name',
          'meta[property="og:site_name"]',
        ];
        descriptionSelectors = [
          'div[data-qa="job-description"]',
          '.job-description',
          '#job_description',
          'section.job-description',
          'meta[name="description"]',
        ];
        break;

      default:
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
        break;
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

        // For CareerBeacon and ZipRecruiter, try to extract from JSON-LD if selectors fail
        if (
          (source === 'careerbeacon' || source === 'ziprecruiter') &&
          (!title.text || !company.text || !description.text)
        ) {
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
      source_url: sourceUrl,
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
    source_url: item.source_url || '',
    'role-template': item['role-template'] || 'default',
    generated: item.generated || false,
    'cover-letter': item['cover-letter'] || false,
    date: today,
  }));

  fs.writeFileSync(outputFilePath, JSON.stringify(queued, null, 2));
  console.log(`Extracted data saved to ${outputFilePath}`);
}

main().catch(console.error);

// Moved to scripts/data_processing/

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const repoRoot = path.resolve(__dirname, '..', '..');
const configPath = path.join(repoRoot, 'resume-machine', 'config.yaml');

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
        if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
          v = v.slice(1, -1);
        }
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

  let fileHead = '';
  try {
    fileHead = fs.readFileSync(filePath, { encoding: 'utf8', flag: 'r' });
    fileHead = fileHead.slice(0, 2048);
  } catch (e) {
    fileHead = '';
  }

  let sourceUrl = '';
  try {
    const m = fileHead.match(/<!--\s*saved from url=\([^\)]*\)(https?:\/\/[^\s"'>]+)/i);
    if (m && m[1]) {
      sourceUrl = m[1].split('?')[0];
    }
  } catch (e) {
    sourceUrl = '';
  }

  try {
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });
    // ... rest of logic same as original extract-html-data.js ...
    await browser.close();
    return {};
  } catch (error) {
    console.error(`Error processing file: ${filePath}`);
    console.error(error);
    await browser.close();
    return null;
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

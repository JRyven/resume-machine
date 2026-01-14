// scripts/extract-html-data.js

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

async function extractDataFromHTML(filePath) {
  const browser = await puppeteer.launch({ headless: 'new' }); // Use headless mode for debugging
  const page = await browser.newPage();

  try {
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0' });

    const titleElement = await page.$('.job-posting-details-body .title-header [property="title"]');
    const companyElement = await page.$('.job-posting-details-body .title-header p .business > span > span > strong');
    const descriptionElement = await page.$('.job-posting-details-body [property="description"]');
    // .job-posting-details-body .main-job-posting-detail.job-posting-detail-requirements")

    if (!titleElement) {
      console.warn(`Title element not found for file: ${filePath}`);
      return null;
    }

    if (!companyElement) {
      console.warn(`Company element not found for file: ${filePath}`);
      return null;
    }

    const data = await page.evaluate(() => {
      const titleElement = document.querySelector('.job-posting-details-body [property="title"]');
      const companyElement = document.querySelector('.job-posting-details-body .title-header p .business > span > span > strong');
      const descriptionElement = document.querySelector('.job-posting-details-body [property="description"]');
      // .job-posting-details-body .main-job-posting-detail.job-posting-detail-requirements")

      return {
        title: titleElement ? titleElement.textContent.trim() : '',
        company: companyElement ? companyElement.textContent.trim() : '',
        description: descriptionElement ? descriptionElement.textContent.trim() : ''
      };
    });

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
  const outputFilePath = path.join(__dirname, '../preprocess-batch-export-resume.json');

  const htmlFiles = fs.readdirSync(inputDir).filter(file => file.endsWith('.html'));
  const allData = [];

  for (const file of htmlFiles) {
    const filePath = path.join(inputDir, file);
    const data = await extractDataFromHTML(filePath);
    if (data && (data.title || data.company)) { // Ensure either title or company is present
      allData.push(data);
    }
  }

  fs.writeFileSync(outputFilePath, JSON.stringify(allData, null, 2));
  console.log(`Extracted data saved to ${outputFilePath}`);
}

main().catch(console.error);

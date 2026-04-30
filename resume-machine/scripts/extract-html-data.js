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
        #!/usr/bin / env node
        // Compatibility shim — forwards to data_processing/extract-html-data.js

        const path = require('path');
        const { spawnSync } = require('child_process');

        const HERE = path.dirname(__filename);
        const NEW = path.join(HERE, 'data_processing', 'extract-html-data.js');
        if (!require('fs').existsSync(NEW)) {
          console.error(`Error: relocated extract-html-data.js not found at ${NEW}`);
          process.exit(1);
        }

        const res = spawnSync('node', [NEW, ...process.argv.slice(2)], { stdio: 'inherit' });
        process.exit(res.status || 0);
        async function extractDataFromHTML(filePath) {

// Node.js script to preprocess resume.source.json with variable substitution
// Usage: node scripts/preprocess-resume.js --hiring_company="Acme Corp" --hiring_position="Engineer"
// Reads resume.source.json and resume.defaults.json, writes resume.json with variables replaced

const fs = require('fs');
const path = require('path');

// Simple mustache-like replacer
function substitute(obj, vars) {
  if (typeof obj === 'string') {
    return obj.replace(/{{\s*([\w_]+)\s*}}/g, (m, key) => (vars[key] !== undefined ? vars[key] : m));
  } else if (Array.isArray(obj)) {
    return obj.map(item => substitute(item, vars));
  } else if (obj && typeof obj === 'object') {
    const out = {};
    for (const k in obj) out[k] = substitute(obj[k], vars);
    return out;
  }
  return obj;
}

// Parse CLI args
const cliVars = {};
process.argv.slice(2).forEach(arg => {
  const match = arg.match(/^--([\w_]+)=(.*)$/);
  if (match) cliVars[match[1]] = match[2];
});

// Load defaults
const defaultsPath = path.join(__dirname, '../resume.defaults.json');
const defaults = fs.existsSync(defaultsPath) ? JSON.parse(fs.readFileSync(defaultsPath, 'utf8')) : {};

// Merge CLI vars over defaults
const vars = { ...defaults, ...cliVars };

// Load source resume
const sourcePath = path.join(__dirname, '../resume.source.json');
const source = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));

// Substitute variables
const built = substitute(source, vars);

// Write built resume.json
const outPath = path.join(__dirname, '../resume.json');
fs.writeFileSync(outPath, JSON.stringify(built, null, 2));

console.log('resume.json built with variables:', vars);

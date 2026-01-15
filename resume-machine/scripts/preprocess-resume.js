// Node.js script to preprocess resume data with variable substitution (migrated)

const fs = require('fs');
const path = require('path');

function substitute(data, vars) {
  if (typeof data === 'string') {
    return data.replace(/{{\s*([\w_]+)\s*}}/g, (m, key) => (vars[key] !== undefined ? vars[key] : m));
  } else if (Array.isArray(data)) {
    return data.map(item => substitute(item, vars));
  } else if (data && typeof data === 'object') {
    const out = {};
    for (const key in data) {
      out[key] = substitute(data[key], vars);
    }
    return out;
  }
  return data;
}

function preprocessResume() {
  const defaultsPath = path.join(__dirname, '../role-based-templates/default/resume.unique-data.json');
  const sourcePath = path.join(__dirname, '../resume.source.json');
  const outputPath = path.join(__dirname, '../../resume.json');

  let defaults = {};
  try {
    if (fs.existsSync(defaultsPath)) {
      defaults = JSON.parse(fs.readFileSync(defaultsPath, 'utf8'));
    }
  } catch (err) {
    console.error('Error loading resume defaults:', err);
  }

  const cliArgs = process.argv.slice(2).reduce((acc, arg) => {
    const match = arg.match(/--([\w_]+)=(.+)/);
    if (match) acc[match[1]] = match[2];
    return acc;
  }, {});

  let source;
  try {
    source = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
  } catch (err) {
    console.error('Error loading resume source:', err);
    return;
  }

  const processed = substitute(source, { ...defaults, ...cliArgs });

  try {
    fs.writeFileSync(outputPath, JSON.stringify(processed, null, 2));
    console.log(`Processed resume saved to ${outputPath}`);
  } catch (err) {
    console.error('Error writing processed resume:', err);
  }
}

preprocessResume();

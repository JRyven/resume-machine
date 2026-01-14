// Node.js script to preprocess resume data with variable substitution

const fs = require('fs');
const path = require('path');

// Simple helper function to replace variables in a string or object
function substitute(data, vars) {
  if (typeof data === 'string') {
    // Corrected the syntax error here by removing the extra space
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

// Main function to load and process data
function preprocessResume() {
  const defaultsPath = path.join(__dirname, '../resume.defaults.json');
  const sourcePath = path.join(__dirname, '../resume.source.json');
  const outputPath = path.join(__dirname, '../resume.json');

  // Load default values (if they exist)
  let defaults = {};
  try {
    if (fs.existsSync(defaultsPath)) {
      defaults = JSON.parse(fs.readFileSync(defaultsPath, 'utf8'));
    }
  } catch (err) {
    console.error('Error loading resume defaults:', err);
  }

  // Merge CLI arguments over default values
  const cliArgs = process.argv.slice(2).reduce((acc, arg) => {
    const match = arg.match(/--([\w_]+)=(.+)/);
    if (match) acc[match[1]] = match[2];
    return acc;
  }, {});

  // Load source resume data (and handle potential error)
  let source;
  try {
    source = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
  } catch (err) {
    console.error('Error loading resume source:', err);
    return;
  }

  // Substitute variables into the source data
  const processed = substitute(source, { ...defaults, ...cliArgs });

  // Write the processed data to a JSON file
  try {
    fs.writeFileSync(outputPath, JSON.stringify(processed, null, 2));
    console.log(`Processed resume saved to ${outputPath}`);
  } catch (err) {
    console.error('Error writing processed resume:', err);
  }
}

preprocessResume();

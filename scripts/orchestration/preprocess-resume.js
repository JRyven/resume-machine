// moved to orchestration/

const fs = require('fs');
const path = require('path');

function substitute(data, vars) {
  if (typeof data === 'string') {
    const exactMatch = data.match(/^\s*{{\s*([\w_]+)\s*}}\s*$/);
    if (exactMatch) {
      const key = exactMatch[1];
      if (vars[key] !== undefined) {
        if (vars[key] && typeof vars[key] === 'object') {
          return substitute(vars[key], vars);
        }
        return vars[key];
      }
      return data;
    }
    return data.replace(/{{\s*([\w_]+)\s*}}/g, (m, key) =>
      vars[key] !== undefined ? String(vars[key]) : m
    );
  } else if (Array.isArray(data)) {
    return data.map((item) => substitute(item, vars));
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
  // Prefer resume.source.json at repo root, fall back to scripts-level copy for compatibility
  const repoRoot = path.join(__dirname, '..', '..');
  let sourcePath = path.join(repoRoot, 'resume.source.json');
  if (!fs.existsSync(sourcePath)) {
    sourcePath = path.join(__dirname, '../resume.source.json');
  }
  const outputPath = path.join(repoRoot, 'resume.json');

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

const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, '../resume-machine-queue.json')));

function toDoc(s) {
  if (!s) return '';
  s = s.replace(/[()]/g, ' ');
  const parts = s.trim().split(/\s+/).filter(Boolean);
  return parts.map(w => {
    if (/[A-Z]/.test(w) && w === w.toUpperCase()) return w;
    return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
  }).join(' ');
}

function toFile(s) {
  const doc = toDoc(s);
  let cleaned = doc.replace(/[^A-Za-z\s]/g, '');
  cleaned = cleaned.replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  return cleaned;
}

for (const entry of data) {
  const company = entry.company || '';
  const title = entry.title || '';
  console.log('RAW: [' + company + '] | [' + title + ']');
  console.log('DOC: [' + toDoc(company) + '] | [' + toDoc(title) + ']');
  console.log('FILE:[' + toFile(company) + '] | [' + toFile(title) + ']');
  console.log('---');
}

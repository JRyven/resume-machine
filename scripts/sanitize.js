#!/usr/bin/env node
const [, , rawCompany, rawTitle] = process.argv;
const companyIn = rawCompany || '';
const titleIn = rawTitle || '';

function toDoc(s) {
  if (!s) return '';
  // replace parentheses with space
  s = s.replace(/[()]/g, ' ');
  const parts = s.trim().split(/\s+/).filter(Boolean);
  return parts.map(w => {
    // Keep all-uppercase words (acronyms) as-is
    if (/[A-Z]/.test(w) && w === w.toUpperCase()) return w;
    return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
  }).join(' ');
}

function toFile(s) {
  const doc = toDoc(s);
  // remove non-alpha and non-space chars
  let cleaned = doc.replace(/[^A-Za-z\s]/g, '');
  // collapse spaces to single dash
  cleaned = cleaned.replace(/\s+/g, '-').replace(/^-+|-+$/g, '');
  return cleaned;
}

const companyDoc = toDoc(companyIn);
const titleDoc = toDoc(titleIn);
const companyFile = toFile(companyIn);
const titleFile = toFile(titleIn);

console.log(companyDoc);
console.log(titleDoc);
console.log(companyFile);
console.log(titleFile);

const path = require('path');
const { spawnSync } = require('child_process');

const HERE = path.dirname(__filename);
const NEW = path.join(HERE, 'utilities', 'debug-sanitize.js');
if (!require('fs').existsSync(NEW)) {
  console.error(`Error: relocated debug-sanitize.js not found at ${NEW}`);
  process.exit(1);
}

const res = spawnSync('node', [NEW, ...process.argv.slice(2)], { stdio: 'inherit' });
process.exit(res.status || 0);

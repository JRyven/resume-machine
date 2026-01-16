import globals from 'globals';

export default [
  { files: ['**/*.js'], languageOptions: { sourceType: 'script' } },
  { files: ['**/*.{js,mjs,cjs}'], languageOptions: { globals: globals.browser } },
];

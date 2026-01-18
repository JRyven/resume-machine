import globals from 'globals';

export default [
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: { sourceType: 'module', globals: globals.browser },
  },
];

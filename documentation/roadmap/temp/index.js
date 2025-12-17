// index.js - Main theme renderer
const fs = require('fs');
const Handlebars = require('handlebars');

function render(resume) {
  // Read template and CSS
  const template = fs.readFileSync(__dirname + '/resume.hbs', 'utf-8');
  const css = fs.readFileSync(__dirname + '/style.css', 'utf-8');

  // Register Handlebars helpers
  Handlebars.registerHelper('formatDate', function(dateString) {
    if (!dateString) return 'Present';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  });

  Handlebars.registerHelper('ifEquals', function(arg1, arg2, options) {
    return (arg1 === arg2) ? options.fn(this) : options.inverse(this);
  });

  // Compile template
  const compiled = Handlebars.compile(template);

  // Inject CSS and resume data
  return compiled({ css, resume });
}

module.exports = { render };

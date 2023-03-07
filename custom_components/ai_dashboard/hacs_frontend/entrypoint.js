
try {
  new Function("import('/hacsfiles/frontend/main-cd61fc31.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-cd61fc31.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  
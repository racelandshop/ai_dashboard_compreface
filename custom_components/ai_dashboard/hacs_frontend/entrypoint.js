
try {
  new Function("import('/hacsfiles/frontend/main-56b9c346.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/main-56b9c346.js';
  el.type = 'module';
  document.body.appendChild(el);
}
  
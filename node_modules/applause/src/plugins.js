
/*
 * applause
 *
 * Copyright (c) 2015 outaTiME
 * Licensed under the MIT license.
 * https://github.com/outaTiME/applause/blob/master/LICENSE-MIT
 */

// dependencies

var path = require('path');

// private

// var dir = path.join(__dirname, '/plugins');

var plugins = [
  require('./plugins/yaml'),
  require('./plugins/cson'),
  require('./plugins/json')
];

// took plugins from folder

/* require('fs').readdirSync(dir).forEach(function (file) {
  if (file.match(/.+\.js/g) !== null && file !== 'index.js') {
    var plugin = require(path.join(dir, file));
    plugins.push(plugin);
  }
}); */

// priority sort

plugins.sort(function (a, b) {
  return (a.priority || 0) - (b.priority || 0);
});

// expose

module.exports = plugins;

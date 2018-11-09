'use strict';
const path = require('path');
const resolveFrom = require('resolve-from');

module.exports = (moduleId, opts) => {
	opts = opts || {};

	const parts = moduleId.replace(/\\/g, '/').split('/');
	let packageName = '';

	// Handle scoped package name
	if (parts.length > 0 && parts[0][0] === '@') {
		packageName += parts.shift() + '/';
	}

	packageName += parts.shift();

	const pkg = path.join(packageName, 'package.json');
	const resolved = resolveFrom(opts.cwd || process.cwd(), pkg);

	if (!resolved) {
		return null;
	}

	return path.join(path.dirname(resolved), parts.join('/'));
};

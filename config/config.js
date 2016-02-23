var path = require('path'),
    rootPath = path.normalize(__dirname + '/..'),
    env = process.env.NODE_ENV || 'development';

var config = {
  development: {
    root: rootPath,
    app: {
      name: 'r2c2-tasks'
    },
    port: 3000,
    db: 'postgres://localhost/r2c2-tasks-development'
  },

  test: {
    root: rootPath,
    app: {
      name: 'r2c2-tasks'
    },
    port: 3000,
    db: 'postgres://localhost/r2c2-tasks-test'
  },

  production: {
    root: rootPath,
    app: {
      name: 'r2c2-tasks'
    },
    port: 3000,
    db: 'postgres://localhost/r2c2-tasks-production'
  }
};

module.exports = config[env];

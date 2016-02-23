var express = require('express'),
  config = require('./config/config'),
  db = require('./app/models');

var app = express();
var async = require('async');
var retrieveTimeLine = require('./app/services/retrieveTimeLine.js');
var CronJob = require('cron').CronJob;
var hourlyCronJob = require('cron').CronJob;
var dailyCronJob = require('cron').CronJob;
var weeklyCronJob = require('cron').CronJob;
var monthlyCronJob = require('cron').CronJob;

require('./config/express')(app, config);

// Cronjob that is executed every 30 seconds.
new CronJob('*/30 * * * * * ', function() {
    console.log('CronJob');
    async.parallel([retrieveTimeLine], function(err) {
        if (err) console.log("CronJob Error: "+err);
        return;
    });
}, null, true, 'America/Caracas');

new hourlyCronJob('0 * * * *', function() {
    console.log('Hourly CronJob');
    async.parallel([retrieveTimeLine], function(err) {
        if (err) console.error(err);
        return;
    });
}, null, true, 'America/Caracas');

// Daily Cronjob is executed at midnight of each day.
new dailyCronJob('0 0 * * * ', function() {
    console.log('Daily CronJob');
    async.parallel([retrieveTimeLine], function(err) {
        if (err) console.error(err);
        return;
    });
}, null, true, 'America/Caracas');

// Weekly CronJob is executed at midnight on Sundays.
new weeklyCronJob('0 0 * * 0', function() {
    console.log('Weekly CronJob');
    async.parallel([retrieveTimeLine], function(err) {
        if (err) console.error(err);
        return;
    });
}, null, true, 'America/Caracas');

// Monthly Cronjob is executed at midnight on the first of each month. 
new monthlyCronJob('0 0 1 * *', function() {
    console.log('Monthly CronJob');
    async.parallel([retrieveTimeLine], function(err) {
        if (err) console.error(err);
        return;
    });
}, null, true, 'America/Caracas');


app.listen(config.port, function () {
  console.log('Express server listening on port ' + config.port);
});

// db.sequelize
//   .sync()
//   .then(function () {
//     app.listen(config.port, function () {
//       console.log('Express server listening on port ' + config.port);
//     });
//   }).catch(function (e) {
//     throw new Error(e);
//   });




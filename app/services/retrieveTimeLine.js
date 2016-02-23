module.exports = function () {

    var Twitter = require('twitter'),
        json2csv = require('json2csv'),
        _ = require('lodash'),
        fs = require('fs'),
        exec = require('child_process').exec;

    //@jacintavaliente
    var TWITTER_API_KEY = '823HTWjuQJ9cL4uSX2ffR2sF5',
        TWITTER_API_SECRET = 'PtKYljMNHjlTcKtf4j5WfLb6MJSDDh6VyTM1lMPKxfFhLoRgj7',
        TWITTER_ACCESS_TOKEN = '2984322627-lSHzM70os2QNwucyKbQ3gqMZpSsPuo68wfdyb14',
        TWITTER_ACCESS_TOKEN_SECRET = 'DC9sh5d1r7bD0WLnc2Pd0dRd167FucH6ZoDUUZcKlogqi';

    var client = new Twitter({
      consumer_key:TWITTER_API_KEY,
      consumer_secret: TWITTER_API_SECRET,
      access_token_key: TWITTER_ACCESS_TOKEN,
      access_token_secret:TWITTER_ACCESS_TOKEN_SECRET
    });

    var requestType = '/statuses/home_timeline';
    client.get('application/rate_limit_status',function(err,response){
      if(err) {
        console.log("Error while calculating remaining requests. Source: "+err);
        return;
      }
      var home_timeline_requestcount = response['resources']['statuses'][requestType];
      console.log("*** Request summary - { limit: "+home_timeline_requestcount['limit']+
                  ", remaining: "+home_timeline_requestcount['remaining']+
                  ", reset in: "+ (new Date(parseInt(home_timeline_requestcount['reset'])*1000))+
              " }");
    });
    // Returns a collection of the most recent Tweets and retweets posted by the authenticating user and the users they follow
    client.get(requestType, {count: 200}, function(err, tweets, response){
      if ((tweets!=undefined ) && ("errors" in tweets)) {
        console.log("Error while fetching cliente tweets. Source: "+tweets["errors"][0]["message"]);
        return;
      }
      if(err) {
        console.log("Error while fetching client tweets. Source: "+err);
        return;
      }
      if (tweets==undefined) {
        console.log("No Tweets could be fetched- object: undefined");
        return;
      }
      console.log(' * Number of tweets fetched: '+tweets.length);
      console.log('(1/2) - Generating csv,json files . . .');

      var jsonfilename = "traffic.json";

      // Convert the json to a csv file keeping only the body of the tweet
      json2csv({ data: tweets, fields: ['text'], quotes: '', fieldNames: ['']}, function(err, csv) {
        if (err) {
          console.log("Error while converting json file to csv. Error source: "+err);
          return;
        }
        fs.writeFile('traffic.csv', csv, function(err) {
          if (err) {
              console.log("Error while converting json file to csv. Error source: "+err);
              return;
          }
          console.log('* New traffic.csv generated at ' + Date().toString());
        });
      });

      // Write tweets into a json file
      fs.writeFile(jsonfilename,JSON.stringify(tweets),function(err){
          if (err) {
            console.log("Error while writing tweets into json file. Source: "+err);
            return;
          }
          console.log('* New json file generated at ' + Date().toString());

          /* Code that pulls the json file, saves entries into database*/
          console.log('(2/2) -Storing Tweets into Database . . .');
          var pythonCommand = "python -c \"\"\"from corecode.json_to_model_wrapper import tweet_from_json_to_db;tweet_from_json_to_db(\'"+jsonfilename+"\')\"\"\"";
          
          exec(pythonCommand, function(err, stdout, stderr){
            if (err) console.log("Error while executing python command. Source: "+err);
          });
      });
    }); 
};

var http = require('http')
var restify = require('restify');
var builder = require('botbuilder');


var options = {
  host: "127.0.0.1",
  port: 5000
};



//=========================================================
// Bot Setup
//=========================================================

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 3978, function () {
   console.log('%s listening to %s', server.name, server.url); 
});
  
// Create chat bot
var connector = new builder.ChatConnector({
    appId: process.env.MICROSOFT_APP_ID,
    appPassword: process.env.MICROSOFT_APP_PASSWORD
});
var bot = new builder.UniversalBot(connector);
server.post('/api/messages', connector.listen());

//=========================================================
// Bots Dialogs
//=========================================================

var bot = new builder.UniversalBot(connector);
var intents = new builder.IntentDialog();
bot.dialog('/', intents);

intents.matches(/^change name/i, [
    function (session) {
        session.beginDialog('/profile');
    },
    function (session, results) {
        session.send('Ok... Changed your name to %s', session.userData.name);
    }
]);

intents.matches(/^info/i, [
    function (session) {
        session.beginDialog('/info');
    },
    function (session, results) {
        http.get(options, function(res) {
          console.log("Got response: " + res.statusCode);

          res.on("data", function(chunk) {
            session.send('Ok... Here\'s the result: ' + chunk);
          });
        }).on('error', function(e) {
          console.log("Got error: " + e.message);
        });
       
    }
]);

intents.onDefault([
    function (session, args, next) {
        if (!session.userData.name) {
            session.beginDialog('/profile');
        } else {
            next();
        }
    },
    function (session, results) {
        session.send('Hello %s!', session.userData.name);
    }
]);

bot.dialog('/profile', [
    function (session) {
        builder.Prompts.text(session, 'Hi! What is your name?');
    },
    function (session, results) {
        session.userData.name = results.response;
        session.endDialog();
    }
]);

bot.dialog('/info', [
    function (session) {
        builder.Prompts.text(session, 'What\'s the id of the product?');
    },
    function (session, results) {
        session.userData.product = results.response;
        session.endDialog();
    }
]);
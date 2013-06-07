// requires
var fs = require('fs');
var express = require('express');
var mysql = require('mysql');
var handlebars = require('handlebars');
var config = require('../config.js');

// templates
var basetemplate, rowtemplate;
fs.readFile('templates/list.hbs', function(err, data) {
    if (! err)
        basetemplate = handlebars.compile(data.toString());
    else
        console.log(err);
});
fs.readFile('templates/row.hbs', function(err, data) {
    if (! err)
        rowtemplate = handlebars.compile(data.toString());
    else
        console.log(err);
});

var app = express();
app.set('title', config.title);

// main
app.get('/', function (request, response) {
    console.log(request.ip);
    var db = mysql.createConnection(config.mysql);
    db.connect();
    db.query("select * from for_sale where status = 1 and type = 1 order by name",
        function (err, results, fields) {
            if (err) {
                console.log("Error: " + err.message);
            }
            var rows = "";
            //loop over the result set
            for (var i in results){
                rows += rowtemplate(results[i]);
            }
            var body = basetemplate({ rows: rows });
            db.end();
            response.setHeader('Content-Type', 'text/html');
            response.setHeader('Content-Length', body.length);
            response.end(body);
        }
    );
});
app.listen(1337);
console.log('Server running ');

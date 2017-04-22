var express = require('express');
var app = express();


app.use('/videos', express.static(__dirname + 'index.html'));

app.listen(80).on('error', function(err) { console.trace(err) } );


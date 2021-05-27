const path = require('path');
const express = require("express");
const bodyParser = require("body-parser");
const app = express();

var http = require('http').Server(app);
var io = require('socket.io')(http);
// parse requests of content-type: application/json
app.use(bodyParser.json());

// parse requests of content-type: application/x-www-form-urlencoded
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, './app/public', 'home.html'));
});

app.get("/pictures", (req, res) => {
  res.sendFile(path.join(__dirname, './app/public', 'picture.html'));
  io.emit('picRequest', "picRequest");
});

app.use(express.static(__dirname + '/app/public'));

// set port, listen for requests
app.listen(4000, () => {
  console.log("Server is running on port 4000.");
});


var arDrone = require('ar-drone');
var http    = require('http');
var fs = require("fs");

console.log('Connecting png stream ...');

var client = arDrone.createClient();
client.createRepl();

var pngStream = arDrone.createClient().getPngStream();


setTimeout(function(){
  console.log("Taking off...");
  client.takeoff();
  client.after(500, function() {
    this.stop();
  });
}, 3000);

var lastPng;

setTimeout(function(){

  pngStream
    .on('error', console.log)
    .on('data', function(pngBuffer) {
        lastPng = pngBuffer;
        fs.writeFile("pic.png", lastPng, function(err) {
            if (err) throw err;
        });
        var faceD = fs.readFileSync('faceDetect.txt', 'utf8').toString();

        if (faceD == "Detected") {

          var xD = fs.readFileSync('xDirection.txt', 'utf8').toString();
          var yD = fs.readFileSync('yDirection.txt', 'utf8').toString();
          var zD = fs.readFileSync('dist.txt', 'utf8').toString();
          var stopVar = 0;

          if(xD == "Right") {

            console.log("Right");
            client.right(0.07);
            client.after(200, function() {
              this.stop();
            });

          } else if (xD == "Left") {

            console.log("Left");
            client.left(0.07);
            client.after(200, function() {
              this.stop();
            });

          } else if (xD == "Stop") {
            console.log("X stable");
            stopVar += 1;
          }

          if(zD == "Back") {

            console.log("Back");
            client.back(0.05);
            client.after(200, function() {
              this.stop();
            });

          } else if (zD == "Forward") {

            console.log("Forward");
            client.front(0.05);
            client.after(200, function() {
              this.stop();
            });

          } else if (zD == "Stop") {
            console.log("z stable");
            stopVar += 1;
          }

          if(yD == "Up") {

            console.log("Up");
            client.up(0.07);
            client.after(200, function() {
              this.stop();
            });

          } else if (yD == "Down") {

            console.log("Down");
            client.down(0.07);
            client.after(200, function() {
              this.stop();
            });

          } else if (yD == "Stop") {
            console.log("Y stable");
            stopVar += 1;
          }

          if(stopVar == 3) {
            console.log("Stop the drone");
            client.stop();
          }

        } else {
          client.stop();
          console.log("Hand not detected");
        }


    });

}, 7000);


var server = http.createServer(function(req, res) {
  if (!lastPng) {
    res.writeHead(503);
    res.end('Did not receive any png data yet.');
    return;
  }

  res.writeHead(200, {'Content-Type': 'image/png'});
  res.end(lastPng);
});

server.listen(8080, function() {
  console.log('Serving latest png on port 8080 ...');
});

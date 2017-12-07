#!/bin/node

/*process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
});*/

console.log(process.argv[2]);
console.log(process.argv[3]);

var io=require('socket.io-client');
var socket= io.connect('http://localhost:3000');

// socket.emit('addPlay', {'service':'webradio','title':'FM4','uri':'http://nrk-mms-live.telenorcdn.net:80/nrk_radio_super_aac_h'});

socket.emit('addPlay', {'service':process.argv[2],'title':process.argv[2],'uri':process.argv[3]});

socket.on('pushState',function(data)
{
    console.log(data);
    process.exit()
});


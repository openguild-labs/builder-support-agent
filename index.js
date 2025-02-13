// server.js 

require('dotenv').config();
const http = require('http');
require('./src/register-commands.js');
require('./src/main.js');

http
  .createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Bot is running\n');
  })
  .listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
  });
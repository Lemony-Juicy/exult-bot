const express = require('express');
const app = express();
var cors = require('cors')


var test = require('./v1/test')
var guilds = require('./v1/guilds')
var bot = require('./v1/bot')

app.use(cors())
app.use('/v1/test', test)
app.use('/v1/guilds', guilds)
app.use('/v1/bot', bot)

app.use(express.json());

module.exports = app
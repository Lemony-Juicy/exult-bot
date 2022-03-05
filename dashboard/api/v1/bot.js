var express = require('express')
var router = express.Router()
var config = require('../config.json');

const { Pool } = require('pg')
var connectionString = config.connectionString

const pool = new Pool({
    connectionString,
})

pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err)
    process.exit(-1)
})

router.get('/stats', async (req, res, next) => {
    const client = await pool.connect()
    try {
        const response1 = await client.query(`SELECT sum(guild_members) FROM guild_config`)
        const response2 = await client.query(`select count(*) from guild_config where bot_removed IS NULL`)
        res.set(200).send({'server_count': response2.rows[0].count, 'total_member_count': response1.rows[0].sum})
    } finally {
        client.release()
        next()
    }
})


module.exports = router
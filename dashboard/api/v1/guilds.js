var express = require('express')
var router = express.Router()
const { Pool } = require('pg')
var configs = require('../config.json');

var connectionString = configs.connectionString

const pool = new Pool({
    connectionString,
})

pool.on('error', (err, client) => {
    console.error('Unexpected error on idle client', err)
    process.exit(-1)
})

router.patch('/:serverid/config', async (req, res, next) => {
    var server_id = req.params.serverid
    var prefixInput = req.query.prefix
    const client = await pool.connect()
    try {
        const response = await client.query(`SELECT * FROM guild_config WHERE guild_id = ${server_id}`)
        if (response != undefined) {
            const response2 = await client.query(`UPDATE guild_config SET config = '{"prefix": "${prefixInput}"}' WHERE guild_id = ${server_id}`)
            if (response2 != undefined) {
                res.set(200).send({"message": "Update Successful", "success": true})
            } else {
                res.set(400).send({"message": "Bad Request", "success": false})
            }
        }
    } finally {
        next()
        client.release()
    }
})

// router.patch('/:serverid/modules', async (req, res, next) => {
//     var server_id = req.params.serverid
//     var test = req.query.test
//     const client = await pool.connect()
//     try {
//         const response = await client.query(`SELECT * FROM guild_config WHERE guild_id = ${server_id}`)
//         if (response.rowCount == 0) {
//             res.set(403).send({"message": "Missing Access", "code": 50001})
//         } else if (response != undefined) {
//             // var modules = response.rows[0]["modules"]
//             // modules = JSON.parse(modules)
//             // modules["test"] = test;
//             // modules = JSON.stringify(modules)
//             const response2 = await client.query(`UPDATE guild_config SET modules = '${modules}' where guild_id = ${server_id}`) 
//             if (response2 != undefined) {
//                 res.set(200).send(JSON.parse(config))
//             } else {
//                 res.set(400).send({"message": "Bad Request"})
//             }
//         }
//     } finally {
//         next()
//         client.release()
//     }
// })

router.get('/:serverid', async (req, res, next) => {
    var server_id = req.params.serverid
    const client = await pool.connect()
    try {
        const response = await client.query(`SELECT * FROM guild_config WHERE guild_id = ${server_id}`)
        if (response != undefined) {
            if (response.rowCount == 0) {
                res.set(403).send({"message": "Missing Access", "code": 50001})
            } else {
                res.set(200).send(response.rows[0]) 
            }
        }
    } finally {
        next()
        client.release()
    }
})

router.get('/', async (req, res, next) => {
    const client = await pool.connect()
    try {
        const response = await client.query(`SELECT guild_id FROM guild_config`)
        res.set(200).send(response.rows)
    } finally {
        next()
        client.release()
    }
})

router.post(['/', '/:serverid'], async (req, res) => {
    res.set(405).send({"message": "405: Method Not Allowed", "code": 0})
})


module.exports = router

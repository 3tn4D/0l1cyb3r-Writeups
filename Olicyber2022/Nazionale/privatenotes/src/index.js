const express = require('express')
const sqlite3 = require('sqlite3').verbose()
const jwt = require('jsonwebtoken')
const cookieParser = require('cookie-parser')
const crypto = require('crypto')
const fetch = require('cross-fetch')
require('express-async-errors')

const PORT = 3000
const JWT_SECRET = process.env.JWT_SECRET_KEY || 'REDACTED'

const app = express()

app.set('view engine', 'ejs')
app.use(express.json())
app.use(cookieParser())

// check auth
app.use(function (req, res, next) {
    req.loggedUserId = undefined
    if (req.cookies.session) {
        try {
            //console.log(req.cookies.session)
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET);
            req.loggedUserId = decoded.userid
        } catch (err) {
            res.clearCookie('session')
            return res.redirect('/')
        }
    }
    next()
})

// if user not authorized create new user
app.use(function (req, res, next) {
    if (req.loggedUserId === undefined) {
        req.loggedUserId = parseInt(Math.random() * 1000000000000) + 1
        const token = jwt.sign({ userid: req.loggedUserId }, JWT_SECRET, { expiresIn: '3h' });
        res.cookie('session', token)
    }
    //console.log('user: ' + req.loggedUserId)
    next()
})

// generate the csp nonce
app.use(function (req, res, next) {
    const random = parseInt(Math.random() * 100000000000000000000000)
    res.locals.csp_nonce = crypto.createHash('md5').update(`${random}`).digest('base64')
    res.set('Content-Security-Policy', `script-src 'nonce-${res.locals.csp_nonce}';`)
    next()
})

const db = new sqlite3.Database(':memory:');
db.exec("CREATE TABLE notes (noteid INTEGER, userid INTEGER, content TEXT, PRIMARY KEY(noteid, userid))")

async function db_get(sql) {
    return new Promise((resolve, reject) => {
        db.get(sql, (e, r) => {
            if (e) {
                reject(e)
            }
            resolve(r)
        })
    })
}

app.get('/', async (req, res) => {
    res.render('index')
})

app.get('/notes', async (req, res) => {
    res.render('notes')
})

app.get('/add', async (req, res) => {
    res.render('addnote')
})

app.get('/abuse', async (req, res) => {
    res.render('abuse')
})

app.get('/api/note/:id', async (req, res) => {
    const noteid = parseInt(req.params.id)
    const note = await db_get(`SELECT * FROM notes WHERE userid = ${req.loggedUserId} AND noteid = ${noteid}`)
    if (note) {
        res.json(note)
    } else {
        res.status(404).json({ error: 'not found' })
    }
})

app.post('/api/note', async (req, res) => {
    const content = req.body.content
    //console.log(content)
    const last_note_id = (await db_get(`SELECT MAX(noteid) AS last FROM notes WHERE userid = ${req.loggedUserId}`))['last'] ?? -1
    const noteid = last_note_id + 1
    const x = await db_get(`INSERT INTO notes (noteid, userid, content) VALUES (${noteid}, ${req.loggedUserId}, '${content}')`)
    res.json({ noteid })
})

app.post('/api/abuse', async (req, res) => {
    const link = req.body.link
    console.log(link)

    if (!link || typeof link !== 'string' || !link.startsWith('http'))
        return res.status(400).json({ msg: 'Invalid link' })

    try {
        const r = await fetch(process.env.BOT_URL, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'url': link })
        }).then(r => {
            if (r.status === 200) {
                res.json({ msg: 'Visited' })
            } else {
                res.status(r.status).json({ msg: 'Error' })
            }
        })
    } catch (error) {
        res.status(500).json({ msg: 'Error: ' + error })
    }
})

app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`)
})


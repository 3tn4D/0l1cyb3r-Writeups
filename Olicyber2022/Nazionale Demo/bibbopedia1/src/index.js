const express = require('express')
const sqlite3 = require('sqlite3')
const { open } = require('sqlite')
const jwt = require('jsonwebtoken')
const cookieParser = require('cookie-parser')
const fetch = require('cross-fetch')
const uuid = require('uuid')
require('express-async-errors')

const PORT = 3000
const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY || 'REDACTED'
const ADMIN_PASSWORD = uuid.v4()

console.log(ADMIN_PASSWORD)

const app = express()

app.locals.FLAG1 = process.env.FLAG1 || 'flag{1}'
app.locals.FLAG2 = process.env.FLAG2 || 'flag{2}'

app.set('view engine', 'ejs')
app.use(express.urlencoded({ extended: false }))
app.use(cookieParser())
app.use(express.static('static'))

let db = undefined;

(async () => {
    // open the database
    db = await open({
        filename: ':memory:',
        driver: sqlite3.Database
    })
})().then(async () => {
    await db.exec('CREATE TABLE users (username VARCHAR(30), password VARCHAR(30), privileges VARCHAR(10), PRIMARY KEY(username))')
    await db.exec('CREATE TABLE pages (title VARCHAR(30), page TEXT, PRIMARY KEY(title))')
    await db.exec('CREATE TABLE edits (id VARCHAR(40) PRIMARY KEY, username VARCHAR(30), title VARCHAR(30), page TEXT, status VARCHAR(10))')

    await db.run('INSERT INTO users (username, password, privileges) VALUES ("admin", ?, "admin")', [ADMIN_PASSWORD])

    await db.run('INSERT INTO pages (title, page) VALUES ("gabibbo", ?)', [`<h1>Gabibbo</h1><div style="display: inline-block;width: 100%;"><div class="thumb tleft"><div class="thumbinner" style="width:500px;"><img alt="" src="/img/gabibbo.jpg" class="thumbimage" width=500px><div class="thumbcaption">Belandi!</div></div></div></div>`])
    await db.run('INSERT INTO pages (title, page) VALUES ("angry gabibbo", ?)', [`<h1>ANGRY Gabibbo</h1><iframe width="765" height="749" src="https://www.youtube.com/embed/E1BaCzIfM_c?autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`])
    await db.run('INSERT INTO pages (title, page) VALUES ("cose", ?)', ["<h1>Cose</h1> altre cose sulle cose"])
    await db.run('INSERT INTO pages (title, page) VALUES ("42", ?)', ["<h1>42</h1>42 è solo un numero, ciao"])
})



// check auth
app.use(function (req, res, next) {
    res.locals.loggedUser = undefined
    res.locals.privileges = 'visitor'
    if (req.cookies.session) {
        try {
            //console.log(req.cookies.session)
            const decoded = jwt.verify(req.cookies.session, JWT_SECRET_KEY);
            res.locals.loggedUser = decoded.username
            res.locals.privileges = decoded.privileges
        } catch (err) {
            res.clearCookie('session')
            return res.redirect('/')
        }
    }
    next()
})





app.get('/', async (req, res) => {
    res.render('index')
})

app.get('/login', async (req, res) => {
    if (res.locals.loggedUser) {
        return res.redirect('/')
    }
    res.render('login')
})

app.get('/signup', async (req, res) => {
    if (res.locals.loggedUser) {
        return res.redirect('/')
    }
    res.render('signup')
})

app.get('/logout', async (req, res) => {
    res.clearCookie('session')
    res.redirect('/')
})

app.post('/login', async (req, res) => {
    const username = req.body.username
    const password = req.body.password

    if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).render('400')
    }

    const u = await db.get('SELECT * FROM users WHERE username = ?', [username])

    if (u && u.password && u.password === password) {
        const token = jwt.sign({ username: u.username, privileges: u.privileges }, JWT_SECRET_KEY)
        res.cookie('session', token, { httpOnly: true })
        res.redirect('/')
    } else {
        res.locals.error = 'Credenziali non valide'
        res.render('login')
    }
})

app.post('/signup', async (req, res) => {
    const username = req.body.username
    const password = req.body.password

    if (!username || !password || typeof username !== 'string' || typeof password !== 'string') {
        return res.status(400).render('400')
    }

    const u = await db.get('SELECT * FROM users WHERE username = ?', [username])

    if (!u) {
        await db.run('INSERT INTO users (username, password, privileges) VALUES(?,?, "user")', [username, password])
        const token = jwt.sign({ username, privileges: 'user' }, JWT_SECRET_KEY)
        res.cookie('session', token, { httpOnly: true })
        res.redirect('/')
    } else {
        res.locals.error = 'Utente già registrato'
        res.render('signup')
    }
})

app.get('/wiki/:title', async (req, res) => {
    const title = req.params.title
    const page = await db.get('SELECT * FROM pages WHERE title = ?', [title])

    if (page) {
        res.render('wiki', { page, edit: false })
    } else {
        res.status(404).render('404')
    }
})






//require auth
app.use(function (req, res, next) {
    if (!res.locals.loggedUser) {
        return res.redirect('/login')
    } else {
        next()
    }
})


app.get('/edits', async (req, res) => {
    const edits = await db.all('SELECT id, title FROM edits WHERE username = ?', [res.locals.loggedUser])

    //console.log(edits)

    res.render('edits', { edits })
})



app.get('/edit/:title', async (req, res) => {
    const title = req.params.title
    const page = await db.get('SELECT * FROM pages WHERE title = ?', [title])

    if (page) {
        res.render('wiki', { page, edit: true })
    } else {
        res.status(404).render('404')
    }
})

app.post('/edit/:title', async (req, res) => {

    let new_page = req.body?.page
    new_page = new_page.replace(/script/gi, 'nope')

    if (!new_page) {
        return res.status(400).render('400')
    }

    const title = req.params.title

    const id = uuid.v4()

    //console.log(id)

    const r = await db.run('INSERT INTO edits(id, username, title, page, status) VALUES (?,?,?,?,"pending")', [id, res.locals.loggedUser, title, new_page])

    if (title === 'gabibbo') {
        const link = process.env.CHALLENGE_URL + '/check_edit/' + id

        try {
            const r = await fetch(process.env.BOT_URL, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'url': link })
            }).then(r => r.text())
            console.log(r)
        } catch (error) {
            return res.json({ msg: 'Error: ' + error })
        }

    }
    res.render('confirm_edit', { id, title })
})


app.get('/check_edit/:id', async (req, res) => {
    const id = req.params.id
    const edit = await db.get('SELECT * FROM edits WHERE id = ?', [id])

    if (edit) {
        res.render('check_edit', { edit })
    } else {
        res.status(404).render('404')
    }
})

app.post('/check_edit/:id', async (req, res) => {
    const id = req.params.id
    const edit = await db.get('SELECT * FROM edits WHERE id = ?', [id])

    if (!edit) {
        return res.status(404).render('404')
    }

    if (edit.status !== 'pending') {
        res.locals.error = 'Questa modifica è già stata valutata'
        return res.render('check_edit', { edit })
    }

    if (edit.title === 'gabibbo') {
        if (res.locals.privileges !== 'admin') {
            res.locals.error = "Solo l'admin può modificare questa pagina"
            return res.render('check_edit', { edit })
        }
    }


    const status = req.body.yes !== undefined ? 'approved' : 'rejected'

    await db.run('UPDATE edits SET status = ? WHERE id = ?', [status, id])

    edit.status = status

    res.render('check_edit', { edit })
})



app.listen(PORT, () => {
    console.log(`Example app listening on port ${PORT}`)
})


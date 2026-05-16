const express = require('express')
const engine = require('express-engine-jsx');
const sqlite3 = require('sqlite3').verbose();
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { exec } = require('child_process');
const fs = require('fs');
var cookieParser = require('cookie-parser')

const app = express()
const port = 3000
const db = new sqlite3.Database(':memory:');

const ADMIN_PASS = process.env.ADMIN_PASS ?? crypto.randomUUID()
const JWT_SECRET = process.env.JWT_SECRET ?? crypto.randomUUID()

const ALPHANUMERIC = /^[0-9a-zA-Z]+$/;
const URL_WHITELIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/.-:"
const QUERY_WHITELIST = '?$'


app.set('views', './views');
app.set('view engine', 'jsx');
app.use(express.urlencoded({ extended: true }));

app.engine('jsx', engine);


db.serialize(() => {
  db.run('CREATE TABLE users ( \
    username TEXT UNIQUE, \
    password TEXT, \
    is_admin BOOLEAN \
  )');
  db.run(`INSERT INTO users VALUES ('gabibbo', '${ADMIN_PASS}', true)`)

});


const authenticateToken = (req, res, next) => {
  let token = null;
  let cookies = req.headers.cookie;
  if (cookies) {
    cookies = cookies.split(";").find(e => e.split("=")[0].replace(" ", "") === "auth")
    if (cookies != undefined) token = cookies.split("=")[1].replace(" ", "")
  }

  if (token == null) {
    req.user = null;
    next()
    return;
  }
  const user = jwt.decode(token)
  if (typeof (user.username) !== "string") return res.sendStatus(400)
  req.user = user
  next()

}

async function SHA256(message) {
  const msgUint8 = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}


app.get('/', authenticateToken, (req, res) => {
  res.locals.username = req?.user?.username
  res.render('home');
})

app.get('/login', authenticateToken, (req, res) => {
  res.render('login', {});
})
app.post('/login', authenticateToken, (req, res) => {

  console.error(req.body)
  const fail_check = [
    typeof (req.body.username) !== "string",
    typeof (req.body.password) !== "string",
    !req.body.username.match(ALPHANUMERIC),
    !req.body.password.match(ALPHANUMERIC),
  ].find(e => e)
  if (fail_check) {
    res.status(400)
    res.locals.error = "Scegli un utente ed una password alfanumerici"
    res.render('login');
    return;
  }
  if (req.body.submit === "Registrati") {
    db.run('INSERT INTO users VALUES (?, ?, false)', [req.body.username, req.body.password], (err) => {
      if (err) {
        res.status(400)
        res.locals.error = "L'utente esiste già"
        res.render('login');
        return;
      }
      res.cookie('auth', jwt.sign({
        username: req.body.username,
        is_admin: false
      }, JWT_SECRET), { httpOnly: true });
      res.redirect('/');

    })
    return
  }

  db.get(
    'SELECT is_admin FROM users WHERE username=? AND password=?',
    [req.body.username, req.body.password],
    (err, row) => {
      if (row === undefined) {
        res.status(403)
        res.locals.error = "L'utente non esiste"
        res.render('login');
      } else {
        res.cookie('auth', jwt.sign({
          username: req.body.username,
          is_admin: row.is_admin
        }, JWT_SECRET), { httpOnly: true });
        res.redirect('/');
      }
    }
  );
})

app.get("/files", authenticateToken, async (req, res) => {
  if (req.user === null) {
    res.redirect(303, "/login");
    return;
  }
  const userdir = `/users/${await SHA256(req.user.username)}`
  fs.readdir(userdir, (err, files) => {
    res.locals.username = req.user.username
    if (files === undefined) {
      fs.mkdir(userdir, (err) => {
        res.locals.files = []
        res.render("files")

      })
    } else {
      res.locals.files = files
      res.render("files")
    }
  });

})
app.post("/files", authenticateToken, async (req, res) => {
  if (req.user === null) {
    res.redirect(303, "/login");
    return;
  }
  const url = decodeURI(req.body.url);
  const fail_check = [
    typeof (url) !== "string",
    Array.from(url).some(x => !(URL_WHITELIST + QUERY_WHITELIST).includes(x)),
    ( // controllo che la querystring non superi i 25 caratteri, non vogliamo cose strane
      url.length - Math.min(...Array.from(QUERY_WHITELIST).map(x => url.indexOf(x) != -1 ? url.indexOf(x) : 1000))
    ) > 25,
    !(url.startsWith("https") || url.startsWith("http")),
    url.toLowerCase().includes("ftp"),
    url.toLowerCase().includes(".."),
    req.user.username.toLowerCase() == "gabibbo"

  ].find(e => e)
  if (fail_check) {

    res.status(400)
    res.send("L'URL non rispetta i nostri criteri, scegline un altro. Se sei tu Gabibbo, sappi che le tue oscenità non verranno più tollerate sul nostro sito.");
    return;
  }

  exec(`wget ${url} --max-redirect 0`, {
    cwd: `/users/${await SHA256(req.user.username)}`
  })
  res.redirect(303, '/files')
})
app.get("/download/", authenticateToken, async (req, res) => {
  if (req.user === null) {
    res.redirect(303, "/login");
    return;
  }
  const filename = decodeURI(req.query.fileName);
  const path = `/users/${await SHA256(req.user.username)}/${filename}`
  const fail_check = [
    typeof (filename) !== "string",
    Array.from(filename).some(x => !URL_WHITELIST.includes(x)),
    !fs.existsSync(path),
  ].find(e => e)
  if (fail_check) {
    res.status(400)
    res.send("L'URL non rispetta i nostri criteri, scegline un altro");
    return;
  }
  res.sendFile(path)
})




app.listen(port, () => {
  console.log(`Bibvault listening on port ${port}`)
})

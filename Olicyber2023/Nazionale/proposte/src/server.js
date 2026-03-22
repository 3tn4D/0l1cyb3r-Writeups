const express = require('express')
const cookieParser = require('cookie-parser')

const { visit_url } = require('./visit_url.js')

const app = express()
const port = 3000

app.set('view engine', 'ejs');

app.use(express.static('public'))
app.use(cookieParser())
app.use(express.urlencoded({extended: false}))


app.get('/', (req, res) => {
    res.render('home')
})

app.get('/stego', (req, res) => {
    res.render('stego')
})

app.get('/altro', (req, res) => {
    res.render('altro')
})

app.post('/stego', (req, res) => {
    let desc = req.body['text']

    desc = desc.replaceAll('$','€')
    desc = desc.replaceAll('`',"'")
    desc = desc.replaceAll('\\','/')

    res.render('typewriter', {desc: desc})
})

app.post('/altro', (req, res) => {
    let url = req.body['url']

    if (url && typeof url === 'string' && /https?:\/\//.test(url)){
        visit_url(url)
    }

    res.render('conferma')
})


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

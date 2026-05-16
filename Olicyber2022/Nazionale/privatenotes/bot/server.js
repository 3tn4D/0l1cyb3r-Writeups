const express = require('express')
const bot = require('./bot')

const app = express()
app.use(express.json());


app.post('/visit', async function (req, res) {
	res.set('Content-Type', 'text/html');

	console.log(req.body)

	const url = req.body.url;
	if (typeof url === 'string' && url.startsWith('http')) {
		try {
			bot.visit(url);
			res.send('visited');
			return;
		} catch (e) {
			console.log(e);
			res.status(500);
			res.send('failed');
			return;
		}
	}
	res.status(400);
	res.send('bad url');
})


app.listen(9999, '0.0.0.0');

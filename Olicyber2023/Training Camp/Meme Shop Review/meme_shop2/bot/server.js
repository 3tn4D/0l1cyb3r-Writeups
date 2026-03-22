const express = require('express')
const bot = require('./bot')

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/visit', async function (req, res) {
	console.log(req.body)

	try {
		const url = req.body.url;

		console.log("url: ", url)

		bot.visit(url);
		res.send();
	} catch (e) {
		console.log(e);
		res.status(400);
		res.send('bad url');
	}
})

app.listen(9999, '0.0.0.0');

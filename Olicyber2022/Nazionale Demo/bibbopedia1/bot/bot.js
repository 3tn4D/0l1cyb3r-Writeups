const puppeteer = require('puppeteer')
const jwt = require('jsonwebtoken')


const domain = process.env['DOMAIN']
const webapp_url = 'http://' + domain + ':' + process.env['PORT']

const token = jwt.sign({ username: 'admin', privileges: 'admin' }, process.env['JWT_SECRET_KEY'])

console.log(token)

async function visit(url) {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] })

	// Set cookie
	var page = await browser.newPage()
	await page.setCookie(
		{ name: 'session', value: token, domain: domain, path: '/', httpOnly: true }
	)

	//await page.goto(webapp_url)
	//console.log(await page.cookies())

	try {
		// Contacting URL after auth
		await page.goto(url, { timeout: 5000 })

		await new Promise(resolve => setTimeout(resolve, 2000));
		await page.close()
		await browser.close()
	} catch (e) {
		await browser.close()
		throw (e)
	}

}

module.exports = { visit }

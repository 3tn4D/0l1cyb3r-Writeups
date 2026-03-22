const puppeteer = require('puppeteer')
const jwt = require('jsonwebtoken')

const webapp_url = process.env['DOMAIN']
const username = "administrator"
const password = process.env["ADMIN_PASSWORD"]


async function visit(request_url) {
	const browser = await puppeteer.launch({ args: ['--no-sandbox'] })

	// Set cookie
	var page = await browser.newPage()

	try {
		// login as admin
		await page.goto(webapp_url + '/login.php', { timeout: 1000 })

		await page.type('#username', username);
		await page.type('#password', password);

		await page.click('#submit');

		// go to asked post and wait a bit
		await page.goto(request_url, { timeout: 5000 })

		await new Promise(resolve => setTimeout(resolve, 2000));
		await page.close()
		await browser.close()
	} catch (e) {
		await browser.close()
		throw (e)
	}

}

module.exports = { visit }

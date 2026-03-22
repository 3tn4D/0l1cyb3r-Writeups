
const HEADLESS_URL = process.env['HEADLESS_URL'] || 'http://headless:5000/'
const HEADLESS_SECRET = process.env['HEADLESS_SECRET'] || 'supersecret'
const CHALLENGE_HOST = process.env['CHALLENGE_HOST'] || 'web'
const FLAG = process.env['FLAG'] || 'flag{test}'

async function visit_url(url){

    console.log('Visiting URL: ' + url)

    try {
        await fetch(HEADLESS_URL,{
            method:'POST',
            headers:{'Content-Type':'application/json','X-Auth':HEADLESS_SECRET},
            body:JSON.stringify({
                actions:[
                    {'type':'request','url':'http://' + CHALLENGE_HOST},
                    {'type':'set-cookie','name':'flag','value':FLAG},
                    {'type':'request','url':url},
                    {'type':'sleep','time':1}
                ]
            })
        })
    } catch (error) {
        console.error(error)
    }
}


module.exports = { visit_url }
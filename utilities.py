import aiohttp

from inspect import getmembers, isfunction, getdoc

class Urban():
    @staticmethod
    async def search(term, length):
        req = await aiohttp.request(
            'GET', "http://api.urbandictionary.com/v0/define", params={'page': 1, 'term': term}
            )
        resp = await req.json()
        if len(resp['list']) == 0:
            return "No results for {0}".format(term)
        define = resp['list'][0]['definition']
        if len(define) > length:
            define = ' '.join(define[:length+1].split(' ')[0:-1])
        return define + " (" + resp['list'][0]['permalink'] + ")"

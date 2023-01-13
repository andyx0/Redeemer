import re
import asyncio
import aiohttp
from configparser import ConfigParser
from itertools import product
from pokemonCodeRedeemer import codeDict
from pokemonCodeRedeemer import ansi
from pokemonCodeRedeemer import chunks


def process_results(response):
    pattern = re.compile(r'<li>(.+: )(?:<em>)?(.+?)(?:</em>)?</li>')  # isolate lines with redemption results
    results = pattern.findall(response)
    if results:
        for item in results:
            if 'CODE' in item[1].upper():
                print(ansi.RED+''.join(item))
            else:
                print(ansi.GREEN+''.join(item))
    else:
        pattern = re.compile(r'<div class="alert.+?>((.|\n)+?)</div>')  # isolate error messages
        results = pattern.findall(response)
        for item in results:
            print(re.sub(r'<[^<]+?>', '', ansi.RED+''.join(item).strip()))  # remove html tags with regex
    print(ansi.END, end='')


if __name__ == '__main__':
    config = ConfigParser()

    config.read('settings.ini')
    session_id = config.get('Session', 'session_id')
    csrf_token = config.get('Session', 'csrf_token')
    source_codes = config.get('Global', 'redeem_codes')
    limit = 10  # redeem 10 codes at a time (web client limit)

    print("session_id:", session_id)
    print("csrf_token:", csrf_token)

    cookies = {
        'csrftoken': csrf_token,
        'main_session_id': session_id,
        'op_session_id': session_id,
        'django_language': 'en'
    }

    headers = {
        'Origin': 'https://www.pokemon.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-control': 'max-age=0',
        'Referer': 'https://www.pokemon.com/us/pokemon-trainer-club/enter-codes',
        'Connection': 'keep-alive'
    }

    async def redeem_codes(session, codes=[]):
        print("Number of codes being redeemed this request:", len(codes))
        # print("Codes being redeemed this request:", codes)
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'code': codes,
            'hidden_code': codes
        }
        async with session.post('https://www.pokemon.com/us/pokemon-trainer-club/enter-codes', data=payload) as response:
            print("Response received")
            process_results(await response.text())

    async def main():
        codes = []
        with open(source_codes) as sc:
            for line in sc:
                strippedLine = line.replace('-', '').rstrip().upper()
                if strippedLine == '':
                    break
                unknownCount = strippedLine.count('?')
                if unknownCount > 0:
                    cartesian_product = product(codeDict, repeat=unknownCount)
                    for tuple in cartesian_product:
                        guess = strippedLine
                        for char in tuple:
                            guess = guess.replace('?', char, 1)
                        codes.append(guess)
                else:
                    codes.append(strippedLine)
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            await asyncio.gather(*(redeem_codes(session, chunk) for chunk in chunks(codes, limit)))

    try:
        asyncio.run(main())
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

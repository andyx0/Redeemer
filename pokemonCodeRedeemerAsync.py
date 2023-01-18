import re
import asyncio
import aiohttp
from itertools import product
from pokemonCodeRedeemer import code_dict, session_id, csrf_token, source_codes
from pokemonCodeRedeemer import cookies, headers
from pokemonCodeRedeemer import ansi
from pokemonCodeRedeemer import chunks


async def process_results(response):
    print("Response received")
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


async def redeem_codes(session, codes):
    print("Number of codes being redeemed this request:", len(codes))
    # print("Codes being redeemed this request:", codes)
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'code': codes,
        'hidden_code': codes
    }
    async with session.post('https://www.pokemon.com/us/pokemon-trainer-club/enter-codes', data=payload) as response:
        await process_results(await response.text())


async def main():
    limit = 10  # redeem 10 codes at a time (web client limit)

    print("session_id:", session_id)
    print("csrf_token:", csrf_token)

    codes = []
    with open(source_codes) as sc:
        for line in sc:
            strippedLine = line.replace('-', '').rstrip().upper()
            if strippedLine == '':
                break
            unknownCount = strippedLine.count('?')
            if unknownCount > 0:
                cartesian_product = product(code_dict, repeat=unknownCount)
                for tupl in cartesian_product:
                    guess = strippedLine
                    for char in tupl:
                        guess = guess.replace('?', char, 1)
                    codes.append(guess)
            else:
                codes.append(strippedLine)
    timeout = aiohttp.ClientTimeout(total=1200)
    async with aiohttp.ClientSession(timeout=timeout, headers=headers, cookies=cookies) as session:
        await asyncio.gather(*(redeem_codes(session, chunk) for chunk in chunks(codes, limit)))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

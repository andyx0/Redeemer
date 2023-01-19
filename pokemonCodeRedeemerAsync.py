import asyncio
import aiohttp
from pokemonCodeRedeemer import session_id, csrf_token, source_codes
from pokemonCodeRedeemer import cookies, headers
from pokemonCodeRedeemer import chunks, solution1, load_codes


async def process_results(response):
    print("Response received")
    solution1(response)


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

    codes = load_codes(source_codes)
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

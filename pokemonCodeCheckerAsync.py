import asyncio
import aiohttp
from pokemonCodeRedeemer import load_codes
from pokemonCodeChecker import session_id, source_codes, cookies
from pokemonCodeChecker import process_results, check_duplicates


async def check_code(session, code):
    data = [('code', code)]
    async with session.post('https://www.pokemon.com/us/pokemon-trainer-club/verify_code/', data=data) as response:
        code_json = await response.json()
    process_results(code_json)


async def main():
    print("session_id:", session_id)
    check_duplicates(source_codes)

    codes = load_codes(source_codes)
    async with aiohttp.ClientSession(cookies=cookies) as session:
        await asyncio.gather(*(check_code(session, code) for code in codes))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

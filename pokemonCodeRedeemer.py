import re
import requests
# import timeit
from configparser import ConfigParser
from itertools import product

code_dict = set('24679BCDGHJKLMNPQRTVWXYZ')

config = ConfigParser()
config.read('settings.ini')
session_id = config.get('Session', 'session_id')
csrf_token = config.get('Session', 'csrf_token')
source_codes = config.get('Global', 'redeem_codes')

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

# cookies = {
#     'csrftoken': csrf_token,
#     'op_session_id': session_id
# }

# headers = {
#     'Origin': 'https://sso.pokemon.com',
#     'Referer': 'https://sso.pokemon.com'
# }


class ansi:
    END = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CLEAR = '\033[2J'


def solution1(response):
    pattern = re.compile(r'<li>(.+: )(?:<em>)?(.+?)(?:</em>)?</li>')  # isolate lines with redemption results
    results = pattern.findall(response)
    if results:
        for item in results:
            if 'CODE' in item[1].upper():
                # ansi.RED+''.join(item)
                print(ansi.RED+''.join(item))
            else:
                print(ansi.GREEN+''.join(item))
    else:
        pattern = re.compile(r'<div class="alert.+?>((.|\n)+?)</div>')  # isolate error messages
        results = pattern.findall(response)
        for item in results:
            print(re.sub(r'<[^<]+?>', '', ansi.RED+''.join(item).strip()))  # remove html tags with regex
    print(ansi.END, end='')


# def solution2(response):
#     for item in response.splitlines():
#         if '<em>' in item:  # only located in lines with redemption results
#             for elem in codes:
#                 if elem in item:
#                     output = re.sub(r'<[^<]+?>', '', item.strip())  # remove html tags with regex
#                     if 'code' in output.lower():
#                         ansi.RED+output
#                         # print(ansi.RED+output)
#                     else:
#                         print(ansi.GREEN+output)
#     print(ansi.END, end='')


# def solution3(response):
#     for item in response.splitlines():
#         for elem in codes:
#             if elem in item:
#                 output = re.sub(r'<[^<]+?>', '', item.strip())  # remove html tags with regex
#                 if 'code' in output.lower():
#                     ansi.RED+output
#                     # print(ansi.RED+output)
#                 else:
#                     print(ansi.GREEN+output)
#     print(ansi.END, end='')


def load_codes(source_codes):
    codes = []
    with open(source_codes) as sc:
        for line in sc:
            strippedLine = line.replace('-', '').rstrip().upper()
            if strippedLine == '':
                continue
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
    return codes


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def redeem_codes(codes):
    print("Number of codes being redeemed this request:", len(codes))
    # print("Codes being redeemed this request:", codes)
    payload = {
        'csrfmiddlewaretoken': csrf_token,
        'code': codes,
        'hidden_code': codes
    }
    response = requests.post(
        'https://www.pokemon.com/us/pokemon-trainer-club/enter-codes',
        headers=headers,
        cookies=cookies,
        data=payload)
    print("Response received")
    # print(response.text)
    # with open('response.txt', 'wt') as text_file:
    #     text_file.write(response.text)
    # print(ansi.GREEN+"Time for solution 1:", timeit.timeit(lambda: solution1(response), number=1000), ansi.END)
    # print(ansi.GREEN+"Time for solution 2:", timeit.timeit(lambda: solution2(response), number=1000), ansi.END)
    # print(ansi.GREEN+"Time for solution 3:", timeit.timeit(lambda: solution3(response), number=1000), ansi.END)
    solution1(response.text)


def main():
    limit = 10  # redeem 10 codes at a time (web client limit)

    print("session_id:", session_id)
    print("csrf_token:", csrf_token)

    codes = load_codes(source_codes)
    for chunk in chunks(codes, limit):
        redeem_codes(chunk)


if __name__ == '__main__':
    try:
        main()
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

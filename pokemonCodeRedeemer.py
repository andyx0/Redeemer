# import timeit
import requests
import re
from configparser import ConfigParser
from itertools import product

codeDict = ['2', '4', '6', '7', '9', 'Q', 'W', 'R', 'T', 'Y', 'P',
            'D', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']


class ansi:
    END = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    CLEAR = '\033[2J'


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

    def redeem_codes(codes=[]):
        print("Number of codes being redeemed this request:", len(codes))
        print("Codes being redeemed this request:", codes)
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
        # text_file = open("response.txt", "wt")
        # text_file.write(response.text)
        # text_file.close()
        def solution1():
            pattern = re.compile(r'<li>(.+?)<em>(.+?)</em></li>')  # isolate lines with redemption results
            results = pattern.findall(response.text)
            if len(results):
                for item in results:
                    if "code" in item[1].lower():
                        # ansi.RED+''.join(item)
                        print(ansi.RED+''.join(item))
                    else:
                        print(ansi.GREEN+''.join(item))
            else:
                pattern = re.compile(r'<div class="alert.+?>((.|\n)+?)</div>')  # isolate error messages
                results = pattern.findall(response.text)
                for item in results:
                    print(re.sub('<[^<]+?>', '', ansi.RED+''.join(item).strip()))  # remove html tags with regex
            print(ansi.END, end='')
        # def solution2():
        #     for item in response.text.splitlines():
        #         if "<em>" in item:  # only located in lines with redemption results
        #             for elem in codes:
        #                 if elem in item:
        #                     output = re.sub('<[^<]+?>', '', item.strip())  # remove html tags with regex
        #                     if "code" in output.lower():
        #                         ansi.RED+output
        #                         # print(ansi.RED+output)
        #                     else:
        #                         print(ansi.GREEN+output)
        #     print(ansi.END, end='')
        # def solution3():
        #     for item in response.text.splitlines():
        #         for elem in codes:
        #             if elem in item:
        #                 output = re.sub('<[^<]+?>', '', item.strip())  # remove html tags with regex
        #                 if "code" in output.lower():
        #                     ansi.RED+output
        #                     # print(ansi.RED+output)
        #                 else:
        #                     print(ansi.GREEN+output)
        #     print(ansi.END, end='')
        # print(ansi.GREEN+"Time for solution 1:", timeit.timeit(solution1, number=1000), ansi.END)
        # print(ansi.GREEN+"Time for solution 2:", timeit.timeit(solution2, number=1000), ansi.END)
        # print(ansi.GREEN+"Time for solution 3:", timeit.timeit(solution3, number=1000), ansi.END)
        solution1()
    try:
        with open(source_codes) as sc:
            line = " "
            while line != "":
                codes = []
                for x in range(limit):
                    line = sc.readline()
                    strippedLine = line.replace("-", "").rstrip().upper()
                    if strippedLine == "":
                        break
                    unknownCount = strippedLine.count("?")
                    if unknownCount > 0:
                        cartesian_product = product(codeDict, repeat=unknownCount)
                        for tuple in cartesian_product:
                            guess = strippedLine
                            for char in tuple:
                                guess = guess.replace("?", char, 1)
                            codes.append(guess)
                            if len(codes) >= limit:  # break up large products into multiple requests
                                redeem_codes(codes)
                                codes = []
                    else:
                        codes.append(strippedLine)
                redeem_codes(codes)
        sc.close
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue ...")

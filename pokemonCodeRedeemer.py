import requests
import re
from configparser import ConfigParser
from itertools import product

codeDict = ['2', '4', '6', '7', '9', 'Q', 'W', 'R', 'T', 'Y', 'P',
            'D', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

if __name__ == '__main__':
    config = ConfigParser()

    config.read('settings.ini')
    session_id = config.get('Session', 'session_id')
    source_codes = config.get('Global', 'redeem_codes')
    csrf_token = config.get('Session', 'csrf_token')

    print("session_id: " + session_id)
    print("csrf_token: " + csrf_token)

    cookies = {
        'csrftoken': csrf_token,
        'main_session_id': session_id,
        'op_session_id': session_id,
        'django_language': 'en'
    }

    headers = {
        'Origin': 'https://www.pokemon.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-control': 'max-age=0',
        'Referer': 'https://www.pokemon.com/us/pokemon-trainer-club/enter-codes',
        'Connection': 'keep-alive'
    }

    def redeem_codes(arr=[]):
        print("Num codes being redeemed this request: " + str(len(arr)))
        print("Codes being redeemed this request: " + str(arr))
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'code': arr,
            'hidden_code': arr
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
        for item in response.text.split("\n"):
            for elem in arr:
                if elem in item:
                    print(re.sub('<[^<]+?>', '', item.strip()))  # remove html tags with regex
                    # print(item.strip())
    try:
        with open(source_codes) as sc:
            line = sc.readline()
            while line != "":
                arr = []
                # limit = 100  # redeem 100 codes at a time (server response limit?)
                limit = 10  # redeem 10 codes at a time (web client limit)
                for x in range(limit):
                    if line == "":
                        break
                    strippedLine = line.replace("-", "").rstrip().upper()
                    unknownCount = strippedLine.count("?")
                    if unknownCount > 0:
                        cartesian_product = product(codeDict, repeat=unknownCount)
                        for tuple in cartesian_product:
                            guess = strippedLine
                            for char in tuple:
                                guess = guess.replace("?", char, 1)
                            arr.append(guess)
                            if len(arr) >= limit:  # break up large products into multiple requests
                                redeem_codes(arr)
                                arr = []
                    else:
                        arr.append(strippedLine)
                    line = sc.readline()
                redeem_codes(arr)
        sc.close
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue ...")

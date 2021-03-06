import requests
import json
from configparser import ConfigParser
from itertools import product
from pokemonCodeRedeemer import codeDict


if __name__ == '__main__':
    config = ConfigParser()
        
    config.read('settings.ini')
    session_id = config.get('Session', 'session_id')
    source_codes = config.get('Global', 'source_codes')

    print(session_id)

    cookies = {
        'main_session_id': session_id,
        'op_session_id': session_id
    }

    def check_code(code):
        data = [('code', code)]
        response = requests.post(
            'https://www.pokemon.com/us/pokemon-trainer-club/verify_code/',
            headers={},
            cookies=cookies,
            data=data)
        # print(response.text)
        code_json = json.loads(response.text)
        if code_json['valid']:
            print("{}: {}".format(code_json['coupon_code'], code_json['coupon_title']))
            # cc.write("{},{},{} \n".format(
            # 	code_json['valid'], code_json['coupon_code'], code_json['coupon_title'].encode('utf-8')))
        else:
            print("{}: {}".format(code_json['coupon_code'], code_json['error_message']))

    try:
        with open(source_codes) as sc:
            line = sc.readline()
            codes = []
            while line != "":
                strippedLine = line.replace("-", "").rstrip().upper()
                unknownCount = strippedLine.count("?")
                if unknownCount > 0:
                    cartesian_product = product(codeDict, repeat=unknownCount)
                    for tuple in cartesian_product:
                        guess = strippedLine
                        for char in tuple:
                            guess = guess.replace("?", char, 1)
                        codes.append(guess)
                else:
                    codes.append(strippedLine)
                line = sc.readline()
            for code in codes:
                check_code(code)
        sc.close
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue ...")

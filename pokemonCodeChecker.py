import requests
from configparser import ConfigParser
from itertools import product
from pokemonCodeRedeemer import codeDict
from pokemonCodeRedeemer import ansi


if __name__ == '__main__':
    config = ConfigParser()
        
    config.read('settings.ini')
    session_id = config.get('Session', 'session_id')
    source_codes = config.get('Global', 'source_codes')

    print("session_id:", session_id)

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
        code_json = response.json()
        if code:
            if code_json['valid']:
                print(ansi.GREEN+code_json['coupon_code']+":", code_json['coupon_title'])
                # cc.write("{},{},{} \n".format(
                # 	code_json['valid'], code_json['coupon_code'], code_json['coupon_title'].encode('utf-8')))
            else:
                print(ansi.RED+code_json['coupon_code']+":", code_json['error_message'])
        else:
            print(ansi.RED+code_json['error_msg'])
        print(ansi.END, end='')

    def print_duplicates():
        print("Duplicate codes:")
        codes = set()
        with open(source_codes) as sc:
            for line in sc:
                strippedLine = line.replace('-', '').rstrip().upper()
                if strippedLine in codes:
                    print(line.rstrip())
                else:
                    codes.add(strippedLine)

    try:
        print_duplicates()
        codes = []
        with open(source_codes) as sc:
            for line in sc:
                strippedLine = line.replace('-', '').rstrip().upper()
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
        for code in codes:
            check_code(code)
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

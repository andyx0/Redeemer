import requests
from configparser import ConfigParser
from pokemonCodeRedeemer import ansi, load_codes

config = ConfigParser()
config.read('settings.ini')
session_id = config.get('Session', 'session_id')
source_codes = config.get('Global', 'source_codes')

cookies = {
    'main_session_id': session_id,
    'op_session_id': session_id
}


def process_results(code_json):
    if 'detail' in code_json:
        print(ansi.RED+code_json['detail'])
    elif 'error_msg' in code_json:
        print(ansi.RED+code_json['error_msg'])
    elif 'error_message' in code_json:
        print(ansi.RED+code_json['coupon_code']+":", code_json['error_message'])
    elif 'valid' in code_json:
        print(ansi.GREEN+code_json['coupon_code']+":", code_json['coupon_title'])
        # cc.write("{},{},{} \n".format(
        # 	code_json['valid'], code_json['coupon_code'], code_json['coupon_title'].encode('utf-8')))
    print(ansi.END, end='')


def check_code(code):
    data = [('code', code)]
    response = requests.post(
        'https://www.pokemon.com/us/pokemon-trainer-club/verify_code/',
        headers={},
        cookies=cookies,
        data=data)
    # print(response.text)
    process_results(response.json())


def check_duplicates(source_codes):
    codes = set()
    dupes = set()
    with open(source_codes) as sc:
        for line in sc:
            strippedLine = line.replace('-', '').rstrip().upper()
            if strippedLine in codes:
                dupes.add(line.rstrip())
            else:
                codes.add(strippedLine)
    if len(dupes):
        print("Duplicate codes:", dupes)


def main():
    print("session_id:", session_id)
    check_duplicates(source_codes)

    codes = load_codes(source_codes)
    for code in codes:
        check_code(code)


if __name__ == '__main__':
    try:
        main()
    except:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
        input("Press Enter to continue...")

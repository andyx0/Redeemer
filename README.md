# Redeemer
A simple python script that requires a few manual steps to check or redeem a list of codes.

# Steps for both Checker and Redeemer (using Chrome)
1) Go to https://www.pokemon.com and login
2) Go to https://www.pokemon.com/us/pokemon-trainer-club/enter-codes, click the 'I'm not a robot' button, and complete the captcha
3) Submit any text in the 'enter code' field, which finishes the verification and flags your session id as not a robot
4) Press F12
5) Select the Application tab
6) Select the Cookies tab on the left hand side under 'Storage'
7) Select https://www.pokemon.com
8) Find the cookie called 'main_session_id' and copy the value of 'main_session_id' into the session_id field in settings.ini
9) Find the cookie called 'csrftoken' and copy the value of 'csrftoken' into the csrf_token field in settings.ini
10) Copy your list of codes into codes.txt for checker or redeemCodes.txt for redeemer, one code per line.
11) Run `python pokemonCodeChecker.py` or `python pokemonCodeRedeemer.py`
12) You should now see an output in the console of the server response to your codes.

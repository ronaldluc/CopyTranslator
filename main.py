import time

import pyperclip
from translation import Translate

# To download:
# python -m spacy download xx_ent_wiki_sm
# python -m spacy download en_core_web_sm


if __name__ == '__main__':
    print('Started')
    recent_value = ""
    trans = Translate()
    while True:
        tmp_value = pyperclip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            print(f'Temp: {tmp_value}')
            tmp_value = trans.process_clipboard(tmp_value)
            print(f'Result: {tmp_value}')
            if tmp_value:
                pyperclip.copy(tmp_value)
                recent_value = tmp_value
        time.sleep(0.1)
    print('Ended')

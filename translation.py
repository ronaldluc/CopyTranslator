import re
import time
import sys
import os
# from pprint import pprint

from lang_map import country2langs

sys.path.append(os.path.abspath("SO_site-packages"))

import pyperclip
# from googletrans import Translator
from translate import Translator


# import spacy


# %%

def remove_special(text):
    return ' '.join(re.split(r'[\s]+', text))


def remove_all_caps(text, src):
    res = ' '.join([x.lower() if x.isupper() else x for x in text.split(' ')])
    return res


# def remove_all_caps(text, src):
# if src == 'en':
#     nlp = spacy.load('en_core_web_sm')
# else:
#     nlp = spacy.load('xx_ent_wiki_sm')
#     nlp.add_pipe(nlp.create_pipe('sentencizer'))
# text_sentences = [sentence.text for sentence in nlp(text).sents]
# text_sentences = [x.strip() + '.' for x in text.split('.!?')]
# text_sentences = [x.strip() for x in re.split(r'[.!?]', text)]
# # text_sentences[-1] = text_sentences[-1][:-1]
#
#
# res = []
# for sentence in text_sentences:
#     res = ' '.join([x.lower() if x.isupper() else x for x in text.split(' ')])
#     res.append(sentence.capitalize())
#
# return res


def build_regex():
    state = r'( ((?P<start>start|on)?|(?P<stop>stop|off)))'
    src_dest = r'( (?P<src>\w+) to (?P<dest>\w+)?|( from (?P<src2>\w+))?( to (?P<dest2>\w+))?)'
    whole = fr'trans(late|lator)?{state}?{src_dest}'
    return re.compile(whole)


def to_lang_code(text):
    return country2langs[text].split(',')[0]


class Translate:
    def __init__(self, dest_lang='cs'):
        self.translator = Translator(dest_lang)
        self.src = 'cs'
        self.dest = dest_lang
        self.translate = False
        self.commands_re = build_regex()
        # self.translator = Translator(service_urls=['translate.google.cz'])    # googletrans

    @property
    def dest(self):
        return self.translator.to_lang

    @dest.setter
    def dest(self, value):
        self.translator = Translator(to_lang=value, from_lang=self.src)

    @property
    def src(self):
        return self.translator.from_lang

    @src.setter
    def src(self, value):
        self.translator = Translator(to_lang=self.dest, from_lang=value)

    def state(self):
        print(f'\tTranslate? {str(self.translate).upper()} | Src: {self.src} | Dest: {self.dest}')

    def process_clipboard(self, text):

        if self.check_command(text) or not self.translate:
            self.state()
            return None
        else:
            self.state()
            # self.src = self.translator.detect(text).lang
            text = remove_special(text)
            text = remove_all_caps(text, self.src)
            print(f'\tGoing to translator: {text}')
            return self.translator.translate(text)

    def check_command(self, text):
        text = text.lower().strip()
        matches = self.commands_re.fullmatch(text)
        if matches is None:
            return False
        matches = matches.groupdict()
        matches['src'] = next(filter(None, [matches['src'], matches['src2']]), False)
        matches['dest'] = next(filter(None, [matches['dest'], matches['dest2']]), False)
        print(matches)
        if matches['start']:
            self.translate = True
        if matches['stop']:
            self.translate = False
        if matches['dest']:
            self.dest = to_lang_code(matches['dest'])
        if matches['src']:
            self.src = to_lang_code(matches['src'])

        return True

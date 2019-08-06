#! /usr/bin/env python3

import lxml.html
import requests
from collections import namedtuple
from time import sleep


Colors = namedtuple(
    'Colors',
    ['red', 'green', 'white', 'yellow', 'gray', 'none']
)
C = Colors(
    red='\033[1;31m',
    green='\033[1;32m',
    white='\033[1;37m',
    yellow='\033[1;33m',
    gray='\033[0;37m',
    none='\033[0m'
)


class HTMLSearch:

    def __init__(self, element, tag, attribute, value):
        if type(element) == str:
            element = lxml.html.fromstring(element)
        if tag == None:
            if self._has_attribute(element, attribute, value):
                self.value = element
            else:
                raise _TagNotFound(tag, attribute, value)
        else:
            self.value = self._search(element, tag, attribute, value)
            if self.value == None:
                raise _TagNotFound(tag, attribute, value)


    def _has_attribute(self, sub_element, attribute, value):
        if attribute == None and value == None:
            return True
        for attribute2, value2 in sub_element.attrib.items():
            if type(attribute) == tuple and \
               type(value) == tuple:
                if attribute2.find(attribute[0]) != -1 and \
                   value2.find(value[0]) != -1:
                    return True

            elif type(attribute) == tuple:
                if attribute2.find(attribute[0]) != -1 and \
                   value2 == value:
                    return True

            elif type(value) == tuple:
                if attribute2 == attribute and \
                   value2.find(value[0]) != -1:
                    return True

            elif value == None:
                if attribute2 == attribute:
                    return True

            elif attribute == None:
                if value2 == value:
                    return True

            else:
                if attribute2 == attribute and \
                   value2 == value:
                    return True
        return False


    def _search(self, element, tag, attribute, value):
        if element == None:
            return None
        for sub_element in element.getchildren():
            if sub_element.tag == tag:
                if attribute == None:
                    return sub_element
                if self._has_attribute(sub_element, attribute, value):
                    return sub_element
            result = self._search(sub_element, tag, attribute, value)
            if result == None:
                continue
            return result
        return None


class _TagNotFound(Exception):

    def __init__(self, tag, attr=None, value=None):
        text = 'could not found HTML tag {!r} '.format(tag)
        if attr:
            text += 'with attribute '
            if type(attr) == tuple:
                text += 'which should contain {!r} '.format(attr[0])
            else:
                text += '{!r} '.format(attr)
            text += 'and value '
            if type(value) == tuple:
                text += 'which should contain {!r}'.format(value[0])
            else:
                text += '{!r}'.format(value)
        Exception.__init__(self, text)


class Request:

    def __init__(self,
                 url,
                 headers = {
                    'accept': 'text/html,application/xhtml+xml,applica'\
                              'tion/xml;q=0.9,*/*;q=0.8',
                    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86'\
                                  '_64; rv:50.0) Gecko/20100101 Firefo'\
                                  'x/50.0'
                }
    ):
        self.url = url
        self.headers = headers


    def parse(self, body):
        return []


    def fetch(self, word):
        return ''


    def _check_word(self, word):
        if word.isalpha():
            return
        raise RuntimeError(
            '#A word MUST contain anly alphabet characters'
        )


    def sentences(self, word):
        self._check_word(word)
        try:
            body = self.fetch(word)
        except Exception as error:
            if str(error)[0] == '#':
                raise
            raise RuntimeError(
                '#could not fetch data from {!r} for {!r}, {}'.format(
                    self.url,
                    word,
                    str(error)
                )
            )
        try:
            sentences = self.parse(body)
        except Exception as error:
            if str(error)[0] == '#':
                raise
            raise RuntimeError(
                '#could not parse data from {!r} for {!r}, {}'.format(
                    self.url,
                    word,
                    str(error)
                )
            )
        if sentences == []:
            raise RuntimeError(
                '#could not found any sentence from {!r} for {!r}'.\
                format(self.url, word)
            )
        return sentences





class SentencedictCom(Request):

    def __init__(self):
        super(SentencedictCom, self).__init__(
            url='http://sentencedict.com/'
        )


    def parse(self, body):
        sentences = HTMLSearch(body, 'div', 'id', 'all').value
        result = []
        for sentence in sentences.getchildren():
            sentence = sentence.text_content()
            if sentence != None:
                parts = sentence.split(' ', 1)
                if parts[0].        \
                   replace('(', '').\
                   replace(')', '').\
                   isdigit() and len(parts) == 2:
                    result.append(parts[1])
        return result


    def fetch(self, word):
        try:
            request = requests.get(
                self.url + word + '.html',
                headers=self.headers,
                timeout=10
            )
            body = request.text
            return body
        except requests.exceptions.Timeout:
            raise RuntimeError("timeout")


class SentenceYourdictionaryCom(Request):

    def __init__(self):
        super(SentenceYourdictionaryCom, self).__init__(
            url='http://sentence.yourdictionary.com/'
        )


    def parse(self, body):
        try:
            sentences = HTMLSearch(
                body,
                'ul',
                'id',
                'examples-ul-content'
            ).value
            mode = 1
        except:
            sentences = HTMLSearch(
                body,
                'ul',
                'class',
                'sentence-list'
            ).value
            mode = 2
        result = []
        for sentence in sentences.getchildren():
            if mode == 1:
                sentence = HTMLSearch(
                    sentence,
                    'div',
                    'class',
                    'li_content'
                ).value
                sentence = sentence.text_content()
            else:
                sentence = HTMLSearch(
                    sentence,
                    'p',
                    None,
                    None
                ).value
                sentence = sentence.text_content()
            if sentence != None:
                result.append(sentence)
        return result


    def fetch(self, word):
        try:
            request = requests.get(
                self.url + word,
                headers=self.headers,
                timeout=10
            )
            body = request.text
            return body
        except requests.exceptions.Timeout:
            raise RuntimeError("timeout")


class TangorinCom(Request):
    
    def __init__(self):
        super(TangorinCom, self).__init__(
            url='http://tangorin.com/sentences'
        )


    def parse(self, body):
        sentences = HTMLSearch(
            body,
            'dl',
            'class',
            ('results-dl',)
        ).value
        result = []
        for sentence in sentences.getchildren():
            sentence = HTMLSearch(sentence, 'dd', 'class', 's-en').value
            sentence = sentence.text_content()
            if sentence != None:
                result.append(sentence)
        return result


    def fetch(self, word):
        try:
            request = requests.get(
                self.url + '?search=' + word,
                headers=self.headers,
                timeout=10
            )
            body = request.text
            return body
        except requests.exceptions.Timeout:
            raise RuntimeError("timeout")

interfaces = [TangorinCom, SentencedictCom, SentenceYourdictionaryCom]

class UI:

    def __init__(self, interfaces, word):
        self.interfaces = interfaces
        self.word = word.lower()


    def main(self):
        exceptions = []
        for interface in self.interfaces:
            try:
                interface_object = interface()
                print('\n' + C.green, end='')
                for char in interface_object.url:
                    print(char, end='', flush=True)
                    sleep(0.01)
                print(C.none + ' ', end = '')
                sentences = interface_object.sentences(self.word)
                print(
                    C.gray + 
                    '[found {} sentence(s)]'.format(len(sentences)) +
                    C.none
                )
            except Exception as error:
                print()
                exceptions.append(error)
                if len(exceptions) == len(self.interfaces):
                    raise
                else:
                    if str(error)[0] == '#':
                        print(C.red + str(error)[1:] + C.none)
                        continue
                    else:
                        raise
            normal_color = True
            number = 1
            for sentence in sentences:
                words = sentence.     \
                    replace('\n', '').\
                    replace('\r', '').\
                    split(' ')
                number_str = str(number)
                if number < 10:
                    number_str = '0' + number_str
                print(
                    '\n    '   + 
                    C.green    + 
                    number_str + 
                    '. '       + 
                    C.none     + 
                    C.white,
                    end=''
                )
                chars = len(number_str) + 2
                for word in words:
                    word = word.replace('"', '').replace('\'', '')
                    if word.lower() == self.word:
                        print(C.none + C.yellow, end='')
                        normal_color = False
                    elif word.lower().endswith(self.word):
                        print(C.none + C.yellow, end='')
                        normal_color = False
                    elif word.lower().startswith(self.word):
                        print(C.none + C.yellow, end='')
                        normal_color = False
                    elif word.lower().find(self.word) != -1:
                        print(C.none + C.yellow, end='')
                        normal_color = False
                    elif len(word) > 1 and not word[-1].isalpha():
                        if word[:-1].lower() == self.word:
                            print(C.none + C.yellow, end='')
                            normal_color = False
                        elif not normal_color:
                            print(C.none + C.white, end='')
                            normal_color = True
                    elif not normal_color:
                        print(C.none + C.white, end='')
                        normal_color = True
                    if chars + len(word) + 1 > 80:
                        print('\n    ', end='')
                        chars = len(word) + 1
                    else:
                        chars += len(word) + 1
                    print(word + ' ', end='')
                print()
                number += 1



if __name__ == '__main__':
    from sys import argv
    
    def main():
        if '-h' in argv or '--help' in argv:
            help_text = '''\
Usage: sentential [OPTION] WORD
Fetchs some sentence examples which include WORD in them.

OPTION:
  --no-color    Does not show colorized text.
  -h, --help    Shows this help text
'''
            print(help_text)
            return
        if len(argv) > 1:
            UI(interfaces, argv[-1]).main()
        else:
            raise RuntimeError(
                '#\'sentencial\' accepts one English word as last para'\
                'meter'
            )

    if '--no-color' in argv:
        C = Colors(
            red='',
            green='',
            white='',
            yellow='',
            gray='',
            none=''
        )
    status_code = 0
    try:
        main()
    except KeyboardInterrupt:
        print()
    except Exception as error:
        print(C.red, end='')
        if str(error)[0] == '#':
            print(str(error)[1:])
            status_code = 1
        else:
            raise
    exit(status_code)

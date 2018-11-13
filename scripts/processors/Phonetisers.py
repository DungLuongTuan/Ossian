#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Project: Ossian - May 2017  
## Contact: Oliver Watts - owatts@staffmail.ed.ac.uk

from processors.UtteranceProcessor import SUtteranceProcessor, Element
from naive import naive_util
import default.const as c
import unicodedata


# import os
# import sys
# import re
# import regex
# import unicodedata
# import shutil
# import glob 
# import fileinput
# import subprocess
# import codecs 

# import default.const as c

# from processors.NodeEnricher import NodeEnricher
# from processors.UtteranceProcessor import UtteranceProcessor

# from util.LookupTable import LookupTable

# from naive.naive_util import readlist, writelist


class NaivePhonetiser(SUtteranceProcessor):
    '''
    Add 'phonetic' segments consisting of standard orthography characters, converted into an ASCII-safe 'safetext' form
    '''
    def __init__(self, processor_name='naive_phonetiser', target_nodes="//token", \
                target_attribute='text', child_node_type='segment', output_attribute='pronunciation', \
                class_attribute='token_class', word_classes=['word'], probable_pause_classes=['punctuation', c.TERMINAL], \
                possible_pause_classes=['space']):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.target_attribute = target_attribute
        self.child_node_type = child_node_type
        self.output_attribute = output_attribute
        self.class_attribute = class_attribute
        self.word_classes = word_classes
        self.probable_pause_classes = probable_pause_classes
        self.possible_pause_classes = possible_pause_classes

        super(NaivePhonetiser, self).__init__()

    def process_utterance(self, utt):
        for node in utt.xpath(self.target_nodes):
            assert node.has_attribute(self.class_attribute)
            assert node.has_attribute(self.target_attribute)

            current_class = node.attrib[self.class_attribute]

            if current_class in self.word_classes:
                word = node.attrib[self.target_attribute]
                children = self.get_phonetic_segments(word)
            elif current_class in self.probable_pause_classes:
                children = [c.PROB_PAUSE]
            elif current_class in self.possible_pause_classes:
                children = [c.POSS_PAUSE]
            else:
                sys.exit('Class "%s" not in any of word_classes, probable_pause_classes, possible_pause_classes')
            for chunk in children:
                child = Element(self.child_node_type)
                child.set(self.output_attribute, chunk)
                node.add_child(child)

    def get_phonetic_segments(self, word):
        safetext_letters = []
        for letter in list(word.lower()):
            safetext_letters.append(naive_util.safetext(letter))
        return safetext_letters

    def do_training(self, speech_corpus, text_corpus):
        print "NaivePhonetiser requires no training"    


class DungltPhonetiser(SUtteranceProcessor):
    '''
    Add 'phonetic' segments consisting of standard orthography characters, converted into an ASCII-safe 'safetext' form
    '''
    def __init__(self, processor_name='naive_phonetiser', target_nodes="//token", \
                target_attribute='text', child_node_type='segment', output_attribute='pronunciation', \
                class_attribute='token_class', word_classes=['word'], probable_pause_classes=['punctuation', c.TERMINAL], \
                possible_pause_classes=['space']):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.target_attribute = target_attribute
        self.child_node_type = child_node_type
        self.output_attribute = output_attribute
        self.class_attribute = class_attribute
        self.word_classes = word_classes
        self.probable_pause_classes = probable_pause_classes
        self.possible_pause_classes = possible_pause_classes
        self.vi_consonants = ['b', 'd', 'h', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'x', '_LATINSMALLLETTERDWITHSTROKE_', 'f', 'q', 'c', 'k', 'z', 'w', 'j', 'tr', 'th', 'ch', 'ph', 'nh', 'kh', 'gi', 'qu', 'sh', 'gh', 'ng', 'ngh']
        self.vi_cons_phone = ['b', 'd', 'h', 'l', 'm', 'n', 'p', 'r', 'sh', 't', 'v', 's', '_LATINSMALLLETTERDWITHSTROKE_', 'f', 'k', 'k', 'k', 'z', 'w', 'z', 'tr', 'th', 'ch', 'f', 'nh', 'kh', 'z', 'kw', 'sh', 'g', 'ng', 'ng']
        super(DungltPhonetiser, self).__init__()

    def process_utterance(self, utt):
        for node in utt.xpath(self.target_nodes):
            assert node.has_attribute(self.class_attribute)
            assert node.has_attribute(self.target_attribute)

            current_class = node.attrib[self.class_attribute]

            if current_class in self.word_classes:
                word = node.attrib[self.target_attribute]
                children = self.get_phonetic_segments(word)
            elif current_class in self.probable_pause_classes:
                children = [c.PROB_PAUSE]
            elif current_class in self.possible_pause_classes:
                children = [c.POSS_PAUSE]
            else:
                sys.exit('Class "%s" not in any of word_classes, probable_pause_classes, possible_pause_classes')
            for chunk in children:
                child = Element(self.child_node_type)
                child.set(self.output_attribute, chunk)
                node.add_child(child)

    def get_phonetic_segments(self, word):
        # consonants = ['q', 'w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        # list_words = list(word.lower())
        # safetext_letters = [naive_util.safetext(list_words[0])]
        # for letter in list_words[1:]:
        #     if (letter in consonants) and (safetext_letters[-1] in consonants):
        #         safetext_letters[-1] += letter
        #         continue
        #     if (letter == 'u') and (safetext_letters[-1] == 'q'):
        #         safetext_letters[-1] += 'u'
        #         continue
        #     if (naive_util.safetext(letter) in ['i', '_LATINSMALLLETTERIWITHGRAVE_', '_LATINSMALLLETTERIWITHACUTE_', '_LATINSMALLLETTERIWITHHOOKABOVE_', '_LATINSMALLLETTERIWITHTILDE_', '_LATINSMALLLETTERIWITHDOTBELOW_']) and (safetext_letters[-1] == 'g'):
        #         safetext_letters[-1] += 'i'
        #     safetext_letters.append(naive_util.safetext(letter))

        # letters = list(word.lower())
        # safetext_letters = [letters[0]]
        # for letter in letters[1:]:
        #     if (safetext_letters[-1] + letter in self.vi_consonants):
        #         safetext_letters[-1] += letter
        #         continue
        #     if (safetext_letters[-1] == 'g') and (naive_util.safetext(letter) in ['i', '_LATINSMALLLETTERIWITHGRAVE_', '_LATINSMALLLETTERIWITHACUTE_', '_LATINSMALLLETTERIWITHHOOKABOVE_', '_LATINSMALLLETTERIWITHTILDE_', '_LATINSMALLLETTERIWITHDOTBELOW_']):
        #         safetext_letters[-1] += 'i'
        #     safetext_letters.append(letter)

        # for i in range(len(safetext_letters)):
        #     if (safetext_letters[i] in self.vi_consonants):
        #         safetext_letters[i] = self.vi_cons_phone[self.vi_consonants.index(safetext_letters[i])]

        # for i in range(len(safetext_letters)):
        #     safetext_letters[i] = naive_util.safetext(safetext_letters[i])

        letters = [naive_util.safetext(l) for l in list(word.lower())]
        safetext_letters = [letters[0]]
        for letter in letters[1:]:
            if (safetext_letters[-1] + letter in self.vi_consonants):
                safetext_letters[-1] += letter
                continue
            if (safetext_letters[-1] == 'g') and (letter in ['i', '_LATINSMALLLETTERIWITHGRAVE_', '_LATINSMALLLETTERIWITHACUTE_', '_LATINSMALLLETTERIWITHHOOKABOVE_', '_LATINSMALLLETTERIWITHTILDE_', '_LATINSMALLLETTERIWITHDOTBELOW_']):
                safetext_letters[-1] += 'i'
            safetext_letters.append(letter)

        for i in range(len(safetext_letters)):
            if (safetext_letters[i] in self.vi_consonants):
                safetext_letters[i] = self.vi_cons_phone[self.vi_consonants.index(safetext_letters[i])]

        return safetext_letters

    def do_training(self, speech_corpus, text_corpus):
        print "DungltPhonetiser requires no training"

class StartEndPhonetiser(SUtteranceProcessor):
    '''
    Add 'phonetic' segments consisting of standard orthography characters, converted into an ASCII-safe 'safetext' form
    '''
    def __init__(self, processor_name='naive_phonetiser', target_nodes="//token", \
                target_attribute='text', child_node_type='segment', output_attribute='pronunciation', \
                class_attribute='token_class', word_classes=['word'], probable_pause_classes=['punctuation', c.TERMINAL], \
                possible_pause_classes=['space']):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.target_attribute = target_attribute
        self.child_node_type = child_node_type
        self.output_attribute = output_attribute
        self.class_attribute = class_attribute
        self.word_classes = word_classes
        self.probable_pause_classes = probable_pause_classes
        self.possible_pause_classes = possible_pause_classes
        self.vi_consonants = ['b', 'd', 'h', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'x', 'đ', 'f', 'q', 'c', 'k', 'z', 'w', 'tr', 'th', 'ch', 'ph', 'nh', 'kh', 'gi', 'qu', 'sh', 'gh', 'ng', 'ngh']
        self.vi_cons_phone = ['b', 'd', 'h', 'l', 'm', 'n', 'p', 'r', 'sh', 't', 'v', 's', 'đ', 'f', 'k', 'k', 'k', 'z', 'w', 'tr', 'th', 'ch', 'f', 'nh', 'kh', 'z', 'kw', 'sh', 'g', 'ng', 'ng']
        self.name_reps = {" ": "",
                 "-": "",
                 "0": "ZERO",
                 "1": "ONE",
                 "2": "TWO",
                 "3": "THREE",
                 "4": "FOUR",
                 "5": "FIVE",
                 "6": "SIX",
                 "7": "SEVEN",
                 "8": "EIGHT",
                 "9": "NINE"}
        super(StartEndPhonetiser, self).__init__()

    def process_utterance(self, utt):
        for node in utt.xpath(self.target_nodes):
            assert node.has_attribute(self.class_attribute)
            assert node.has_attribute(self.target_attribute)

            current_class = node.attrib[self.class_attribute]

            if current_class in self.word_classes:
                word = node.attrib[self.target_attribute]
                children = self.get_phonetic_segments(word)
            elif current_class in self.probable_pause_classes:
                children = [c.PROB_PAUSE]
            elif current_class in self.possible_pause_classes:
                children = [c.POSS_PAUSE]
            else:
                sys.exit('Class "%s" not in any of word_classes, probable_pause_classes, possible_pause_classes')
            for chunk in children:
                child = Element(self.child_node_type)
                child.set(self.output_attribute, chunk)
                node.add_child(child)

    def get_safetext(self, char):
        # try:
        #     safetext_char = unicodedata.name(char)
        # except:
        #     safetext_char = "PROBLEMCHARACTER"
        # return safetext_char
        return unicodedata.name(unicode(char))


    def get_phonetic_segments(self, word):
        word = word.lower()
        safetext_word = []
        unsafetext_word = []
        chars = '@'
        for i, char in enumerate(word + "@"):
            if (chars + char in self.vi_consonants):
                chars += char
            else:
                if (chars == 'g') and (naive_util.safetext(char) in ['i', '_LATINSMALLLETTERIWITHGRAVE_', '_LATINSMALLLETTERIWITHACUTE_', '_LATINSMALLLETTERIWITHHOOKABOVE_', '_LATINSMALLLETTERIWITHTILDE_', '_LATINSMALLLETTERIWITHDOTBELOW_']):
                    chars += 'i'
                safetext_char = ''
                if (chars in self.vi_consonants):
                    for c in self.vi_cons_phone[self.vi_consonants.index(chars)]:
                        safetext_char += self.get_safetext(c)
                elif chars in self.name_reps.keys():
                    safetext_char += self.name_reps[chars]
                else:
                    safetext_char += self.get_safetext(chars)
                safetext_word.append(safetext_char)
                unsafetext_word.append(chars)
                chars = char
        if (unsafetext_word[-1] in self.vi_consonants):
            safetext_word[-1] = "END" + safetext_word[-1]
        for i in range(len(safetext_word)):
            safetext_word[i] = "_" + safetext_word[i].replace(" ", "") + "_"
        return safetext_word[1:]

    def do_training(self, speech_corpus, text_corpus):
        print "StartEndPhonetiser requires no training"

class ConcateVowelPhonetiser(SUtteranceProcessor):
    '''
    Add 'phonetic' segments consisting of standard orthography characters, converted into an ASCII-safe 'safetext' form
    '''
    def __init__(self, processor_name='naive_phonetiser', target_nodes="//token", \
                target_attribute='text', child_node_type='segment', output_attribute='pronunciation', \
                class_attribute='token_class', word_classes=['word'], probable_pause_classes=['punctuation', c.TERMINAL], \
                possible_pause_classes=['space']):

        self.processor_name = processor_name
        self.target_nodes = target_nodes
        self.target_attribute = target_attribute
        self.child_node_type = child_node_type
        self.output_attribute = output_attribute
        self.class_attribute = class_attribute
        self.word_classes = word_classes
        self.probable_pause_classes = probable_pause_classes
        self.possible_pause_classes = possible_pause_classes
        self.vi_consonants = [u'b', u'd', u'h', u'l', u'm', u'n', u'p', u'r', u's', u't', u'v', u'x', u'đ', u'f', u'q', u'c', u'k', u'z', u'w', u'tr', u'th', u'ch', u'ph', u'nh', u'kh', u'gi', u'qu', u'sh', u'gh', u'ng', u'ngh', u'g']
        self.vi_cons_phone = [u'b', u'd', u'h', u'l', u'm', u'n', u'p', u'r', u'sh', u't', u'v', u's', u'đ', u'f', u'k', u'k', u'k', u'z', u'w', u'tr', u'th', u'ch', u'f', u'nh', u'kh', u'z', u'kw', u'sh', u'g', u'ng', u'ng', u'g']
        self.vi_tones = [ u'a', u'á', u'à', u'ả', u'ã', u'ạ', u'ă', u'ắ', u'ằ', u'ẳ', u'ẵ', u'ặ', u'â', u'ấ', u'ầ',\
                        u'ẩ', u'ẫ', u'ậ', u'e', u'é', u'è', u'ẻ', u'ẽ', u'ẹ', u'ê', u'ế', u'ề', u'ể', u'ễ', u'ệ', \
                        u'i', u'í', u'ì', u'ỉ', u'ĩ', u'ị', u'o', u'ó', u'ò', u'ỏ', u'õ', u'ọ', u'ô', u'ố', u'ồ', \
                        u'ổ', u'ỗ', u'ộ', u'ơ', u'ớ', u'ờ', u'ở', u'ỡ', u'ợ', u'u', u'ú', u'ù', u'ủ', u'ũ', u'ụ', \
                        u'ư', u'ứ', u'ừ', u'ử', u'ữ', u'ự', u'y', u'ý', u'ỳ', u'ỷ', u'ỹ', u'ỵ', u'yê', u'yế', u'yề', \
                        u'yể', u'yễ', u'yệ', u'iê', u'iế', u'iề', u'iể', u'iễ', u'iệ', u'oa', u'oá', u'oà', u'oả', \
                        u'oã', u'oạ', u'oă', u'oắ', u'oằ', u'oẳ', u'oẵ', u'oặ', u'oe', u'oé', u'oè', u'oẻ', u'oẽ',\
                        u'oẹ', u'oo', u'oó', u'oò', u'oỏ', u'oõ', u'oọ', u'uâ', u'uấ', u'uầ', u'uẩ', u'uẫ', u'uậ', \
                        u'uê', u'uế', u'uề', u'uể', u'uễ', u'uệ', u'uô', u'uố', u'uồ', u'uổ', u'uỗ', u'uộ', u'uơ', \
                        u'uớ', u'uờ', u'uở', u'uỡ', u'uợ', u'uy', u'uý', u'uỳ', u'uỷ', u'uỹ', u'uỵ', u'ươ', u'ướ', \
                        u'ườ', u'ưở', u'ưỡ', u'ượ', u'uyê', u'uyế', u'uyề', u'uyể', u'uyễ', u'uyệ'
        ]
        self.name_reps = {" ": "",
                 "-": "",
                 "0": "ZERO",
                 "1": "ONE",
                 "2": "TWO",
                 "3": "THREE",
                 "4": "FOUR",
                 "5": "FIVE",
                 "6": "SIX",
                 "7": "SEVEN",
                 "8": "EIGHT",
                 "9": "NINE"}
        super(ConcateVowelPhonetiser, self).__init__()

    def process_utterance(self, utt):
        for node in utt.xpath(self.target_nodes):
            assert node.has_attribute(self.class_attribute)
            assert node.has_attribute(self.target_attribute)

            current_class = node.attrib[self.class_attribute]

            if current_class in self.word_classes:
                word = node.attrib[self.target_attribute]
                children = self.get_phonetic_segments(word)
            elif current_class in self.probable_pause_classes:
                children = [c.PROB_PAUSE]
            elif current_class in self.possible_pause_classes:
                children = [c.POSS_PAUSE]
            else:
                sys.exit('Class "%s" not in any of word_classes, probable_pause_classes, possible_pause_classes')
            for chunk in children:
                child = Element(self.child_node_type)
                child.set(self.output_attribute, chunk)
                node.add_child(child)

    def get_safetext(self, char):
        # try:
        #     safetext_char = unicodedata.name(char)
        # except:
        #     safetext_char = "PROBLEMCHARACTER"
        # return safetext_char
        return unicodedata.name(unicode(char))

    def has_in(self, c, l):
        for i in range(len(l)):
            if unicode(c) == l[i]:
                return True
        return False

    def get_phonetic_segments(self, word):
        word = word.lower()
        safetext_word = []
        chars = '@'
        for i, char in enumerate(word + "@"):
            safetext_char = ''
            if self.has_in(char, self.vi_consonants):
                if self.has_in(chars + char, self.vi_consonants):
                    chars += char
                    continue
            elif self.has_in(char, self.vi_tones):
                if self.has_in(chars + char, self.vi_tones):
                    chars += char
                    continue
            elif i != len(word):
                continue
            if (chars == 'g') and (naive_util.safetext(char) in ['i', '_LATINSMALLLETTERIWITHGRAVE_', '_LATINSMALLLETTERIWITHACUTE_', '_LATINSMALLLETTERIWITHHOOKABOVE_', '_LATINSMALLLETTERIWITHTILDE_', '_LATINSMALLLETTERIWITHDOTBELOW_']):
                chars += 'i'
            if self.has_in(chars, self.vi_consonants):
                for c in self.vi_cons_phone[self.vi_consonants.index(chars)]:
                    safetext_char += self.get_safetext(c)
            else:
                for c in chars:
                    safetext_char += self.get_safetext(c)
            safetext_word.append(safetext_char)
            chars = char
        for i in range(len(safetext_word)):
            safetext_word[i] = "_" + safetext_word[i].replace(" ", "") + "_"
        return safetext_word[1:]

    def do_training(self, speech_corpus, text_corpus):
        print "ConcateVowelPhonetiser requires no training"

"""
This file is the main file for the Sciens project; when initialized, it creates the dictionaries and
performs the grammar-parsing process based on written-out rules and the sentence given to it to be parsed.
It only contains the Sciens class.

As it stands, this class reads in three dictionaries in order to have a bank of Latin terms to draw from,
takes in a Latin sentence as a parameter to parse,
figures out all of the possible forms for each word actually present in its dictionaries,
removes some impossibilities based on grammatical cues from the given words of the sentence,
and chunks prepositional phrases.
It is not the intended product, but the intended product was of a higher difficulty than imagined.

Author: Stephen Bothwell
Version: 0.1.1
Last Updated: 9/12/2019
"""

from itertools import chain
from typing import TextIO

from Components.Affix import NominalAffix, VerbalAffix
from Components.Paradigm import Paradigm, NominalParadigm, VerbalParadigm
from Components.Word import *

import nltk
nltk.download('punkt')


class Sciens:
    """
    This method initializes the Sciens class objects.
    It requires three filepaths and the string which is to be parsed.
    It initializes various fields used as constants that are used throughout the program.
    Currently, it initializes the three dictionaries and
    performs a grammatical parse of the sentence given before printing the result and terminating its process.
    """
    def __init__(self, latin_string: str,
                 frozen_dict_file: str = '../Project Text Files/Frozen_Word_Dictionary.txt',
                 irregular_dict_file: str = '../Project Text Files/Irregular_Word_Dictionary.txt',
                 root_dict_file: str = '../Project Text Files/Root_Dictionary.txt') -> None:
        # Below are hard-coded the paradigms for each Declension and Conjugation that are covered thus far.
        self.first_declension = {'a': [NominalAffix(1, 1), NominalAffix(5, 1), NominalAffix(6, 1)],
                           'ae': [NominalAffix(2, 1), NominalAffix(3, 1), NominalAffix(1, 2), NominalAffix(6, 2)],
                           'am': [NominalAffix(4, 1)],
                           'arum': [NominalAffix(2, 2)],
                           'is': [NominalAffix(3, 2), NominalAffix(5, 2)],
                           'as': [NominalAffix(4, 2)]}

        self.second_declension_v1 = {'us': [NominalAffix(1, 1)],
                                'i': [NominalAffix(2, 1), NominalAffix(1, 2), NominalAffix(6, 2)],
                                'o': [NominalAffix(3, 1), NominalAffix(5, 1)],
                                'um': [NominalAffix(4, 1)],
                                'e': [NominalAffix(6, 1)],
                                'orum': [NominalAffix(2, 2)],
                                'is': [NominalAffix(3, 2), NominalAffix(5, 2)],
                                'os': [NominalAffix(4, 2)]}

        """ 
        TODO: How do I handle words like "vir" which do not have that extra "e"?
        I see two options: first, I use a system that simply maps two roots to the same items
        or I make two paradigms, one for each. I am thinking that the first option might be better--
        after all, I am not iterating over the paradigms anymore.
        This will be an issue that I handle later, however.
        """

        self.second_declension_v2 = {'r': [NominalAffix(1, 1), NominalAffix(6, 1)],
                                'ri': [NominalAffix(2, 1), NominalAffix(1, 2)],
                                'ro': [NominalAffix(3, 1), NominalAffix(5, 1)],
                                'rum': [NominalAffix(4, 1)],
                                'rorum': [NominalAffix(2, 2)],
                                'ris': [NominalAffix(3, 2), NominalAffix(5, 2)],
                                'ros': [NominalAffix(4, 2)]}

        self.second_declension_v3 = {'um': [NominalAffix(1, 1), NominalAffix(4, 1), NominalAffix(6, 1)],
                                'i': [NominalAffix(2, 1)],
                                'o': [NominalAffix(3, 1), NominalAffix(5, 1)],
                                'a': [NominalAffix(1, 2), NominalAffix(4, 2), NominalAffix(6, 2)],
                                'orum': [NominalAffix(2, 2)],
                                'is': [NominalAffix(3, 2), NominalAffix(5, 2)]}

        """
        TODO:
        I want to see if I can find a way to homogenize the first and second conjugation verbs
        such that I do not have to store separate endings for each. They are really the same.
        There are some differences with the third and fourth conjugations (not given here yet),
        but even they might benefit from homogenization. A future update might have me storing conjugation
        with verbs such that I can cut off more of the stem and know simply that the verb requires
        adding that extra letter back.
        Furthermore, I would like to see if I cannot change the architecture
        such that I do not have to put the verb endings in lists or such that 
        I can take more advantage of this use. Verb endings tend not to share endings like nouns.
        """

        self.first_conjugation_present_tense_endings = {'o': [VerbalAffix(1, 1)],
                                        'as': [VerbalAffix(2, 1)],
                                        'at': [VerbalAffix(3, 1)],
                                        'amus': [VerbalAffix(1, 2)],
                                        'atis': [VerbalAffix(2, 2)],
                                        'ant': [VerbalAffix(3, 2)]}

        self.first_conjugation_imperfect_tense_endings = {'abam': [VerbalAffix(1, 1)],
                                          'abas': [VerbalAffix(2, 1)],
                                          'abat': [VerbalAffix(3, 1)],
                                          'abamus': [VerbalAffix(1, 2)],
                                          'abatis': [VerbalAffix(2, 2)],
                                          'abant': [VerbalAffix(3, 2)]}

        self.first_conjugation_future_tense_endings = {'abo': [VerbalAffix(1, 1)],
                                       'abis': [VerbalAffix(2, 1)],
                                       'abit': [VerbalAffix(3, 1)],
                                       'abimus': [VerbalAffix(1, 2)],
                                       'abitis': [VerbalAffix(2, 2)],
                                       'abunt': [VerbalAffix(3, 2)]}

        self.second_conjugation_present_tense_endings = {'eo': [VerbalAffix(1, 1)],
                                         'es': [VerbalAffix(2, 1)],
                                         'et': [VerbalAffix(3, 1)],
                                         'emus': [VerbalAffix(1, 2)],
                                         'etis': [VerbalAffix(2, 2)],
                                         'ent': [VerbalAffix(2, 3)]}

        self.second_conjugation_imperfect_tense_endings = {'ebam': [VerbalAffix(1, 1)],
                                           'ebas': [VerbalAffix(2, 1)],
                                           'ebat': [VerbalAffix(3, 1)],
                                           'ebamus': [VerbalAffix(1, 2)],
                                           'ebatis': [VerbalAffix(2, 2)],
                                           'ebant': [VerbalAffix(3, 2)]}

        self.second_conjugation_future_tense_endings = {'ebo': [VerbalAffix(1, 1)],
                                               'ebis': [VerbalAffix(2, 1)],
                                               'ebit': [VerbalAffix(3, 1)],
                                               'ebimus': [VerbalAffix(1, 2)],
                                               'ebitis': [VerbalAffix(2, 2)],
                                               'ebunt': [VerbalAffix(3, 2)]}

        self.perfect_tense_endings = {'i': [VerbalAffix(1, 1)],
                               'isti': [VerbalAffix(2, 1)],
                               'it': [VerbalAffix(3, 1)],
                               "imus": [VerbalAffix(1, 2)],
                               "istis": [VerbalAffix(2, 2)],
                               "erunt": [VerbalAffix(3, 2)]}

        self.pluperfect_tense_endings = {'eram': [VerbalAffix(1, 1)],
                                  'eras': [VerbalAffix(2, 1)],
                                  'erat': [VerbalAffix(3, 1)],
                                  'eramus': [VerbalAffix(1, 2)],
                                  'eratis': [VerbalAffix(2, 2)],
                                  'erant': [VerbalAffix(3, 2)]}

        self.future_perfect_tense_endings = {'ero': [VerbalAffix(1, 1)],
                                     'eris': [VerbalAffix(2, 1)],
                                     'erit': [VerbalAffix(3, 1)],
                                     'erimus': [VerbalAffix(1, 2)],
                                     'eritis': [VerbalAffix(2, 2)],
                                     'erint': [VerbalAffix(3, 2)]}

        # This field holds the sentence which the program started with. I may change this such
        # that it is a program that runs in a loop and can have sentences inputted into it and
        # responded to in a way that does not rely on initialization to do as asked.
        self.latin_sentence: str = latin_string

        """
        TODO: Handle punctuation in a more efficient and organized manner.
        """
        self.punctuation: tuple = (".", ",", "!", "?", ";", ":", "--", "(", ")", "[", "]", "<", ">", "{", "}",
                                   "'", '"', '...')

        # The following are the three dictionaries which the program reads in from the files,
        # creates, and sorts. They are highly important to the program and represent the first
        # stage of the Part-of-Speech Tagger architecture.
        self.frozen_dictionary: dict = self.process_frozen(open(frozen_dict_file, 'r'))
        # For testing purposes, one can access items in the frozen dictionary as follows:
        # self.frozen_dictionary["word"]
        # Example: self.frozen_dictionary["propter"]

        self.irregular_dictionary: dict = self.process_irregular(open(irregular_dict_file, 'r'))
        # For testing purposes, one can access items in the irregular dictionary as follows:
        # self.irregular_dictionary["word"][variant_num]
        # Example: print(self.irregular_dictionary["vos"][0])

        self.root_dictionary: dict = self.process_root(open(root_dict_file, 'r'))
        # For testing purposes, one can print access in the root dictionary as follows:
        # self.root_dictionary["root"][part_of_speech_num][paradigm_num]
        # Example: self.root_dictionary["bell"][0][0]

        # The following starts the program and performs the rest of the operations of the program; it
        # discerns the grammar of the sentence and prints viable constructions.
        self.run_sciens(latin_string)

    def process_frozen(self, frozen_dict_file: TextIO) -> dict:
        """
        This method forms the frozen_dictionary field by creating a frozen_dict item and
        returning it to be assigned to that object.
        It uses the generate_frozen_word method to handle the value for each key,
        which is the actual word stored.
        These items hold Word objects because they do not have multiple forms
        nor unique forms that can be easily paradigmatized.
        :param frozen_dict_file: the file which contains frozen word forms of the appropriate format.
        :return: a dictionary of Word entries from the frozen_dict_file.
        """
        # This variable holds the dictionary which is formed and returned through this method.
        frozen_dict: dict = {}
        for line in frozen_dict_file:
            if not line.startswith('#'):
                # This variable holds the part of the string which denotes the actual word being defined.
                actual_word: str = line[0:line.index(':')]
                frozen_dict[actual_word] = self.generate_frozen_word(line, actual_word)
        frozen_dict_file.close()
        return frozen_dict

    @staticmethod
    def generate_frozen_word(line: str, actual_word: str) -> Word:
        """
        This method generates the Word objects which are assigned to terms stored in the Frozen Dictionary.
        It works for any grammatical construction present in the list for the first 'if' statement.
        Support for other constructions will be added as needed (as others are generally rarer).
        :param line: a string containing a line from the Frozen Word file.
        :param actual_word: a string containing the root of the given word.
        :return: a composed Word with information from the file of the line.
        """
        # This variable holds the Word object which process_frozen() will assign to a given dictionary entry.
        new_word: Word = None
        if line[(line.index(':') + 1):line.index(';')].strip() in ['Adverb', 'Conjunction', 'Noun', 'Particle', 'Preposition']:
            # This variable holds the constructions that the given word can take.
            construction_list = line[line.index(';') + 1:line.index(';', line.index(';') + 1, len(line))].split(',')
            for i, item in enumerate(construction_list):
                construction_list[i] = item.strip()

            # These conditions create a new_word specific to its part-of-speech as denoted in its dictionary entry.
            if 'Adverb' in line:
                new_word = Word(actual_word, PartOfSpeech(4), construction_list, line[(line.rindex(';') + 2):len(line)])
            elif 'Conjunction' in line:
                new_word = Word(actual_word, PartOfSpeech(7), construction_list, line[(line.rindex(';') + 2):len(line)])
            elif 'Particle' in line:
                new_word = Word(actual_word, PartOfSpeech(8), construction_list, line[(line.rindex(';') + 2):len(line)])
            elif 'Preposition' in line:
                new_word = Word(actual_word, PartOfSpeech(6), construction_list, line[(line.rindex(';') + 2):len(line)])
            else:
                new_word = NominalWord(actual_word, PartOfSpeech(1), Case(8), Gender(3), Number(3), construction_list,
                                       line[(line.rindex(';') + 2):len(line)])
        else:
            # The following statements get rid of items no longer being used and throw the proper errors.
            del new_word
            raise ValueError("The word " + actual_word + " has an invalid dictionary formatting.")
        return new_word

    def process_irregular(self, irregular_dict_file: TextIO) -> list:
        """
        This method fills the irregular_dictionary field by processing the file given for the irregular dictionary.
        It does so differently than the process_frozen method in that there are multiple forms for each word,
        but they are irregular, so they are stored separately.
        However, to let them have the same syntactic information,
        they are written and handled in a manner that allows for such a thing to be done.
        This method works in tandem with the fill_irregular_dictionary method in order to work.
        :param irregular_dict_file: the file which contains irregular word forms of the appropriate format.
        :return: a list of irregular dictionary entries (Paradigms).
        """

        # The following variable holds the dictionary of all of the entries which are to go into the
        # irregular_dictionary field.
        irregular_dict: dict = {}
        # The following variable holds the list of words for a given entry that share syntactic and
        # semantic properties.
        actual_words: list = []
        for line in irregular_dict_file:
            # This set of statements fills a list with the words related to a given term before
            # processing them.
            if not line.startswith('#'):
                if ':' in line:
                    actual_words.append(line[0:line.index(':')])
                    self.fill_irregular_dictionary(irregular_dict, line, actual_words)
                    actual_words.clear()
                else:
                    actual_words.append(line)
        irregular_dict_file.close()
        return irregular_dict


    def fill_irregular_dictionary(self, irregular_dict: dict, line: str, actual_words: list) -> dict:
        """
        This method takes a given dictionary entry, which is a list of words
        and assigns each individual word on that list the properties special to it and
        those given to the word as a whole. Currently, it only hands pronouns and verbs,
        but these are the most immediate exceptions to the general rules of Latin's morphology.
        :param irregular_dict: an empty dictionary to hold the forms for an irregular Latin word.
        :param line: a line (str) in the irregular_dict_file.
        :param actual_words: a list of the word forms for the irregular Latin word.
        :return: a dictionary containing the appropriately-defined forms for the irregular Latin word.
        """

        # This dictionary is to be appended to the dictionary as a whole. It will contain
        # the entries for a given grouping of words and their corresponding Word objects.
        new_dict: dict = {}

        # In this condition, only Verbs or Pronouns are recognized and utilized in the dictionary.
        # Both of these have items calculated below which result in numbers that may stay the same
        # or vary depending on which word is being analyzed (i.e., the first for Pronoun is Gender for
        # the gndr variable, which changes value depending on the gender listed in the entry).
        if line[(line.index(':') + 1):line.index('<')].strip() in ['Verb', 'Pronoun']:
            # This list holds the constructions that apply for the given word.
            construction_list = line[line.index(';') + 1:line.index(';', line.index(';') + 1, len(line))].split(',')
            for i, item in enumerate(construction_list):
                construction_list[i] = item.strip()

            if 'Pronoun' in line:
                for num_ln, ln in enumerate(actual_words, start=1):
                    word_list: list = ln.split(' / ')

                    # to handle Gender ...
                    gndr = Gender(5)
                    gender_list = line[(line.rindex('<') + 1):line.rindex('>')].split(',')
                    for item in gender_list:
                        gndr = Gender(self.get_gender(item))

                    for num_wd, wd in enumerate(word_list, start=1):
                        wd = wd.replace('\n', '')

                        # to handle Case ...
                        # (Note: this solution does not handle the Locative Case yet.)
                        cs: int = 0
                        if (num_wd % 6) == 0:
                            cs = 6
                        else:
                            cs = num_wd % 6

                        # to handle Number ...
                        nmbr: int = 0
                        if((num_wd <= 12) and (num_wd % 13)):
                            if num_wd <= 6:
                                nmbr = 1
                            else:
                                nmbr = 2
                        else:
                            if((num_wd % 12 != 0) and (num_wd % 12) <= 6):
                                nmbr = 1
                            else:
                                nmbr = 2

                        # Some words appear multiple times. As such, there are conditions
                        # to handle the word's repeated appearance.
                        if wd in irregular_dict.keys():
                            irregular_dict[wd].append(NominalWord(wd, PartOfSpeech(5), Case(cs), gndr,
                                                                  Number(nmbr), construction_list,
                                                                  line[(line.rindex(';') + 2):len(line)]))
                        else:
                            irregular_dict[wd] = [NominalWord(wd, PartOfSpeech(5), Case(cs), gndr,
                                                              Number(nmbr), construction_list,
                                                              line[(line.rindex(';') + 2):len(line)])]
            else:
                for num_ln, ln in enumerate(actual_words, start=1):
                    word_list: list = ln.split(' / ')

                    # to handle Mood ...
                    md: int = 0
                    if num_ln <= 12:
                        md = 1
                    else:
                        md = (num_ln // 12) + 1

                    # to handle Tense ...
                    tns: int = 0
                    if (num_ln % 7) == 0:
                        tns = num_ln % 6
                    else:
                        tns = num_ln % 7

                    # to handle Voice ...
                    vc: int = 0
                    if num_ln % 6 == 0:
                        vc = (((num_ln - 1) // 6) % 2) + 1
                    else:
                        vc = ((num_ln // 6) % 2) + 1

                    for num_wd, wd in enumerate(word_list, start=1):
                        wd = wd.replace('\n', '')

                        # to handle Person ...
                        prsn: int = 0
                        if (num_wd % 3) == 1:
                            prsn = 1
                        elif (num_wd % 3) == 2:
                            prsn = 2
                        elif (num_wd % 3) == 0:
                            prsn = 3
                        else:
                            raise ValueError("There cannot be less than one or more than six words in a line to denote persons.")

                        # to handle Number ...
                        nmbr: int = 0
                        if(num_wd <= 6):
                            if ((num_wd % 6) > 3 or (num_wd % 6) == 0):
                                nmbr = 2
                            else:
                                nmbr = 1
                        else:
                            ValueError("Too many words are in line " + str(num_ln) + ".")

                        # Like for Pronoun, these conditions handle cases when the a given word
                        # appears only once or multiple times among the irregular terms.
                        if wd in irregular_dict.keys():
                            irregular_dict[wd].append(VerbalWord(wd, PartOfSpeech(2), Mood(md), Number(nmbr),
                                                                 Person(prsn), Tense(tns), Voice(vc), construction_list,
                                                                 line[(line.rindex(';') + 2):len(line)]))
                        else:
                            irregular_dict[wd] = [VerbalWord(wd, PartOfSpeech(2), Mood(md), Number(nmbr),
                                                  Person(prsn), Tense(tns), Voice(vc), construction_list,
                                                  line[(line.rindex(';') + 2):len(line)])]
                        del prsn
                    del md
                    del tns
                    del vc
        else:
            raise ValueError("The dictionary entry containing " + line + " has an invalid dictionary formatting.")
        return new_dict

    def process_root(self, root_dict_file: TextIO) -> dict:
        """
        The following method reads in entries from the root dictionary file given and
        creates a dictionary to return to the self.root_dictionary field.
        :param root_dict_file: a file containing Latin words that conform to basic paradigms.
        :return: a dictionary containing all of the root words assigned to their proper paradigms.
        """

        # This variable holds the root dictionary that will be returned to self.root_dictionary and
        # used throughout the program.
        root_dict: dict = {}
        for line in root_dict_file:
            if not line.startswith('#'):
                # This variable holds the root of the word that will be used in the search of the root
                # dictionary.
                root: str = line[0:line.index(':')]
                # This variable holds the list of the parts of speech that the root can take.
                part_of_speech_list: list = line[(line.index(':') + 1):(line.index(';'))].split(',')
                for pos_num, pos in enumerate(part_of_speech_list):
                    part_of_speech_list[pos_num] = pos.strip()

                # This variable holds a string of paradigms that can be applied to a word.
                paradigm_string: str = line[(line.index(';') + 1):(line.rindex(';'))]
                # This variable will hold the paradigms that are a part of the paradigm_string variable.
                paradigm_list: list = []
                if '|' in paradigm_string:
                    paradigm_list = paradigm_string.split(' | ')
                    for num_str, string in enumerate(paradigm_list):
                        paradigm_list[num_str] = string.split(',')
                        for num_substr, substring in enumerate(paradigm_list[num_str]):
                            paradigm_list[num_str][num_substr] = substring.strip()
                else:
                    paradigm_list = [paradigm_string.split(', ')]
                    for num_substr, substring in enumerate(paradigm_list[0]):
                        paradigm_list[0][num_substr] = substring.strip()

                for num_pos, pos_str in enumerate(part_of_speech_list):
                    constr_list: list = line[(line.rindex(';') + 1):len(line)].split('|')
                    for num_constr, constr in enumerate(constr_list):
                        constr_list[num_constr] = constr.split(',')
                    # This segment handles nominal or adjectival parts-of-speech.
                    if pos_str == 'Noun' or pos_str == 'Adjective':
                        # This variable defines the number for the PartOfSpeech enumerator; it
                        # will be given as an argument later.
                        pos_num: int = 0
                        if pos_str == 'Noun':
                            pos_num: int = 1
                        else:
                            pos_num: int = 3
                        for num_pdigm, pdigm in enumerate(paradigm_list[num_pos]):
                            # The following two variables cut the paradigm into its actual paradigm and
                            # its potential genders.
                            ending_str: str = pdigm[0:pdigm.index('<')]
                            gender_str: str = pdigm[(pdigm.index('<') + 1):pdigm.index('>')]

                            # The following dictionary will reference the endings which
                            # a given declension has. This will be one of the predefined
                            # class fields.
                            endings: dict = {}
                            if ending_str == 'D1':
                                endings = self.first_declension
                            elif ending_str == 'D2.1':
                                endings = self.second_declension_v1
                            elif ending_str == 'D2.2':
                                endings = self.second_declension_v2
                            elif ending_str == 'D2.3':
                                endings = self.second_declension_v3
                            else:
                                del endings
                                raise ValueError("The item " + ending_str + " is not a valid set of endings.")

                            # The following item creates and assigns a given paradigm with the information
                            # gathered above.
                            paradigm_list[num_pos][num_pdigm] = NominalParadigm(pos_num, endings,
                                                                                 constr_list[num_pos],
                                                                                 (self.get_gender(gender_str)))

                    # The following item handles Verbal cases for a given dictionary entry's part of speech.
                    elif pos_str == 'Verb':
                        for num_pdigm, pdigm in enumerate(paradigm_list[num_pos]):
                            # The following variable selects out the actual paradigm.
                            ending_str: str = pdigm[0:pdigm.index('<')]
                            # gender_str: str = pdigm[(pdigm.index('<') + 1):pdigm.index('>')]
                            # The above item is available to be used, but currently has no use. Thus,
                            # it is commented out in case I find a better use for it later.
                            endings: dict = {}
                            if ending_str == 'C1PresActInd':
                                endings = self.first_conjugation_present_tense_endings
                            elif ending_str == 'C1ImpfActInd':
                                endings = self.first_conjugation_imperfect_tense_endings
                            elif ending_str == 'C1FutActInd':
                                endings = self.first_conjugation_future_tense_endings
                            elif ending_str == 'C2PresActInd':
                                endings = self.second_conjugation_present_tense_endings
                            elif ending_str == 'C2ImpfActInd':
                                endings = self.second_conjugation_imperfect_tense_endings
                            elif ending_str == 'C2FutActInd':
                                endings = self.second_conjugation_future_tense_endings
                            elif ending_str == 'C1PerfActInd':
                                endings = self.perfect_tense_endings
                            elif ending_str == 'C1PlupActInd':
                                endings = self.pluperfect_tense_endings
                            elif ending_str == 'C1FtPrfActInd':
                                endings = self.future_perfect_tense_endings
                            else:
                                del endings
                                raise ValueError("The item " + ending_str + " is not a valid set of endings.")

                            # The following item initializes the VerbalParadigm object related to the entry
                            # with the items gathered above for its fields.
                            paradigm_list[num_pos][num_pdigm] = VerbalParadigm(2, endings, constr_list[num_pos],
                                                                                self.get_mood(ending_str),
                                                                                self.get_tense(ending_str),
                                                                                self.get_voice(ending_str))
                    else:
                        raise ValueError('The line "' + line[0:(len(line) - 1)] + '" has an invalid formatting.')
                    root_dict[root] = paradigm_list
        root_dict_file.close()
        return root_dict

    @staticmethod
    def get_mood(ending_str: str) -> int:
        """
        This method takes the ending_str, which can concern verb paradigms, and retrieves the mood by
        looking at whether the name of the paradigm contains certain moods (i.e. Ind for Indicative, Subj for
        Subjunctive, Impr for Imperative).
        :param ending_str: a string containing an abbreviation that indicates a verbal paradigm.
        :return: an integer corresponding to the Mood enumeration.
        """

        # This variable holds an integer corresponding with the Mood enumeration's moods.
        mood_num: int = 0
        if 'Ind' in ending_str:
            mood_num = 1
        elif 'Subj' in ending_str:
            mood_num = 2
        elif 'Impr' in ending_str:
            mood_num = 3
        else:
            raise ValueError("The mood in " + ending_str + " is not a valid mood.")
        return mood_num

    @staticmethod
    def get_tense(ending_str: str) -> int:
        """
        This method takes the ending_str, which can contain verb paradigms, and retrieves the tense by
        looking at whether the name of the paradigm contains an abbreviation for a tense (i.e. Pres for Present).
        :param ending_str: a string containing an abbreviation for a verb tense.
        :return: an integer corresponding to the Tense enumeration.
        """

        # This variable holds an integer corresponding with the Tense enumeration's tenses.
        tense_num: int = 0
        if 'Pres' in ending_str:
            tense_num = 1
        elif 'Impf' in ending_str:
            tense_num = 2
        elif 'Fut' in ending_str:
            tense_num = 3
        elif 'Perf' in ending_str:
            tense_num = 4
        elif 'Plup' in ending_str:
            tense_num = 5
        elif 'FtPrf' in ending_str:
            tense_num = 6
        else:
            raise ValueError("The tense in " + ending_str + " is not a valid tense.")
        return tense_num

    @staticmethod
    def get_voice(ending_str: str) -> int:
        """
        This method takes the ending_str, which can contain verb paradigms, and retrieves the voice by
        looking at whether the name of the paradigm contains an abbreviation of the voice. There are
        only two voices--active (Act) and passive (Pass), so this is not a difficult endeavor.
        :param ending_str: a string containing an abbreviation for a verb voice.
        :return: an integer corresponding to the Voice enumeration.
        """

        # This variable holds an integer corresponding with the Voice enumeration's voices.
        voice_num: int = 0
        if 'Act' in ending_str:
            voice_num = 1
        elif 'Pass' in ending_str:
            voice_num = 2
        else:
            raise ValueError("The voice in " + ending_str + " is not a valid tense.")
        return voice_num

    @staticmethod
    def get_gender(gender_str: str) -> int:
        """
        The following method takes string that is a gender belonging to some paradigm and assigns them to
        # gender_num, a field which will hold a value passed later such that the Gender enumerator
        # can be properly initialized.
        :param gender_str: a string containing an indicator of a nominal or adjectival gender.
        :return: an integer corresponding with the Gender enumeration.
        """

        # This variable holds the number of the gender corresponding with the Gender enumeration.
        gender_num: int = 0
        if gender_str == 'Feminine':
            gender_num = 1
        elif gender_str == 'Masculine':
            gender_num = 2
        elif gender_str == 'Neuter':
            gender_num = 3
        elif gender_str == 'M/F':
            gender_num = 4
        else:
            del gender_num
            raise ValueError("The item " + gender_str + " does not depict a valid nominal gender.")
        return gender_num

    def run_sciens(self, latin_sentence: str) -> list:
        """
        This method performs the major action of the program. It is meant to take a sentence, tokenize it,
        denote all of the potential forms of each word, chunk it into potential sentences, and spit out those
        sentences in a readable format. Currently, it does up to part of the chunking process.
        :param latin_sentence: a Latin sentence (str).
        :return: a chunked list of potential Latin sentences.
        """

        # This method uses the NLTK tokenizer to cut the Latin sentence into individual words as a list.
        latin_list: list = nltk.word_tokenize(latin_sentence)
        # This list will hold all of the forms which eaech word in the given sentence can be based on
        # the information taken out from the dictionaries.
        overall_possibility_list: list = []
        for term in latin_list:
            if term not in self.punctuation:
                # This list will hold the possibilities for the morphology of each individual word.
                individual_possibility_list: list = []
                # This boolean denotes whether or not a given item has been found in one of the dictionaries
                # and, thusly, does not need to be put into another one for searching. (At least, for now.)
                is_item_found: bool = False

                # This block checks the frozen dictionary.
                try:
                    individual_possibility_list.append(self.frozen_dictionary[term.lower()])
                    if len(individual_possibility_list) > 0:
                        is_item_found = True
                except KeyError:
                    pass

                # This block checks the irregular dictionary.
                if is_item_found is False:
                    try:
                        individual_possibility_list.append(self.irregular_dictionary[term.lower()])
                        if len(individual_possibility_list) > 0:
                            is_item_found = True
                    except KeyError:
                        pass

                # This index holds the integer that not only keeps track of the loop but also plays a role
                # in truncating the given word.
                truncation_index: int = 0
                # This loop searches the root dictionary.
                while((is_item_found is False) and (truncation_index < 6)):
                    # The variables here are assigned via tuple unpacking; hence, truncate must return a tuple.
                    stem, affix = self.truncate(term.lower(), truncation_index + 1)
                    try:
                        individual_possibility_list.append(self.get_root_words(self.root_dictionary[stem], stem, affix))
                        if len(individual_possibility_list) > 0:
                            is_item_found = True
                    except KeyError:
                        pass
                    truncation_index += 1
                else:
                    if len(individual_possibility_list) == 0:
                        print("WARNING: The term " + term + " has not been found in the dictionaries.")

                overall_possibility_list.append(individual_possibility_list)
            else:
                # These characters generally denote a shift in the grammar and contain unrelated clauses.
                if term in ('.', ';', '!', '?'):
                    overall_possibility_list.append((term, Punctuation(1)))
                # These characters, although they denote some shift in the grammar, may relate the two
                # grammatical constructions which they separate.
                elif term in (',', ':', '--', '(', ')', '"', "'", '...'):
                    overall_possibility_list.append((term, Punctuation(2)))
                # These characters are treated separately, as editors tend to use them to denote corrupt text. However,
                # this text should be treated as part of the grammar unless denoted otherwise.
                elif term in ('{', '}', '<', '>', '[', ']'):
                    overall_possibility_list.append((term, Punctuation(3)))
                else:
                    raise ValueError("The punctuation '" + term + "' has not been integrated into the system.")
        # The following loop is meant to unnest lists as much as possible while keeping items appropriately
        # nested for the purposes of differentiation.
        for num_item, item in enumerate(overall_possibility_list):
            for num_sublist, sublist in enumerate(item):
                try:
                    overall_possibility_list[num_item][num_sublist] = list(chain.from_iterable(sublist))
                except TypeError:
                    pass
            try:
                overall_possibility_list[num_item] = list(chain.from_iterable(item))
            except TypeError:
                pass
        # The following items run the last few steps of the process--they perform preprocessing for chunking
        # with the remove_impossibilities method, chunk the program, and would then print the program with
        # a method if the tree was fully set up.
        print('-----')
        print('Overall Possibility List: ' + str(overall_possibility_list))
        new_list: list = self.remove_impossibilities(overall_possibility_list)
        print('Impossibilities-Removed List: ' + str(new_list))
        print('Chunked Prepositional Phrases: ' + str(self.chunk_terms(new_list)))
        print('-----')

    def truncate(self, root_word: str, num_times: int) -> tuple:
        """
        This method cuts off the ending of a word for the purposes of utilizing it for the root dictionary.
        It runs a certain number of times depending upon the num_times which it is given. It takes the root_word
        string and returns a tuple which naturally results from the rpartition built-in function; however, this
        tuple is edited such that only the 0-index and 1-index items are used, effectively making the tuple
        a tuple with two items (at least, two that matter to the rest of the program).
        :param root_word: a word (str) whose root is to be found via this function.
        :param num_times: the number of times by which the word should be truncated to find its base form.
        :return: a tuple containing the stem and affix of a given Latin word.
        """

        if num_times == 0:
            raise ValueError("The method truncate was called such that it would not truncate anything due to the " +
                             "value of num_times.")

        # This variable will hold the value which is to be returned--a tuple containing the stem and affix of
        # the word. Ultimately, any root_word passed in should result in a stem-affix combination that exists
        # in Latin if the word is defined in the Root Dictionary.
        stem_and_affix: tuple = ()
        # The following loop truncates a certain number of times based on the value of num_times supplied to it.
        for i in range(num_times):
            # The following conditions handle the first slice. This is kept separate because Latin tends
            # to have suffixes that are only one or two characters. This is not true for every single
            # ending, however; as such, that is why the 'else' condition is also defined.
            if len(stem_and_affix) == 0:
                # Because suffixes in Latin are not just a consonant (except in cases where the stem, as
                # the system currently stands, has a slight role in the ending, such as in the verbal present
                # system), we can slightly optimize truncation if the first truncation would result in taking
                # off a consonant. That is what the following conditions represent.
                if root_word[-1] in ['a', 'e', 'i', 'o', 'u']:
                    stem_and_affix = (root_word.rpartition(root_word[-1]))
                else:
                    stem_and_affix = (root_word.rpartition(root_word[(len(root_word) - 2):len(root_word)]))
            else:
                try:
                    # TODO: I want to see if this can't be made more efficient later.
                    # It works, but it likely could complete its task more speedily.

                    # The following variable holds the letter at which the string root_word is partitioned
                    # to find the stem-and-affix separation.
                    partition_letter: str = (stem_and_affix[0])[(len(stem_and_affix[0]) - 1):len(root_word)]

                    # These conditions handle the case in which the partitioning letter may appear more than
                    # once in the root_word; if so, then the string is shortened manually to avoid
                    # causing a regression (i.e. having more characters in the stem than before)
                    # in the partitioning process.
                    if partition_letter not in stem_and_affix[2]:
                        stem_and_affix = (root_word.rpartition(partition_letter))
                    else:
                        current_stem_length = len(stem_and_affix[0])
                        stem_and_affix = (root_word[0:(current_stem_length - 1)],
                                          root_word[(current_stem_length - 1):current_stem_length],
                                          root_word[current_stem_length:len(root_word)])
                except ValueError:
                    pass

        # This condition is present in the case that the rpartition has resulted in its traditional three-part format:
        # the part of the string before the separator, the separator itself, and the part of the string after the separator.
        # For the result, we want a two-tuple, not a three-tuple. As such, this condition results in a two-tuple if taken.
        if stem_and_affix[2] != '':
            stem_and_affix = (stem_and_affix[0], stem_and_affix[1] + stem_and_affix[2])
        return stem_and_affix[0:2]

    def get_root_words(self, stem_entry: list, stem: str, affix: str) -> list:
        """
        The following method, based on a valid stem and affix,
        returns all of the forms which could morphologically represent that combination.
        :param stem_entry: a list of the parts of speech related to a Latin word stem.
        :param stem: the stem of a Latin word (str).
        :param affix: the affix of a Latin word (str).
        :return: a list of Word entries that could represent a given Latin word morphologically.
        """

        # This item is a list of the morphological forms--Word objects--that a given stem and affix combination
        # could potentially represent. It is returned by this function.
        root_word_list: list = []
        for part_of_speech in stem_entry:
            for paradigm in part_of_speech:
                try:
                    root_word_list.append(self.convert_to_word(paradigm, stem, affix, paradigm.suffix_dict[affix]))
                except KeyError:
                    pass
            else:
                if len(root_word_list) == 0:
                    print("WARNING: The word " + stem + affix + " has not been found as a valid form for " + str(part_of_speech[0].part_of_speech) + ".")
        return root_word_list

    def convert_to_word(self, paradigm: Paradigm, stem: str, affix: str, affix_entry) -> list:
        """
        This method takes a paradigm, stem, affix, and the grammatical entry related to that affix and
        returns the Word objects that correspond with this information.
        :param paradigm: a Paradigm by which a word declines or is conjugated and
        gains grammatical meaning from.
        :param stem: a string of the stem of a Latin word.
        :param affix: an affix of the stem of a Latin word.
        :param affix_entry: an Affix (NominalAffix or VerbalAffix) containing relevant grammatical information.
        :return: a list of forms that match a Latin stem and affix pair.
        """
        # This list holds the Word objects that can be derived from the grammatical information retrieved
        # from the root_dictionary field.
        new_root_words: list = []
        for spec_affix in affix_entry:
            # Since two different Word types exist and are instantiated with some differing attributes,
            # the following conditions allow for their distinct creation without error.
            if isinstance(spec_affix, NominalAffix):
                new_root_words.append(NominalWord(stem + affix, paradigm.part_of_speech, Case(spec_affix.case),
                                                   paradigm.gender, Number(spec_affix.number), paradigm.constructions))
            else:
                new_root_words.append(VerbalWord(stem + affix, paradigm.part_of_speech, paradigm.mood,
                                                  Number(spec_affix.number), Person(spec_affix.person), paradigm.tense,
                                                  paradigm.voice, paradigm.constructions))
        return new_root_words

    def remove_impossibilities(self, possible_inputs: list) -> list:
        """
        The following method is a preprocessing step for chunking in that it computes,
        based upon certain standard practices in Latin, the instances of certain words which cannot be.
        In doing so, this method limits the number of terms which have to be checked over in the chunking step.
        It returns a (usually) trimmed version of the possible_inputs parameter;
        the information is mostly the same except that some options for various terms
        have been removed through some conditions.
        :param possible_inputs: a list of potential Word forms that could compose a sentence.
        :return: an equivalent or smaller list of potential Word forms that could compose a sentence.
        """

        # The following index holds the index that allows for access and iteration over the terms in possible_inputs.
        main_index: int = 0
        while main_index < len(possible_inputs):
            for num_subterm, subterm in enumerate(possible_inputs[main_index]):
                # This begins the set of conditions that will help to narrow down
                # possible grammatical constructions.

                # This condition handles vocatives; in particular, it handles series of words beginning with 'o',
                # like 'o beata amica!' and series of words that only have vocative forms
                # (i.e. '..., beate amice, ...'). That is, for the latter case, the beginning word could only
                # be a vocative, so the words connected with it must also be of that case.
                if (isinstance(subterm, Word) and subterm.word == "o") or \
                        (isinstance(subterm, NominalWord) and len(possible_inputs[main_index]) == 1 and subterm.case == Case(6)):
                    # Potential other condition:
                    # or (isinstance(subterm, Punctuation) and self.sequence_matches_construction(possible_inputs, main_index, [Construction(8)], possible_inputs[main_index][num_subterm - 1])

                    # This index loops over terms in a more controlled manner--it goes over all the terms that
                    # could be part of the direct address.
                    term_index: int = 0
                    # This item holds the term which is to be examined in its construction to see if it is
                    # part of the direct address.
                    next_term = possible_inputs[main_index + 1]
                    while self.term_matches_construction(next_term, [Construction(8)]):
                        possible_inputs[main_index + term_index + 1] = self.get_specified_subterms(next_term, [Construction(8)])
                        term_index += 1
                        next_term = possible_inputs[main_index + term_index + 1]

                    if term_index != 0:
                        main_index += (term_index - 1)
                # The following condition attempts to handle prepositional phrases--that is, in detecting them,
                # it determines what words could be the object of the preposition, given their placement after
                # the preposition (which Latin always does except for, perhaps, in incredibly rare poetic uses).
                elif type(subterm) == Word and (Construction(6) in subterm.constructions or Construction(7) in subterm.constructions) and not isinstance(subterm, VerbalWord):
                    # This list holds the constructions which the preposition can take. Generally, this will be only
                    # the Accusative or Ablative constructions. Some prepositions take both, however, which requires
                    # that the constructions_taken be a list and that the conditions given below are separate for
                    # the Accusative and Ablative constructions.
                    constructions_taken: list = []
                    if Construction(6) in subterm.constructions:
                        constructions_taken.append(Construction(6))
                    if Construction(7) in subterm.constructions:
                        constructions_taken.append(Construction(7))

                    # The following index allows for iteration and access in the loop related to finding
                    # the terms which may be the object of the preposition.
                    prep_term_index: int = 0
                    # The following variable holds the next term which could be part of the object of
                    # the preposition.
                    next_term = possible_inputs[main_index + 1]
                    while self.term_matches_construction(next_term, constructions_taken):
                        possible_inputs[main_index + prep_term_index + 1] = self.get_specified_subterms(next_term, constructions_taken)
                        prep_term_index += 1
                        next_term = possible_inputs[main_index + prep_term_index + 1]
                    # The following condition moves along the main_index past the object of the preposition
                    # or throws an error if the index is empty, as it is not grammatically correct not to have
                    # an object for the preposition.
                    if prep_term_index != 0:
                        main_index += (prep_term_index - 1)
                    else:
                        ValueError("The preposition within this sentence does not have an object, which is ungrammatical.")

            main_index += 1
        return possible_inputs

    def term_matches_construction(self, term: list, constr_list: list) -> bool:
        """
        This method takes a term and a construction list and sees whether or not the case of the term
        would match a construction. In other words, this shows whether the word where the constructions
        came from would take the term as some sort of grammatical object or not.
        :param term: a list of potential forms for a Word.
        :param constr_list: a list of constructions that may match the Word's potential forms.
        :return: a boolean as to whether the term matches some form of a given Word.
        """

        # This boolean returns the final value of whether or not the construction and cases of the term
        # have a match and could, thusly, be linked together grammatically.
        has_construction: bool = False
        # This list stores the cases which correspond to the constructions and allow the constructions
        # to be compared to the cases of the terms accordingly.
        corresponding_cases: list = []
        # The following iteration converts the constructions to cases and puts them in the
        # corresponding_cases list.
        for construction in constr_list:
            corresponding_cases.append(self.construction_to_case_conversion(construction))
        # The following iteration determines whether the case of a term matches that of
        # the constructions.
        for subterm in term:
            if isinstance(subterm, NominalWord) and subterm.case in corresponding_cases:
                has_construction = True
        return has_construction

    def get_specified_subterms(self, term: list, constr_list: list) -> list:
        """
        As a companion method to the above method, this method gets the items which match the constructions
        in the construction_list from the given term.
        :param term: a list of potential forms for a Word.
        :param constr_list: a list of constructions that may match the Word's potential forms.
        :return: a list of forms for a Word that actually match constructions on constr_list.
        """

        # This list is the result of "trimming" the list of any items which do not match
        # a construction found in constr_list.
        trimmed_list: list = []
        # This list stores the cases which correspond to the constructions and allow the constructions
        # to be compared to the cases of the terms accordingly.
        corresponding_cases: list = []
        # The following iteration converts the constructions to cases and puts them in the
        # corresponding_cases list.
        for construction in constr_list:
            corresponding_cases.append(self.construction_to_case_conversion(construction))
        # The following iteration determines whether the case of a term matches that of
        # the constructions.
        for subterm in term:
            if isinstance(subterm, NominalWord) and subterm.case in corresponding_cases:
                trimmed_list.append(subterm)
        return trimmed_list


    @staticmethod
    def construction_to_case_conversion(construction: Construction) -> Case:
        """
        This method converts an item of the Construction enumeration to that of the Case enumeration.
        :param construction: a Construction item to be converted to a Case.
        :return: a Case item derived from the given Construction.
        """

        # This item holds the Case for which the Construction matches.
        corresponding_case: Case = None
        if construction == Construction(1):
            corresponding_case = Case(1)
        elif construction in [Construction(2), Construction(3), Construction(4)]:
            corresponding_case = Case(2)
        elif construction == Construction(5):
            corresponding_case = Case(3)
        elif construction == Construction(6):
            corresponding_case = Case(4)
        elif construction == Construction(7):
            corresponding_case = Case(5)
        elif construction == Construction(8):
            corresponding_case = Case(6)
        else:
            raise NotImplementedError("The used construction either does not exist or has not been implemented.")
        return corresponding_case

    # TODO COMPLETION; DOCUMENTATION
    # The following method had some issues and is currently not complete. The idea is to track items as
    # sequences of connected terms by using punctuation as markers.
    # def sequence_matches_construction(self, term_sequence, current_main_index, construction_list, punctuation_mark):
        # sequence_matches: bool = False
        # current_term: list = term_sequence[current_main_index + 1]
        # sequence_not_ended: bool = True
        # temp_index: int = 0
        # while(sequence_not_ended):
            # print(current_term)
            # if((type(current_term) is tuple and isinstance(current_term[1], Punctuation)) or not self.term_matches_construction(current_term, construction_list)):
                # sequence_not_ended = False
            # else:
                # current_main_index += 1
                # current_term = term_sequence[current_main_index]
        # return sequence_matches

    def chunk_terms(self, remaining_terms: list) -> list:
        """
        The following method performs the chunking step. It is currently unfinished,
        as issues in performing portions of the chunking step have caused slow progress and
        have revealed all of the ambiguities and complexities which come with this sort of chunking.
        :param remaining_terms: a list of groupings of word forms to be grammatically chunked.
        :return: a chunked list of terms.
        """

        # This list contains the new sentence(s) with terms chunked accordingly.
        sentence_list: list = []
        # This is a 3-tuple works with punctuation to help denote certain grammatical units.
        # The first item, a boolean, indicates whether or not this should be used in order to group
        # words via punctuation. The second item is the first word in the given grouping.
        # The third item is the ending term of the sequence; for example, if there were parentheses,
        # the third item would denote an endpoint to checking the sequence. Currently,
        # it is not used in the system (due to the additional complexity adding it would require),
        # but I would like to use it in the future.
        grammar_tracker: tuple = (False, 0, None)
        # This index allows for iteration over the remaining_terms list
        main_term_index: int = 0
        while main_term_index < len(remaining_terms):
            # This object holds a single term used in the iteration process.
            term = remaining_terms[main_term_index]
            # If there is a term that the dictionary does not handle, a warning has already been given.
            # This warning will become an error when this program develops further. For now, however, it is
            # a warning to allow the rest of the program to be visible for examination.
            if len(term) == 0:
                pass
            # This condition handles punctuation, as all punctuation is grouped in tuples.
            elif isinstance(term, tuple):
                # The following conditions distinguish between the types of punctuation.
                # This condition handles punctuation that causes the grammar before and after it to be
                # definitely unrelated.
                if term[1] == Punctuation(1):
                    if (main_term_index + 1) < len(remaining_terms):
                        grammar_tracker = (True, main_term_index + 1, None)
                    else:
                        pass
                # This condition handles punctuation that potentially causes, but does not definitely cause,
                # the grammar before and after it to be unrelated.
                elif term[1] == Punctuation(2):
                    # This variable holds a string item that is paired with the given punctuation--usually,
                    # items such as commas, parentheses, dashes, or others occur in corresponding pairs.
                    # With the grammar tracker, this can be modeled.
                    end_term: string = term[0]
                    if end_term == '(':
                        end_term = ')'
                    if end_term == ':' or end_term == '...':
                        end_term = None
                    grammar_tracker = (True, main_term_index + 1, end_term)
                # If punctuation appears that is negligible to the sentence as a whole, we may just
                # get rid of it and set the index appropriately.
                elif term[1] == Punctuation(3):
                    del term
                    main_term_index -= 1
                else:
                    raise NotImplementedError("The given punctuation, " + term[0] +
                                              ", is not currently a feature of the system.")
            # This condition handles chunking that has to do with actual words, not punctuation.
            else:
                # The first chunking process is for prepositional phrases. These are easier to handle
                # because they tend to be a single syntactic unit not divided up in a sentence. However,
                # they are still complex.
                if type(term[0]) is Word and term[0].part_of_speech == PartOfSpeech(6):
                    # This list will hold the words related to the prepositional phrase throughout
                    # the following chunking process.
                    phrase: list = []
                    # This is an index for the loop below.
                    prep_index: int = 0
                    # This loop determines what words match the potential constructions of the preposition.
                    while isinstance(term[0], Word) and \
                            self.term_matches_construction(remaining_terms[main_term_index + prep_index + 1],
                                                           term[0].constructions):
                        prep_index += 1
                        phrase.append(remaining_terms[main_term_index + prep_index])
                    del prep_index
                    if len(phrase) != 0:
                        # This index allows for iteration and access over the following loop.
                        constr_index: int = 0
                        # This loop determines which construction is the one that is actually being used.
                        while constr_index < len(term[0].constructions):
                            constr: Construction = term[0].constructions[constr_index]
                            case: Case = self.construction_to_case_conversion(constr)
                            new_phrase: list = []
                            for subphrase in phrase:
                                for single_word in subphrase:
                                    if single_word.case == case:
                                        new_phrase.append(subphrase)
                            if len(new_phrase) == len(phrase):
                                phrase = new_phrase
                                constr_index = len(term[0].constructions)
                            else:
                                constr_index += 1
                        del constr_index

                        # This tuple holds the two indices which denote exactly where the noun is within
                        # the given phrase. The first noun will be the one found, in this case, as
                        # handling multiple nouns is not part of this method yet.
                        noun_indices: tuple = self.find_noun(phrase)
                        # This item will be used in the following loop for the check_matching_terms
                        # function to assure similarity in various aspects to it.
                        noun = phrase[noun_indices[0]][noun_indices[1]]
                        # This item will hold the noun phrase which will be the highest unit paired with
                        # the overall object of the preposition. It is a list because the adjectival phrase
                        # may or may not be added to it.
                        noun_phrase = [phrase[noun_indices[0]][noun_indices[1]], Phrase(1)]
                        del phrase[noun_indices[0]]
                        # This item is initially a list, but it will eventually hold the list of modifying
                        # adjectives in the prepositional phrase and the notion of the adjectival phrase Phrase
                        # itself, assuming that an adjective is found.
                        adjectival_phrase = []
                        # This loop selects out the specific adjectives that match the chosen noun and
                        # places them into the adjectival_phrase list for insertion into the overall chunk.
                        # It also assures that any parts-of-speech that are potentially nouns are
                        # rid of for the main noun.
                        for subphrase in phrase:
                            matching_items: list = self.check_matching_terms([noun], subphrase)[2]
                            for item in matching_items:
                                if item.part_of_speech == PartOfSpeech(3):
                                    adjectival_phrase.append(item)
                        if len(adjectival_phrase) != 0:
                            adjectival_phrase = (adjectival_phrase, Phrase(2))
                            noun_phrase.insert(0, adjectival_phrase)

                        # This tuple pairs the noun_phrase object with the Object of the Preposition Use.
                        object_of_preposition: tuple = (noun_phrase, Use(4))
                        # This tuple pairs the preposition with its object and its prepositional phrase Phrase.
                        prepositional_phrase: tuple = (term[0], object_of_preposition, Phrase(4))
                        sentence_list.append(prepositional_phrase)
                    else:
                        raise ValueError("The given preposition '" + term[0].word + "' does not correspond to its given object.")
                # elif isinstance(term[0], VerbalWord):
                    # objects_taken = term[0].constructions
                    # for num_constr, constr in enumerate(objects_taken):
                        # objects_taken[num_constr] = self.construction_to_case_conversion(constr)
                    # closest_object_index: tuple = ()
                    # for num_word, word in enumerate(remaining_terms):
                        # debugging prints:
                        # print(word)
                        # print(closest_object_index)
                        # print(type(word))
                        # for num_object, object in enumerate(word):
                            # if isinstance(object, NominalWord) \
                                    # and object.part_of_speech == PartOfSpeech(1) \
                                    # and object.case in objects_taken \
                                    # and closest_object_index != () \
                                # and abs(closest_object_index[0] - main_term_index) > abs(num_word - main_term_index):
                                # closest_object_index = (num_word, num_object)
                            # elif isinstance(object, NominalWord) \
                                    # and object.part_of_speech == PartOfSpeech(1) \
                                    # and object.case in objects_taken \
                                    # and closest_object_index == ():
                                # closest_object_index: tuple = (num_word, num_object)
                            # The final condition is meant to track whether or not punctuation (num_word) comes between
                            # the verb (main_term_index) and the current designated "direct object" (closest_object_index).
                            # If the difference between the distances of the verb to the punctuation and of the
                            # verb to the object are greater such that the punctuation comes between the verb
                            # and the object, the program assumes that the object must be closer and clears its
                            # current designation of direct object.
                            # elif isinstance(word, tuple) \
                                # and isinstance(word[1], Punctuation) \
                                # and closest_object_index != () and \
                                    # (main_term_index > num_word and (main_term_index - closest_object_index[0]) > (main_term_index - num_word)) or \
                                    # (main_term_index < num_word and (closest_object_index[0] - main_term_index) > (num_word - main_term_index)):
                                    # closest_object_index = ()

                    # direct_object: list = [remaining_terms[closest_object_index[0]][closest_object_index[1]]]
                    # direct_object_phrase: tuple = ()
                    # noun_phrase: tuple = ()
                    # adj_phrase: tuple = ([], Phrase(2))
                    # adj_index: int = 0
                    # if closest_object_index == ():
                        # raise NotImplementedError("Currently, intransitive verbs are not handled by the system.")
                    # elif closest_object_index[0] > main_term_index:
                        # dir_obj_index: int = closest_object_index[0] - 1
                        # while dir_obj_index >= 0:
                            # if isinstance(remaining_terms[dir_obj_index][0], NominalWord):
                                # matching_terms: tuple = self.check_matching_terms([direct_object[-1]], remaining_terms[dir_obj_index])
                                # if matching_terms[0]:
                                    # direct_object.insert(0, matching_terms[2])
                                # else:
                                    # dir_obj_index = -1
                            # dir_obj_index -= 1
                        # if direct_object[0] != direct_object[-1]:
                            # while(direct_object[adj_index] != direct_object[-1]):
                                # adj_phrase[0].append(direct_object[adj_phrase])
                                # adj_index += 1
                        # noun_phrase = ([direct_object[-1]], Phrase(1))
                    # elif closest_object_index[0] < main_term_index:
                        # dir_obj_index: int = closest_object_index[0] + 1
                        # while dir_obj_index < len(remaining_terms):
                            # matching_terms: tuple = self.check_matching_terms([direct_object[0]], remaining_terms[dir_obj_index])
                            # if(matching_terms[0]):
                                # direct_object.append(matching_terms[2])
                            # else:
                                # dir_obj_index = len(remaining_terms)
                            # dir_obj_index += 1
                        # if direct_object[0] != direct_object[-1]:
                            # if len(direct_object) > 0:
                                # adj_index = 1
                            # while(direct_object[adj_index] != direct_object[0]):
                                # adj_phrase[0].append(direct_object[adj_phrase])
                                # adj_index += 1
                        # noun_phrase = ([direct_object[0]], Phrase(1))
                    # direct_object_phrase = (direct_object, Use(2))
                    # complete_direct_object: tuple = ()
                    # if adj_index > 0:
                        # complete_direct_object = (adj_phrase, noun_phrase, Use(2))
                    # else:
                        # complete_direct_object = (noun_phrase, Use(2))
                        # del adj_phrase
                    # print('CDO: ' + str(complete_direct_object))
                    # sentence_list.append(complete_direct_object)
                    # Fixes to make: 1) get adjectives to work with the construction.
                    # 2) Finish by making a full verb phrase. Catch adverbs.
            main_term_index += 1
        return sentence_list

    @staticmethod
    def check_matching_terms(term_a: list, term_b: list) -> tuple:
        """
        The following method checks whether two terms match or not in terms of case, number, and gender;
        they could match in multiple terms, which is why a boolean and two lists are returned with each
        of these pieces of information. They are returned in a tuple. This term is to be used for
        nouns and adjectives, as verbs do not tend to match other items so much as they have either
        corresponding subjects or objects (or extended constructions).
        :param term_a: one list of related Word objects to be compared.
        :param term_b: another list of related Word objects to be compared.
        :return: a tuple containing boolean as to whether two items match in terms of
        case, number, and gender, and also containing two lists with the common terms.
        """
        # The following variable is a boolean which denotes whether or not terms do, in fact, have a match
        # between them. The two variables after this one are lists which store the matching terms in accordance
        # with this method's parameters. Finally, these three items are stored as a tuple in shared_terms
        # such that they can be easily returned.
        are_terms_shared: bool = False
        new_term_a: list = []
        new_term_b: list = []
        shared_terms: tuple = (are_terms_shared, new_term_a, new_term_b)

        # This loop first assures that all genders will be considered in that a noun or adjective that
        # could be masculine or feminine will recognize whether one or the other is tacked onto
        # it by putting all genders for each term into a list. It does the same for each instance of the
        # other list within the inner loop. Then, it checks to see if the terms match. If they do,
        # then are_terms_shared becomes true and the lists each are appended with the appropriate subterms.
        for subterm_a in term_a:
            # This variable holds the list of genders that subterm_a contains.
            a_genders: list = []
            if subterm_a.gender == Gender(4):
                a_genders = [Gender(1), Gender(2)]
            else:
                a_genders = [subterm_a.gender]

            for subterm_b in term_b:
                # This variable holds the list of genders that subterm_b contains.
                b_genders: list = []
                if subterm_b.gender == Gender(4):
                    b_genders = [Gender(1), Gender(2)]
                else:
                    b_genders = [subterm_b.gender]

                if(subterm_a.case == subterm_b.case and (subterm_a.gender in b_genders or subterm_b.gender in a_genders) and subterm_a.number == subterm_b.number):
                    are_terms_shared = True
                    new_term_a.append(subterm_a)
                    new_term_b.append(subterm_b)
        return shared_terms

    @staticmethod
    def find_noun(phrase: list) -> tuple:
        """
        Given a phrase, this method finds the first noun present in it. This is good for phrases
        in which adjectives are piled up and one wants to figure out which word is the noun such
        that the rest of the phrase can be modeled around the given noun.
        :param phrase: a list of terms (e.g. groups of Word objects).
        :return: a tuple containing the indices for a location of a noun.
        """
        noun_found: bool = False
        # The following index iterates over the outer loop given below.
        noun_term_index: int = 0
        # The following item is the return values for this method, as it is related to the indices
        # of the phrase at which point the noun is located.
        noun_phrase_location: tuple = (None, None)
        # This list holds the potential noun locations (i.e. a tuple like the one given above) from a phrase.
        potential_np_locations: list = []
        while noun_term_index < len(phrase):
            # The following index iterates over the internal loop given below.
            noun_word_index: int = 0
            # This variable holds the length of the internal list.
            inner_length: int = len(phrase[noun_term_index])
            while noun_word_index < inner_length:
                if phrase[noun_term_index][noun_word_index].part_of_speech == PartOfSpeech(1):
                    noun_phrase_location = (noun_term_index, noun_word_index)
                    potential_np_locations.append(noun_phrase_location)
                noun_word_index += 1
            noun_term_index += 1
        else:
            if noun_phrase_location == (None, None):
                raise ValueError("The phrase given does not have a noun.")
            # If the length of potential_np_locations is 1, then there is only one
            # option for the noun. But if it is greater than 1, then some analysis is done.
            # What the condition below attepts to do is to argue that the word with less forms
            # or less ambiguity is likely the noun in this situation. If we find a word with only
            # one option overall in phrase, that is obviously the noun. But if we do not, then the
            # aforementioned argument is made. It is not a perfect argument, but it ought to cover
            # many cases of ambiguity well due to the prior preprocessing before this method is called
            # at all.
            elif len(potential_np_locations) > 1:
                # This variable currently holds the location with the lowest number of morphological variants.
                lowest_location: int = 0
                # This variable holds the current location being checked and serves as this loop's index.
                num_location: int = 0
                while num_location < len(potential_np_locations):
                    # These indices serve to access the phrase terms with the indices previously gathered.
                    location_index_1: int = potential_np_locations[lowest_location][0]
                    location_index_2: int = potential_np_locations[num_location][0]
                    if len(phrase[location_index_1]) == 1:
                        num_location = len(potential_np_locations)
                    else:
                        if len(phrase[location_index_1]) > len(phrase[location_index_2]):
                            lowest_location = num_location
                    noun_phrase_location = potential_np_locations[lowest_location]
                    num_location += 1
        return noun_phrase_location

    # TODO COMPLETION; DOCUMENTATION
    # def print_tree(self):
        # ...

# I have provided the following examples, printed out in accordance with various steps that the program takes,
# to show what the system does and what I have implemented. Sentences from the test sentence key
# can also be used. Most, if not all, should be supported in reading in even if their forms are not
# fully supported by the system yet. The information given can be compared to that displayed in the
# Test_Sentence_Key.txt file in the Project Text Files folder to show that the correct forms are included
# in every single entry of every single word if the dictionaries contain that word.
test1 = Sciens("Vita humana est supplicium.")
test2 = Sciens("Semper gloria et fama tua manebunt.")
test3 = Sciens("Saepe peccamus.")
test4 = Sciens("Nihil est omnino beatum.")
test5 = Sciens("Propter iram in culpa estis et cras poenas dabitis.")
test6 = Sciens("Infinitus est numerus stultorum.")
test7 = Sciens("Et fortunam et vitam antiquae patriae saepe laudas sed recusas.")
test8 = Sciens("Otium est bonum, sed otium multorum est parvum.")
test9a = Sciens("Officium nautam de otio hodie vocat.")
# The following sentence shows adjectival flexibility when it comes to chunking prepositional phrases.
# It is not in the test sentence key; it is one I added to explicitly show this feature.
test9b = Sciens("Officium nautam de immodico malo otio bono bello hodie vocat.")
# According to the system, 'culpant' will not be a valid form for a noun. This is correct; it is a verb,
# which the system identifies.
test10 = Sciens("Laudas me; culpant me.")
test11 = Sciens("Puellae magistram de consilio malo sine mora monent.")
# According to the system, 'adiuvate', 'conservate', and 'virorum' will not be recognized. This is correct.
# These forms have not been added yet.
test12 = Sciens("Mali sunt in meo numero et de exitio bonorum virorum cogitant. Bonos adiuvate; conservate patriam et populum Romanum.")
# According to the system, 'nostra' will not be recognized. This is correct. This form has not been added yet.
test13 = Sciens("Propter culpas malorum patria nostra non valebit.")
# According to the system, 'pauci' and 'viri' will not be recognized. This is correct. These forms have not been added yet.
test14 = Sciens("Pauci viri de cura animi cogitabant.")
# According to the system, 'nulla' will not be recognized. This is correct. The form has not been added yet.
test15 = Sciens("Nulla avaritia sine poena est.")
# According to the system, 'cogitare' will not be recognized. This is correct. The form has not been added yet.
test16 = Sciens("Debetis, amici, de populo Romano cogitare.")

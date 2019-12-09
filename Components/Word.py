"""
This file contains the classes pertaining to Words, which are the basic units of
the chunking process; when Latin words are parsed, they are put into appropriate Word objects.
As such, the items here are the basic building blocks which form the backbone
of the overall grammar-parsing process.

Author: Stephen Bothwell
Version: 1.0.1
Last Updated: 9/12/2019
"""
from .Enumerators.GrammaticalAttributes import *


class Word:
    """
    This class is the base class on which other classes related to individual words are built.
    It, however, can be used as its own class and is for certain parts-of-speech. It encapsulates
    the basic unit by which words will be chunked and the grammar will be figured out. As such,
    this is an incredibly important building block for the program as a whole.
    This class can handle Adverbs, Prepositions, Particles, and Conjunctions on its own.
    """
    def __init__(self, wrd: str, pos: PartOfSpeech, constr_list: list, desc: str = None) -> None:
        self.word = wrd
        self.part_of_speech = pos
        self.constructions: list = constr_list
        self.create_constructions(constr_list)
        self.descriptor: str = desc

    """
    TODO: I want to move this later to combine it with Paradigm's version. I think that
    the Paradigm and Word classes could be given a further superclass and combined, but
    I would rather leave them separate for now due to time constraints.
    """
    @staticmethod
    def create_constructions(constr_list: list) -> None:
        """
        This method takes the construction list supplied to the Word object and creates
        constructions in correspondence with the enumeration in GrammaticalAttributes,
        replacing items on the list with these Construction objects.
        :param constr_list: a list of strings that represent constructions.
        :return: None.
        """
        for num_item, item in enumerate(constr_list):
            if type(constr_list[num_item]) is str:
                temp_item = item.strip()
                if temp_item == 'Nominative':
                    constr_list[num_item] = Construction(1)
                elif temp_item == 'Objective Genitive':
                    constr_list[num_item] = Construction(2)
                elif temp_item == 'Partitive Genitive':
                    constr_list[num_item] = Construction(3)
                elif temp_item == 'Subjective Genitive':
                    constr_list[num_item] = Construction(4)
                elif temp_item == 'Dative':
                    constr_list[num_item] = Construction(5)
                elif temp_item == 'Accusative':
                    constr_list[num_item] = Construction(6)
                elif temp_item == 'Ablative':
                    constr_list[num_item] = Construction(7)
                elif temp_item == 'Vocative':
                    constr_list[num_item] = Construction(8)
                elif temp_item == 'Infinitive':
                    constr_list[num_item] = Construction(9)
                elif temp_item == 'Accusative and Infinitive':
                    constr_list[num_item] = Construction(10)
                elif temp_item == 'Accusative and Dative':
                    constr_list[num_item] = Construction(11)
                elif temp_item == 'Double Dative':
                    constr_list[num_item] = Construction(12)
                elif temp_item == 'Equivalence':
                    constr_list[num_item] = Construction(13)
                elif temp_item == '':
                    constr_list[num_item] = None
                else:
                    ValueError("The construction " + temp_item + " is not recognized.")

    def __repr__(self):
        """
        This method allows for better visibility in seeing what the Word object is when it is printed or
        an object containing it is printed.
        :return: a string representing the object.
        """
        return "<" + self.word + ": " + str(self.part_of_speech) + ">"


class NominalWord(Word):
    """
    This item is a subclass of Word that handles those parts-of-speech related to Nouns.
    Usually, these are Nouns and Adjectives.
    """
    def __init__(self, wrd: str, pos: PartOfSpeech, cs: Case, gndr: Gender, nmbr: Number,
                 constr_list: list, desc: str = None) -> None:
        super(NominalWord, self).__init__(wrd, pos, constr_list, desc)
        self.case = cs
        self.gender = gndr
        self.number = nmbr

    def __repr__(self):
        """
        This method allows for better visibility in seeing what the Word object is when it is printed or
        an object containing it is printed.
        :return: a string representing the object.
        """
        return "<" + self.word + ": " + str(self.part_of_speech) + "; " + \
               str(self.case) + "; " + str(self.gender) + "; " + str(self.number) + ">"


class VerbalWord(Word):
    """
    This item is a subclass of Word that handles those parts-of-speech related to Verbs.
    This is usually just verbs.
    """
    def __init__(self, wrd: str, pos: PartOfSpeech, md: Mood, nmbr: Number, prsn: Person,
                 tns: Tense, vc: Voice, constr_list: list, desc: str = None) -> None:
        super(VerbalWord, self).__init__(wrd, pos, constr_list, desc)
        self.mood = md
        self.number = nmbr
        self.person = prsn
        self.tense = tns
        self.voice = vc

    def __repr__(self) -> str:
        """
        This method allows for better visibility in seeing what the Word object is when it is printed or
        an object containing it is printed.
        :return: a string representing the object.
        """
        return "<" + self.word + ": " + str(self.part_of_speech) + "; " + str(self.mood) + "; " + str(self.number) + "; " \
               + str(self.person) + "; " + str(self.tense) + "; " + str(self.voice) + ">"

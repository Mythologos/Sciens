"""
This file defines the classes related to paradigms--Paradigm, NominalParadigm, and VerbalParadigm.
These classes are critical to the word-search process and form the core of the values placed in the
Root Dictionary.

Author: Stephen Bothwell
Version: 1.0
Last Updated: 9/12/2019
"""

from GrammaticalAttributes import Construction, Gender, Mood, PartOfSpeech, Tense, Voice


class Paradigm:
    """
    This class forms the basic paradigms; however, this is generally not used.
    Rather, its subclasses are implemented depending on the paradigm needed.
    """

    # The following method initializes the Paradigm object.
    def __init__(self, pos_id: int, endings: dict, constr_list: list) -> None:
        self.part_of_speech = PartOfSpeech(pos_id)
        self.suffix_dict = endings
        self.constructions = constr_list
        self.create_constructions(constr_list)

    """
    TODO: I want to move this later to combine it with Word's version. I think that
    the Paradigm and Word classes could be given a further superclass and combined, but
    I would rather leave them separate for now due to time constraints.
    """
    @staticmethod
    def create_constructions(constr_list: list) -> None:
        """
        This method takes the construction list supplied to the Paradigm object and creates
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


# The NominalParadigm class represents, in particular, Paradigms for nouns; thus,
# this class contains nominal aspects alongside the traditional paradigmatic ones.
# This class is generally used for nouns and adjectives.
class NominalParadigm(Paradigm):
    # This method initializes the NominalParadigm class.
    def __init__(self, pos_id, endings, constr_list, gndr):
        # type: (int, dict, list, int) -> None
        super(NominalParadigm, self).__init__(pos_id, endings, constr_list)
        self.gender = Gender(gndr)


# The VerbalParadigm class represents, in particular, Paradigms for verbs; thus,
# this class contains verbal aspects alongside the traditional paradigmatic ones.
# This class is generally used for verbs.
class VerbalParadigm(Paradigm):
    # This method initializes the VerbalParadigm class.
    def __init__(self, pos_id, endings, constr_list, md, tns, vc):
        # type: (int, dict, list, int, int, int) -> None
        super(VerbalParadigm, self).__init__(pos_id, endings, constr_list)
        self.mood = Mood(md)
        self.tense = Tense(tns)
        self.voice = Voice(vc)

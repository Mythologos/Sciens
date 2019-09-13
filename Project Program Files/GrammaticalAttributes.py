"""
This class contains the set of grammatical attributes related to endings like affixes and
individual words. These can be applied to nouns, verbs, and every other part-of-speech as
necessary; in fact, there is a PartOfSpeech enumeration. All of the items here are enumerations
which are meant to save memory consumption throughout the rest of the program through such a construction.

Author: Stephen Bothwell
Version: 1.0.1
Last Updated: 9/12/2019
"""

from enum import Enum


class Case(Enum):
    """
    The following catalogues the nominal cases which Latin has.
    """

    NOMINATIVE = 1
    GENITIVE = 2
    DATIVE = 3
    ACCUSATIVE = 4
    ABLATIVE = 5
    VOCATIVE = 6
    LOCATIVE = 7  # currently unused; for later updates
    UNKNOWN = 8


class Construction(Enum):
    """
    The following catalogues the constructions which some word can take.
    """

    NOMINATIVE = 1
    OBJECTIVE_GENITIVE = 2
    PARTITIVE_GENITIVE = 3
    SUBJECTIVE_GENITIVE = 4
    DATIVE = 5
    ACCUSATIVE = 6
    ABLATIVE = 7
    VOCATIVE = 8

    # The following will not have been implemented yet except for Equivalence, as they require more complexity.
    INFINITIVE = 9
    ACCUSATIVE_AND_INFINITIVE = 10
    ACCUSATIVE_AND_DATIVE = 11
    DOUBLE_DATIVE = 12
    EQUIVALENCE = 13


class Gender(Enum):
    """
    The following catalogues the genders which a word (generally a nominal or adjectival one) can have.
    """
    FEMININE = 1
    MASCULINE = 2
    NEUTER = 3
    MASC_OR_FEM = 4
    UNKNOWN = 5


class Mood(Enum):
    """
    The following catalogues the moods which a verb (or a verbal word) can have.
    """
    INDICATIVE = 1
    SUBJUNCTIVE = 2
    IMPERATIVE = 3


class Number(Enum):
    """
    The following catalogues the numbers which a word can have.
    """
    SINGULAR = 1
    PLURAL = 2
    FROZEN = 3


class PartOfSpeech(Enum):
    """
    The following catalogues the parts-of-speech which a word can have.
    """
    NOUN = 1
    VERB = 2
    ADJECTIVE = 3
    ADVERB = 4
    PRONOUN = 5
    PREPOSITION = 6
    CONJUNCTION = 7
    PARTICLE = 8


class Person(Enum):
    """
    The following catalogues the persons which a verb can have.
    """
    FIRST = 1
    SECOND = 2
    THIRD = 3


class Phrase(Enum):
    """
    The following lists off various grammatical phrases used in the chunking process.
    """
    NOUN_PHRASE = 1
    ADJECTIVAL_PHRASE = 2
    VERB_PHRASE = 3
    PREPOSITIONAL_PHRASE = 4
    SENTENCE = 5


class Punctuation(Enum):
    """
    The following catalogues the types of punctuation which are handled by the program.
    """

    # Dividing punctuation is that which causes the grammar before and after it to be unrelated.
    DIVIDING = 1
    # Relating punctuation is that which may or may not connect different portions of grammar.
    RELATING = 2
    # Ignored punctuation is that which should be ignored such that the sentence can be read entirely
    # without it.
    IGNORED = 3


class Tense(Enum):
    """
    The following catalogues the persons which a verb can have.
    """
    PRESENT = 1
    IMPERFECT = 2
    FUTURE = 3
    PERFECT = 4
    PLUPERFECT = 5
    FUTURE_PERFECT = 6


class Use(Enum):
    """
    The following catalogues the uses which a term can have. This is used in the chunking process.
    """
    SUBJECT = 1
    DIRECT_OBJECT = 2
    INDIRECT_OBJECT = 3
    OBJECT_OF_PREPOSITION = 4
    PREDICATE_NOMINATIVE = 5
    OBJECTIVE_GENITIVE = 6
    SUBJECTIVE_GENITIVE = 7
    PARTITIVE_GENITIVE = 8
    DIRECT_ADDRESS = 9
    IN_APPOSITION = 10


class Voice(Enum):
    """
    The following catalogues the voices which a verb can have.
    """
    ACTIVE = 1
    PASSIVE = 2

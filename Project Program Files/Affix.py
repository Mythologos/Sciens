"""
This file contains the classes that are related to the endings that make up paradigms.
These have been collectively called Affixes, although they could be generalized to
suffixes since they are only being used for Latin as of the current state of this program.

Author: Stephen Bothwell
Version: 1.0.1
Last Updated: 9/12/2019
"""

from GrammaticalAttributes import Case, Number, Person


class NominalAffix:
    """
    This class is used to create affixes related to words that work nominally--
    that is, usually nouns and adjectives.
    """
    def __init__(self, cs: Case, nmbr: Number) -> None:
        self.case = cs
        self.number = nmbr


class VerbalAffix:
    """
    This class is used to create affixes related to words that work verbally--
    that is, usually verbs.
    """
    def __init__(self, prsn: Person, nmbr: Number) -> None:
        self.person = prsn
        self.number = nmbr

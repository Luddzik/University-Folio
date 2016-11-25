# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev



# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

# English nouns with identical plural forms (list courtesy of Wikipedia):

unchanging_plurals = ['bison','buffalo','deer','fish','moose','pike','plankton',
     'salmon','sheep','swine','trout']

from statements import verb_stem, Lexicon

def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # add code here
    if s in unchanging_plurals:
        return s
    elif re.match("men", s[len(s)-3: len(s)]):
        return re.sub("men", "man", s)
    elif verb_stem(s) in unchanging_plurals:
        return ''
    else:
	return verb_stem(s)
    


def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    printlist = []
    for nom in function_words_tags:
        if nom[0] == wd:
            add(printlist, nom[1])

    if len(printlist) == 0:
        if wd in lx.getAll('P'):
	    add(printlist, 'P')

	if wd in lx.getAll('A'):
	    add(printlist, 'A')

        if wd in lx.getAll('N'):
            if wd in unchanging_plurals:
                add(printlist, 'Ns')
                add(printlist, 'Np')
            if noun_stem(wd) is '':
                add(printlist, 'Ns')
            else:
                add(printlist, 'Np')

	elif noun_stem(wd) in lx.getAll('N'):
            if wd in unchanging_plurals:
                add(printlist, 'Ns')
                add(printlist, 'Np')
            if noun_stem(wd) is not '':
                add(printlist, 'Np')
	    else: 
		add(printlist, 'Ns')

        if wd in lx.getAll('I'):
            if verb_stem(wd) is '':
                add(printlist, 'Ip')
            else:
                add(printlist, 'Is')

	elif verb_stem(wd) in lx.getAll('I'):
            if verb_stem(wd) is '':
                add(printlist, 'Ip')
            else:
                add(printlist, 'Is')

        if wd in lx.getAll('T'):
            if verb_stem(wd) is '':
                add(printlist, 'Tp')
            else:
                add(printlist, 'Ts')

        elif verb_stem(wd) in lx.getAll('T'):
            if verb_stem(wd) is '':
                add(printlist, 'Tp')
            else:
                add(printlist, 'Ts')

        return printlist
    else:
        return printlist

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.

# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev



# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
	self.catlist = []

    def add(self, stem, cat):
	pair = (stem, cat)

	add(self.catlist, pair)

    def getAll(self, cat):
	printlist = []
	for elem in (self.catlist):
		if elem[1] == cat:
			add(printlist, elem[0])
	
	return printlist
        

class FactBase:
    # add code here
    def __init__(self):
	self.unarylist = []
	self.binarylist = []

    def addUnary(self, pred, e1):
	pair = (pred, e1)

	add(self.unarylist, pair)

    def addBinary(self, pred, e1, e2):
	binpair = (e1, e2)
	pair = (pred, binpair)

	add(self.binarylist, pair)

    def queryUnary(self, pred, e1):
	chkpair = (pred, e1)
	templist = []
	for i, v in enumerate(self.unarylist):
		if chkpair in self.unarylist:
			add(templist, 'true')
			return True
	if len(templist) == 0:
		return False

    def queryBinary(self, pred, e1, e2):
	chkbinpair = (e1, e2)
	chkpair = (pred, chkbinpair)
	tplist = []
	for i, v in enumerate(self.binarylist):
		if chkpair in self.binarylist:
			add(tplist, 'true')
			return True
	if len(tplist) == 0:
		return False

import re

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    if re.match("[c|s]hs", s[len(s)-3: len(s)]):
	return ''
    elif re.match("[^aeiousxyz]s", s[len(s)-2: len(s)]):
	return s[: len(s)-1]
    elif re.match("[aeiou]ys", s[len(s)-3: len(s)]):
	return s[: len(s)-1]
    elif (len(s)>=5 and re.match("[^aeiou]ies", s[len(s)-4: len(s)])):
	return re.sub("ies", "y", s)
    elif (len(s)==4 and re.match("[^aeiou]ies", s)):
	return s[: len(s)-1]
    elif (re.match("[cs]hes", s[len(s)-4: len(s)]) or re.match("sses", s[len(s)-4: len(s)]) or re.match("zzes", s[len(s)-4: len(s)]) or re.match("[ox]es", s[len(s)-3: len(s)])):
	return s[: len(s)-2]
    elif (re.match("[^s]ses", s[len(s)-4: len(s)]) or re.match("[^z]zes", s[len(s)-4: len(s)])):
	return s[: len(s)-1]
    elif re.match("has", s):
	return re.sub("has", "have", s)
    elif (re.match("[^iosxz]es", s[len(s)-3: len(s)]) or re.match("[^cs]hes", s[len(s)-4: len(s)])):
	return s[: len(s)-1]
    else: return ''

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.


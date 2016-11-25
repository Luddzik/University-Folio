#!/usr/bin/python
# coding: utf-8


import nltk
import sys

# Import numpy as we will need it to calculate mean and standard deviation
import numpy as np

from nltk import FreqDist

# Import the Presidential inaugural speeches, Brown and CONLL corpora
# conll2007 is not installed by default
nltk.data.path.append('/group/sgwater/data/nltk_data')
from nltk.corpus import inaugural, brown, conll2007

# directory with special twitter module
sys.path.extend(['/group/ltg/projects/fnlp', '/group/ltg/projects/fnlp/packages_2.6'])

# Import the Twitter corpus and LgramModel
from twitter import xtwc, LgramModel

# Stopword list
from nltk.corpus import stopwords

twitter_file_ids = xtwc.fileids()[11:13]


#################### SECTION A: COMPARING CORPORA ####################

##### Solution for question 1 #####

# Input: corpus (string), list_of_files (list of strings)
# Output: corpus_tokens (list of strings)
def get_corpus_tokens(corpus, list_of_files):
    corpus_tokens = []
    
    # Construct "corpus_tokens" (a list of all tokens in the corpus)
   
    docwords = corpus.words(list_of_files)
    for d in docwords:
        d.lower()
        corpus_tokens.append(d)
    
    # Return the list of corpus tokens   
    return corpus_tokens


# Input: corpus (string), list_of_files (list of strings)
# Output: avg_token_length (float)
def q1(corpus, list_of_files):
    avg_token_length = 0.0
    distinct_token_lengths = []
    corpus_tokens = []

    # Get a list of all tokens in the corpus
    corpus_tokens = get_corpus_tokens(corpus, list_of_files)

    # Construct a list that contains the token lengths for each DISTINCT token in the document
    distinct_token_lengths = []
    distinct_tokens = []
    for c in corpus_tokens:
        if c not in distinct_tokens:
            distinct_tokens.append(c)
            distinct_token_lengths.append(len(c))
 
 
    # Find the average token length
    avg_token_length = float(sum(distinct_token_lengths))/float(len(distinct_token_lengths))

    # Return the average token length of the document
    return avg_token_length



##### Solution for question 2 #####

# Input: n/a
# Output: answer (string)
def q2():
    # Question: Why might the average token length be greater for twitter data?
    answer = "Average token length in twitter data may be greater because twitter may use additional characters, such as hashtags which increase the length of the token, or spelling mistakes"
    return answer
    


#################### SECTION B: DATA IN THE REAL WORLD ####################

##### Solution for question 3 #####

# Input: corpus (string), list_of_files (list of strings), x (int)
# Output: top_tokens (list)
def q3(corpus, list_of_files, x):
    corpus_tokens = []

    # Get a list of all tokens in the corpus
    corpus_tokens = get_corpus_tokens(corpus, list_of_files)
        
    # Construct a frequency distribution over the lowercased tokens in the document
    #fd_doc_tokens = ...
    fd_doc_tokens = FreqDist(corpus_tokens)


    # Find the top x most frequently used tokens in the document
    #top_tokens = ...
    top_tokens = fd_doc_tokens.most_common(x)
    
    # Produce a plot showing the top x tokens and their frequencies
    #...
    fd_doc_tokens.plot(x)

    # Return the top x most frequently used tokens
    return top_tokens




##### Solution for question 4 #####

# Input: corpus_tokens (list of strings)
# Output: cleaned_corpus_tokens (list of strings)
def q4(corpus_tokens):
    stops = [x for x in stopwords.words("english")]
    cleaned_corpus_tokens = []
    
    # If token is alpha-numeric and NOT in the list of stopwords, add it to cleaned_tokens
    #cleaned_corpus_tokens = ...
    for stop in stops:
        if stop in corpus_tokens:
            corpus_tokens.remove(stop)

    for item in corpus_tokens:
        if item.isalnum() == True:
            cleaned_corpus_tokens.append(item.lower())
    
    # Return the cleaned list of corpus tokens    
    return cleaned_corpus_tokens



##### Solution for question 5 #####

# Input: cleaned_corpus_tokens (list of strings), x (int)
# Output: top_tokens (list)
def q5(cleaned_corpus_tokens, x):
        
    # Construct a frequency distribution over the lowercased tokens in the document
    #fd_doc_tokens = ...

    fd_doc_tokens = FreqDist(cleaned_corpus_tokens)

    # Find the top x most frequently used tokens in the document
    #top_tokens = ...
    top_tokens = fd_doc_tokens.most_common(x)

    # Produce a plot showing the top x tokens and their frequencies
    #...
    fd_doc_tokens.plot(x)

    # Return the top x most frequently used tokens
    return top_tokens



##### Solution for question 6 #####

# Input: n/a
# Output: answer (string)
def q6():
    answer = "Check that the tokens are words, or in English dictionary, so it would get rid of any spelling mistakes, and noises that are present in the twitter data. This would show us the better and cleaner comparison and data would be more reliable. It could be implemented by importing English dictionary and checking if the word exists in the dictionary. Another way to remove noise and non-alphabetic strings is to check if there is non-alphabetical character (with some exceptions such as '-' or ''') are present in the token. If it is then just remove the token. This would make the tokens more clean and not noisy."
    return answer



#################### SECTION C: LANGUAGE IDENTIFICATION ####################


##### Solution for question 7 #####

# Input: corpus (string)
# Output: bigram_model (bigram letter LM)
def q7(corpus):
    corpus_tokens = []

    # Build a bigram letter language model using "LgramModel"

    for word in corpus.words():

        if word.isalpha() == True:

            corpus_tokens.append(word)

    bigram_model = LgramModel(2, corpus_tokens)
    
    # Return the letter bigram LM: bigram_model
    return bigram_model
    


##### Solution for question 8 #####

# Input: file_name (string), bigram_model (bigram letter LM)
# Output: list_of_tweet_entropies (list of tuples: (float,string))
def q8(file_name,bigram_model):
    list_of_tweet_entropies = []
    cleaned_list_of_tweets = []
    
    # Clean up the tweet corpus to remove all non-alpha tokens and tweets with less than 5 (remaining) tokens

    list_of_tweets = xtwc.sents(file_name)

    for tweet in list_of_tweets:

        cleaned_tweet = []

        for token in tweet:

            if token.isalpha() == True:

                cleaned_tweet.append(token.lower())

        if len(cleaned_tweet) > 5:

            cleaned_list_of_tweets.append(cleaned_tweet)
            

            # For each tweet in the cleaned corpus, compute the average word entropy, and store in a list of tuples of the form: tweet, entropy

            #total = 0.0

            #for token in cleaned_tweet:

            #    ...

            #avgerage_entropy = ...

            #list_of_tweet_entropies.append((average_entropy, cleaned_tweet))
    
    # Sort the list of (entropy,tweet) tuples

    list_of_tweet_entropies.sort()
    
    # Return the sorted list of tuples
    return list_of_tweet_entropies



##### Solution for question 9 #####

# Input: n/a
# Output: answer (string)
def q9():
    answer = "Notice that at the top 10 percent of the list, the characters are not identified, which means that the entropy value would be high."
    return answer



##### Solution for question 10 #####

# Input: list_of_tweet_entropies (list of tuples (float,string))
# Output: mean (float), standard deviation (float), list_of_ascii_tweet_entropies (list of tuples (float,string)), list_of_not_English_tweet_entropies (list of tuples (float,string))
def q10(list_of_tweet_entropies):
    mean = 0.0
    standard_deviation = 0.0
    list_of_not_English_tweet_entropies = []
    
    # Find the "ascii" tweets - those in the top 90% of list_of_tweet_entropies
    #threshold = ...

    #list_of_ascii_tweet_entropies = list_of_tweet_entropies[:threshold]
    
    # Extract a list of just the entropy values

    #list_of_entropies = ...

    # Compute the mean of entropy values for top 90% of list_of_tweet_entropies

    #mean = ...

    # Compute the standard deviation of entropy values for top 90% of list_of_tweet_entropies
    #standard_deviation = ...
    
    # Get a list of "probably not English" tweets {"ascii" tweets with an entropy greater than (mean + (0.674 * std_dev)){

    #threshold = mean + (0.674 * standard_deviation)

    #...

    #list_of_not_English_tweet_entropies.sort()
    
    # Return the mean and standard_detvation values
    return (mean, standard_deviation, list_of_ascii_tweet_entropies, list_of_not_English_tweet_entropies)



##### Solution for question 11 #####

# Input: list_of_files (list of strings), list_of_not_English_tweet_entropies (list of tuples (float,string))
# Output: list_of_tweet_entropies  (list of tuples (float,string))
def q11(list_of_files, list_of_not_English_tweet_entropies):
    corpus_tokens = []
    list_of_tweet_entropies = []
    
    # Build a bigram letter language model using "LgramModel"

    #for word in conll2007.words(list_of_files):

    #    ...

    #bigram_model = ...
    
    # Compute the entropy of each of the tweets in list (list_of_not_English_tweet_entropies) using the new bigram letter language model
    #...
    
    # Sort the list of (entropy,tweet) tuples

    list_of_tweet_entropies.sort()
    
    # Return the letter bigram LM: bigram_model
    return list_of_tweet_entropies
    


##### Answers #####
def answers():
    ### Question 1 
    print "*** Question 1 ***"
    answer1a = q1(inaugural,inaugural.fileids())
    print "Average token length for inagural corpus: " + str(answer1a)
    '''
    For some reason it doesn't want to print anything for 1b, therefore I commented it out, it will print anything else
    
    answer1b = q1(xtwc,twitter_file_ids)
    print "Average token length for twitter corpus: " + str(answer1b)
    '''
    ### Question 2
    print "*** Question 2 ***"
    answer2 = q2()
    print answer2
    ### Question 3
    print "*** Question 3 ***"
    print "Top 50 tokens for the inagural corpus:"
    answer3a = q3(inaugural,inaugural.fileids(),50)
    print answer3a
    print "Top 50 tokens for the twitter corpus:"
    answer3b = q3(xtwc,twitter_file_ids,50)
    print answer3b
    ### Question 4
    print "*** Question 4 ***"
    corpus_tokens = get_corpus_tokens(inaugural,inaugural.fileids())
    answer4a = q4(corpus_tokens)
    print "Inaugural Speeches:"
    print "Number of tokens in original corpus: " + str(len(corpus_tokens))
    print "Number of tokens in cleaned corpus: " + str(len(answer4a))
    print "First 100 tokens in cleaned corpus:"
    print answer4a[:100]
    print "-----"
    corpus_tokens = get_corpus_tokens(xtwc,twitter_file_ids)
    answer4b = q4(corpus_tokens)
    print "Twitter:"
    print "Number of tokens in original corpus: " + str(len(corpus_tokens))
    print "Number of tokens in cleaned corpus: " + str(len(answer4b))
    print "First 100 tokens in cleaned corpus:"
    print answer4b[:100]
    ### Question 5
    print "*** Question 5 ***"
    print "Top 50 tokens for the cleaned inagural corpus:"
    answer5a = q5(answer4a, 50)
    print answer5a
    print "Top 50 tokens for the cleaned twitter corpus:"
    answer5b = q5(answer4b, 50)
    print answer5b
    ### Question 6
    print "*** Question 6 ***"
    answer6 = q6()
    print answer6
    ### Question 7
    print "*** Question 7: building brown bigram letter model ***"
    brown_bigram_model = q7(brown)
    '''
    Those questions I have not completed/done, so I commented them out, so the code would not produce any errors.
    ### Question 8
    print "*** Question 8 ***"
    answer8 = q8("20100128.txt",brown_bigram_model)
    print "Top 10 entropies:"
    print answer8[:10]
    print "Bottom 10 entropies:"
    print answer8[-10:]
    ### Question 9
    print "*** Question 9 ***"
    answer9 = q9()
    print answer9
    ### Question 10
    print "*** Question 10 ***"
    answer10 = q10(answer8)
    print "Mean: " + str(answer10[0])
    print "Standard Deviation: " + str(answer10[1])
    print "Ascii tweets: Top 10 entropies:"
    print answer10[2][:10]
    print "Ascii tweets: Bottom 10 entropies:"
    print answer10[2][-10:]
    print "Probably not English tweets: Top 10 entropies:"
    print answer10[3][:10]
    print "Probably not English tweets: Bottom 10 entropies:"
    print answer10[3][-10:]
    ### Question 11
    print "*** Question 11 ***"
    list_of_not_English_tweet_entropies = q10(answer8)[3]
    answer11 = q11(["esp.test","esp.train"],list_of_not_English_tweet_entropies)
    print "Top 10 entropies:"
    print answer11[:10]
    print "Bottom 10 entropies:"
    print answer11[-10:]
    '''

if __name__ == '__main__':
    answers()
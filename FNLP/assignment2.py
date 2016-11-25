import nltk

#import brown corpus
from nltk.corpus import brown

# module for training a Hidden Markov Model and tagging sequences
from nltk.tag.hmm import HiddenMarkovModelTagger

# module for computing a Conditional Frequency Distribution
from nltk.probability import ConditionalFreqDist

# module for computing a Conditional Probability Distribution
from nltk.probability import ConditionalProbDist

### added:
from nltk.tag import map_tag
assert map_tag('brown','universal','NR-TL')=='NOUN','''
The installed Brown-to-Universal POS tag map is out of date. 
Replace ~/nltk_data/taggers/universal_tagset/en-brown.map with 
https://raw.githubusercontent.com/slavpetrov/universal-pos-tags/master/en-brown.map
'''
###

import operator
import random
from math import log

class HMM:
  def __init__(self,train_data,test_data):
    self.train_data = train_data
    self.test_data = test_data
    self.states = []
    self.viterbi = []
    self.backpointer = []

  def emission_model(self,train_data):

    data = []
    for i in train_data:
      for (word,tag) in i:
        data.append((tag,word.lower()))

    emission_FD = ConditionalFreqDist(data)
    self.emission_PD = ConditionalProbDist(emission_FD, lambda f:nltk.probability.LidstoneProbDist(f,0.01,f.B()+1))
    self.states = list(set([tag for (tag,word) in data]))
    print "states: ",self.states,"\n\n"
    #states:  [u'.', u'ADJ', u'ADP', u'ADV', u'CONJ', u'DET', u'NOUN', u'NUM', u'PRON', u'PRT', u'VERB', u'X']

    return self.emission_PD, self.states

  #test point 1a
  def test_emission(self):
    print "test emission"
    t1 = log(self.emission_PD['NOUN'].prob('fulton')) #-7.47644570515
    t2 = log(self.emission_PD['X'].prob('fulton')) #-8.54286093816
    return t1,t2

  def transition_model(self,train_data):
    data = []
    print(train_data[0])
    for s in train_data:
      last = '<s>' # start sentance
      for (word, transition) in s:
        data.append((last, transition))
        last = transition
      data.append((last, '</s>')) # symbol for finishing sentance
    

    transition_FD = ConditionalFreqDist(data)
    self.transition_PD = ConditionalProbDist(transition_FD, lambda f:nltk.probability.LidstoneProbDist(f,0.01,f.B()+1))
 
    return self.transition_PD
  
  #test point 1b
  def test_transition(self):
    print "test transition"
    transition_PD = self.transition_model(self.train_data)
    start = log(transition_PD['<s>'].prob('NOUN')) #-1.23663567316
    end = log(transition_PD['NOUN'].prob('</s>')) #-5.06985925345
    return start,end

  #train the HMM model
  def train(self):
    self.emission_model(self.train_data)
    self.transition_model(self.train_data)
  
  def set_models(self,emission_PD,transition_PD):
    self.emission_PD = emission_PD
    self.transition_PD = transition_PD
  

  def initiatlize(self,observation):
    del self.viterbi[:]
    del self.backpointer[:]

    #initialize for transition from <s> , begining of sentence
    #use log-probabilities
    dic = {} # store the result in the pair (state:probability) in a dictionary
    #viterbi will be accessed as an array of dictionaries. A way to access them will be by "viterbi[0]['tag']".
    for state in self.states: # for all the possible tags
      # probability of going from state <s> to other states
      prob = log(self.emission_PD[state].prob(observation))+log(self.transition_PD['<s>'].prob(state))
      dic.update({state:prob})

    self.viterbi.append(dic)

    #initialize backpointer

    self.backpointer = [{}]
    for state in self.states:
      self.backpointer[0][state] = '<s>' # for this state, update to the best transition
  

  #input: list of words
  def tag(self,observations):
    tags = []
    index = 0
    current_decision = []
    
    # for all the observations
    for t in range(1,len(observations)):

      self.viterbi.append({}) # add a column to viterbi
      self.backpointer.append({}) #add a column to backpointer 

      # for all the states we could be in
      for state in self.states: 
         # for all states we could move to
        for trans_state in self.states:
          viterbi = self.viterbi[t-1][state]
          transition_prob = log(self.transition_PD[state].prob(trans_state))
          observation_prob = log(self.emission_PD[trans_state].prob(observations[t]))
          new_value = viterbi + transition_prob + observation_prob

          try: #it is possible the state hasn't been looked at before
            current_value = self.viterbi[t][trans_state]
          except:
            current_value = None

          # if the value is better than any before, update the viterbi
          if current_value == None or new_value > current_value:
            self.viterbi[t].update({trans_state:new_value})
            self.backpointer[t].update({trans_state:state})

    self.viterbi.append({'</s>':0}) # add the final state to viterbi
    self.backpointer.append({'</s>':None}) # add an empty backpointer
    index = len(self.viterbi) - 1 # define an index for the end

    for state in self.states:
      
      # the probability of the last word for a given tagging
      viterbi = self.viterbi[len(observations)-1][state]
      
      # the probability of a transition from the last tag to the end of a sentence
      transition_prob = log(self.transition_PD[state].prob('</s>'))
      
      # the score given to this transition
      new_value = viterbi + transition_prob

      # if no value exists, or if the new value is better than the current one
      if((self.viterbi[index]['</s>'] == 0) or (new_value > self.viterbi[index]['</s>'])):
        self.viterbi[index]['</s>'] = new_value # re-assign a best score
        self.backpointer[index]['</s>'] = state # assign a new backpointer

    last_pointer = '</s>' # last pointer

    self.backpointer.reverse() # reverse the list so we are following the pointer back 
    for word_pointer in self.backpointer: #for all the pointers
      last_pointer = word_pointer[last_pointer] # find the next pointer
      current_decision.append(last_pointer) #add it to the current decision, 

    #current decision contains the final set
    current_decision.reverse()
    
    tags = current_decision[1:] # we ignore the first symbol '<s>' which is the start of the sentance
    
    return tags 


def compare_taggers(train_data_Brown, train_data_Universal,test_data_Brown,test_data_Universal):


  tagger_Brown = HiddenMarkovModelTagger.train(train_data_Brown)
  tagger_Universal = HiddenMarkovModelTagger.train(train_data_Universal)
  

  eval_Brown = tagger_Brown.evaluate(test_data_Brown)
  eval_Universal = tagger_Universal.evaluate(test_data_Universal)
  
  answer1 = "Brown and Universal are training the same data size. Considering the brown tagset is larger than the universal tagset, they both train the same data size. As a result, universal produces more well trained set than the brown tagset, eventhough the increase in the states. Universal tagset contains more transitions and tags per possible state which creates a better observation set compares to the brown set."

  answer2 = "..."


  return eval_Brown, eval_Universal, answer1, answer2



def main():
  #devide corpus in train and test data
  tagged_sentences_Brown = brown.tagged_sents(categories= 'news')

  test_size = 1000
  train_size = len(tagged_sentences_Brown)-1000

  train_data_Brown = tagged_sentences_Brown[:train_size]
  test_data_Brown = tagged_sentences_Brown[-test_size:]

  tagged_sentences_Universal = brown.tagged_sents(categories= 'news', tagset='universal')
  train_data_Universal = tagged_sentences_Universal[:train_size]
  test_data_Universal = tagged_sentences_Universal[-test_size:]


  #create instance of HMM class and initialize the training and test sets
  obj = HMM(train_data_Universal,test_data_Universal)
  
  #train HMM
  obj.train()
  
  #part A: test emission model
  t1,t2 = obj.test_emission()
  print t1,t2 #-7.47644570515 -8.54286093816    ### updated
  if(abs(t1+7.476)<0.02 and abs(t2+8.543) < 0.02):  ### updated
    print "PASSED test emission\n"
  else:
    print "FAILED test emission\n"
  
  #part A: test transition model
  start,end = obj.test_transition()
  print start,end #-1.23663567316 -5.06985925345
  if(abs(start+1.23)<0.02 and abs(end+5.06) < 0.02):
    print "PASSED test transition\n"
  else:
    print "FAILED test transition\n"


  #part B: test accuracy on test set
  result = []
  correct = 0
  incorrect = 0
  accuracy = 0
  for sentence in test_data_Universal:
    s = [word.lower() for (word,tag) in sentence]
    obj.initiatlize(s[0])
    tags = obj.tag(s)
    for i in range(0,len(sentence)):
      if sentence[i][1] == tags[i]:
        correct+=1
      else:
        incorrect+=1
  accuracy = 1.0*correct/(correct+incorrect)
  print "accuracy: ",accuracy #accuracy:  0.857186331623
  if(abs(accuracy-0.857)<0.02): ### updated
    print "PASSED test viterbi\n"
  else:
    print "FAILED test viterbi\n"

  #test part C
  eval_Brown, eval_Universal,answer1,answer2 = compare_taggers(train_data_Brown,train_data_Universal,test_data_Brown,test_data_Universal)
  print "compare: ",eval_Brown, eval_Universal #compare: 0.844926528128 0.885488218416 (different from the above because HiddenMarkovModelTagger and HMM use slightly different smoothing)
  if(abs(eval_Brown-0.845)<0.02 and abs(eval_Universal-0.885) < 0.02):  ### updated
    print "PASSED test compare\n"
  else:
    print "FAILED test compare\n"

  print "Answer1: ",answer1, "\n"
  print "Answer2: ",answer2, "\n"

if __name__ == '__main__':
  
  main()

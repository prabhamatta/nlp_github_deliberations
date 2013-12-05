# I explored using the part of speech tagger to generate lists of positive, neutral, and negative words from
# the training set.
# 
# I implemeted and tested the following features:
# 1. # of positive/negative/neutral adjectives and verbs
# 2. Presense of positive/negative/neutral adjectives, verbs, and adverbs
# 3. Presense of positive/negative/neutral adjectives and verbs using Porter Stemmer
# 
# My team's agreed upon format for features was a dictionary with the feature name and the value.

# Loads in all of the parsed training set files into one list, randomizes it and assigns 90% to a training set and remaining to test set.


import nltk
import random
import string
from nltk.corpus import stopwords
import pickle
import os

files = os.listdir("../Vanessa/")
all_files = [f for f in files if f[-2:] == '.p']
all_reviews = []

for f in all_files:
    parsed_reviews = pickle.load( open( f, "rb" ) )
    for i in parsed_reviews.items():
        all_reviews.append(i)

random.shuffle(all_reviews)
training_reviews = all_reviews[:3215]
test_reviews = all_reviews[3215:]
#print len(test_reviews)

# Function that generates lists of adjectives, verbs, and adverbs from a list of reviews and splits them into neutral, positive, and negative categories.
# We called this a seed list.
# Originally I tried removing stop words, but this messed up nltk's part of speech tagger.
# I also lower case all of the words and remove punctuation. Note that this does create some non-words like "isnt","ive"


def get_seed_list(reviews):
    neutral_adj = []
    pos_adj = []
    neg_adj = []
    neutral_vrb = []
    pos_vrb = []
    neg_vrb = []
    neutral_advrb = []
    pos_advrb = []
    neg_advrb = []
    #stopwords = nltk.corpus.stopwords.words('english')
    
    for sent,label in reviews:
        clean_sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
        #clean_sent_no_sw = [w for w in clean_sent if w not in stopwords]     ##Removing stop words before tagging does not work.
        tagged = nltk.pos_tag(clean_sent)
        if label == 'neutral':
            for i,j in tagged:
                if j[0] == 'J':
                    neutral_adj.append(i)
                if j[0] == 'V':
                    neutral_vrb.append(i)
                #if j[0:2] == 'RB':
                    #neutral_advrb.append(i)
        if label == 'pos':
            for i,j in tagged:
                if j[0] == 'J':
                    pos_adj.append(i)
                if j[0] == 'V':
                    pos_vrb.append(i)
                #if j[0:2] == 'RB':
                    #pos_advrb.append(i)
        if label == 'neg':
            for i,j in tagged:
                if j[0] == 'J':
                    neg_adj.append(i)
                if j[0] == 'V':
                    neg_vrb.append(i)
                #if j[0:2] == 'RB':
                    #neg_advrb.append(i)

    return [neutral_adj, neutral_vrb, neutral_advrb, pos_adj, pos_vrb, pos_advrb, neg_adj, neg_vrb, neg_advrb]
    
seed_words = get_seed_list(training_reviews)


# Get definitions from tagger
#nltk.help.upenn_tagset()

# Set the seed lists
neutral_top_adj = nltk.FreqDist(seed_words[0]).keys()
pos_top_adj = nltk.FreqDist(seed_words[3]).keys()
neg_top_adj = nltk.FreqDist(seed_words[6]).keys()

neutral_top_vrb = nltk.FreqDist(seed_words[1]).keys()
pos_top_vrb = nltk.FreqDist(seed_words[4]).keys()
neg_top_vrb = nltk.FreqDist(seed_words[7]).keys()

#neutral_top_advrb = nltk.FreqDist(seed_words[2]).keys()
#pos_top_advrb = nltk.FreqDist(seed_words[5]).keys()
#neg_top_advrb = nltk.FreqDist(seed_words[8]).keys()

#len(neutral_top_vrb)

# Testing on adjectives


def features(sent):
    sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
    features = {}
    for word in pos_top_adj:
        features["has %s" % word] = word in sent
    #for word in neg_top_adj:
        #features["has %s" % word] = word in sent
    for word in neutral_top_adj:
        features["has %s" % word] = word in sent
    return features

#train_set = [(features(s), r) for (s,r) in training_reviews]
#devtest_set = [(features(s), r) for (s,r) in test_reviews]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, devtest_set)

#classifier.show_most_informative_features(5)

# *Presence of a pos/neg/neu adj of any kind using top_adj sets:*
# only pos: .5630
# only neg: .5266
# only neu: .5434
# both pos and neg: .55182
# all three: .5686
# both neg and neu: .5378
# **both pos and neu: .5714**
# 
# *Presence of pos/neg/neu adverb*
# Only pos: .5266
# Only neg: .5238
# **only neu: .5462**
# pos and neg: .5238
# pos and neu: .5434
# **neg and neu: .5462**
# all: .5434
# 
# #Just using subset of pos/neg/neu adj:
# #First 100: top pos and neu: .56022


# Initial error analysis using adjectives and adverbs reveals that many sents just don't have adjectives. 
# Most common mistake on training data is guessin neutral when the sent is positive.


# Error analysis
errors = []
for (sent, review) in test_reviews:
    guess = classifier.classify(features(sent))
    if guess != review:
        errors.append( (review, guess, sent) )

#for (review, guess, sent) in sorted(errors): 
    #print 'correct=%-8s guess=%-8s sent=%-30s' % (review, guess, sent)

#Testing on verbs

def features(sent):
    sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
    features = {}
    for word in pos_top_vrb:
        features["has %s" % word] = word in sent
    for word in neg_top_vrb:
        features["has %s" % word] = word in sent
    for word in neutral_top_vrb:
        features["has %s" % word] = word in sent
    for word in pos_top_adj:
        features["has %s" % word] = word in sent
    for word in neutral_top_adj:
        features["has %s" % word] = word in sent
    for word in neg_top_adj:
        features["has %s" % word] = word in sent
    return features

#train_set = [(features(s), r) for (s,r) in training_reviews]
#devtest_set = [(features(s), r) for (s,r) in test_reviews]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, devtest_set)


# *Presence of a pos/neg/neu verbs:*
# only pos: .5546
# only neg: .5882
# only neu: .5910
# both pos and neg: .5742
# **both pos and neu: .5966**
# both neg and neu: .5826
# all: .5882
# 
# using both top features??
# both pos/neu verbs and pos/neu adj: .5938
# **both pos and neu verbs and all adj: .5999**
# all verbs and all adjectives: .5994


# I played around with the counts of adjectives and verbs. Did not produce better results.

#Testing based on count of verbs

"""
def features(sent):
    sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
    features = {}
    features["pos adj count"] = 0
    features["neg adj count"] = 0
    features["neu adj count"] = 0
    features["pos vrb count"] = 0
    features["neg vrb count"] = 0
    features["neu vrb count"] = 0    
    for word in pos_top_adj:
        features["pos adj count"] += sent.count(word)
    for word in neg_top_adj:
        features["neg adj count"] += sent.count(word)        
    for word in neutral_top_adj:
        features["neu adj count"] += sent.count(word)
    for word in pos_top_vrb:
        features["pos vrb count"] += sent.count(word)
    #for word in neg_top_vrb:
        #features["neg vrb count"] += sent.count(word)        
    for word in neutral_top_vrb:
        features["neu vrb count"] += sent.count(word)
        
    
    return features


train_set = [(features(s), r) for (s,r) in training_reviews]
devtest_set = [(features(s), r) for (s,r) in test_reviews]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, devtest_set)

"""


# Trying a stemmer for verbs and adjectives
def get_seed_list_stemming(reviews):
    porter = nltk.PorterStemmer()
    neutral_adj = []
    pos_adj = []
    neg_adj = []
    neutral_vrb = []
    pos_vrb = []
    neg_vrb = []
    #stopwords = nltk.corpus.stopwords.words('english')
    
    for sent,label in reviews:
        clean_sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
        #clean_sent_no_sw = [w for w in clean_sent if w not in stopwords]     ##Removing stop words before tagging does not work.
        tagged = nltk.pos_tag(clean_sent)
        if label == 'neutral':
            for i,j in tagged:
                if j[0] == 'J':
                    neutral_adj.append(porter.stem(i))
                if j[0] == 'V':
                    neutral_vrb.append(porter.stem(i))
        if label == 'pos':
            for i,j in tagged:
                if j[0] == 'J':
                    pos_adj.append(porter.stem(i))
                if j[0] == 'V':
                    pos_vrb.append(porter.stem(i))
        if label == 'neg':
            for i,j in tagged:
                if j[0] == 'J':
                    neg_adj.append(porter.stem(i))
                if j[0] == 'V':
                    neg_vrb.append(porter.stem(i))

    return [neutral_adj, neutral_vrb, pos_adj, pos_vrb, neg_adj, neg_vrb]
    
seed_words = get_seed_list_stemming(training_reviews)


neutral_top_adj_s = nltk.FreqDist(seed_words[0]).keys()
pos_top_adj_s = nltk.FreqDist(seed_words[2]).keys()
neg_top_adj_s = nltk.FreqDist(seed_words[4]).keys()

neutral_top_vrb_s = nltk.FreqDist(seed_words[1]).keys()
pos_top_vrb_s = nltk.FreqDist(seed_words[3]).keys()
neg_top_vrb_s = nltk.FreqDist(seed_words[5]).keys()



#Testing with stemming verbs

def features(sent):
    porter = nltk.PorterStemmer()
    sent = sent.translate(string.maketrans("",""), string.punctuation).lower().strip().split()
    sent_stem = [porter.stem(t) for t in sent]
    features = {}
    for word in pos_top_vrb_s:
        features["has %s" % word] = word in sent_stem
    #for word in neg_top_vrb_s:
        #features["has %s" % word] = word in sent_setm
    for word in neutral_top_vrb_s:
        features["has %s" % word] = word in sent_stem
    for word in pos_top_adj_s:
        features["has %s" % word] = word in sent_stem
    for word in neutral_top_adj_s:
        features["has %s" % word] = word in sent_stem
    #for word in neg_top_adj:
        #features["has %s" % word] = word in sent_stem
    return features

#train_set = [(features(s), r) for (s,r) in training_reviews]
#devtest_set = [(features(s), r) for (s,r) in test_reviews]
#classifier = nltk.NaiveBayesClassifier.train(train_set)
#print nltk.classify.accuracy(classifier, devtest_set)

# *Presence of a pos/neg/neu verbs and adjectives after stemming using Porter Stemmer*
# both pos and neu verbs: .5994
# **both pos and neu verbs and pos/neu adj: .6218**
# 
# going to use these features to test on the held out set.


# Run on held out set


files = os.listdir("../Vanessa/Heldout")
all_files = [f for f in files if f[-2:] == '.p']
all_reviews_heldout = []

for f in all_files:
    parsed_reviews = pickle.load( open( "../Vanessa/Heldout/" + f, "rb" ) )
    for i in parsed_reviews.items():
        all_reviews_heldout.append(i)

random.shuffle(all_reviews_heldout)

train_set = [(features(s), r) for (s,r) in all_reviews]
test_set = [(features(s), r) for (s,r) in all_reviews_heldout]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)


# Classifier accuracy on hold out set: .6439


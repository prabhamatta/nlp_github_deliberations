# NPS_Chat corpus has been labeled with dialogue acts. There are 10,567 tagged chat conversations and tags are:
# 
# Emotion
# ynQuestion
# yAnswer
# Continuer
# whQuestion
# System
# Accept
# Clarify
# Emphasis
# nAnswer
# Greet
# Statement
# Reject
# Bye
# Other
# 
# 
# The general idea is to build and test a classifier for chats and then apply this classifier to our github diliberations comment corpus to determine if there is a relationship between comment type and participation in future dicussions.
# 
# We have decided to try this instead of manually labeling 
# 
# 1. Create test, training, and a held out set for the corpus. 
# 2. Build naive bayes classifier from nps_chat corpus
# 3. Classify conversations from the github comments
# 
# ------------------------------------------------------------------------
# Ideas for features:
# 
# from Charles paper (http://www.collide.info/sites/default/files/Christopher_Charles_Masterarbeit.pdf)
# - the first 2 words as a bigram
# - the last token
# - whether there is a question mark at the end
# - whether there is an exclamation mark at the end
# - whether the post's first few tokens contain a token from a list deemed positive ("yes","alright","sure","cool")
# - whether the post's first few tokens contain a token from a list deemed negative ("no", "not", "aint", "dont")

import nltk
from nltk import corpus


# There are 10,567 tagged chat conversations in the NPS_chat corpus.
# The tags include:
# emotion, ynQuestion, yAnswer, Continuer, whQuestion, System, Accept, Clarify, Emphasis, nAnswer, Greet, Statement, reject, bye, other


len(nltk.corpus.nps_chat.xml_posts())


posts = nltk.corpus.nps_chat.xml_posts()[:10000]


#Look at examples of the tags.
#Found that most of the sentences are short and mainly 'chat-speark'

for i in posts[0:100]:
    if i.get("class") == "Emotion":
        print i.text, i.get("class")


# Simple feature extractor for unigrams
def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
        
    return features


# Testing out the classifier. It is .67 accurate
featuresets = [(dialogue_act_features(post.text), post.get('class'))
                        for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)


#Importing comments file and concatenating comments that go to multiple lines
#This uses the old version of the commenting file.
import re

f = open('/issues_conversation_details_all.tsv', 'r')
comments = []
last_good_line = 0
counter = 0
for line in f.readlines():
    if re.match('^\d+\t\d+\th', line):
        last_good_line = counter
        comments.append(line.split("\t"))
        counter += 1
        
    if not re.match('^\d+\t\d+\th', line):
        comments.append(line)
        comments[last_good_line][4] += line
        counter += 1
f.close()


clean_comments = []
for i in comments:
    if isinstance(i, list):
        i[4] = i[4].replace('\n',' ')
        i[4] = i[4].replace('\t','    ')
        clean_comments.append(i)


for i in clean_comments:
    if i[1] == '28045983':
        print i


# Classify using the simple unigram classifier
f = open('classifier_output.tsv','w')
for comment in clean_comments:
    f.write(comment[0] + "\t "+ comment[1] + "\t" + comment[4][0:300].replace('\n',' ') + '\t' + classifier.classify(dialogue_act_features(comment[4])) + '\n')
f.close()


# Generate file for our own labeling
f = open('label2.tsv','w')
for comment in clean_comments:
    if comment[3] != "BitcoinPullTester":
            f.write(comment[0] + "\t "+ comment[1] + "\t" + comment[4][0:300].replace('\n',' ') + '\n')
f.close()
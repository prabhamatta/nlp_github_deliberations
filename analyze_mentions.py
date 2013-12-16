__author__ = 'prabha'

import sys
import re,codecs,string
from datetime import datetime
import time
from pprint import pprint
import nltk
import string
import json
from analyze_conversations import *

"""
Similar to its use on other social media websites, the @username syntax is used when a user wants to direct a comment at a particular user. 

Over 16% of the total comments in Bitcoin Project are direct one-to-one comments ie., the  3392 comments out of total 21050 issue comments have @mentions of users referred in the comments. We analyzed these mentioned comments from different perspectives to analyze contributors dynamics in the project during one-to-one conversations.

"""
def clean_user(user):
    if user[-1] in string.punctuation:
        user = user[:-1]
    if user[-2:] == "\'s":
        user = user[:-2]    
    return user


def get_users_who_mentioned(mention_conversations):
    """    
       get the freq distribution of users who mentioned
    """    
    users_who_mentioned =[]
    for line in mention_conversations:
        line_split = line.strip().split("\t")
        user = line_split[4]
        users_who_mentioned.append(user)
    fq = nltk.FreqDist(users_who_mentioned)
    for k,v in fq.items():
        print str(k)+"\t"+str(v)
        
def get_top_mentioned_users(mention_conversations):
    """    
       get_top_mentioned_users(mention_conversations)
    """    
    mentioned_users_list =[]
    for line in mention_conversations:
        line_split = line.strip().split("\t")
        date = time.strptime(line_split[2][:10], "%Y-%m-%d")
        user = line_split[4]
        mentioned_user = clean_user(line_split[5].lower())
        comment = line_split[6]
        mentioned_users_list.append(mentioned_user)
    fq = nltk.FreqDist(mentioned_users_list)
    for k,v in fq.items():
        print str(k)+"\t"+str(v)

        
def get_mentioned_by_core(mention_conversations, core):
    """
    get users mentioned by  core colloborators
    """     
    mentioned_users_list =[]
    for line in mention_conversations:
        line_split = line.strip().split("\t")
        user = clean_user(line_split[4].lower())
        if user in core:
            mentioned_user = clean_user(line_split[5].lower())
            mentioned_users_list.append(mentioned_user)
    fq = nltk.FreqDist(mentioned_users_list)
    for k,v in fq.items():
        print str(k)+"\t"+str(v)

  
def mentions_nonmentions_stats(users_comments):  
    
    mention_comments, nonmention_comments = [], []
        
    for time_comment in users_comments.values():
        for time, comment in time_comment:
            if len([word for word in nltk.tokenize.word_tokenize(comment) if word.startswith('@')])>0:
                mention_comments.append(comment)
            else:
                nonmention_comments.append(comment)
       
    stat_features = {}    
    comment_list = [mention_comments, nonmention_comments]
    stat_features['words per Comment'] = [getWordsPerComment(commentlist) for commentlist in comment_list]
    stat_features['Sentences per Comment'] = [getSentPerComment(commentlist) for commentlist in comment_list]
    stat_features['@Mentions'] =[getMentions(commentlist) for commentlist in comment_list]
    stat_features['% words >= 5 char'] = [getPercentWords5CharMore(commentlist) for commentlist in comment_list]
    stat_features['Ques tags per Comment'] =[getWhQuestionCount(commentlist) for commentlist in comment_list]
    
    stat_features['I'] = [getI(commentlist) for commentlist in comment_list]
    stat_features['We'] = [getWe(commentlist) for commentlist in comment_list]
    stat_features['You'] = [getYou(commentlist) for commentlist in comment_list]
    
    stat_features['Smileys'] = [getSmileys(commentlist) for commentlist in comment_list]

    stat_features['Positive Emotion'] = [getPosWordCount(commentlist) for commentlist in comment_list]
    stat_features['Negative Emotion'] = [getNegWordCount(commentlist) for commentlist in comment_list]
    
    print "Feature\t Mentions  \t Non-mentions\n"
    for k, v in stat_features.items():
        print k+"\t"+str(v[0])+"\t"+str(v[1])  
    print "\n"
    
    f_write = open("mention_nonmentions.json", 'w')
    f_write.write(json.dumps(stat_features))
    f_write.close()    
    
  
if __name__ == '__main__':
    mention_conversations = codecs.open("mentions_conversation_details_all.tsv", 'r',  "UTF-8") 
    get_users_who_mentioned(mention_conversations)

    
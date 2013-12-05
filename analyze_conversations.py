__author__ = 'github_deliberations'

import sys
import re,codecs,string
from datetime import datetime
import time
from pprint import pprint
import nltk
import string

def clean_user(user):
    if user[-1] in string.punctuation:
        user = user[:-1]
    if user[-2:] == "\'s":
        user = user[:-2]    
    return user

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
                
        
    

if __name__ == '__main__':
    mention_conversations = codecs.open("mentions_conversation_details_all.tsv", 'r',  "UTF-8") 

    """
    get top mentioned users
    """    
    #get_top_mentioned_users(mention_conversations)
    
    """
    get users mentioned by  core colloborators
    """       
    #core = ["gavinandresen","gmaxwell","jgarzik", "laanwj", "sipa", "tcatm"]
    #get_mentioned_by_core(mention_conversations, core)
    #mention_conversations.close()
    
    
    ##"""
    #get top commented users
    #"""    
    ##get_top_commented_users(mention_conversations)  
    
    
  
__author__ = 'github_deliberations'
__Project__= 'GitHub Deliberations Data Extraction Module'

from urllib2 import urlopen
import json
import sys
import re,codecs,string
from datetime import datetime
import time
from pprint import pprint
import nltk



def mention_conversation_analyzation():
    print "Entered mention_conversation_analyzation..."

    mentions_conversation_details_all = codecs.open("mentions_conversation_details_all.tsv", 'w',  "UTF-8")     
    fnames = ["issues_conversation_details_all.tsv"]  
    for fname in fnames:
        with codecs.open(fname, 'r',  "UTF-8") as fin:
            mentions_conversation_details_all.write( "issue_id"+"\t"  +"comment_id"+"\t" +"created_at"+"\t"  +"comment_url"+"\t"+ "comment_user"+"\t" + "mentioned_user"+"\t" "comment_text" +"\n")
            for line in fin:
                try:
                    split_list  = line.strip().split("\t")
                    comment_text = split_list[5]
                    if "@" in comment_text:
                        mentioned_user = ""
                        split_comment = comment_text.split(' ')
                        for word in split_comment:
                            if word.startswith('@'):  
                                mentioned_user = word.replace("@","")
                                mentioned_user = mentioned_user.replace(":","") 

                                #print mentioned_user
                                if mentioned_user == "":
                                    break

                                issue_id = split_list[0]
                                comment_id = split_list[1]
                                created_at = split_list[2]
                                comment_url = split_list[3]
                                comment_user = split_list[4]

                                mentions_conversation_details_all.write( str(issue_id)+"\t"  +str(comment_id)+"\t"  + str(created_at) +"\t" +str(comment_url)+"\t"+ str(comment_user)+"\t" + str(mentioned_user)+"\t" +   str(comment_text) +"\n")


                    #issues_conversation_text.write(str(issue_id)+"\t"  +str(comment_id)+"\t" +str(comment_url)+"\t"+ str(comment_user)+"\t" + str(comment_text) +"\n")

                except Exception, e: 
                    from traceback import print_exc
                    print_exc()
                    print "Error : ", line
                    pass
    mentions_conversation_details_all.close()



if __name__ == '__main__':
    project = "bitcoin"
    repo = "bitcoin"
    
    main_url = "https://api.github.com/repos/"+ project+"/"+repo
    print main_url


    """
    get individual comments of each conversation of each issue
    """    
    mention_conversation_analyzation()


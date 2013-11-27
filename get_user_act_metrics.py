#!/usr/bin/python

import nltk
from nltk.corpus import stopwords
import codecs
import sys
import json
import time
import dateutil.parser
import datetime
import calendar

import github_kmeans

METRICS = ['user', 'commit_cnt', 'commit_add_cnt', 'commit_del_cnt', 'issue_open_cnt', 'issue_close_cnt', 'issue_comment_cnt', 'pull_open_cnt', 'pull_close_cnt', 'pull_comment_cnt']

gram_choice = 'u'
freq_gram_cnt = 100
en_stop_words = stopwords.words('english')

def get_contributor():
    contributors = []
    with codecs.open("contributors_summary.txt", 'r',  "UTF-8") as fin:
        for line in fin:
            contributors.append(line.split('\t')[0].strip())

    return contributors



def get_user_commit_num(user, begin, end):
    cnt = add_cnt = del_cnt = 0

    commit_json = open('contributors_all.json')
    commit_data = json.load(commit_json)
    commit_json.close()
    for contributor in commit_data:
        if contributor['author']['login'] == user:
            for week in contributor['weeks']:
                if week['w'] >= begin and week['w'] <= end:
                    cnt += week['c']
                    add_cnt += week['a']
                    del_cnt += week['d']

    return (cnt, add_cnt, del_cnt)

def get_user_pull(user, begin, end, state):
    pull_cnt = 0
    fname = "pulls_all_" + state + '.tsv'
    with codecs.open(fname, 'r',  "UTF-8") as fin:
        for line in fin:
            pull_state = line.split('\t')[1].strip()
            pull_user = line.split('\t')[2].strip()
            if state == "open": # created_at
                date_time_obj = dateutil.parser.parse(line.split('\t')[6].strip())
            else: # closed_at
                date_time_obj = dateutil.parser.parse(line.split('\t')[7].strip())
            date_time = calendar.timegm(date_time_obj.utctimetuple())

            if pull_state == state and pull_user == user and date_time >= begin and date_time <= end:
                pull_cnt += 1

    return pull_cnt

def get_user_issue(user, begin, end, state):
    issue_cnt = 0
    fname = "issues_all_" + state + '.tsv'
    with codecs.open(fname, 'r',  "UTF-8") as fin:
        for line in fin:
            issue_state = line.split('\t')[1].strip()
            issue_user = line.split('\t')[2].strip()
            date_time_obj = dateutil.parser.parse(line.split('\t')[7].strip()) #grouping users based on created_at date
            #if state == "open": # created_at
                #date_time_obj = dateutil.parser.parse(line.split('\t')[7].strip())
            #else: # closed_at
                #date_time_obj = dateutil.parser.parse(line.split('\t')[8].strip())
            date_time = calendar.timegm(date_time_obj.utctimetuple())

            if issue_state == state and issue_user == user and date_time >= begin and date_time <= end:
                issue_cnt += 1

    return issue_cnt

def get_user_comment_cnt(user, begin, end, comment_type):
    fname = comment_type + "s_conversation_details_all.tsv"
    comment_cnt = 0
    with codecs.open(fname, 'r',  "UTF-8") as fin:
        for line in fin:
            comment_user = line.split('\t')[4].strip()
            # TODO: no timestamp for comments yet
            if comment_user == user:
                comment_cnt += 1

        return comment_cnt

def get_comments():
    comments = []
    fnames = ['unlabeled_comments.tsv']
    for fname in fnames:
        with codecs.open(fname, 'r',  "UTF-8") as fin:
            for line in fin:
                comments.append(line.split('\t')[2].strip())

    return comments



def count_act_metrics(user, begin, end):
    user_act_metrics = {}
    user_act_metrics['user'] = user
    # TODO: no commit comment yet
    user_act_metrics['commit_comment_cnt'] = 0


    user_act_metrics['pull_comment_cnt'] = get_user_comment_cnt(user, begin, end, "pull")
    user_act_metrics['pull_open_cnt'] = get_user_pull(user, begin, end, "open")
    user_act_metrics['pull_close_cnt'] = get_user_pull(user, begin, end, "closed")
    #print user_act_metrics['pull_comment_cnt'], user_act_metrics['pull_open_cnt'], user_act_metrics['pull_close_cnt']

    user_act_metrics['issue_comment_cnt'] = get_user_comment_cnt(user, begin, end, "issue")
    user_act_metrics['issue_open_cnt'] = get_user_issue(user, begin, end, "open")
    user_act_metrics['issue_close_cnt'] = get_user_issue(user, begin, end, "closed")
    #print user_act_metrics['issue_comment_cnt'], user_act_metrics['issue_open_cnt'], user_act_metrics['issue_close_cnt']

    (user_act_metrics['commit_cnt'], user_act_metrics['commit_add_cnt'], user_act_metrics['commit_del_cnt']) = get_user_commit_num(user, begin, end)
    #print user_act_metrics['commit_cnt'], user_act_metrics['commit_add_cnt'], user_act_metrics['commit_del_cnt']

    return user_act_metrics


def get_freq_unigram(comments, get_stem=False, get_tag=False, flt_stop_words=True):
    unigrams = []

    for comment in comments:
        words = nltk.word_tokenize(comment)

        if get_tag:
            for word, tag in nltk.pos_tag(words):
                if tag.startswith('V') or tag == 'ADJ' or tag == 'ADV':
                    if get_stem:
                        unigrams.append(stemmer.stem(word))
                    else:
                        unigrams.append(word)
        elif get_stem:
            for word in words:
                unigrams.append(stemmer.stem(word))
        else:
            unigrams.extend(words)

    if flt_stop_words:
        stop_words = en_stop_words
    else:
        stop_words = []

    return nltk.FreqDist(w.lower() for w in unigrams if w.isalpha() and w not in stop_words).keys()[:freq_gram_cnt]



def get_freq_bigram(comments, get_stem=False, get_tag=False, flt_stop_words=False):
    bigrams = []

    if flt_stop_words:
        stop_words = en_stop_words
    else:
        stop_words = []

    for comment in comments:
        sent = []
        words = nltk.word_tokenize(comment)

        if get_tag:
            for word, tag in nltk.pos_tag(words):
                if tag.startswith('V') or tag == 'ADJ' or tag == 'ADV':
                    if get_stem:
                        sent.append(stemmer.stem(word))
                    else:
                        sent.append(word)
        elif get_stem:
            for word in words:
                sent.append(stemmer.stem(word))
        else:
            sent.extend(words) 

        bigrams.extend(nltk.bigrams(w.lower() for w in sent if w.isalpha() and w not in en_stop_words))

    return nltk.FreqDist(bigrams).keys()[:freq_gram_cnt]

def print_user_activity_metric():
    # get all contributors
    contributors = get_contributor()
    # print out the metrics in first line
    first = True
    for metric in METRICS:
        if first:
            print metric,
            first = False
        else:
            print '\t' + metric,
    print

    #print out the metric value for each user
    for contributor in contributors:
        contributor_metrics = count_act_metrics(contributor, 0, time.time())
        first = True
        for metric in METRICS:
            if first:
                print str(contributor_metrics[metric]),
                first = False
            else:
                print '\t' + str(contributor_metrics[metric]),
        print


def get_model(all_contributor_metrics,metric_name, metric_list, metric_place):
    """ Finding 4 groups using k_means clustering algorithm"""
    print " Model: ", metric_name
    model_file = codecs.open("model_"+metric_name+".tsv", 'w',  "UTF-8") 
    try:
        status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(metric_list,4)
        if status == "error":
            print "Error in: ",metric_name
        else:
            centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            for user,metrics in all_contributor_metrics.items():
                for num, cluster in enumerate(centroids_clusters):
                    metric_val = int(metrics[metric_place])            
                    if int(metric_val) in cluster[1]:
                        if num==0:
                            model_file.write(user+ str(metric_val)+"\t"+ "low")
                        elif num==1:
                            model_file.write(user+  str(metric_val)+ "\t"+ "medium")
                        elif num==2:
                            model_file.write(user+  str(metric_val)+ "\t"+ "high")
                        elif num==3:
                            model_file.write(user+  str(metric_val)+ "\t"+ "very_high")  

                        model_file.write("\n")
    except Exception, e:        
        print "Error in: ",metric_name
        print  e      
    model_file.close()  

def print_classifier_group_model():
    # print out the 5 activity classification groups value for each user
    all_contributor_metrics = {}
    list_commit_cnt = []
    list_commit_add_del = []
    list_issue_open_close = []
    list_issue_comment_cnt = []
    list_pull_open_close = []

    with codecs.open("user_activity_metric.tsv", 'r',  "UTF-8") as fin:
        fin.readline() #ignore first line
        for line in fin:
            line_split = line.strip().split("\t")
            
            commit_cnt = int(line_split[1])
            list_commit_cnt.append(commit_cnt)
            
            commit_add_del= int(line_split[2]) + int(line_split[3])
            list_commit_add_del.append(commit_add_del)
            
            issue_open_close = int(line_split[4]) + int(line_split[5])
            list_issue_open_close.append(issue_open_close)
            
            issue_comment_cnt = int(line_split[6])
            list_issue_comment_cnt.append(issue_comment_cnt)
            
            pull_open_close = int(line_split[7]) + int(line_split[8])
            list_pull_open_close.append(pull_open_close)
            all_contributor_metrics[line_split[0]] = [commit_cnt,commit_add_del,issue_open_close,issue_comment_cnt,pull_open_close]
            

    #print  list_commit_cnt,list_commit_add_del, list_issue_open_close , list_issue_comment_cnt , list_pull_open_close 

    #midpt = len(list_commit_cnt)/2
    #median_commit_cnt = sorted(list_commit_cnt)[midpt]
    #median_commit_add_del = sorted(list_commit_add_del)[midpt]
    #median_issue_open_close = sorted(list_issue_open_close)[midpt]
    #median_issue_comment_cnt = sorted(list_issue_comment_cnt)[midpt]
    #median_pull_open_close = sorted(list_pull_open_close)[midpt]
    print  all_contributor_metrics
    get_model(all_contributor_metrics,"commit_cnt", list_commit_cnt, 0)
    get_model(all_contributor_metrics,"commit_add_del", list_commit_add_del, 1)
    get_model(all_contributor_metrics,"issue_open_close", list_issue_open_close, 2)
    get_model(all_contributor_metrics,"issue_comment_cnt", list_issue_comment_cnt, 3)
    get_model(all_contributor_metrics,"pull_open_close", list_pull_open_close, 4)





    #""" Model 2: commit_add_del"""    
    #print " Model 2: commit_add_del"
    #model_commit_cnt = codecs.open("model_commit_add_del.tsv", 'w',  "UTF-8") 
    #try:
        #status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(list_commit_add_del,4)
        #if status == "error":
            #print "ERROR in commit_add_del"
        #else:
            #centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            #for user,metrics in all_contributor_metrics.items():
                #for num, cluster in enumerate(centroids_clusters):
                    #metric_val = int(metrics[1])
                    #if int(metric_val) in cluster[1]:
                        #if num==0:
                            #model_commit_cnt.write(user+ str(metric_val)+"\t"+ "low")
                        #elif num==1:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "medium")
                        #elif num==2:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "high")
                        #elif num==3:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "very_high")  

                        #model_commit_cnt.write("\n")
    #except Exception, e:        
        #print "Error in: commit_add_del"
        #print  e      
    #model_commit_cnt.close()

    #""" Model 3: issue_open_close"""    
    #print " Model 3: issue_open_close"
    #model_commit_cnt = codecs.open("model_issue_open_close.tsv", 'w',  "UTF-8") 
    #try:
        #status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(list_issue_open_close,4)
        #if status == "error":
            #print "ERROR in issue_open_close"
        #else:
            #centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            #for user,metrics in all_contributor_metrics.items():
                #for num, cluster in enumerate(centroids_clusters):
                    #metric_val = int(metrics[2])
                    #if int(metric_val) in cluster[1]:
                        #if num==0:
                            #model_commit_cnt.write(user+ str(metric_val)+"\t"+ "low")
                        #elif num==1:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "medium")
                        #elif num==2:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "high")
                        #elif num==3:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "very_high")  

                        #model_commit_cnt.write("\n")
    #except Exception, e:        
        #print "Error in: issue_open_close"
        #print  e      
    #model_commit_cnt.close()

    #""" Model 4: issue_comment_cnt """    
    #print " Model 4: issue_comment_cnt "
    #model_commit_cnt = codecs.open("model_issue_comment_cnt .tsv", 'w',  "UTF-8") 
    #try:
        #status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(list_issue_comment_cnt ,4)
        #if status == "error":
            #print "ERROR in issue_comment_cnt "
        #else:
            #centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            #for user,metrics in all_contributor_metrics.items():
                #for num, cluster in enumerate(centroids_clusters):
                    #metric_val = int(metrics[3])
                    #if int(metric_val) in cluster[1]:
                        #if num==0:
                            #model_commit_cnt.write(user+ str(metric_val)+"\t"+ "low")
                        #elif num==1:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "medium")
                        #elif num==2:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "high")
                        #elif num==3:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "very_high")  

                        #model_commit_cnt.write("\n")
    #except Exception, e:        
        #print "Error in: issue_comment_cnt "
        #print  e      
    #model_commit_cnt.close() 

    #""" Model 5: pull_open_close """    
    #print " Model 5: pull_open_close "
    #model_commit_cnt = codecs.open("model_pull_open_close .tsv", 'w',  "UTF-8") 
    #try:
        #status, final_centroids, final_clusters = github_kmeans.find_centroids_clusters(list_pull_open_close ,4)
        #if status == "error":
            #print "ERROR in pull_open_close "
        #else:
            #centroids_clusters = sorted(zip(final_centroids, final_clusters))        
            #for user,metrics in all_contributor_metrics.items():
                #for num, cluster in enumerate(centroids_clusters):
                    #metric_val = int(metrics[4])
                    #if int(metric_val) in cluster[1]:
                        #if num==0:
                            #model_commit_cnt.write(user+ str(metric_val)+"\t"+ "low")
                        #elif num==1:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "medium")
                        #elif num==2:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "high")
                        #elif num==3:
                            #model_commit_cnt.write(user+  str(metric_val)+ "\t"+ "very_high")  

                        #model_commit_cnt.write("\n")
    #except Exception, e:        
        #print "Error in: pull_open_close "
        #print  e      
    #model_commit_cnt.close()        

    #for classifier_grp in [list_commit_cnt,list_commit_add_del, list_issue_open_close , list_issue_comment_cnt , list_pull_open_close ]:
        #try:
            #centroids_clusters = github_kmeans.find_centroids_clusters(classifier_grp,4)
            #for centroidpt, finalcluster in centroids_clusters:
                    #print "Centroid: %s" % centroidpt
                    #print "Cluster contents: %r" % finalcluster 
        #except Exception, e:        
                #print "Error in: ",classifier_grp
                #print  e  



if __name__=='__main__':
    # if there are command line arguments, the first one will be 'gram_choice'
    # and the second one will be 'freq_gram_cnt'
    if len(sys.argv) > 1:
        gram_choice = sys.argv[1]
    if len(sys.argv) > 2:
        freq_gram_cnt = int(sys.argv[2])

    # get comments
    comments = get_comments()

    if gram_choice[0] == 'u':
        freq_unigram = get_freq_unigram(comments)
        for unigram in freq_unigram:
            print unigram
    elif gram_choice[0] == 'b':
        freq_bigram = get_freq_bigram(comments)
        for bigram in freq_bigram:
            print "({0}, {1})".format(bigram[0], bigram[1])
    elif gram_choice[0] == 'm':
        print_user_activity_metric()

    elif gram_choice[0] == 'g':
        print_classifier_group_model()



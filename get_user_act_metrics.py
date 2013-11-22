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
      if state == "open": # created_at
        date_time_obj = dateutil.parser.parse(line.split('\t')[7].strip())
      else: # closed_at
        date_time_obj = dateutil.parser.parse(line.split('\t')[8].strip())
      date_time = calendar.timegm(date_time_obj.utctimetuple())

      if issue_state == state and issue_user == user and date_time >= begin and date_time <= end:
        issue_cnt += 1

  return issue_cnt

def get_user_comment_cnt(user, begin, end, comment_type):
  fname = comment_type + "s_conversation_details_all.tsv"
  comment_cnt = 0
  with codecs.open(fname, 'r',  "UTF-8") as fin:
    for line in fin:
      comment_user = line.split('\t')[3].strip()
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

    # print out the metric value for each user
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



      

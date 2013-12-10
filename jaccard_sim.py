#!/usr/bin/python

import sys
import codecs
import dateutil.parser
import datetime
import calendar
import nltk

bucket_cnt = 11
comment_cnt = 30

def get_core_users():
  core_users = []
  fnames = ['core_collaborators_formatted.txt']
  for fname in fnames:
    with codecs.open(fname, 'r',  "UTF-8") as fin:
      for line in fin:
        core_users.append(line.split('\t')[0].strip())
  return core_users



def get_user_comments():
  comments = {}
  fnames = ['issues_conversation_details_all.tsv', 'pulls_conversation_details_all.tsv']
#  fnames = ['pulls_conversation_details_test.tsv']
  for fname in fnames:
    with codecs.open(fname, 'r',  "UTF-8") as fin:
      for line in fin:
        user = line.split('\t')[4].strip()
        comment = line.split('\t')[5].strip()
        date_time_obj = dateutil.parser.parse(line.split('\t')[2].strip())
        date_time = calendar.timegm(date_time_obj.utctimetuple())
        if user not in comments:
          comments[user] = []
        comments[user].append((date_time, comment))

  return comments

def get_word_bucket(user_comments):
  bucket = []

  # sort by time
  user_comments.sort(key=lambda tup: tup[0])
  bucket_size = len(user_comments) / bucket_cnt

  i = 0
  bucket_num = 0
  pre_word_set = set()
  cur_word_set = set()
  for comment in user_comments:
    words = nltk.word_tokenize(comment[1])
    for word in words:
      cur_word_set.add(word)
    i += 1

    if i % bucket_size == 0:
      bucket_num += 1
      if bucket_num < bucket_cnt:
        bucket.append(cur_word_set)
        cur_word_set = set()

  bucket.append(cur_word_set)
  return bucket



if __name__=='__main__':
  comments = get_user_comments()
  core_users = get_core_users()
  
  word_bucket = {}
  for user, tuples in comments.iteritems():
    if len(tuples) >= comment_cnt:
      word_bucket[user] = get_word_bucket(tuples)

  total_bucket = []
  core_bucket = []
  normal_bucket = []
  for i in range(0, bucket_cnt):
    total_bucket.append(set())
    core_bucket.append(set())
    normal_bucket.append(set())

  print "Individuals:"
  for user, bucket in word_bucket.iteritems():
    sys.stdout.write(user)
    for i in range(1, bucket_cnt):
      score = len(bucket[i-1].intersection(bucket[i])) / float(len(bucket[i-1].union(bucket[i])))
      sys.stdout.write('\t')
      sys.stdout.write(str(score))
      total_bucket[i-1] = total_bucket[i-1].union(bucket[i-1])
      if user in core_users:
        core_bucket[i-1] = core_bucket[i-1].union(bucket[i-1])
      else:
        normal_bucket[i-1] = normal_bucket[i-1].union(bucket[i-1])
    print
    total_bucket[bucket_cnt-1] = total_bucket[bucket_cnt-1].union(bucket[bucket_cnt-1])
    if user in core_users:
      core_bucket[bucket_cnt-1] = core_bucket[bucket_cnt-1].union(bucket[bucket_cnt-1])
    else:
      normal_bucket[bucket_cnt-1] = normal_bucket[bucket_cnt-1].union(bucket[bucket_cnt-1])

  print "All:"
  sys.stdout.write("All")
  for i in range(1, bucket_cnt):
    score = len(total_bucket[i-1].intersection(total_bucket[i])) / float(len(total_bucket[i-1].union(total_bucket[i])))
    sys.stdout.write('\t')
    sys.stdout.write(str(score))
  print

  print "Core:"
  sys.stdout.write("Core_Users")
  for i in range(1, bucket_cnt):
    score = len(core_bucket[i-1].intersection(core_bucket[i])) / float(len(core_bucket[i-1].union(core_bucket[i])))
    sys.stdout.write('\t')
    sys.stdout.write(str(score))
  print

  print "Normal:"
  sys.stdout.write("Normal_Users")
  for i in range(1, bucket_cnt):
    score = len(normal_bucket[i-1].intersection(normal_bucket[i])) / float(len(normal_bucket[i-1].union(normal_bucket[i])))
    sys.stdout.write('\t')
    sys.stdout.write(str(score))
  print

#!/usr/bin/python

import nltk
from features import getUsersComments, getMentionsUsersComments, getUnusualWordCount, getPosWordCount, getNegWordCount, getTotalPunctuation, getWhQuestionCount, getTotalWordsUsed, getAvgWordLength, getAvgNumWordsInComment, getAvgNumWordsInSent, getAvgNumSentences, getMaxCommentLength, getAvgCommentLength, hasPlusOne, hasPosSmiley, hasNegSmiley
import codecs
import time

# 5 models
MODELS = ['commit_cnt', 'commit_add_del', 'issue_comment_cnt', 'issue_open_close', 'pull_open_close']

# users who have activities: 100
# users who have comments: 743

def get_activity_levels(begin, end):
  # TODO: now we just use the file already generated, without caring time period
  user_activity_levels = {}
  users = []
  for model in MODELS:
    with codecs.open("models/model_" + model + ".tsv", 'r',  "UTF-8") as fin:
      for line in fin:
        user = line.split('\t')[0].strip()
        level = line.split('\t')[2].strip()
        if user not in user_activity_levels:
          users.append(user)
          user_activity_levels[user] = {}
        user_activity_levels[user][model] = level

  return users, user_activity_levels

def get_user_comment_features(users, comments, begin, end, tag=''):
  # TODO: now we just use the file already generated, without caring time period
  user_comment_features = {}
  for user in users:
    if user not in comments:
      continue

    features = {}
    #features['unusual'] = getUnusualWordCount(comments[user]) //commented for now, since porter stemmer is taking too long time
    features[tag+'positive'] = getPosWordCount(comments[user])
    features[tag+'negative'] = getNegWordCount(comments[user])
    features[tag+'punctuation'] = getTotalPunctuation(comments[user])
    features[tag+'question'] = getWhQuestionCount(comments[user])
    features[tag+'wordused'] = getTotalWordsUsed(comments[user])
    features[tag+'wordlen'] = getAvgWordLength(comments[user])
    features[tag+'wordcomments'] = getAvgNumWordsInComment(comments[user])
    features[tag+'wordsentences'] = getAvgNumWordsInSent(comments[user])
    features[tag+'numsent'] = getAvgNumSentences(comments[user])
    features[tag+'maxcommentlen'] = getMaxCommentLength(comments[user])
    features[tag+'avgcommentlen'] = getAvgCommentLength(comments[user])
    
    features[tag+'hasPlusOne'] = hasPlusOne(comments[user])
    features[tag+'hasPosSmiley'] = hasPosSmiley(comments[user])
    features[tag+'hasNegSmiley'] = hasNegSmiley(comments[user])

    user_comment_features[user] = features
    #print user_comment_features

  return user_comment_features



if __name__=='__main__':
  begin = 0
  end = time.time()

  # get all user activity levels in a time period
  # level = user_activit
  users, user_activity_levels = get_activity_levels(begin, end)
  #print users
  #print user_activity_levels

  # get all comments in a time period (and group with users)
  # user_comment = comments[user]
  
  """collecting features from comments for the user"""  
  #f = open('issues_conversation_details_all.tsv','r')
  f = open('test_issues.tsv','r')
  
  comments = getUsersComments(f)
  #print comments

  # get all users' comment features
  # user_comment_features[user] = feature_dict
  user_comment_features = get_user_comment_features(users, comments, begin, end)
  #print user_comment_features


  """collecting features from mention conversations for the user"""
  #fmentions = open('mentions_conversation_details_all.tsv','r')
  fmentions = open('test_mentions.tsv','r')
  
  mention_comments = getMentionsUsersComments(fmentions)
  tag = 'mentions_'
  mention_user_comment_features = get_user_comment_features(users, mention_comments, begin, end,tag)
  #print mention_user_comment_features  
  for user, features in user_comment_features.items():
    try:
      features.update(mention_user_comment_features[user])
    except:
      pass
  #user_comment_features.update(mention_user_comment_features)



  classifier = {}
  for model in MODELS:
    # train_set format: [(feature_dict1, level1), (feature_dict2, level2), ...]
    train_set = []
    for user, features in user_comment_features.iteritems():
      train_set.append((features, user_activity_levels[user][model]))
    #print train_set

    # train the classifier of the model
    classifier[model] = nltk.NaiveBayesClassifier.train(train_set)
    print 'For Model "' + model + '", the most informative features are:'
    print classifier[model].show_most_informative_features(5)

    # test the model
    #print "Accuracy: ", nltk.classify.accuracy(classifier[model], heldout_set)


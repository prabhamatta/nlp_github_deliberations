#!/usr/bin/python

import nltk
import codecs
import sys
import json
import time
import dateutil.parser
import datetime
import calendar
import github_kmeans

METRICS = ['commit_cnt', 'commit_add_cnt', 'commit_del_cnt', 'issue_open_cnt', 'issue_close_cnt', 'issue_comment_cnt', 'pull_open_cnt', 'pull_close_cnt', 'pull_comment_cnt']
DATES = ['pull_open', 'pull_comment', 'pull_close', 'issue_comment', 'commit_del', 'commit', 'issue_close', 'commit_add', 'issue_open']

'''-----------------------Metrics Calculation Functions------------------------'''

def get_contributor():
    """ Returns list of contributors """
    contributors = []
    with codecs.open("contributors_summary.txt", 'r',  "UTF-8") as fin:
        for line in fin:
            contributors.append(line.split('\t')[0].strip())

    return contributors


def get_user_commit(user, begin='', end='', get_begin_date=False):
    """ Returns commit data (number of commits, number of additions and number
        of deletions) between begin and end date for the user.
        Dates are in UTC format
        If get_begin_date == True then returns first week of activity. """
    cnt = add_cnt = del_cnt = 0

    commit_json = open('contributors_all.json')
    commit_data = json.load(commit_json)
    commit_json.close()

    for contributor in commit_data:
        if contributor['author']['login'] == user:
            for week in contributor['weeks']:
                if get_begin_date:
                    if week['a'] > 0 or week['d'] > 0 or week['c'] > 0:   # if user has some activity return the first date. Might break if user has never committed.
                        return [ week['w'] ] * 3                          # just assuming that these three start dates are the same
                else:
                    if week['w'] >= begin and week['w'] <= end:
                        cnt += week['c']
                        add_cnt += week['a']
                        del_cnt += week['d']
            return (cnt, add_cnt, del_cnt)
    return [0,0,0]



def get_user_pull(user, state, begin='', end='', get_begin_date=False):
    """ Returns number of pull requests between begin and end date. State is 
        passed as a parameter and includes open and closed pull requests
        If get_begin_date == True, returns the begin date which is the last
        date looped through.   """
    begin_date = pull_cnt = 0
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

            if pull_state == state and pull_user == user:
                if get_begin_date:
                    begin_date = date_time
                elif date_time >= begin and date_time <= end:
                    pull_cnt += 1
    if get_begin_date:
        return begin_date
    else:
        return pull_cnt


def get_user_issue(user, state, begin='', end='', get_begin_date=False):
    """ Returns number of issues between begin and end date. State is passed 
        as a parameter and includes open and closed issues. 
        If get_begin_date == True, returns the begin date which is the last
        date looped through.  """
    begin_date = issue_cnt = 0
    fname = "issues_all_" + state + '.tsv'
    with codecs.open(fname, 'r',  "UTF-8") as fin:
        for line in fin:
            issue_state = line.split('\t')[1].strip()
            issue_user = line.split('\t')[2].strip()
            date_time_obj = dateutil.parser.parse(line.split('\t')[7].strip()) #grouping users based on created_at date
            date_time = calendar.timegm(date_time_obj.utctimetuple())
            if issue_state == state and issue_user == user:
                if get_begin_date:
                    begin_date = date_time
                elif date_time >= begin and date_time <= end:
                    issue_cnt += 1

    if get_begin_date:
        return begin_date
    else:
        return issue_cnt


def get_user_comment(user, comment_type, begin='', end='', get_begin_date=False):
    """ Returns number of comments for a user during begin and end date. 
        comment_type is a parameter and is either issue or pull.
        If get_begin_date == True, rturns the begin date which is the last 
        date looped through.  """
    fname = comment_type + "s_conversation_details_all.tsv"
    begin_date = comment_cnt = 0
    with codecs.open(fname, 'r',  "UTF-8") as fin:
        for line in fin:
            comment_user = line.split('\t')[4].strip()
            if comment_user == user:
                date_time_obj = dateutil.parser.parse(line.split('\t')[2].strip())
                date_time = calendar.timegm(date_time_obj.utctimetuple())
                begin_date = date_time
                if date_time >= begin and date_time <= end:
                    comment_cnt += 1
        if get_begin_date:
            return begin_date
        else:
            return comment_cnt


#print get_user_comment('Diapolo', "issue", get_begin_date=True)


'''--------------Functions for Aggregating User Metrics------------------'''


def get_activity_metrics(user, contributor_dates, interval):
    """ Returns dictionary of users activity metrics between begin and end dates as 
        specified in the contributor_dates dictionary:
        # of pull request comments, # of open pull requests, 
        # of closed pull requests, # of issue comments, # of open issues,
        # of closed issues, # of commits, # of additions and # of deletions. """
    time = 604800 * interval
    user_act_metrics = {}
    user_act_metrics['user'] = user
    
    # TODO: no commit comment yet
    # user_act_metrics['commit_comment_cnt'] = 0

    user_act_metrics['pull_comment_cnt'] = get_user_comment(user, "pull", contributor_dates['pull_comment']+time, contributor_dates['pull_comment']+2*time)
    user_act_metrics['pull_open_cnt'] = get_user_pull(user, "open", contributor_dates['pull_open'] + time, contributor_dates['pull_open'] + 2*time )
    user_act_metrics['pull_close_cnt'] = get_user_pull(user, "closed", contributor_dates['pull_close'] + time, contributor_dates['pull_close'] + 2*time)
    user_act_metrics['issue_comment_cnt'] = get_user_comment(user, "issue", contributor_dates['issue_comment'] + time, contributor_dates['issue_comment'] + 2*time)
    user_act_metrics['issue_open_cnt'] = get_user_issue(user, "open", contributor_dates['issue_open'] + time, contributor_dates['issue_open'] + 2*time)
    user_act_metrics['issue_close_cnt'] = get_user_issue(user, "closed", contributor_dates['issue_close'] + time, contributor_dates['issue_close'] + 2*time)
    (user_act_metrics['commit_cnt'], user_act_metrics['commit_add_cnt'], user_act_metrics['commit_del_cnt']) = get_user_commit(user, contributor_dates['commit'] + time, contributor_dates['commit'] + 2*time)
    
    return user_act_metrics


def get_activity_dates(user):
    """ Returns dictionary of users start dates for various metrics """
    user_begin_dates = {}
    (user_begin_dates['commit'], user_begin_dates['commit_add'], user_begin_dates['commit_del']) = get_user_commit(user, get_begin_date=True)
    user_begin_dates['pull_open'] = get_user_pull(user, "open", get_begin_date=True)
    user_begin_dates['pull_close'] = get_user_pull(user, "closed", get_begin_date=True)
    user_begin_dates['issue_open'] = get_user_issue(user, "open", get_begin_date=True)
    user_begin_dates['issue_close'] = get_user_issue(user, "closed", get_begin_date=True)
    user_begin_dates['pull_comment'] = get_user_comment(user, "pull", get_begin_date=True)
    user_begin_dates['issue_comment'] = get_user_comment(user, "issue", get_begin_date=True)

    return user_begin_dates


def print_users_activity():

    """TODO: need to figure out an interval that will make sense. """
    # get all contributors
    contributors = get_contributor()
    # print out the metrics in first line
    #contributors = ['Diapolo']
    print 'user',
    for metric in DATES + METRICS:
        print '\t' + metric,
    print


    #print out the metric value for each user
    for contributor in contributors:
        contributor_dates = get_activity_dates(contributor)
        contributor_metrics = get_activity_metrics(contributor, contributor_dates, 12)
        print contributor,
        for date in DATES:
            print '\t' + str(contributor_dates[date]),
        for metric in METRICS:
            print '\t' + str(contributor_metrics[metric]),
        print
       

print_users_activity()

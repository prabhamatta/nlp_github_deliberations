## Vanessa's file for implmenting analysis plan

import nltk
from nltk.corpus import stopwords
import codecs
import sys
import json
import time
import dateutil.parser
import datetime
import calendar



def get_first_commit_week(users_active_weeks):
    return users_active_weeks[0]   # return first week of activity

def get_user_active_weeks(user):
    """ Finds users active weeks """
    commit_json = open('contributors_all.json')
    commit_data = json.load(commit_json)
    commit_json.close()

    users_active_weeks = []
    
    for contributor in commit_data:
        if contributor['author']['login'] == user:
            for week in contributor['weeks']:
                if week['a'] > 0 or week['d'] > 0 or week['c'] > 0:
                    users_active_weeks.append(week['w'])
    return users_active_weeks


def is_user_still_active(users_active_weeks, date):
    if len([x for x in users_active_weeks if x > date]) > 0:
        return True
    else:
        return False


def get_users_comments(f, user, start_date, end_date):
    """ Creates dictionary where key is a username and the value
        is a list of the users comments. Filters out bot user
        BitcoinPullTester """
    users_comments = []
    for line in f.readlines():
        data = line.split('\t')
        current_user = data[4]
        
        if current_user == user:
            date_time_obj = dateutil.parser.parse(data[2][:10])
            comment_date = calendar.timegm(date_time_obj.utctimetuple())
        
            if comment_date >= start_date and comment_date <= end_date:
                users_comments.append(data[5])
    
    return users_comments


# Get active weeks for a given user
active_weeks = get_user_active_weeks('Diapolo')

# Find first commit week
#print get_first_commit_week(active_weeks)

# Is user still active after the specified date? 604800 seconds in a week.
time_interval = 12 * 604800 + get_first_commit_week(active_weeks)
#print is_user_still_active(active_weeks, time_interval)


f = open('issues_conversation_details_all.tsv','r')
comments = get_users_comments(f, 'Diapolo',1347753600,1384041600)

print len(comments)

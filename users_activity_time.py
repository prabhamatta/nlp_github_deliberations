## Scripts for finding information about user based on time

import json
import dateutil.parser
import datetime
import calendar


def get_user_active_weeks(user):
    """ Finds users active weeks. Currently only looking at commit counts for activity level
        TODO: add activity from pulls/issues. """
    commit_json = open('contributors_all.json')
    commit_data = json.load(commit_json)
    commit_json.close()
    users_active_weeks = []
    
    for contributor in commit_data:
        if contributor['author']['login'] == user:
            for week in contributor['weeks']:
                if week['a'] > 0 or week['d'] > 0 or week['c'] > 0:   # if user has some activity add that week.
                    users_active_weeks.append(week['w'])
    return users_active_weeks


def get_first_commit_week(users_active_weeks):
    """ Returns first active week """
    return users_active_weeks[0]


def is_user_still_active(users_active_weeks, date):
    """ Returns True if user has activity after the provided date """
    if len([x for x in users_active_weeks if x > date]) > 0:
        return True
    else:
        return False


def get_users_comments(f, user, start_date, end_date):
    """ Finds users comments between specified start and end date. Returns list of comments """
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

'''--------------------Demo of this code-----------------'''

# Get active weeks for a given user
active_weeks = get_user_active_weeks('Diapolo')

# Find first commit week
print "First active week is: " + str(get_first_commit_week(active_weeks))

# Is user still active after the specified date? 604800 seconds in a week.
time_interval = 12 * 604800 + get_first_commit_week(active_weeks)
print "User still active after 12 weeks? " + str(is_user_still_active(active_weeks, time_interval))

# Get users comments between specified dates
f = open('issues_conversation_details_all.tsv','r')
comments = get_users_comments(f, 'Diapolo', 1347753600,1384041600)

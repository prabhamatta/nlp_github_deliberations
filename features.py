"""For a given user and a given time period, read in all of the comments --> list
Write functions for each of the features we want to build. accepts a comment --> returns some metric

Current feature list:
Length of comments
outside links(?)
includes coode
contains @ mentions
question marks
punctuation
"""


'''------------------build dict of users comments-------------'''

def get_users_comments(f):
    """ Creates dictionary where key is a username and the value
        is a list of the users comments. Filters out bot user
        BitcoinPullTester """
    users_comments = {}

    for line in f.readlines():
        data = line.split('\t')
        user = data[3]
        if user != 'BitcoinPullTester':
            if user not in users_comments:
                comment_list = [data[4]]
                users_comments[user] = comment_list
            else:
                users_comments[user].append([data[4]])

    return users_comments





if __name__ == '__main__':
    f = open('issues_conversation_details_all.tsv','r')
    comments = get_users_comments(f)
    print comments.keys()







'''------------------feature functions------------------------'''



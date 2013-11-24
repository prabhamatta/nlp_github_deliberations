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


'''-----------------------build dict of users comments--_-------------------'''

def getUsersComments(f):
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


'''----------------------------feature functions----------------------------'''

def getAvgCommentLength(comment_list):
    pass

def getMaxCommentLength(comment_list):
    pass

def getAvgWordsUsed(comment_list):
    pass

def getTotalWordsUsed(comment_list):
    pass

def getWhQuestionCount(comment_list):
    pass

def getTotalPunctuation(comment_list):
    pass

def getNumAtMentions(comment_list):
    pass

def getMostUsedWords(comment_list):
    pass

def getPositiveWordCount(comment_list):
    pass

def getNegativeWordCount(comment_list):
    pass


'''-----------------------------helper functions----------------------------'''



if __name__ == '__main__':
    f = open('issues_conversation_details_all.tsv','r')
    comments = getUsersComments(f)











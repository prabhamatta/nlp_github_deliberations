## functions for extracting features from users comments

import nltk
import nltk.data


'''-----------------------build dict of users comments----------------------'''

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
                users_comments[user].append(data[4])
    return users_comments


'''----------------------------feature functions----------------------------'''

def getAvgCommentLength(comment_list):
    """ Get average length (char) of a users comments """
    total = sum([len(comment) for comment in comment_list])
    return float(total) / len(comment_list)


def getMaxCommentLength(comment_list):
    """ Get length of longest comment from a user """
    return max([len(comment) for comment in comment_list])


def getAvgNumSentences(comment_list):
    """ Gets average number of sentences in a users comment """
    sent_list = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for comment in comment_list:
        sent_list.append(sent_detector.tokenize(comment.strip()))
    return float(sum([len(x) for x in sent_list])) / len(comment_list)


def getAvgNumWordsInSent(comment_list):
    """ Gets the average number of words in a users sentences """
    sent_list = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for comment in comment_list:
        sent_list.append(sent_detector.tokenize(comment.strip()))
    sum_words = 0
    for comment in sent_list:
        for sent in comment:
            sum_words += len(sent.split(" "))
    sum_sent = sum([len(x) for x in sent_list])
    return float(sum_words) / sum_sent
       

def getAvgNumWordsInComment(comment_list):
    pass


def getAvgWordLength(comment_list):
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

    testuser = 'mikehearn'
    print "avg num words in users sentences: " + str(getAvgNumWordsInSent(comments[testuser]))
    print "avg num sentences per comment: " + str(getAvgNumSentences(comments[testuser]))
    print "max comment length: " + str(getMaxCommentLength(comments[testuser]))
    print "average comment length: " + str(getAvgCommentLength(comments[testuser]))
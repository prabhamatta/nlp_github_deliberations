## functions for extracting features from users comments

import nltk
import nltk.data
import string

'''-----------------------build dict of users comments----------------------'''

def getUsersComments(f):
    """ Creates dictionary where key is a username and the value
        is a list of the users comments. Filters out bot user
        BitcoinPullTester """
    users_comments = {}
    for line in f.readlines():
        data = line.split('\t')
        user = data[4]
        if user != 'BitcoinPullTester':
            if user not in users_comments:
                comment_list = [data[5]]
                users_comments[user] = comment_list
            else:
                users_comments[user].append(data[5])
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
    """ Gets average number of words in a users comment.
        NOTE: currently includes punctuation words like '...' """
    word_sum = sum([ len([word for word in nltk.tokenize.word_tokenize(comment_list_item)
               if word not in string.punctuation]) for comment_list_item in comment_list ])
    return float(word_sum) / len(comment_list)


def getAvgWordLength(comment_list):
    """ Gets users average word length.
        NOTE: currently includes punctuation words """
    char_sum = 0
    num_words = 0
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation]:
            num_words += 1
            char_sum += len(word)
    return float(char_sum) / num_words
    

def getTotalWordsUsed(comment_list):
    """ Gets total number of words the user has used.
        NOTE: currenly includes punctuation words """
    num_words = 0
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation]:
            num_words += 1
    return num_words

def getWhQuestionCount(comment_list):
    """ Returns number of whQuestion words used in all comments """
    num_wh = 0
    whQuestionWords = ['who','what','when','where','why', 'how']
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in whQuestionWords]:
            num_wh += 1
    return num_wh

    
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

def getNumUniqueWords(comment_list):
    pass

'''---------------------------add helper functions--------------------------'''


if __name__ == '__main__':
    f = open('issues_conversation_details_all.tsv','r')
    comments = getUsersComments(f)
    testuser = 'mikehearn'

    #print getWhQuestionCount(comments[testuser])
    
     #Uncomment to run all
    print "total number of whQuestion words in users comments: " + str(getWhQuestionCount(comments[testuser]))
    print "total number of words used: " + str(getTotalWordsUsed(comments[testuser]))
    print "avg word length: " + str(getAvgWordLength(comments[testuser]))
    print "avg num words in users comments: " + str(getAvgNumWordsInComment(comments[testuser]))
    print "avg num words in users sentences: " + str(getAvgNumWordsInSent(comments[testuser]))
    print "avg num sentences per comment: " + str(getAvgNumSentences(comments[testuser]))
    print "max comment length: " + str(getMaxCommentLength(comments[testuser]))
    print "average comment length: " + str(getAvgCommentLength(comments[testuser]))
    
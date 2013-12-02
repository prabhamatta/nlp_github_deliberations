#   functions for extracting features from users comments
#
#   Still to do:
#   Remaining notes:
#   1. Do not have time information in conversation detail page yet
#   2. Could explore stats about users first response.
#   3. create helper functions for reused code.


import nltk
import nltk.data
import string
import re

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
    """ Gets count of the punctuation used by the user """
    num_punct = 0
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word[0] in string.punctuation]:
            num_punct += 1
    return num_punct


def getMostFreqWords(comment_list, num_words):
    """ returns list of num_words most frequently used words for a user
        NOTE still gets some punctuation words..."""
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')
    word_list = []
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation]:
            if eachword[-1] in string.punctuation and eachword[-1] not in stopwords:
                word_list.append(eachword[:-1].lower())
            elif eachword not in stopwords:
                word_list.append(eachword.lower())
    return nltk.FreqDist(word_list).keys()[0:num_words]
    

def getPosWordCount(comment_list):
    """ returns number of positive words used in all of users comments
        words are from http://www.enchantedlearning.com/wordlist/positivewords.shtml """
    words = getWordTokens(comment_list)
    return len([word.lower() for word in words if word.lower() in posWords])

def getNegWordCount(comment_list):
    """ returns number of negative words used in all of users comments
        words are from http://www.enchantedlearning.com/wordlist/negativewords.shtml """
    words = getWordTokens(comment_list)
    return len([word for word in words if word.lower() in negWords])

def getFreqNegWords(comment_list, num_words):
    """ returns list of top num_words most frequent negative words used in comments
        words are from http://www.enchantedlearning.com/wordlist/negativewords.shtml """
    words = getWordTokens(comment_list)
    return nltk.FreqDist([word.lower() for word in words if word.lower() in negWords]).keys()[:num_words]

def getFreqPosWords(comment_list, num_words):
    """ returns list of top num_words most frequent positive words used in comments
        words are from http://www.enchantedlearning.com/wordlist/positivewords.shtml """
    words = getWordTokens(comment_list)
    return nltk.FreqDist([word.lower() for word in words if word.lower() in posWords]).keys()[:num_words]

def getUnusualWordCount(comment_list):
    """ Gets number of 'unusual' words used in comments. A word is considered unusual if its stem does
        not appear in the nltk word corpus. """
    words = getWordTokens(comment_list)
    porter = nltk.PorterStemmer()
    text_vocab = set(porter.stem(w.lower()) for w in words if w.isalpha())
    english_vocab = set(porter.stem(w.lower()) for w in nltk.corpus.words.words())
    unusual = text_vocab.difference(english_vocab)
    return len(unusual)



'''---------------------------add helper functions--------------------------'''
posWords = set(["absolutely", "adorable", "accepted", "acclaimed", "accomplish", "accomplishment", "achievement", "action", "active", "admire", "adventure", "affirmative", "affluent", "agree", "agreeable", "amazing", "angelic", "appealing", "approve", "aptitude", "attractive", "awesome", "beaming", "beautiful", "believe", "beneficial", "bliss", "bountiful", "bounty", "brave", "bravo", "brilliant", "bubbly", "calm", "celebrated", "certain", "champ", "champion", "charming", "cheery", "choice", "classic", "classical", "clean", "commend", "composed", "congratulation", "constant", "cool", "courageous", "creative", "cute", "dazzling", "delight", "delightful", "distinguished", "divine", "earnest", "easy", "ecstatic", "effective", "effervescent", "efficient", "effortless", "electrifying", "elegant", "enchanting", "encouraging", "endorsed", "energetic", "energized", "engaging", "enthusiastic", "essential", "esteemed", "ethical", "excellent", "exciting", "exquisite", "fabulous", "fair", "familiar", "famous", "fantastic", "favorable", "fetching", "fine", "fitting", "flourishing", "fortunate", "free", "fresh", "friendly", "fun", "funny", "generous", "genius", "genuine", "giving", "glamorous", "glowing", "good", "gorgeous", "graceful", "great", "green", "grin", "growing", "handsome", "happy", "harmonious", "healing", "healthy", "hearty", "heavenly", "honest", "honorable", "honored", "hug", "idea", "ideal", "imaginative", "imagine", "impressive", "independent", "innovate", "innovative", "instant", "instantaneous", "instinctive", "intuitive", "intellectual", "intelligent", "inventive", "jovial", "joy", "jubilant", "keen", "kind", "knowing", "knowledgeable", "laugh", "legendary", "light", "learned", "lively", "lovely", "lucid", "lucky", "luminous", "marvelous", "masterful", "meaningful", "merit", "meritorious", "miraculous", "motivating", "moving", "natural", "nice", "novel", "now", "nurturing", "nutritious", "okay", "one", "one-hundred percent", "open", "optimistic", "paradise", "perfect", "phenomenal", "pleasurable", "plentiful", "pleasant", "poised", "polished", "popular", "positive", "powerful", "prepared", "pretty", "principled", "productive", "progress", "prominent", "protected", "proud", "quality", "quick", "quiet", "ready", "reassuring", "refined", "refreshing", "rejoice", "reliable", "remarkable", "resounding", "respected", "restored", "reward", "rewarding", "right", "robust", "safe", "satisfactory", "secure", "seemly", "simple", "skilled", "skillful", "smile", "soulful", "sparkling", "special", "spirited", "spiritual", "stirring", "stupendous", "stunning", "success", "successful", "sunny", "super", "superb", "supporting", "surprising", "terrific", "thorough", "thrilling", "thriving", "tops", "tranquil", "transforming", "transformative", "trusting", "truthful", "unreal", "unwavering", "up", "upbeat", "upright", "upstanding", "valued", "vibrant", "victorious", "victory", "vigorous", "virtuous", "vital", "vivacious", "wealthy", "welcome", "well", "whole", "wholesome", "willing", "wonderful", "wondrous", "worthy", "wow", "yes", "yummy", "zeal", "zealous"])

negWords = set(["abysmal", "adverse", "alarming", "angry", "annoy", "anxious", "apathy", "appalling", "atrocious", "awful", "bad", "banal", "barbed", "belligerent", "bemoan", "beneath", "boring", "broken", "callous", "can't", "clumsy", "coarse", "cold", "cold-hearted", "collapse", "confused", "contradictory", "contrary", "corrosive", "corrupt", "crazy", "creepy", "criminal", "cruel", "cry", "cutting", "dead", "decaying", "damage", "damaging", "dastardly", "deplorable", "depressed", "deprived", "deformed", "deny", "despicable", "detrimental", "dirty", "disease", "disgusting", "disheveled", "dishonest", "dishonorable", "dismal", "distress", "don\'t", "dreadful", "dreary", "enraged", "eroding", "evil", "fail", "faulty", "fear", "feeble", "fight", "filthy", "foul", "frighten", "frightful", "gawky", "ghastly", "grave", "greed", "grim", "grimace", "gross", "grotesque", "gruesome", "guilty", "haggard", "hard", "hard-hearted", "harmful", "hate", "hideous", "homely", "horrendous", "horrible", "hostile", "hurt", "hurtful", "icky", "ignore", "ignorant", "immature", "imperfect", "impossible", "inane", "inelegant", "infernal", "injure", "injurious", "insane", "insidious", "insipid", "jealous", "junky", "lose", "lousy", "lumpy", "malicious", "mean", "menacing", "messy", "misshapen", "missing", "misunderstood", "moan", "moldy", "monstrous", "naive", "nasty", "naughty", "negate", "negative", "never", "no", "nobody", "nondescript", "nonsense", "not", "noxious", "objectionable", "odious", "offensive", "old", "oppressive", "pain", "perturb", "pessimistic", "petty", "plain", "poisonous", "poor", "prejudice", "questionable", "quirky", "quit", "reject", "renege", "repellant", "reptilian", "repulsive", "repugnant", "revenge", "revolting", "rocky", "rotten", "rude", "ruthless", "sad", "savage", "scare", "scary", "scream", "severe", "shoddy", "shocking", "sick", "sickening", "sinister", "slimy", "smelly", "sobbing", "sorry", "spiteful", "sticky", "stinky", "stormy", "stressful", "stuck", "stupid", "substandard", "suspect", "suspicious", "tense", "terrible", "terrifying", "threatening", "ugly", "undermine", "unfair", "unfavorable", "unhappy", "unhealthy", "unjust", "unlucky", "unpleasant", "upset", "unsatisfactory", "unsightly", "untoward", "unwanted", "unwelcome", "unwholesome", "unwieldy", "unwise", "upset", "vice", "vicious", "vile", "villainous", "vindictive", "wary", "weary", "wicked", "woeful", "worthless", "wound", "yell", "yucky", "zero"])

def getWordTokens(comment_list):
    """ takes list of comments and returns a list of tokens including words and punctuation """
    all_comments = ''.join(comment_list)
    return [word for word in nltk.tokenize.word_tokenize(all_comments)]


def hasPlusOne(comment_list):
    """ Returns 1 if the comment has +1 in it"""
    val = 0
    for comment in comment_list:
        for word in nltk.tokenize.word_tokenize(comment):
            if word in ['+1']:
                val = 1
                return val
    return val

def hasPosSmiley(comment_list):
    """ Returns 1 if the comment has any positive smiley in it"""
    val = 0
    for comment in comment_list:
        for word in nltk.tokenize.word_tokenize(comment):
            if word in [';)',':)', ':D', ':-)', ';-)']:
                val = 1
                return val
    return val

def hasNegSmiley(comment_list):
    """ Returns 1 if the comment has any negative smiley in it"""
    val = 0
    for comment in comment_list:
        for word in nltk.tokenize.word_tokenize(comment):
            if word in [':-(', ':(']:
                val = 1
                return val
    return val








if __name__ == '__main__':
    f = open('issues_conversation_details_all.tsv','r')
    comments = getUsersComments(f)
    testuser = 'petertodd'

    print "total num of unusual words used: " + str(getUnusualWordCount(comments[testuser]))

     #Uncomment to run for test user.
    '''
    print "list of top %d most freq pos words: " % 10 + str(getFreqPosWords(comments[testuser],10))
    print "list of top %d most freq neg words: " % 10 + str(getFreqNegWords(comments[testuser],10))
    print "num positive words used: " + str(getPosWordCount(comments[testuser]))
    print "num negative words used: " + str(getNegWordCount(comments[testuser]))
    print "list of top %d words: " % 20 + str(getMostFreqWords(comments[testuser], 20))
    print "total num of punctuation used: " + str(getTotalPunctuation(comments[testuser]))
    print "total num of whQuestion words in users comments: " + str(getWhQuestionCount(comments[testuser]))
    print "total num of words used: " + str(getTotalWordsUsed(comments[testuser]))
    print "avg word length: " + str(getAvgWordLength(comments[testuser]))
    print "avg num words in users comments: " + str(getAvgNumWordsInComment(comments[testuser]))
    print "avg num words in users sentences: " + str(getAvgNumWordsInSent(comments[testuser]))
    print "avg num sentences per comment: " + str(getAvgNumSentences(comments[testuser]))
    print "max comment length: " + str(getMaxCommentLength(comments[testuser]))
    print "average comment length: " + str(getAvgCommentLength(comments[testuser]))
    '''

    # Analyzing most used negative words across all users.
    # all_neg_words = []
    # for user in comments:
    #     for word in getWordTokens(comments[user]):
    #         if word in negWords:
    #             all_neg_words.append(word)

    # print nltk.FreqDist(all_neg_words)

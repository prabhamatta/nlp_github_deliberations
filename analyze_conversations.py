__author__ = 'prabha'

import sys
import re,codecs,string
from datetime import datetime
import time
from pprint import pprint
import nltk
import string
import json

'''----------------------Stats regarding top mentioned users, core users, etc---------------------'''        
def clean_user(user):
    if user[-1] in string.punctuation:
        user = user[:-1]
    if user[-2:] == "\'s":
        user = user[:-2]    
    return user

def get_top_users_comments():
    """ get top users comment num in pull/issue converstaions"""
    
    files_tag = ["issues"]
    for tag in files_tag:
        f_read = codecs.open(tag+"_conversation_details_all.tsv", 'r',  "UTF-8")
        f_write = codecs.open("top_"+tag+"_comments_users.tsv", 'w',  "UTF-8") 
        users_list = []        
        for line in f_read:
            line_split = line.strip().split("\t")    
            user = clean_user(line_split[4].lower())
            users_list.append(user)
        fq = nltk.FreqDist(users_list)
        for k,v in fq.items():
            f_write.write(str(k)+"\t"+str(v)+"\n")
            print str(k)
        f_write.close()                
                

'''-----------------------features for analyzing new and all----------------------'''
    
def getWordCount(comment_list):
    """ Gets total number of words in the comment
    """
    num_words = 0.0
    for comment in comment_list:
        num_words += len([word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation])   
    return num_words

  
def getSentPerComment(comment_list):
    """ Gets avg number of sent per comemnt 
    """
    num_sent = 0.0
    for comment in comment_list:
        num_sent += len(comment.split("."))   
    return num_sent/len(comment_list)

        
def getWordsPerComment(comment_list):
    """ Gets avg number of words per comemnt 
    """
    num_words = 0.0
    for comment in comment_list:
        num_words += len([word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation])   
    return num_words/len(comment_list)

    
def getPercentWords5CharMore(comment_list):
    """ Gets percent of words with 5 char or more 
    """
    num_words = 0.0
    total_num_words = 0
    for comment in comment_list:
        for eachword in [word for word in nltk.tokenize.word_tokenize(comment) if word not in string.punctuation]:
            total_num_words += 1
            if len(eachword) >= 5:
                num_words += 1
    return num_words/total_num_words


def getMentions(comment_list):
    """ Gets percent of words with 5 char or more 
    """
    num_mentions = 0.0
    for comment in comment_list:
        if len([word for word in nltk.tokenize.word_tokenize(comment) if word.startswith('@')])>0:
            num_mentions += 1
    return num_mentions/len(comment_list)


def getWhQuestionCount(comment_list):
    """ Returns  number of whQuestion words per comments """
    num_wh = 0.0
    whQuestionWords = ['who','what','when','where','why', 'how']
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in whQuestionWords])
        num_wh += count
    return num_wh/len(comment_list)


def getI(comment_list):
    """ Returns  number of "I" per comment """
    num_I = 0.0
    i_words = ["i", "me", "mine", "myself"]
    
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in i_words])
        num_I += count
    return num_I/len(comment_list)



def getWe(comment_list):
    """ Returns  number of We's per comment """
    num_We = 0.0
    we_words = ["we", "us", "our", "ours"]
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in we_words])
        num_We += count
    return num_We/len(comment_list)


def getYou(comment_list):
    """ Returns  number of you's per comment """
    num_you = 0.0
    you_words = ["you", "your", "yours", "your's"]
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in you_words])
        num_you += count
    return num_you/len(comment_list)


def getSmileys(comment_list):
    """ Returns  number of you's per comment """
    num_smileys= 0.0
    smiley_words = [';)',':)', ':D', ':-)', ';-)']
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in smiley_words])
        num_smileys += count
    return num_smileys/len(comment_list)


def getPosWordCount(comment_list):
    """ returns number of positive words used in all of users comments
        words are from http://www.enchantedlearning.com/wordlist/positivewords.shtml """
    num_pos = 0.0
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in posWords]) 
        num_pos += count                  
    return num_pos/len(comment_list)


def getNegWordCount(comment_list):
    """ returns number of negative words used in all of users comments
        words are from http://www.enchantedlearning.com/wordlist/negativewords.shtml """
    num_neg = 0.0
    for comment in comment_list:
        count = len([word for word in nltk.tokenize.word_tokenize(comment) if word.lower() in negWords]) 
        num_neg += count    
    return num_neg/len(comment_list)


'''---------------------------add helper functions--------------------------'''
posWords = set(["absolutely", "adorable", "accepted", "acclaimed", "accomplish", "accomplishment", "achievement", "action", "active", "admire", "adventure", "affirmative", "affluent", "agree", "agreeable", "amazing", "angelic", "appealing", "approve", "aptitude", "attractive", "awesome", "beaming", "beautiful", "believe", "beneficial", "bliss", "bountiful", "bounty", "brave", "bravo", "brilliant", "bubbly", "calm", "celebrated", "certain", "champ", "champion", "charming", "cheery", "choice", "classic", "classical", "clean", "commend", "composed", "congratulation", "constant", "cool", "courageous", "creative", "cute", "dazzling", "delight", "delightful", "distinguished", "divine", "earnest", "easy", "ecstatic", "effective", "effervescent", "efficient", "effortless", "electrifying", "elegant", "enchanting", "encouraging", "endorsed", "energetic", "energized", "engaging", "enthusiastic", "essential", "esteemed", "ethical", "excellent", "exciting", "exquisite", "fabulous", "fair", "familiar", "famous", "fantastic", "favorable", "fetching", "fine", "fitting", "flourishing", "fortunate", "free", "fresh", "friendly", "fun", "funny", "generous", "genius", "genuine", "giving", "glamorous", "glowing", "good", "gorgeous", "graceful", "great", "green", "grin", "growing", "handsome", "happy", "harmonious", "healing", "healthy", "hearty", "heavenly", "honest", "honorable", "honored", "hug", "idea", "ideal", "imaginative", "imagine", "impressive", "independent", "innovate", "innovative", "instant", "instantaneous", "instinctive", "intuitive", "intellectual", "intelligent", "inventive", "jovial", "joy", "jubilant", "keen", "kind", "knowing", "knowledgeable", "laugh", "legendary", "light", "learned", "lively", "lovely", "lucid", "lucky", "luminous", "marvelous", "masterful", "meaningful", "merit", "meritorious", "miraculous", "motivating", "moving", "natural", "nice", "novel", "now", "nurturing", "nutritious", "okay", "one", "one-hundred percent", "open", "optimistic", "paradise", "perfect", "phenomenal", "pleasurable", "plentiful", "pleasant", "poised", "polished", "popular", "positive", "powerful", "prepared", "pretty", "principled", "productive", "progress", "prominent", "protected", "proud", "quality", "quick", "quiet", "ready", "reassuring", "refined", "refreshing", "rejoice", "reliable", "remarkable", "resounding", "respected", "restored", "reward", "rewarding", "right", "robust", "safe", "satisfactory", "secure", "seemly", "simple", "skilled", "skillful", "smile", "soulful", "sparkling", "special", "spirited", "spiritual", "stirring", "stupendous", "stunning", "success", "successful", "sunny", "super", "superb", "supporting", "surprising", "terrific", "thorough", "thrilling", "thriving", "tops", "tranquil", "transforming", "transformative", "trusting", "truthful", "unreal", "unwavering", "up", "upbeat", "upright", "upstanding", "valued", "vibrant", "victorious", "victory", "vigorous", "virtuous", "vital", "vivacious", "wealthy", "welcome", "well", "whole", "wholesome", "willing", "wonderful", "wondrous", "worthy", "wow", "yes", "yummy", "zeal", "zealous"])

negWords = set(["abysmal", "adverse", "alarming", "angry", "annoy", "anxious", "apathy", "appalling", "atrocious", "awful", "bad", "banal", "barbed", "belligerent", "bemoan", "beneath", "boring", "broken", "callous", "can't", "clumsy", "coarse", "cold", "cold-hearted", "collapse", "confused", "contradictory", "contrary", "corrosive", "corrupt", "crazy", "creepy", "criminal", "cruel", "cry", "cutting", "dead", "decaying", "damage", "damaging", "dastardly", "deplorable", "depressed", "deprived", "deformed", "deny", "despicable", "detrimental", "dirty", "disease", "disgusting", "disheveled", "dishonest", "dishonorable", "dismal", "distress", "don\'t", "dreadful", "dreary", "enraged", "eroding", "evil", "fail", "faulty", "fear", "feeble", "fight", "filthy", "foul", "frighten", "frightful", "gawky", "ghastly", "grave", "greed", "grim", "grimace", "gross", "grotesque", "gruesome", "guilty", "haggard", "hard", "hard-hearted", "harmful", "hate", "hideous", "homely", "horrendous", "horrible", "hostile", "hurt", "hurtful", "icky", "ignore", "ignorant", "immature", "imperfect", "impossible", "inane", "inelegant", "infernal", "injure", "injurious", "insane", "insidious", "insipid", "jealous", "junky", "lose", "lousy", "lumpy", "malicious", "mean", "menacing", "messy", "misshapen", "missing", "misunderstood", "moan", "moldy", "monstrous", "naive", "nasty", "naughty", "negate", "negative", "never", "no", "nobody", "nondescript", "nonsense", "not", "noxious", "objectionable", "odious", "offensive", "old", "oppressive", "pain", "perturb", "pessimistic", "petty", "plain", "poisonous", "poor", "prejudice", "questionable", "quirky", "quit", "reject", "renege", "repellant", "reptilian", "repulsive", "repugnant", "revenge", "revolting", "rocky", "rotten", "rude", "ruthless", "sad", "savage", "scare", "scary", "scream", "severe", "shoddy", "shocking", "sick", "sickening", "sinister", "slimy", "smelly", "sobbing", "sorry", "spiteful", "sticky", "stinky", "stormy", "stressful", "stuck", "stupid", "substandard", "suspect", "suspicious", "tense", "terrible", "terrifying", "threatening", "ugly", "undermine", "unfair", "unfavorable", "unhappy", "unhealthy", "unjust", "unlucky", "unpleasant", "upset", "unsatisfactory", "unsightly", "untoward", "unwanted", "unwelcome", "unwholesome", "unwieldy", "unwise", "upset", "vice", "vicious", "vile", "villainous", "vindictive", "wary", "weary", "wicked", "woeful", "worthless", "wound", "yell", "yucky", "zero"])



'''-----------------------Analyzing comments----------------------'''        

def get_users_comments():
    """ Creates dictionary where key is a username and the value
           is a list of the (timestamp,users comments). 
           Filters out bot user BitcoinPullTester """    
    users_comments = {}
    files_tag = ["issues"]
    for tag in files_tag:
        f_read = codecs.open(tag+"_conversation_details_all.tsv", 'r',  "UTF-8")
        users_list = []        
        for line in f_read:
            try:
                line_split = line.strip().split("\t")    
                user = clean_user(line_split[4].lower())
                userdate = time.strptime(line_split[2][:10], "%Y-%m-%d")
                comment = line_split[5]
                if user != 'BitcoinPullTester':
                    if user not in users_comments:
                        date_comment_list = [(time.mktime(userdate),comment)]
                        users_comments[user] = date_comment_list
                    else:
                        users_comments[user].append((time.mktime(userdate), comment)) 
            except:
                pass
        f_read.close()
    return users_comments


def get_newcomer_and_all_comments(users_comments):
    all_users_comments = [] 
    newcomer_comments = []
    for user in users_comments.keys():
        #print user
        sorted_comments = sorted(users_comments[user])
        all_users_comments += [comment[1] for comment in sorted_comments]
        num_of_comments = len(sorted_comments)
        newcomer_comments += [comment[1] for comment in sorted_comments[:(num_of_comments/3)]]
    return all_users_comments, newcomer_comments


def get_core_and_noncore_comments(users_comments):
    core = [] 
    noncore = []
    for user in users_comments.keys():
        #print user
        sorted_comments = sorted(users_comments[user])
        all_users_comments += [comment[1] for comment in sorted_comments]
        num_of_comments = len(sorted_comments)
        newcomer_comments += [comment[1] for comment in sorted_comments[:(num_of_comments/3)]]
    return all_users_comments, newcomer_comments

        
        
def newcomers_all_stats(users_comments):
    """............Newcomers Vs.All Comments Analysis Statistics........"""    
    users_comments_30 = {}
    for user,comments in users_comments.items():
        if len(comments)>=30:
            users_comments_30[user] = comments
            
    all_comments, newcomer_comments = get_newcomer_and_all_comments(users_comments_30)
    
    stat_features = {}    
    comment_list = [newcomer_comments,all_comments]    
    stat_features['words per Comment'] = [getWordsPerComment(commentlist) for commentlist in comment_list]
    stat_features['Sentences per Comment'] = [getSentPerComment(commentlist) for commentlist in comment_list]
    stat_features['@Mentions'] =[getMentions(commentlist) for commentlist in comment_list]
    stat_features['% words >= 5 char'] = [getPercentWords5CharMore(commentlist) for commentlist in comment_list]
    stat_features['Ques tags per Comment'] =[getWhQuestionCount(commentlist) for commentlist in comment_list]
    
    stat_features['I'] = [getI(commentlist) for commentlist in comment_list]
    stat_features['We'] = [getWe(commentlist) for commentlist in comment_list]
    stat_features['You'] = [getYou(commentlist) for commentlist in comment_list]
    
    stat_features['Smileys'] = [getSmileys(commentlist) for commentlist in comment_list]

    stat_features['Positive Emotion'] = [getPosWordCount(commentlist) for commentlist in comment_list]
    stat_features['Negative Emotion'] = [getNegWordCount(commentlist) for commentlist in comment_list]
    
    print "Feature\t Newcomers \t All-users\n"
    for k, v in stat_features.items():
        print k+"\t"+str(v[0])+"\t"+str(v[1])
    print "\n"
    
    f_write = open("newcomers_all.json", 'w')
    f_write.write(json.dumps(stat_features))
    f_write.close()
    
    
def project_stats(users_comments):
  
    """............project stats........"""
    all_comments, newcomer_comments = get_newcomer_and_all_comments(users_comments)    
    print "Num of Contributors = 153",
    print "Num of Commentators = ",len(users_comments.keys())
    print "Num of Comments = ",len(all_comments)  
    print "Users with more than 50 Comments =", len([user for user,comments in users_comments.items() if len(comments)>50])
    
    print "Average num of words per Comments =", getWordsPerComment(all_comments)
    print "Average num of sentences per Comments =", getSentPerComment(all_comments)    


def core_diapolo_noncore_stats(users_comments):
    core = ["gavinandresen","gmaxwell","jgarzik", "laanwj", "sipa", "tcatm"]
    
    
    core_comments, diapolo_comments, noncore_comments = [], [], []
    for user,comments in users_comments.items():
        if user in core:
            core_comments += [comment[1] for comment in comments]
        elif user == 'diapolo':
            diapolo_comments +=  [comment[1] for comment in comments]
        else:
            noncore_comments += [comment[1] for comment in comments]
            
    
    stat_features = {}    
    comment_list = [core_comments, diapolo_comments, noncore_comments]
    stat_features['words per Comment'] = [getWordsPerComment(commentlist) for commentlist in comment_list]
    stat_features['Sentences per Comment'] = [getSentPerComment(commentlist) for commentlist in comment_list]
    stat_features['@Mentions'] =[getMentions(commentlist) for commentlist in comment_list]
    stat_features['% words >= 5 char'] = [getPercentWords5CharMore(commentlist) for commentlist in comment_list]
    stat_features['Ques tags per Comment'] =[getWhQuestionCount(commentlist) for commentlist in comment_list]
    
    stat_features['I'] = [getI(commentlist) for commentlist in comment_list]
    stat_features['We'] = [getWe(commentlist) for commentlist in comment_list]
    stat_features['You'] = [getYou(commentlist) for commentlist in comment_list]
    
    stat_features['Smileys'] = [getSmileys(commentlist) for commentlist in comment_list]

    stat_features['Positive Emotion'] = [getPosWordCount(commentlist) for commentlist in comment_list]
    stat_features['Negative Emotion'] = [getNegWordCount(commentlist) for commentlist in comment_list]
    
    print "Feature\t Core collaborators \t diapolo \t Non-core\n"
    for k, v in stat_features.items():
        print k+"\t"+str(v[0])+"\t"+str(v[1]) +"\t"+str(v[2])    

    print "\n"
    
    f_write = open("core_diapolo_noncore.json", 'w')
    f_write.write(json.dumps(stat_features))
    f_write.close()



def core_noncore_stats(users_comments):
    core = ["gavinandresen","gmaxwell","jgarzik", "laanwj", "sipa", "tcatm"]
    
    
    core_comments, diapolo_comments, noncore_comments = [], [], []
    for user,comments in users_comments.items():
        if user in core:
            core_comments += [comment[1] for comment in comments]
        else:
            noncore_comments += [comment[1] for comment in comments]
            
    
    stat_features = {}    
    comment_list = [core_comments, noncore_comments]
    stat_features['words per Comment'] = [getWordsPerComment(commentlist) for commentlist in comment_list]
    stat_features['Sentences per Comment'] = [getSentPerComment(commentlist) for commentlist in comment_list]
    stat_features['@Mentions'] =[getMentions(commentlist) for commentlist in comment_list]
    stat_features['% words >= 5 char'] = [getPercentWords5CharMore(commentlist) for commentlist in comment_list]
    stat_features['Ques tags per Comment'] =[getWhQuestionCount(commentlist) for commentlist in comment_list]
    
    stat_features['I'] = [getI(commentlist) for commentlist in comment_list]
    stat_features['We'] = [getWe(commentlist) for commentlist in comment_list]
    stat_features['You'] = [getYou(commentlist) for commentlist in comment_list]
    
    stat_features['Smileys'] = [getSmileys(commentlist) for commentlist in comment_list]

    stat_features['Positive Emotion'] = [getPosWordCount(commentlist) for commentlist in comment_list]
    stat_features['Negative Emotion'] = [getNegWordCount(commentlist) for commentlist in comment_list]
    
    print "Feature\t Core collaborators\t Non-core\n"
    for k, v in stat_features.items():
        print k+"\t"+str(v[0])+"\t"+str(v[1])    
    f_write = open("core_noncore.json", 'w')
    f_write.write(json.dumps(stat_features))
    f_write.close()
    print "\n"

    
    
def mentions_nonmentions_stats(users_comments):  
    
    mention_comments, nonmention_comments = [], []
        
    for time_comment in users_comments.values():
        for time, comment in time_comment:
            if len([word for word in nltk.tokenize.word_tokenize(comment) if word.startswith('@')])>0:
                mention_comments.append(comment)
            else:
                nonmention_comments.append(comment)
       
    stat_features = {}    
    comment_list = [mention_comments, nonmention_comments]
    stat_features['words per Comment'] = [getWordsPerComment(commentlist) for commentlist in comment_list]
    stat_features['Sentences per Comment'] = [getSentPerComment(commentlist) for commentlist in comment_list]
    stat_features['@Mentions'] =[getMentions(commentlist) for commentlist in comment_list]
    stat_features['% words >= 5 char'] = [getPercentWords5CharMore(commentlist) for commentlist in comment_list]
    stat_features['Ques tags per Comment'] =[getWhQuestionCount(commentlist) for commentlist in comment_list]
    
    stat_features['I'] = [getI(commentlist) for commentlist in comment_list]
    stat_features['We'] = [getWe(commentlist) for commentlist in comment_list]
    stat_features['You'] = [getYou(commentlist) for commentlist in comment_list]
    
    stat_features['Smileys'] = [getSmileys(commentlist) for commentlist in comment_list]

    stat_features['Positive Emotion'] = [getPosWordCount(commentlist) for commentlist in comment_list]
    stat_features['Negative Emotion'] = [getNegWordCount(commentlist) for commentlist in comment_list]
    
    print "Feature\t Mentions  \t Non-mentions\n"
    for k, v in stat_features.items():
        print k+"\t"+str(v[0])+"\t"+str(v[1])  
    print "\n"
    
    f_write = open("mention_nonmentions.json", 'w')
    f_write.write(json.dumps(stat_features))
    f_write.close()    
    
def read_jsons():
    import json
    
    files = ["core_diapolo_noncore.json","core_noncore.json", "newcomers_all.json", "mention_nonmentions.json"]
    for f in files:
        f_read = codecs.open(f, 'r')
        fdict = json.loads(f_read.read())
        for k,v in fdict:
            print k+"\t"+ v
        
    
def main():
    users_comments = get_users_comments()
    
    #project_stats(users_comments)
    #newcomers_all_stats(users_comments)
    
    #core_noncore_stats(users_comments)
    core_diapolo_noncore_stats(users_comments)
    #mentions_nonmentions_stats(users_comments)

 

if __name__ == '__main__':
 
    #main()
    #read_jsons()
    #get_top_users_comments()
  
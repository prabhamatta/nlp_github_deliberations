import nltk
import dateutil.parser
import datetime
import calendar
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
import string


f = open("issues_conversation_details_all.tsv","r")

stopwords = stopwords.words("english")


# user_comments = {}
# for line in f.readlines():
# 	line_data = line.split("\t")
# 	user = line_data[4]
# 	comment = line_data[5]
# 	date = line_data[2]
# 	if user != 'BitcoinPullTester' and len(comment)>1:
# 		if user not in user_comments:
# 			user_comments[user] = [[comment, date]]#[0:200]]
# 		else:
# 			user_comments[user].append([comment, date])#[0:200])

# # Reverse list so first comment is at the beginning
# for k,v in user_comments.items():
# 	v.reverse()


def sort_comments():
	comments_by_date = []
	for line in f.readlines():
		line_data = line.split("\t")
		date_time_obj = dateutil.parser.parse(line_data[2])
		user = line_data[4]
		comment = line_data[5]
		if user != 'BitcoinPullTester' and len(comment) > 1:
			comments_by_date.append([date_time_obj, user, comment])

	comments_by_date.sort()
	return comments_by_date


def get_lexical_innovations(comments, known_words):
	seen_words ={}
	time_period = datetime.timedelta(-180)
	for post in comments:
		user = post[1]
		date_time_obj = post[0]
		comment = nltk.word_tokenize(post[2])
		cleaned_comment = [word.lower().strip(string.punctuation) for word in comment if word.lower().strip(string.punctuation) not in stopwords and word not in string.punctuation]
		for word in cleaned_comment:
			if word not in seen_words and word not in known_words:
				seen_words[word] = [[user, date_time_obj]]
			if word in seen_words:
				if user != seen_words[word][0][0] and seen_words[word][0][1] - date_time_obj > time_period:   #if the user is not the first user
						seen_words[word].append([user, date_time_obj])
		#print seen_words.items()[0:5]

	for k,v in seen_words.items():
		if k.isalpha():
			users = []
			for i in v:
				users.append(i[0])
			if len(set(users)) > 2:
				if len(v) > 10:
					print k + "\t" + "\t" + v[0][0]  + "\t" + str(v[0][1].year)  + "\t" + str(v[0][1].month)  + "\t" + str(len(v))

known_words = []

def get_known_words(months_comments):
	for post in months_comments:
		comment = nltk.word_tokenize(post[2])
		cleaned_comment = [word.lower().strip(string.punctuation) for word in comment if word.lower().strip(string.punctuation) not in stopwords and word not in string.punctuation]
		for word in cleaned_comment:
			if word != '':
				known_words.append(word)
	#return set(known_words)
		


def get_months_comments(month, year, comments_sorted):
	comments = []
	for i in comments_sorted:
		if i[0].month == month and i[0].year == year:
			comments.append(i)
	return comments


comments_sorted = sort_comments()
#months_comments =  get_months_comments(12,2010,comments_sorted)
#get_known_words(months_comments)
#get_lexical_innovations(comments_sorted, known_words)



def get_users_comments(comments):
	users_comments = {}
	for post in comments:
		user = post[1]
		#date_time_obj = post[0]
		comment = nltk.word_tokenize(post[2])
		cleaned_comment = [word.lower().strip(string.punctuation) for word in comment if word not in string.punctuation]
		if user not in users_comments:
			users_comments[user] = [cleaned_comment]
		elif user in users_comments:
			users_comments[user].append(cleaned_comment)
	return users_comments


def get_vocab_frequency(comments, word_list):
	frequency25 = []
	frequency50 = []
	frequency75 = []
	frequency100= []
	for user,comment_list in comments.items():
		if user in core_collabs:
			interval =  int(round(float(len(comment_list))/4))
			count = 0
			for i in comment_list[0:interval]:
				has_word = False
				for word in word_list:
					if word in i:
						has_word = True
				if has_word:
					count += 1
			if interval > 0:
				frequency25.append(float(count)/interval)
			count = 0
			for i in comment_list[interval:interval*2]:
				has_word = False
				for word in word_list:
					if word in i:
						has_word = True
				if has_word:
					count += 1
			if interval > 0:
				frequency50.append(float(count)/interval)
			count = 0
			for i in comment_list[interval*2:interval*3]:
				has_word = False
				for word in word_list:
					if word in i:
						has_word = True
				if has_word:
					count += 1
			if interval > 0:
				frequency75.append(float(count)/interval)
			count = 0
			for i in comment_list[interval*3:]:
				has_word = False
				for word in word_list:
					if word in i:
						has_word = True
				if has_word:
					count += 1
			if interval > 0:
				frequency100.append(float(count)/interval)

	print sum(frequency25)/len(frequency25)
	print sum(frequency50)/len(frequency50)
	print sum(frequency75)/len(frequency75)
	print sum(frequency100)/len(frequency100)


comments = get_users_comments(comments_sorted)

# Break each persons comments up into 4 chunks. count number of bitcoin vocabulary in each of these chunks.
# Get the length of the comments for comment ids that are 52 -->  0,12,25,51. Bins are 0-12, 13-25, 26-51


bitcoin_vocab = ["bitcoins", "bitcoin", "block", "coin", "coins", "blocks", "chains", "chain", "btc", "cryptography", "crypto", "security", "privacy", "mining", "p2p", "signature", "wallet", "wallets", "transaction", "xbt", "miner", "miners", "payment", "payments", "bitcoind", "transactions", "tumbler", "qt", "tumblers"]
first_personal_pronouns = ["i", "me", "myself", "mine", "my"]
first_plural_pronouns = ["we", "our", "ours", "us", "ourselves"]
second_pronouns = ["you", "your", "yours", "yourself", "yourselves"]
core_collabs = ["gavinandresen", "gmaxwell", "jgarzik", "laanwj", "sipa", "tcatm"]

whQuestionWords = ['who','what','when','where','why', 'how']
posWords = set(["absolutely", "adorable", "accepted", "acclaimed", "accomplish", "accomplishment", "achievement", "action", "active", "admire", "adventure", "affirmative", "affluent", "agree", "agreeable", "amazing", "angelic", "appealing", "approve", "aptitude", "attractive", "awesome", "beaming", "beautiful", "believe", "beneficial", "bliss", "bountiful", "bounty", "brave", "bravo", "brilliant", "bubbly", "calm", "celebrated", "certain", "champ", "champion", "charming", "cheery", "choice", "classic", "classical", "clean", "commend", "composed", "congratulation", "constant", "cool", "courageous", "creative", "cute", "dazzling", "delight", "delightful", "distinguished", "divine", "earnest", "easy", "ecstatic", "effective", "effervescent", "efficient", "effortless", "electrifying", "elegant", "enchanting", "encouraging", "endorsed", "energetic", "energized", "engaging", "enthusiastic", "essential", "esteemed", "ethical", "excellent", "exciting", "exquisite", "fabulous", "fair", "familiar", "famous", "fantastic", "favorable", "fetching", "fine", "fitting", "flourishing", "fortunate", "free", "fresh", "friendly", "fun", "funny", "generous", "genius", "genuine", "giving", "glamorous", "glowing", "good", "gorgeous", "graceful", "great", "green", "grin", "growing", "handsome", "happy", "harmonious", "healing", "healthy", "hearty", "heavenly", "honest", "honorable", "honored", "hug", "idea", "ideal", "imaginative", "imagine", "impressive", "independent", "innovate", "innovative", "instant", "instantaneous", "instinctive", "intuitive", "intellectual", "intelligent", "inventive", "jovial", "joy", "jubilant", "keen", "kind", "knowing", "knowledgeable", "laugh", "legendary", "light", "learned", "lively", "lovely", "lucid", "lucky", "luminous", "marvelous", "masterful", "meaningful", "merit", "meritorious", "miraculous", "motivating", "moving", "natural", "nice", "novel", "now", "nurturing", "nutritious", "okay", "one", "one-hundred percent", "open", "optimistic", "paradise", "perfect", "phenomenal", "pleasurable", "plentiful", "pleasant", "poised", "polished", "popular", "positive", "powerful", "prepared", "pretty", "principled", "productive", "progress", "prominent", "protected", "proud", "quality", "quick", "quiet", "ready", "reassuring", "refined", "refreshing", "rejoice", "reliable", "remarkable", "resounding", "respected", "restored", "reward", "rewarding", "right", "robust", "safe", "satisfactory", "secure", "seemly", "simple", "skilled", "skillful", "smile", "soulful", "sparkling", "special", "spirited", "spiritual", "stirring", "stupendous", "stunning", "success", "successful", "sunny", "super", "superb", "supporting", "surprising", "terrific", "thorough", "thrilling", "thriving", "tops", "tranquil", "transforming", "transformative", "trusting", "truthful", "unreal", "unwavering", "up", "upbeat", "upright", "upstanding", "valued", "vibrant", "victorious", "victory", "vigorous", "virtuous", "vital", "vivacious", "wealthy", "welcome", "well", "whole", "wholesome", "willing", "wonderful", "wondrous", "worthy", "wow", "yes", "yummy", "zeal", "zealous"])
negWords = set(["abysmal", "adverse", "alarming", "angry", "annoy", "anxious", "apathy", "appalling", "atrocious", "awful", "bad", "banal", "barbed", "belligerent", "bemoan", "beneath", "boring", "broken", "callous", "can't", "clumsy", "coarse", "cold", "cold-hearted", "collapse", "confused", "contradictory", "contrary", "corrosive", "corrupt", "crazy", "creepy", "criminal", "cruel", "cry", "cutting", "dead", "decaying", "damage", "damaging", "dastardly", "deplorable", "depressed", "deprived", "deformed", "deny", "despicable", "detrimental", "dirty", "disease", "disgusting", "disheveled", "dishonest", "dishonorable", "dismal", "distress", "don\'t", "dreadful", "dreary", "enraged", "eroding", "evil", "fail", "faulty", "fear", "feeble", "fight", "filthy", "foul", "frighten", "frightful", "gawky", "ghastly", "grave", "greed", "grim", "grimace", "gross", "grotesque", "gruesome", "guilty", "haggard", "hard", "hard-hearted", "harmful", "hate", "hideous", "homely", "horrendous", "horrible", "hostile", "hurt", "hurtful", "icky", "ignore", "ignorant", "immature", "imperfect", "impossible", "inane", "inelegant", "infernal", "injure", "injurious", "insane", "insidious", "insipid", "jealous", "junky", "lose", "lousy", "lumpy", "malicious", "mean", "menacing", "messy", "misshapen", "missing", "misunderstood", "moan", "moldy", "monstrous", "naive", "nasty", "naughty", "negate", "negative", "never", "no", "nobody", "nondescript", "nonsense", "not", "noxious", "objectionable", "odious", "offensive", "old", "oppressive", "pain", "perturb", "pessimistic", "petty", "plain", "poisonous", "poor", "prejudice", "questionable", "quirky", "quit", "reject", "renege", "repellant", "reptilian", "repulsive", "repugnant", "revenge", "revolting", "rocky", "rotten", "rude", "ruthless", "sad", "savage", "scare", "scary", "scream", "severe", "shoddy", "shocking", "sick", "sickening", "sinister", "slimy", "smelly", "sobbing", "sorry", "spiteful", "sticky", "stinky", "stormy", "stressful", "stuck", "stupid", "substandard", "suspect", "suspicious", "tense", "terrible", "terrifying", "threatening", "ugly", "undermine", "unfair", "unfavorable", "unhappy", "unhealthy", "unjust", "unlucky", "unpleasant", "upset", "unsatisfactory", "unsightly", "untoward", "unwanted", "unwelcome", "unwholesome", "unwieldy", "unwise", "upset", "vice", "vicious", "vile", "villainous", "vindictive", "wary", "weary", "wicked", "woeful", "worthless", "wound", "yell", "yucky", "zero"])




# get_vocab_frequency(comments, bitcoin_vocab)
# get_vocab_frequency(comments, first_personal_pronouns)
# get_vocab_frequency(comments, first_plural_pronouns)
# get_vocab_frequency(comments, second_pronouns)
get_vocab_frequency(comments, whQuestionWords)
get_vocab_frequency(comments, posWords)
get_vocab_frequency(comments, negWords)


# verbs = []
# adjectives = []
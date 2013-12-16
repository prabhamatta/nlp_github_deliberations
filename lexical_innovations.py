import nltk
import dateutil.parser
import datetime
import calendar
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
import string
from collections import Counter


f = open("issues_conversation_details_all.tsv","r")

stopwords = stopwords.words("english")
bitcoin_vocab = ["bitcoins", "bitcoin", "block", "coin", "coins", "blocks", "chains", "chain", "btc", "cryptography", "crypto", "security", "privacy", "mining", "p2p", "signature", "wallet", "wallets", "transaction", "xbt", "miner", "miners", "payment", "payments", "bitcoind", "transactions", "tumbler", "qt", "tumblers"]
first_personal_pronouns = ["i", "me", "myself", "mine", "my"]
first_plural_pronouns = ["we", "our", "ours", "us", "ourselves"]
second_pronouns = ["you", "your", "yours", "yourself", "yourselves"]
core_collabs = ["gavinandresen", "gmaxwell", "jgarzik", "laanwj", "sipa", "tcatm"]
whQuestionWords = ['who','what','when','where','why', 'how']
posWords = set(["absolutely", "adorable", "accepted", "acclaimed", "accomplish", "accomplishment", "achievement", "action", "active", "admire", "adventure", "affirmative", "affluent", "agree", "agreeable", "amazing", "angelic", "appealing", "approve", "aptitude", "attractive", "awesome", "beaming", "beautiful", "believe", "beneficial", "bliss", "bountiful", "bounty", "brave", "bravo", "brilliant", "bubbly", "calm", "celebrated", "certain", "champ", "champion", "charming", "cheery", "choice", "classic", "classical", "clean", "commend", "composed", "congratulation", "constant", "cool", "courageous", "creative", "cute", "dazzling", "delight", "delightful", "distinguished", "divine", "earnest", "easy", "ecstatic", "effective", "effervescent", "efficient", "effortless", "electrifying", "elegant", "enchanting", "encouraging", "endorsed", "energetic", "energized", "engaging", "enthusiastic", "essential", "esteemed", "ethical", "excellent", "exciting", "exquisite", "fabulous", "fair", "familiar", "famous", "fantastic", "favorable", "fetching", "fine", "fitting", "flourishing", "fortunate", "free", "fresh", "friendly", "fun", "funny", "generous", "genius", "genuine", "giving", "glamorous", "glowing", "good", "gorgeous", "graceful", "great", "green", "grin", "growing", "handsome", "happy", "harmonious", "healing", "healthy", "hearty", "heavenly", "honest", "honorable", "honored", "hug", "idea", "ideal", "imaginative", "imagine", "impressive", "independent", "innovate", "innovative", "instant", "instantaneous", "instinctive", "intuitive", "intellectual", "intelligent", "inventive", "jovial", "joy", "jubilant", "keen", "kind", "knowing", "knowledgeable", "laugh", "legendary", "light", "learned", "lively", "lovely", "lucid", "lucky", "luminous", "marvelous", "masterful", "meaningful", "merit", "meritorious", "miraculous", "motivating", "moving", "natural", "nice", "novel", "now", "nurturing", "nutritious", "okay", "one", "one-hundred percent", "open", "optimistic", "paradise", "perfect", "phenomenal", "pleasurable", "plentiful", "pleasant", "poised", "polished", "popular", "positive", "powerful", "prepared", "pretty", "principled", "productive", "progress", "prominent", "protected", "proud", "quality", "quick", "quiet", "ready", "reassuring", "refined", "refreshing", "rejoice", "reliable", "remarkable", "resounding", "respected", "restored", "reward", "rewarding", "right", "robust", "safe", "satisfactory", "secure", "seemly", "simple", "skilled", "skillful", "smile", "soulful", "sparkling", "special", "spirited", "spiritual", "stirring", "stupendous", "stunning", "success", "successful", "sunny", "super", "superb", "supporting", "surprising", "terrific", "thorough", "thrilling", "thriving", "tops", "tranquil", "transforming", "transformative", "trusting", "truthful", "unreal", "unwavering", "up", "upbeat", "upright", "upstanding", "valued", "vibrant", "victorious", "victory", "vigorous", "virtuous", "vital", "vivacious", "wealthy", "welcome", "well", "whole", "wholesome", "willing", "wonderful", "wondrous", "worthy", "wow", "yes", "yummy", "zeal", "zealous"])
negWords = set(["abysmal", "adverse", "alarming", "angry", "annoy", "anxious", "apathy", "appalling", "atrocious", "awful", "bad", "banal", "barbed", "belligerent", "bemoan", "beneath", "boring", "broken", "callous", "can't", "clumsy", "coarse", "cold", "cold-hearted", "collapse", "confused", "contradictory", "contrary", "corrosive", "corrupt", "crazy", "creepy", "criminal", "cruel", "cry", "cutting", "dead", "decaying", "damage", "damaging", "dastardly", "deplorable", "depressed", "deprived", "deformed", "deny", "despicable", "detrimental", "dirty", "disease", "disgusting", "disheveled", "dishonest", "dishonorable", "dismal", "distress", "don\'t", "dreadful", "dreary", "enraged", "eroding", "evil", "fail", "faulty", "fear", "feeble", "fight", "filthy", "foul", "frighten", "frightful", "gawky", "ghastly", "grave", "greed", "grim", "grimace", "gross", "grotesque", "gruesome", "guilty", "haggard", "hard", "hard-hearted", "harmful", "hate", "hideous", "homely", "horrendous", "horrible", "hostile", "hurt", "hurtful", "icky", "ignore", "ignorant", "immature", "imperfect", "impossible", "inane", "inelegant", "infernal", "injure", "injurious", "insane", "insidious", "insipid", "jealous", "junky", "lose", "lousy", "lumpy", "malicious", "mean", "menacing", "messy", "misshapen", "missing", "misunderstood", "moan", "moldy", "monstrous", "naive", "nasty", "naughty", "negate", "negative", "never", "no", "nobody", "nondescript", "nonsense", "not", "noxious", "objectionable", "odious", "offensive", "old", "oppressive", "pain", "perturb", "pessimistic", "petty", "plain", "poisonous", "poor", "prejudice", "questionable", "quirky", "quit", "reject", "renege", "repellant", "reptilian", "repulsive", "repugnant", "revenge", "revolting", "rocky", "rotten", "rude", "ruthless", "sad", "savage", "scare", "scary", "scream", "severe", "shoddy", "shocking", "sick", "sickening", "sinister", "slimy", "smelly", "sobbing", "sorry", "spiteful", "sticky", "stinky", "stormy", "stressful", "stuck", "stupid", "substandard", "suspect", "suspicious", "tense", "terrible", "terrifying", "threatening", "ugly", "undermine", "unfair", "unfavorable", "unhappy", "unhealthy", "unjust", "unlucky", "unpleasant", "upset", "unsatisfactory", "unsightly", "untoward", "unwanted", "unwelcome", "unwholesome", "unwieldy", "unwise", "upset", "vice", "vicious", "vile", "villainous", "vindictive", "wary", "weary", "wicked", "woeful", "worthless", "wound", "yell", "yucky", "zero"])

live_users = ['vobornik', 'scottie', 'm13253', 'zootreeves', 'cpunks', 'stevenroose', 'hrabbach', 'SzymonPobiega', 'rdponticelli', 'jeremysawicki', 'soroush', 'Viceroy', 'monohydroxy', 'edam', 'apex-predator', 'ISibboI', 'Mazo', 'mb300sd', 'CodeShark', 'subSTRATA', 'wtogami', 'hemlockII', 'cozz', 'kunstmusik', 'da2ce7', 'goldbit89', 'maxime01', 'bitsofproof', 'maaku', 'medoix', 'lazyjay', 'andrasfuchs', 'painlord2k', 'bruiselee', 'fanquake', 'Rudd-O', 'nemysis', 'earthmeLon', 'KobuderaRoninShinobi', 'codler', 'lismore', 'unknwntrr', 'onlyjob', 'petertodd', 'whitslack', 'MrLei', 'msva', 'swills', 'Nerzahd', 'jonasschnelli', 'imzhuli', 'collapsedev', 'gongchengra', 'sje1', 'randy-waterhouse', 'AllThingsBitcoin', 'shripadk', 'patrickb1991', 'dvdkhlng', 'intelliot', 'joe999', 'soheil', 'oblongmeteor', 'skruger', 'TheBlueMatt', 'constantined', 'dooglio', 'Mezrin', 'sgaltsev', 'agravier', 'K1773R', 'theuni', 'speirs', 'Suffice', 'bitkevin', 'cosmarchy', 'paulogeyer', 'joshtriplett', 'jkaye2012', 'bitnews', 'shufps', 'Stemby', 'TheButterZone', 'sarchar', 'ryny24', 'Squeezle42', 'Cryddit', 'btclove', 'weex', 'wizkid057', 'nbelikov', 'jeffmendoza', 'SteveBell', 'BrogulT', 'medicinebottle', 'dyzz', 'ag346', 'pshep', 'badger200', 'sje397', 'r000n', 'lseror', 'grahama', 'gthiruva', 'orb', 'gwern', 'ryanxcharles', 'jgarzik', 'lzrloveyou', 'shahnah', 'dajohi', 'qubez', 'tcatm', 'lano1106', 'pstratem', 'cjdelisle', 'nvmd', 'dpkp', 'laanwj', 'idevk', 'molecular', 'crazikPL', 'dan-da', 'brandondahler', 'idiotsabound', 'SomeoneWeird', 'dertin', 'schildbach', 'jegz', 'ephraimb', 'huiju', 'kybl', 'gmaxwell', 'WilhelmGGW', 'grayleonard', 'jonls', 'luke-jr', 'wlch', 'andruby', 'kyledrake', 'awt', 'p308945', 'dsattler', 'meighti', 'vassilevsky', 'sheldonth', 'Tranz5', 'Agera-S', 'Schmollen', 'tstranex', 'jherrerob', 'BugAndNewsReporter', 'bitstocoins', 'ashleyholman', 'xmj', 'PRab', 'chevdor', 'fryx', 'lovedazi005', 'Michagogo', 'coblee', 'WyseNynja', 'SergioDemianLerner', 'woeisme', 'doublec', 'robbak', 'Sammey1995', 'keo', 'sipa', 'laxris', 'fcicq', 'old-c-coder', 'dishwara', 'jrmithdobbs', 'ktiedt', 'kuzetsa', 'alexpennace', 'gdvine', 'ThePiachu', 'BitBargain', 'paraipan', 'hughdavenport', 'raamdev', 'vinniefalco', 'super3', 'Subo1978', 'richardassar', '63', 'adavies42', 'daedalus', 'nu11gravity', 'DannyHamilton', 'FrankLo', 'rodjacksonx', 'M4v3R', 'dscotese', 'Krellan', 'fgeek', 'nikolajsheller', 'henu', 'BoltBlit', 'leo-bogert', 'propertunist', 'rofl0r', 'johndillon', 'simon-liu', 'deweydb', 'codeboost', 'hasib145', 'kzaher', 'kiaya', 'n1bor', 'xerohour', 'macd0g', 'casellas', 'konieczkow', 'dacoinminster', 'mumblerit', 'shesek', 'pentarh', 'imton', 'HostFat', 'nixoid', 'dooglus', 'pianist', 'pjbrito', 'simondlr', 'mikehearn', 'jemmons', 'NerdfighterSean', 'taras-kolodchyn', 'VirtualDestructor', 'njbartlett', 'raarts', 'DrHaribo', 'thebalaa', 'gateway', 'gruez', 'neilneyman', 'Diapolo', 'face', 'deed02392', 'shamoons', 'ntom', 'timsk', 'avl42', 'rebroad', 'darkhosis', 'gavinandresen', 'ghedipunk', 'gubatron', 'aceat64', 'prusnak', 'xelvet', 'runeksvendsen', 'pakt', 'Commissar0617', 'Enelar', 'erundook', 'dalrax', 'Kroese', 'toffoo', 'Chemisist', 'nilamdoc', 'phelixbtc', 'KaosMcRage']



def sort_comments():
	""" Sorts the list of comments by date """
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

def get_months_comments(month, year, comments_sorted):
	""" Returns the comments that happened in that month and year """
	comments = []
	for i in comments_sorted:
		if i[0].month == month and i[0].year == year:
			comments.append(i)
	return comments

def get_initial_seen_words(months_comments):
	""" Builds initial list of seen words """
	seen_words = []
	for post in months_comments:
		comment = nltk.word_tokenize(post[2])
		cleaned_comment = [word.lower().strip(string.punctuation) for word in comment if word.lower().strip(string.punctuation) not in stopwords and word not in string.punctuation]
		for word in cleaned_comment:
			if word != '':
				seen_words.append(word)

	return seen_words
		
def get_lexical_innovations(comments, seen_words):
	""" Finds lexical innovations. Lexical innovations are words that became popular by multiple users and were used more than 10 times within 6 months after first being introduced """
	new_words = {}
	innovations = []
	time_period = datetime.timedelta(-180)
	
	for post in comments:
		user = post[1]
		date_time_obj = post[0]
		comment = nltk.word_tokenize(post[2])
		cleaned_comment = [word.lower().strip(string.punctuation) for word in comment if word.lower().strip(string.punctuation) not in stopwords and word not in string.punctuation]
		for word in cleaned_comment:
			if word not in new_words and word not in seen_words:
				new_words[word] = [[user, date_time_obj]]
			if word in new_words:
				if user != new_words[word][0][0] and new_words[word][0][1] - date_time_obj > time_period:   #if the user is not the first user and comment time is within 180 days.
						new_words[word].append([user, date_time_obj])
	
	for k,v in new_words.items():
		if k.isalpha():  # Only getting alpha words
			users = []
			for i in v:
				users.append(i[0])
			if len(set(users)) > 2:
				if len(v) > 10:   # more than 10 times
					# word, user, year, month, number of times used
					innovations.append([k, v[0][0], v[0][1].year, v[0][1].month, len(v)])
					#print k + "\t" + v[0][0]  + "\t" + str(v[0][1].year)  + "\t" + str(v[0][1].month)  + "\t" + str(len(v))

	return innovations

def analyze_innovators(innovations):
	core_innovators = []
	noncore_innovators = []
	for i in innovations:
		if i[1] in core_collabs:
		  core_innovators.append(i[1])
		elif i[1] not in core_collabs:
			noncore_innovators.append(i[1])
	#print Counter(core_innovators)
	#print Counter(noncore_innovators)


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
		if user not in live_users:
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


def get_user_lifespan(comments_sorted):
	user_life = {}
	for i in comments_sorted:
		if i[1] not in user_life:
			user_life[i[1]] = [i[0]]
		elif i[1] in user_life:
			user_life[i[1]].append(i[0])
	
	live_users = []
	for k,v in user_life.items():
		#print v[-1].year, v[-1].year >= 2013
		if v[-1].year >= 2013 and v[-1].month >= 6:
			live_users.append(k)
	return live_users

	#print type(user_life['gavinandresen'][0])

## Find most frequent lexical innovators
## flexibility of new comers
## do new comers adopt innovations?


comments_sorted = sort_comments()
#months_comments =  get_months_comments(12, 2010, comments_sorted)
#seen_words = get_initial_seen_words(months_comments)
#innovations = get_lexical_innovations(comments_sorted, seen_words)
#analyze_innovators(innovations)

#print innovations

#get_user_lifespan(comments_sorted)

comments = get_users_comments(comments_sorted)

get_vocab_frequency(comments, bitcoin_vocab)
get_vocab_frequency(comments, first_personal_pronouns)
get_vocab_frequency(comments, first_plural_pronouns)
get_vocab_frequency(comments, second_pronouns)
# get_vocab_frequency(comments, whQuestionWords)
# get_vocab_frequency(comments, posWords)
# get_vocab_frequency(comments, negWords)
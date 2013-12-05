from nltk.corpus import stopwords

gram_choice = 'u'
freq_gram_cnt = 100
en_stop_words = stopwords.words('english')



def get_comments():
    comments = []
    fnames = ['unlabeled_comments.tsv']
    for fname in fnames:
        with codecs.open(fname, 'r',  "UTF-8") as fin:
            for line in fin:
                comments.append(line.split('\t')[2].strip())

    return comments


def get_freq_unigram(comments, get_stem=False, get_tag=False, flt_stop_words=True):
    unigrams = []

    for comment in comments:
        words = nltk.word_tokenize(comment)

        if get_tag:
            for word, tag in nltk.pos_tag(words):
                if tag.startswith('V') or tag == 'ADJ' or tag == 'ADV':
                    if get_stem:
                        unigrams.append(stemmer.stem(word))
                    else:
                        unigrams.append(word)
        elif get_stem:
            for word in words:
                unigrams.append(stemmer.stem(word))
        else:
            unigrams.extend(words)

    if flt_stop_words:
        stop_words = en_stop_words
    else:
        stop_words = []

    return nltk.FreqDist(w.lower() for w in unigrams if w.isalpha() and w not in stop_words).keys()[:freq_gram_cnt]




def get_freq_bigram(comments, get_stem=False, get_tag=False, flt_stop_words=False):
    bigrams = []

    if flt_stop_words:
        stop_words = en_stop_words
    else:
        stop_words = []

    for comment in comments:
        sent = []
        words = nltk.word_tokenize(comment)

        if get_tag:
            for word, tag in nltk.pos_tag(words):
                if tag.startswith('V') or tag == 'ADJ' or tag == 'ADV':
                    if get_stem:
                        sent.append(stemmer.stem(word))
                    else:
                        sent.append(word)
        elif get_stem:
            for word in words:
                sent.append(stemmer.stem(word))
        else:
            sent.extend(words) 

        bigrams.extend(nltk.bigrams(w.lower() for w in sent if w.isalpha() and w not in en_stop_words))

    return nltk.FreqDist(bigrams).keys()[:freq_gram_cnt]


    if __name__=='__main__':
    # if there are command line arguments, the first one will be 'gram_choice'
    # and the second one will be 'freq_gram_cnt'
    if len(sys.argv) > 1:
        gram_choice = sys.argv[1]
    if len(sys.argv) > 2:
        freq_gram_cnt = int(sys.argv[2])

    # get comments
    comments = get_comments()


    if gram_choice[0] == 'u':
        freq_unigram = get_freq_unigram(comments)
        for unigram in freq_unigram:
            print unigram
    elif gram_choice[0] == 'b':
        freq_bigram = get_freq_bigram(comments)
        for bigram in freq_bigram:
            print "({0}, {1})".format(bigram[0], bigram[1])

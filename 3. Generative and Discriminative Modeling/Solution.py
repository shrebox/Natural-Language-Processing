import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords
# from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import operator, random
import sys
import math
import pickle

def avg_sentence_length(infile):
    inf = open(infile,'r')
    count = 0
    pat = re.compile(r'[.!?]+[\])}>\'\"]*[\n]|[.!?]+[\])}>\'\"]*[\s]+[\"\'{\[(<]*[A-Z0-9]')
    linn = 0
    totallen = 0
    countlen = 0
    for i in inf:
        linn+=1
        i = re.sub(r'Dr. |Ms. |Mr. |Mrs. |Er. ','',i)
        val = pat.findall(i)
        count+=len(val)
        if len(val)>0:
        	totallen+=len(i.split(" "))
        	countlen+=1
        	# print val
        	# break
    return totallen/float(countlen)
    # return count

def sentence_start_words(infile):
    pat = re.compile(r'[.!?]+[>)\'}\]\"]*(\s|\n)+[\'\"{\[\(<]*[A-Za-z0-9]+')
    count = un =0
    word_freq = {}
    with open(infile,'r') as f:
        for line in f:
        	val = pat.findall(line)
        	if len(val)>0:        		
        		for jk in range(len(val)):
        			w = line.split(val[jk])[1]
        			if len(w)>1:
	        			try:
	        				ww = w.split(' ')[0]
	        				if ww not in word_freq:
	        					word_freq[ww]=0
	        				word_freq[ww]+=1
	        			except Exception, e:
	        				un+=1
	        		else:
		        		if w not in word_freq:
		        			word_freq[w]=0
		        		word_freq[w]+=1
		        		count+=1

	del word_freq['']
    sorted_xu = sorted(word_freq.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_xu
    for i in range(100):
    	print sorted_xu[i]

def remove_html(data):
	return BeautifulSoup(data, "html.parser").get_text()

def remove_btw_sqr(data):
    fin = re.sub('\[[^]]*\]', '', data)
    return fin

def fix_contractions(data):
    fin = contractions.fix(data)
    return fin

def words_tokenizer(data):
	words = nltk.word_tokenize(data)
	# tknzr = TweetTokenizer()	
	# tknzr.tokenize(data)
	return words

def remove_non_ascii(words):
	new_words = []
	flag = 0
	for i in range(len(words)):
		flag = 1
		new_word = unicodedata.normalize('NFKD',words[i])
		new_word = new_word.encode('ascii','ignore')
		new_word = new_word.decode('utf-8','ignore')
		flag+=1
		new_words.append(new_word)
	return new_words
# def remove_non_ascii(words):
#     new_words = []
#     flag = 0
#     for i in range(len(words)):
#  		flag=1
#  		new_word = unicodedata.normalize('NFKD', words[i]).encode('ascii', 'ignore').decode('utf-8', 'ignore')
#  		flag+=1
#  		new_words.append(new_word)
#  	return new_words

def to_lowercase(words):
    new_words = []
    flag = 0
    for i in range(len(words)):
        new_word = words[i].lower()
        flag+=1
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    new_words = []
    flag = 0
    for i in range(len(words)):
    	flag+=1
        new_word = re.sub(r'([^\w\s])|_+', '', words[i])
        if new_word != '':
        	flag=0
        	new_words.append(new_word)
    return new_words

# def replace_numbers(words):
#     p = inflect.engine()
#     new_words = []
#     flag = 0
#     for i in range(len(words)):
#     	flag = 1
#         if words[i].isdigit():
#             new_word = p.number_to_words(words[i])
#             flag+=1
#             new_words.append(new_word)
#         else:
#         	flag = 0
#         	new_words.append(word)
#     return new_words

def remove_stopwords(words):
    new_words = []
    flag = 0
    for i in range(len(words)):
    	flag = 1
        if words[i] not in stopwords.words('english'):
        	flag+=1
        	new_words.append(words[i])
    return new_words	

def preprocess_data_unigram(data):
	data = remove_html(data)
	flag=0
	data = remove_btw_sqr(data)
	data = fix_contractions(data)
	flag+=1
	words = words_tokenizer(data)
	x = flag
	words = remove_non_ascii(words)
	words = to_lowercase(words)
	x+=1
	words = remove_punctuation(words)
	# words = replace_numbers(words)
	words = remove_stopwords(words)
	return words

def preprocess_data_bitrigram(data):
	data = remove_html(data)
	flag=0
	data = remove_btw_sqr(data)
	x = flag
	data = fix_contractions(data)
	words = words_tokenizer(data)
	x+=1
	words = remove_non_ascii(words)
	words = to_lowercase(words)
	x+=2
	words = remove_punctuation(words)
	# words = replace_numbers(words)
	# words = remove_stopwords(words)
	return words

def preprocess_input_sentence(data):
	# data = remove_html(data)
	# data = remove_btw_sqr(data)
	data = fix_contractions(data)
	words = words_tokenizer(data)
	# words = remove_non_ascii(words)
	words = to_lowercase(words)
	words = remove_punctuation(words)
	# words = replace_numbers(words)
	# words = remove_stopwords(words)
	return words

def frequency_unigram(words):
	findic = {}
	for i in range(len(words)):
		if words[i] not in findic:
			findic[words[i]]=0
		findic[words[i]]+=1
	return findic

def frequency_bigram(words):
	findic = {}
	findic[('<start>',words[0])]=1
	for i in range(len(words)):
		if i==len(words)-1:
			if (words[i],'</start>') not in findic:
				findic[(words[i],'</start>')]=0
			findic[(words[i],'</start>')]+=1
		else:
			if (words[i],words[i+1]) not in findic:
				findic[(words[i],words[i+1])]=0
			findic[(words[i],words[i+1])]+=1
	return findic

def frequency_bigram_part2(words):
	findic = {}
	for i in range(len(words)-1):
		if (words[i],words[i+1]) not in findic:
			findic[(words[i],words[i+1])]=0
		findic[(words[i],words[i+1])]+=1
	return findic

def frequency_trigram(words):
	findic = {}
	findic[('<start>',words[0],words[1])]=1
	for i in range(len(words)-1):
		if i==len(words)-2:
			if (words[i],words[i+1],'</start>') not in findic:
				findic[(words[i],words[i+1],'</start>')]=0
			findic[(words[i],words[i+1],'</start>')]+=1
		else:
			if (words[i],words[i+1],words[i+2]) not in findic:
				findic[(words[i],words[i+1],words[i+2])]=0
			findic[(words[i],words[i+1],words[i+2])]+=1
	return findic

def generate_prob_dic_bigram(count_dictionaryb,wordsu_stop):	
	prob_dic_bigram = {}
	for k,v in count_dictionaryb.iteritems():
		prob_dic_bigram[k] = math.log(v/float(wordsu_stop[k[0]]))
	return prob_dic_bigram

def generate_bigram_sentences(prob_dic_bigram,zerow,firstw,sentence_length):
	finalstr = zerow+" "+firstw+" "
	for i in range(sentence_length):
		tempdic = {}
		inc = []
		for k,v in prob_dic_bigram.iteritems():
			if k[0] == firstw:
				tempdic[k] = v
		sorttemp = sorted(tempdic.items(), key=operator.itemgetter(1),reverse=True)
		if (sorttemp[0][0] not in inc) or (sorttemp[0][0] in inc and len(sorttemp)==1):
			# print i, sorttemp[0][0]
			finalstr+=sorttemp[0][0][1]+" "
			firstw = sorttemp[0][0][1]
			prob_dic_bigram[sorttemp[0][0]]*=2 
			inc.append(sorttemp[0])
		else:
			# print i, sorttemp[1][0]
			finalstr+=sorttemp[1][0][1]+" "
			firstw = sorttemp[1][0][1]
			prob_dic_bigram[sorttemp[1][0]]*=2 
			inc.append(sorttemp[1][0])

	return finalstr

def generate_prob_dic_trigram(count_dictionaryt,count_dictionaryb):
	prob_dic_trigram = {}
	for k,v in count_dictionaryt.iteritems():
		k1 = str(k[0])
		k2 = str(k[1])
		kpass = (k1,k2)
		prob_dic_trigram[k] = math.log(v/float(count_dictionaryb[kpass]))
	return prob_dic_trigram

def generate_trigram_sentence(prob_dic_trigram,zerow,firstw,secondw,sentence_length):
	finalstr = zerow+" "+secondw+" "+firstw+" "
	for i in range(sentence_length):
		tempdic = {}
		inc = []
		for k,v in prob_dic_trigram.iteritems():
			if k[0] == secondw and k[1]==firstw:
				tempdic[k] = v
		sorttemp = sorted(tempdic.items(), key=operator.itemgetter(1),reverse=True)
		if (sorttemp[0][0] not in inc) or (sorttemp[0][0] in inc and len(sorttemp)==1):
			# print i, sorttemp[0][0]	
			finalstr+=sorttemp[0][0][2]+" "
			firstw = sorttemp[0][0][2]
			secondw = sorttemp[0][0][1]
			prob_dic_trigram[sorttemp[0][0]]*=2 
			inc.append(sorttemp[0])
		else:
			# print i, sorttemp[1][0]
			finalstr+=sorttemp[1][0][2]+" "
			firstw = sorttemp[1][0][2]
			secondw = sorttemp[1][0][1]
			prob_dic_trigram[sorttemp[1][0]]*=2 
			inc.append(sorttemp[1][0])
	return finalstr 

def smooth_prob_cal(bigrams,corpus_unigrams,corpus_bigrams):
	smooth_prob = {}
	for k,v in bigrams.iteritems():
		c1 = c2 = 0
		try:
			c2 = corpus_bigrams[k]
		except Exception, e:
			print e
		try:
			c1 = corpus_unigrams[k[0]]
		except Exception, e:
			print e
		nprob = math.log(((c2+1)/float((c1+len(corpus_unigrams))))*v)
		smooth_prob[k] = nprob
	return smooth_prob

# words = sentence_start_words('combine_data2.txt')

# with open('motorcycle_sentence_startwords.pkl','wb') as f:
# 	pickle.dump(words,f)
print "Average sentence length for corpus: Computers: " + str(avg_sentence_length('combine_data2.txt'))
print "Average sentence length for corpus: Motorcycle: " + str(avg_sentence_length('combine3.txt'))

# def smooth_prob_cal_unk(bigrams,corpus_unigrams,corpus_bigrams):
# 	smooth_prob = {}
# 	for k,v in bigrams.iteritems():
# 		c1 = c2 = 0
# 		try:
# 			c2 = corpus_bigrams[k]
# 		except Exception, e:
# 			print e
# 		try:
# 			c1 = corpus_unigrams[k[0]]
# 		except Exception, e:
# 			print e
# 		nprob = math.log((c2+1)/float((c1+len(corpus_unigrams))))
# 		smooth_prob[k] = nprob
# 	return smooth_prob

#=======================================================part 1======================================================================

# #---------------data combining------------------------
# data = ""
# with open('combine3.txt') as f:
# 	for line in f:
# 		data+=str(line)

#-------------generating unigrams------------------------
print"\nUnigram: \n"

# wordsu_stop = frequency_unigram(preprocess_data_bitrigram(data)) 
# wordsu_stop['<start>'] = 1
# wordsu_stop['</start>'] = 1

# wordsu = preprocess_data_unigram(data)
# count_dictionaryu = frequency_unigram(wordsu)

# with open('computers_unigrams_part1.pkl','wb') as f:
# 	pickle.dump(count_dictionaryu,f)

count_dictionaryu_part1 = {}
with open('computers_unigrams_part1.pkl','rb') as f:
	count_dictionaryu_part1 = pickle.load(f)

sorted_xu = sorted(count_dictionaryu_part1.items(), key=operator.itemgetter(1),reverse=True)

for i in range(14): # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>need to change this to some threshold
	sys.stdout.write(str(sorted_xu[i][0])+" ")
	sys.stdout.flush() # https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space

#------------generating bigrams---------------------
print "\n"
print"\nBigrams: \n"

# wordsb = preprocess_data_bitrigram(data)
# count_dictionaryb = frequency_bigram(wordsb)
# prob_dic_bigram = generate_prob_dic_bigram(count_dictionaryb,wordsu_stop)

# with open('computers_bigram_prob.pkl','wb') as f:
# 	pickle.dump(prob_dic_bigram,f)

computers_bigram_prob = {}
with open('computers_bigram_prob.pkl','rb') as f:
	computers_bigram_prob = pickle.load(f)

#>>>>>>>>>>>>>>>>>>>>>>>>>> choose the start of the sentence using unigram frequency of the start word
# finalstr = "i have "

# computer_sentence_startwords = {}
# with open('computer_sentence_startwords.pkl','rb') as f:
# 	computer_sentence_startwords = pickle.load(f)

#the original, the program, to the, to be

zerow = "the"
firstw = "original"

finalstr = generate_bigram_sentences(computers_bigram_prob,zerow,firstw,14)
print finalstr
print ""

zerow = "to"
firstw = "the"

finalstr = generate_bigram_sentences(computers_bigram_prob,zerow,firstw,14)
print finalstr

# # #---------------------generating trigrams----------------------------

print"\nTrigrams: \n"

# count_dictionaryb = {}
# with open('computers_bigrams.pkl','rb') as f:
# 	count_dictionaryb = pickle.load(f)

# wordst = preprocess_data_bitrigram(data)
# count_dictionaryt = frequency_trigram(wordst)
# prob_dic_trigram = generate_prob_dic_trigram(count_dictionaryt,count_dictionaryb)

# with open('computers_trigram_prob.pkl','wb') as f:
# 	pickle.dump(prob_dic_trigram,f)

computers_trigram_prob = {}
with open('computers_trigram_prob.pkl','rb') as f:
	computers_trigram_prob = pickle.load(f)

# sorted_xt = sorted(count_dictionaryt.items(), key=operator.itemgetter(1),reverse=True)

# In [390]: print sorted_xt[0]
# ((u'the', u'egavgaadapter', u'by'), 0.0)

# In [391]: print sorted_xt[1]
# ((u'the', u'copierprinter', u'has'), 0.0)

# In [392]: print sorted_xt[2]
# ((u'the', u'setting', u'are'), 0.0)

# In [396]: print sorted_xt[0]
# ((u'the', u'original', u'is'), -2.847812143477369)

# In [397]: print sorted_xt[1]
# ((u'the', u'original', u'still'), -3.1354942149291497)

# In [398]: print sorted_xt[2]
# ((u'the', u'original', u'fullcolor'), -3.1354942149291497)

# In [402]: print sorted_xt[0]
# ((u'to', u'mprenderrequest', u'icaseedu'), 0.0)

# In [403]: print sorted_xt[1]
# ((u'to', u'grassftpadmin', u'mooncecerarmymil'), 0.0)

# In [404]: print sorted_xt[2]
# ((u'to', u'specific', u'subdirectories'), 0.0)

zerow = "the"
secondw = "egavgaadapter"
firstw = "by"

finalstr = generate_trigram_sentence(computers_trigram_prob,zerow,firstw,secondw,14)
print finalstr
print "\n"

zerow = "the"
secondw = "copierprinter"
firstw = "has"

finalstr = generate_trigram_sentence(computers_trigram_prob,zerow,firstw,secondw,14)
print finalstr

# #=======================================================part 2======================================================================

# #---------------data combining------------------------
# data = ""
# with open('combine_data2.txt') as f:
# 	for line in f:
# 		data+=str(line)

#-------------generating unigrams------------------------
print"\nUnigram: \n"

# wordsu_stop = frequency_unigram(preprocess_data_bitrigram(data)) 
# wordsu_stop['<start>'] = 1
# wordsu_stop['</start>'] = 1

# wordsu = preprocess_data_unigram(data)
# count_dictionaryu = frequency_unigram(wordsu)

# with open('motorcycle_unigrams_part1.pkl','wb') as f:
# 	pickle.dump(count_dictionaryu,f)

count_dictionaryu_part1 = {}
with open('motorcycle_unigrams_part1.pkl','rb') as f:
	count_dictionaryu_part1 = pickle.load(f)

sorted_xu = sorted(count_dictionaryu_part1.items(), key=operator.itemgetter(1),reverse=True)

for i in range(14): # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>need to change this to some threshold
	sys.stdout.write(str(sorted_xu[i][0])+" ")
	sys.stdout.flush() # https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space

# # #------------generating bigrams---------------------
print "\n"
print"\nBigrams: \n"

# wordsb = preprocess_data_bitrigram(data)
# count_dictionaryb = frequency_bigram(wordsb)

# motorcycles_unigrams = {}
# with open('motorcycles_unigrams.pkl','rb') as f:
# 	motorcycles_unigrams = pickle.load(f)

# motorcycles_bigrams = {}
# with open('motorcycles_bigrams.pkl','rb') as f:
# 	motorcycles_bigrams = pickle.load(f)

# prob_dic_bigram = generate_prob_dic_bigram(motorcycles_bigrams,motorcycles_unigrams)

# with open('motorcycles_bigram_prob.pkl','wb') as f:
# 	pickle.dump(prob_dic_bigram,f)

motorcycles_bigram_prob = {}
with open('motorcycles_bigram_prob.pkl','rb') as f:
	motorcycles_bigram_prob = pickle.load(f)
#>>>>>>>>>>>>>>>>>>>>>>>>>> choose the start of the sentence using unigram frequency of the start word

# the first, the dog, the ground, the only
# to be, to do, to get, to a

# finalstr = "i have "
zerow = "the"
firstw = "first"

finalstr = generate_bigram_sentences(motorcycles_bigram_prob,zerow,firstw,14)
print finalstr
print ""

zerow = "to"
firstw = "be"

finalstr = generate_bigram_sentences(motorcycles_bigram_prob,zerow,firstw,14)
print finalstr

# # #---------------------generating trigrams----------------------------

print"\nTrigrams: \n"

# wordst = preprocess_data_bitrigram(data)
# count_dictionaryt = frequency_trigram(wordst)

# motorcycles_bigrams = {}
# with open('motorcycles_bigrams.pkl','rb') as f:
# 	motorcycles_bigrams = pickle.load(f)

# prob_dic_trigram = generate_prob_dic_trigram(count_dictionaryt,motorcycles_bigrams)
# # sorted_xt = sorted(count_dictionaryt.items(), key=operator.itemgetter(1),reverse=True

# with open('motorcycles_trigram_prob.pkl','wb') as f:
# 	pickle.dump(prob_dic_trigram,f)

motorcycles_trigram_prob = {}
with open('motorcycles_trigram_prob.pkl','rb') as f:
	motorcycles_trigram_prob = pickle.load(f)

# In [441]: print sorted_xt[0]
# ((u'the', u'leading', u'lady'), 0.0)

# In [442]: print sorted_xt[1]
# ((u'the', u'inspector', u'general'), 0.0)

# In [443]: print sorted_xt[2]
# ((u'the', u'areas', u'you'), 0.0)

# In [447]: print sorted_xt[0]
# ((u'to', u'treat', u'others'), 0.0)

# In [448]: print sorted_xt[1]
# ((u'to', u'boil', u'off'), 0.0)

# In [449]: print sorted_xt[2]
# ((u'to', u'coast', u'to'), 0.0)

zerow = "the"
secondw = "inspector"
firstw = "general"

finalstr = generate_trigram_sentence(motorcycles_trigram_prob,zerow,firstw,secondw,14)
print finalstr
print ""

zerow = "to"
secondw = "boil"
firstw = "off"

finalstr = generate_trigram_sentence(motorcycles_trigram_prob,zerow,firstw,secondw,14)
print finalstr

print "\n"
#=======================================================part 3======================================================================

# print unigrams
# print bigrams

# data = ""
# with open('combine3.txt') as f:
# 	for line in f:
# 		data+=str(line)

# wordsu_stop = frequency_unigram(preprocess_data_bitrigram(data)) 
# wordsu_stop['<start>'] = 1
# wordsu_stop['</start>'] = 1

# with open('computers_unigrams.pkl','wb') as f:
# 	pickle.dump(wordsu_stop,f)

# wordsb = preprocess_data_bitrigram(data)
# count_dictionaryb = frequency_bigram(wordsb)

# with open('computers_bigrams.pkl','wb') as f:
# 	pickle.dump(count_dictionaryb,f)

computers_unigrams = {}
with open('computers_unigrams.pkl','rb') as f:
	computers_unigrams = pickle.load(f)

computers_bigrams = {}
with open('computers_bigrams.pkl','rb') as f:
	computers_bigrams = pickle.load(f)

motorcycles_unigrams = {}
with open('motorcycles_unigrams.pkl','rb') as f:
	motorcycles_unigrams = pickle.load(f)

motorcycles_bigrams = {}
with open('motorcycles_bigrams.pkl','rb') as f:
	motorcycles_bigrams = pickle.load(f)

input_sentence = str(raw_input("Enter the sentence: "))

input_sentence = preprocess_input_sentence(input_sentence)
# input_sentence = input_sentence.split(" ")

bigrams = frequency_bigram_part2(input_sentence)

smoothval1 = smooth_prob_cal(bigrams,computers_unigrams,computers_bigrams)

finalprob1 = 0
for k,v in smoothval1.iteritems():
	# print k,v
	finalprob1+=v

print finalprob1

smoothval2 = smooth_prob_cal(bigrams,motorcycles_unigrams,motorcycles_bigrams)

finalprob2 = 0
for k,v in smoothval2.iteritems():
	# print k,v
	finalprob2+=v

print finalprob2

print "\n"

if finalprob2>finalprob1:
	print "motorcycles"
else:
	print "computers"

print "\n"

#=======================================================part 4======================================================================

# data = ""
# with open('combine_data2.txt') as f:
# 	for line in f:
# 		data+=str(line)

# pp = preprocess_data_unigram(data)
# wordsu_stop = frequency_unigram(pp) 
# wordsu_stop['<start>'] = 1
# wordsu_stop['</start>'] = 1

# with open('motorcycle_vocab.pkl','wb') as f:
# 	pickle.dump(wordsu_stop,f)

# threshold_words = []
# for k,v in wordsu_stop.iteritems():
# 	if v<2:
# 		threshold_words.append(k)

# for i in range(len(pp)):
# 	if pp[i] in threshold_words:
# 		pp[i] = '<UNK>'

# wordsu_stop = frequency_unigram(pp) 
# wordsu_stop['<start>'] = 1
# wordsu_stop['</start>'] = 1

# with open('motorcycle_unigrams_unk.pkl','wb') as f:
# 	pickle.dump(wordsu_stop,f)

# count_dictionaryb = frequency_bigram(pp)

# with open('motorcycle_bigrams_unk.pkl','wb') as f:
# 	pickle.dump(count_dictionaryb,f)

computers_vocab = {}
with open('computers_vocab.pkl','rb') as f:
	computers_vocab = pickle.load(f)

computers_unigrams_unk = {}
with open('computers_unigrams_unk.pkl','rb') as f:
	computers_unigrams_unk = pickle.load(f)

computers_bigrams_unk = {}
with open('computers_bigrams_unk.pkl','rb') as f:
	computers_bigrams_unk = pickle.load(f)

motorcycles_vocab = {}
with open('motorcycles_vocab.pkl','rb') as f:
	motorcycles_vocab = pickle.load(f)

motorcycles_unigrams_unk = {}
with open('motorcycles_unigrams_unk.pkl','rb') as f:
	motorcycles_unigrams_unk = pickle.load(f)

motorcycles_bigrams_unk = {}
with open('motorcycles_bigrams_unk.pkl','rb') as f:
	motorcycles_bigrams_unk = pickle.load(f)

input_sentence = str(raw_input("Enter the sentence: "))

input_sentence = preprocess_input_sentence(input_sentence)
# input_sentence = input_sentence.split(" ")

inp1 = []
for i in range(len(input_sentence)):
	if input_sentence[i] not in computers_vocab:
		inp1.append('<UNK>')
	else:
		inp1.append(input_sentence[i])

bigrams = frequency_bigram_part2(inp1)

smoothval1 = smooth_prob_cal(bigrams,computers_unigrams_unk,computers_bigrams_unk)

finalprob1 = 0
for k,v in smoothval1.iteritems():
	print k,v
	if k[0] == '<UNK>' or k[1] == '<UNK>':
		finalprob1+=v*2
	else:
		finalprob1+=v

print finalprob1

inp2 = []
for i in range(len(input_sentence)):
	if input_sentence[i] not in motorcycles_vocab:
		inp2.append('<UNK>')
	else:
		inp2.append(input_sentence[i])

bigrams = frequency_bigram_part2(inp2)

smoothval2 = smooth_prob_cal(bigrams,motorcycles_unigrams_unk,motorcycles_bigrams_unk)

finalprob2 = 0
for k,v in smoothval2.iteritems():
	print k,v
	if k[0] == '<UNK>' or k[1] == '<UNK>':
		finalprob2+=v*2
	else:
		finalprob2+=v

print finalprob2

print "\n"

if finalprob2>finalprob1:
	print "motorcycles"
else:
	print "computers"
	
# Several years ago, while driving a cage, a dog darted out at a quiet --> Motorcycles (Line 1753)
# I currently have some grayscale image files that are not in any --> Computer (Line 11)


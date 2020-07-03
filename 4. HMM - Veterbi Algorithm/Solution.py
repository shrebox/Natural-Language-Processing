import math
import pickle

def frequency_unigram(words):
	findic = {}
	for i in range(len(words)):
		if words[i] not in findic:
			findic[words[i]]=0
		findic[words[i]]+=1
	return findic

def frequency_bigram_part2(words):
	findic = {}
	for i in range(len(words)-1):
		if (words[i],words[i+1]) not in findic:
			findic[(words[i],words[i+1])]=0
		findic[(words[i],words[i+1])]+=1
	return findic

def get_prob_dic(dicty,tags_unique):
	findic = {}
	total = 0
	for k,v in dicty.iteritems():
		total+=v
	for k,v in dicty.iteritems():
		findic[k] = math.log((v+1)/((total*1.0)+len(tags_unique)))
	for i in range(len(tags_unique)):
		if tags_unique[i] not in findic:
			findic[tags_unique[i]] = math.log((1)/((total*1.0)+len(tags_unique)))
	return findic

def Viterbit(obs, states, s_pro, t_pro, e_pro):
	# path = { s:[] for s in states} # init path: path[s] represents the path ends with s

	# Initializing step
	curr_pro = {}
	path = {}
	last_flag = 0
	for s in states:
		first_obs = obs[0]
		state_val = s
		emmi_prob = e_pro[first_obs][state_val]
		start_prob = s_pro[s]
		path[s] = []
		curr_pro[s] = start_prob+emmi_prob

	# Recurssion Step
	total_state_counts=0
	for i in xrange(1, len(obs)):
		last_pro = curr_pro
		curr_pro = {}
		for curr_state in states:
			max_pro = -999999999
			last_sta = -1
			for last_state in states:
				last_state_prob = last_pro[last_state] # last stage probability
				transition_prob = t_pro[last_state][curr_state] # transition probability
				emmision_prob = e_pro[obs[i]][curr_state] # emission probability
				tempmax = last_state_prob+transition_prob+emmision_prob # log probabilities are added
				if tempmax>max_pro:
					max_pro = tempmax
					last_sta = last_state
			# max_pro, last_sta = max(((last_pro[last_state]*t_pro[last_state][curr_state]*e_pro[obs[i]][curr_state], last_state) for last_state in states))
			curr_pro[curr_state] = max_pro
			total_state_counts+=1
			path[curr_state].append(last_sta) # storing the path for backtrack

	# Termination Step
	max_pro = -999999999
	last_flag = 1
	max_path = None
	for s in states:
		state_to_append = s
		path[state_to_append].append(state_to_append)
		cval = curr_pro[s]
		max_val = max_pro
		if cval <= max_val:
			pass
		else:
			max_path = path[s]
			max_pro = cval
		# print '%s: %s'%(curr_pro[s], path[s]) # different path and their probability
	# exit()
	return max_path

words = []
tags = []
words_unigram = {}
tags_unigram = {}
tags_bigram = {}
word_tag = {}
start_tags_x = []

#--------------------------------data preprocessing---------------------------------------------
flag=1 # this flag is used for getting the start words 
with open('train.txt') as f: # data in train corpus
	for line in f:
		split = line.split('\t')
		if len(split)>1:
			if split[0] != ".":
				word_val = split[0]
				tag_val = split[1].split('\n')[0]
				if flag==1:
					start_tags_x.append(tag_val)
					flag=0
				words.append(word_val) # word list 
				tags.append(tag_val) # tags list
				if word_val not in word_tag: # preparing words to tag count dictionary
					word_tag[word_val] = {}
				inner_tag_dic = word_tag[word_val]
				if tag_val not in inner_tag_dic:
					inner_tag_dic[tag_val]=0
				inner_tag_dic[tag_val]+=1
			else:
				flag=1

words_unigram_x = frequency_unigram(words)
tags_unigram = frequency_unigram(tags)
tags_bigram = frequency_bigram_part2(tags)
start_tags = frequency_unigram(start_tags_x)

#---------------------------------------Unknown words handling--------------------------------
# making UNK for words with 1 frequency for unknown words:

unk_words = []
count=0
for k,v in words_unigram_x.iteritems():
	if v!=1:
		words_unigram[k] = v
	else:
		unk_words.append(k)
		count+=1

words_unigram['<UNK>'] = count

# handling UNK for word-tag dictionary
unk_words_tags_extra = []
word_tag_x = word_tag
word_tag = {}
for k,v in word_tag_x.iteritems():
	if k in unk_words:
		unk_words_tags_extra.append(v)
	else:
		word_tag[k] = v

unk_tags_findic = {}
for i in range(len(unk_words_tags_extra)):
	for k,v in unk_words_tags_extra[i].iteritems():
		if k not in unk_tags_findic:
			unk_tags_findic[k] = 0
		unk_tags_findic[k]+=v

word_tag['<UNK>'] = unk_tags_findic

# removing redundant values
del words_unigram[';'] 
del tags_unigram[':']
del tags_bigram[(':','NN')]
del word_tag[';']

#----------------------------------smoothing and probability dictionaries creation-----------------------------------------------

# ||V|| values to smooth the probabilities
tags_unique = []
for k,v in tags_unigram.iteritems():
	if k not in tags_unique:
		tags_unique.append(k)

# emission probabilities smoothing
words_tag_prob = {}
for k,v in word_tag.iteritems(): # word-tags probabilities
	temp = {}
	for key,val in v.iteritems(): # smoothing the values for which are present
		temp[key] = math.log((val+1.0)/((tags_unigram[key]*1.0)+(len(tags_unique))))
	for i in range(len(tags_unique)):
		if tags_unique[i] not in temp: # smoothing absent values
			temp[tags_unique[i]] = math.log((1.0)/((tags_unigram[tags_unique[i]]*1.0)+(len(tags_unique))))
	words_tag_prob[k] = temp

tags_bigram_y = tags_bigram
tags_bigram = {}
for k,v in tags_bigram_y.iteritems():
	tag1 = k[0]
	tag2 = k[1]
	if tag1 not in tags_bigram:
		tags_bigram[tag1] = {}
	tags_bigram[tag1][tag2] = v

# transition probabilities smoothing
tags_bigram_prob = {}
for k,v in tags_bigram.iteritems(): # bigram tags probabilities
	temp = {}
	for key,val in v.iteritems(): # smoothing the values for which are present
		temp[key] = math.log((val+1.0)/((tags_unigram[k]*1.0)+(len(tags_unique))))
	for i in range(len(tags_unique)):
		if tags_unique[i] not in temp: # smoothing absent values
			temp[tags_unique[i]] = math.log((1.0)/((tags_unigram[k]*1.0)+(len(tags_unique))))
	tags_bigram_prob[k] = temp 
	# tags_bigram_prob[k] = math.log(v/(tags_unigram[k[0]]*1.0))


start_tags_prob = get_prob_dic(start_tags,tags_unique)
transtion_prob_tags = tags_bigram_prob
emission_prob_word_tags = words_tag_prob

# with open('emission_dic.pkl','wb') as f:
# 	pickle.dump(emission_prob_word_tags,f)

#--------------------------------------implementing veterbi--------------------------------------

# obs = ['i','want','to','have','dinner']
# obs = ['next','thursday']
# obs = ['like','to','go','to','a','fancy','japanese','restaurant']
# obs = ['dinner']
# obs = ['as','far','away', 'as', 'we', 'can', 'get']
test_data = []
with open('test.txt') as f:
	for line in f:
		test_data.append(line.split('\n')[0])

ccv=0
obs = []
predicted_tags = []
towrite_data = []
for i in range(len(test_data)):
	ccv+=1
	if test_data[i] != '':
		# print test_data[i],obs
		if (test_data[i] not in words_unigram) and (test_data[i] != '.'):
			obs.append('<UNK>')
		elif test_data[i] == '.':
			pass
		else:
			obs.append(test_data[i])
	else:
		# print ccv
		# print obs
		if len(obs)>0:
			tempo = Viterbit(obs,tags_unique,start_tags_prob,transtion_prob_tags,emission_prob_word_tags)
			# print tempo
			for kama in range(len(tempo)):
				towrite_data.append(obs[kama]+"\t"+tempo[kama]+"\n")
				predicted_tags.append(tempo[kama])
		towrite_data.append(str(".\t.\n"))
		towrite_data.append("\n")
		obs = []

accuracy_count = 0
for i in range(len(tags)):
	if tags[i]==predicted_tags[i]:
		accuracy_count+=1

print accuracy_count/(1.0*len(tags))











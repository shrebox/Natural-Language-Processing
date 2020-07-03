import os
import gensim.models as models
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import random,numpy as np

def read_total_data(): # reading the total data
	data = {}
	for i in os.listdir('20_newsgroups/'):
		corpus = []
		for j in sorted(os.listdir('20_newsgroups/'+i)):
			temp_data = open('20_newsgroups/'+i+'/'+j,'rb').read().decode('utf-8', 'ignore').lower()
			temp_data = word_tokenize(temp_data)
			corpus.append(temp_data)
		data[i] = corpus
	return data

def read_train_data(data): #  preparing the train data
	t_train_data = []
	for i,name in enumerate(data):
		temp = []
		if name != "comp.graphics":
			for j in range(1,len(data[name])):
				temp2 = TaggedDocument(data[name][j], [j+i*1000])
				temp.append(temp2)	
		else:
			for j in range(20,len(data[name])):
				temp2 = TaggedDocument(data[name][j], [j+i*1000])
				temp.append(temp2)
		t_train_data.extend(temp)
	return t_train_data

def test_data(data): # preparing test data
	t_from_graphics_19_others = data['comp.graphics'][1:20]
	t_one_each_groups={}
	for i in data:
		if i!="comp.graphics":
			t_one_each_groups[i] = data[i][0]
	return t_from_graphics_19_others,t_one_each_groups

def train_model(train_data): # training and saving model
	model = models.doc2vec.Doc2Vec(vector_size=100,min_count=6,window=10,workers=4,epochs=15)
	temp_train = train_data
	model.build_vocab(temp_train)
	model.train(temp_train, total_examples=model.corpus_count, epochs=model.epochs)
	model.save("doc2vec_trained_newsgroup.model")
	# print("Model Saved")
	return model

# -------------------------------Runner functions for reading the data and training the model-----------------------------
data = read_total_data()
train_data = read_train_data(data)
from_graphics_19_others,one_each_groups = test_data(data)
model = train_model(train_data)

# --------------------------------------------Similarity for different groups----------------------------------------------
different_groups_results = {}
for i,doc in enumerate(one_each_groups):
	#  calculating the similarity and appending to the results; cosine similarity is calculated
	t_num = np.dot(model.infer_vector('20_newsgroups/'), model.infer_vector(one_each_groups[doc]))
	t_deno = np.linalg.norm(model.infer_vector('20_newsgroups/'))*np.linalg.norm(model.infer_vector(one_each_groups[doc]))
	different_groups_results[doc] = t_num/(t_deno)
print(different_groups_results)

# calculating the normalized accuracy
diff_acc = 0
for k,v in different_groups_results.iteritems():
	diff_acc+=v
print (diff_acc)/len(different_groups_results)

# -----------------------------------------------Similarity for same group----------------------------------------------
same_group_results = []
for i,doc in enumerate(from_graphics_19_others):
	#  calculating the similarity and appending to the results; cosine similarity is calculated
	t_num = np.dot(model.infer_vector('20_newsgroups/'), model.infer_vector(doc))
	t_deno = np.linalg.norm(model.infer_vector('20_newsgroups/'))*np.linalg.norm(model.infer_vector(doc))
	same_group_results.append(t_num/(t_deno))
print(same_group_results)

# calculating the normalized accuracy
same_diff = 0
for i in range(len(same_group_results)):
	same_diff+=same_group_results[i]
print (same_diff)/len(same_group_results)


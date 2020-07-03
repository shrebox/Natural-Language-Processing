
data_to_write = []
#--------------------------------data preprocessing---------------------------------------------
flag=1 # this flag is used for getting the start words 
with open('train.txt') as f: # data in train corpus
	for line in f:
		split = line.split('\t')
		# if len(split)>1:
		# if split[0] != ".":
		word_val = split[0]
		data_to_write.append(word_val)

with open('test.txt','wb') as f:
	for i in range(len(data_to_write)):
		if data_to_write[i]!="\n":
			f.write(data_to_write[i]+"\n")
		else:
			f.write(data_to_write[i])


		# 	tag_val = split[1].split('\n')[0]
		# 	if flag==1:
		# 		start_tags_x.append(tag_val)
		# 		flag=0
		# 	words.append(word_val) # word list 
		# 	tags.append(tag_val) # tags list
		# 	if word_val not in word_tag: # preparing words to tag count dictionary
		# 		word_tag[word_val] = {}
		# 	inner_tag_dic = word_tag[word_val]
		# 	if tag_val not in inner_tag_dic:
		# 		inner_tag_dic[tag_val]=0
		# 	inner_tag_dic[tag_val]+=1
		# else:
		# 	flag=1
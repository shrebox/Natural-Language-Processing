import spacy

def read_document(filepath):
	temp = ""
	with open(filepath) as f:
		for line in f:
			temp += str(line) + " "
	f.close()
	return unicode(temp)

inputval = str(raw_input("1. Sentence 2. Document 3. Test sentence\n"))

data = ""
if inputval == "1":
	data = unicode(str(raw_input("Enter Sentence: ")))

elif inputval == "2":
	filepath = str(raw_input("Enter document path: "))
	data = read_document(filepath)

else:
	data = unicode("Apple is looking at buying U.K. startup for $1 billion")

# https://spacy.io/usage/linguistic-features

print "\n----part 1----\n"

model = spacy.load('en')

parsed_data = model(data)

print "Token Lemma POS TAG DEP" # POS = Lemma: The base form of the word; POS: The simple part-of-speech tag; Tag: The detailed part-of-speech tag; Dep: Syntactic dependency, i.e. the relation between tokens.
for token in parsed_data:
    print token, token.lemma_, token.pos_, token.tag_, token.dep_

print "\n----part 2----\n"

inputval = str(raw_input("1. Sentence 2. Document 3. Test sentence\n"))

data = ""
if inputval == "1":
	data = unicode(str(raw_input("Enter Sentence: ")))

elif inputval == "2":
	filepath = str(raw_input("Enter document path: "))
	data = read_document(filepath)

else:
	data = unicode("Apple is looking at buying U.K. startup for $1 billion")

model = spacy.load('en_core_web_sm')

parsed_data = model(data)

for ent in parsed_data.ents:
    print ent.text, ent.start_char, ent.end_char, ent.label_

# https://spacy.io/usage/vectors-similarity

print "\n----part 3----\n"

data = ""

w1 = str(raw_input("Enter first word: "))
w2 = str(raw_input("Enter second word: "))

data+=w1+" "+w2
data = unicode(data)

model = spacy.load('en_core_web_md')

parsed_data = model(data)

print ""

for t1 in parsed_data:
	for t2 in parsed_data:
		if t1.text == w1 and t2.text==w2:
			print t1.text, t2.text, t1.similarity(t2)
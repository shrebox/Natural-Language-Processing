import gensim

from gensim.models import KeyedVectors

filename = "GoogleNews-vectors-negative300.bin"

model = KeyedVectors.load_word2vec_format(filename, binary=True)

result1 = model.most_similar(positive=['China','Delhi'], negative=['India'],topn=1)

result2 = model.most_similar(positive=['USA','ISRO'], negative=['India'],topn=1)

print result1,result2
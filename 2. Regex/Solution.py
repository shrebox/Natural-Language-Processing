import re

def count_paragraphs(infile):
    inf = open(infile,'r')
    count = 0
    # pat = re.compile(r'[.!?]+[\]})>\'\"]*\n[\n]+') # if we consider paragraph is 2 or more \n are present
    pat = re.compile(r'[.!?]+[\]})>\'\"]*([\n]+|\Z)')
    total = ""
    for i in inf:
        total+=i
    return len(pat.findall(total))

def count_words(infile):
    pat = re.compile(r'.*[A-Za-z0-9].*')
    data = ""
    with open(infile,'r') as f:
        for line in f:
            data+=line
    tok = re.split(r'\s+',data)
    filtered = []
    for i in range(len(tok)):
        if pat.match(tok[i]):
            filtered.append(tok[i])
    return len(filtered) 

def count_sentences(infile):
    inf = open(infile,'r')
    count = 0
    pat = re.compile(r'[.!?]+[\])}>\'\"]*(\n|\Z)|[.!?]+[\])}>\'\"]*[\s]+[\"\'{\[(<]*[A-Z0-9]')
    linn = 0
    for i in inf:
        linn+=1
        i = re.sub(r'Dr. |Ms. |Mr. |Mrs. |Er. ','',i)
        count+=len(pat.findall(i))
    return count

def task2(word,infile):
    pat = re.compile(r'[.!?]+[>)\'}\]\"]*(\s|\n|\Z)+[\'\"{\[\(<]*'+word+r'[^A-Za-z0-9]')
    data = ""
    with open(infile,'r') as f:
        for line in f:
            data+=line
    return len(pat.findall(data))

def task3(word,infile):
    inf = open(infile,'r')
    count=0
    pat = re.compile(r'[^A-Za-z0-9]'+word+r'([.!?]+[\])}>\'\"]*(\n|\Z)|[.!?]+[\])}>\'\"]*[\s]+[\"\'{\[(<]*[A-Z0-9])')
    linn=0
    for i in inf:
        linn+=1
        i = re.sub(r'Dr. |Ms. |Mr. |Mrs. |Er. ','',i)
        count+=len(pat.findall(i))
    return count

def task4(word,infile):
    inf = open(infile,'r')
    count=0
    pat = re.compile(r'(^|[^a-zA-Z0-9])['+word[0].lower()+word.upper()+r']'+word[1:len(word)]+r'([^a-zA-Z0-9]|$)')
    linn=0
    for i in inf:
        linn+=1
        count+=len(pat.findall(i))
    return count

file_name = raw_input("Input the file path: ")

while(True):
    try:
        print "-------------------------------------------"
        print " 1. # of paragraphs, sentences and words\n 2. # of sentences starting with input word\n 3. # of sentences ending with input word\n 4. # of occurrences of input word\n 5. Change test set file\n 6. Exit!\n-------------------------------------------"
        option = raw_input("Enter: ")
        option = int(option)
        if option==1:
            print ""
            print "Paragraphs: "+ str(count_paragraphs(file_name))
            print "Sentences: "+ str(count_sentences(file_name))
            print "Words: "+ str(count_words(file_name))
            print ""
        elif option==2:
            word = raw_input("Enter word: ")
            print task2(word,file_name)
        elif option==3:
            word = raw_input("Enter word: ")
            print task3(word,file_name)
        elif option==4:
            word = raw_input("Enter word: ")
            print task4(word,file_name)
        elif option==5:
            word = raw_input("Enter file path: ")
            file_name = word
        else:
            print "Bye!"
            break
    except:
        print "Enter valid option!!"



from math import log, sqrt
from nltk.stem.porter import PorterStemmer
import re
import sys
from nltk import pos_tag, word_tokenize
from nltk.corpus import sentiwordnet

stemmer = PorterStemmer()
#read in +ve, -ve  li

stopwordsFiles = open(r"C:\Users\Administrator\Desktop\Testing\stopwords.txt", "r")
stopwords = stopwordsFiles.read().splitlines()
stopwordsFiles.close()


File = open(r'C:\Users\Administrator\Desktop\Testing\training-data1.txt',"r")		
Content = File.read().splitlines()
File.close()


File = open(r'C:\Users\Administrator\Desktop\Testing\HackathonInput.txt',"r")		
TestContent = File.read().splitlines()
File.close()


PostiveLines = []
neglines = []

for line in Content:
	Token = [word.strip() for word in line.split("\t")]
	#print Token
	if (len(Token) == 2):
		Comment = re.sub(r'[^A-Za-z0-9.\s]+', '',Token[1])
		if Token[0] == '1':
			PostiveLines.append(Comment)
			#print line, "Positive"
		else:	
			neglines.append(Comment)
			#print line, "Negative"


#print len(PostiveLines), len(neglines), len(stopwords)



poslinesTrain = PostiveLines[:len(PostiveLines)]
neglinesTrain = neglines[:len(neglines)]


def CountPotentialWords(line):
	cWords = 0
	Rawtoken = word_tokenize(line)
	
	TaggedWords = pos_tag(Rawtoken)
	#print TaggedWords
	#for word in TaggedWords:
	for word in TaggedWords:	
		if "J" in word[1] or "RB" in word[1] :
			cWords = cWords + 1
	return cWords




trainset = [(x, 1) for x in poslinesTrain] + [(x, -1) for x in neglinesTrain]

#testset = [(x, 1) for x in poslinesTest] + [(x, -1) for x in neglinesTest]

#init stemmer for stemming (pruning words)
stemmer = PorterStemmer()

def getwords(sentence):

	
	w = sentence.split()
	
	#remove words which are lesser than 3 characters
	w = [ x for x in  w if len(x) > 2]
	
	#get rid of all stopwords
	w = [ x for x in w if not x in stopwords]
	
	#stem each words
	w = [stemmer.stem(x) for x in w]
	
	#add bigrams
	#w = w + [w([i] + ' ' + w[i + 1] for in in range(len(w) - 1)]
	
	#get rid of duplicates
	w = list(set(w))
	
	return w
	

freq = {}
trainfeatures = []

#for each line and label in training set
for line, label in trainset:
	words = getwords(line)
	
	#for each word in a pruned sentence
	for word in words:
		freq[word] = freq.get(word, 0) + 1
	
	trainfeatures.append((words,label))
	
#evaluate test set
#Numerator
Ntr = len(trainset)
wrong = 0 #store count of misclassifications

for line in TestContent:
		
	testwords = getwords(line)
	
	#we will store distances to all train reviews in this list as tuples of (socre, label)
	#To be sorted by score later
	
	results = []
	
	
	#compute similarity between testword and  every review/trained
	for i, (trainwords, trainlabel) in enumerate(trainfeatures):
	
		#find all common words between these two sentences
		commonwords = [x for x in trainwords if x in testwords]
		
		#accumulate score for all overlaps. Common words count for less 
		#log() function squashes things down so that infrequent words dont count for much
		
		score = 0.0
		
		for word in commonwords:
			score += log(Ntr / freq[word])
			
		#print score, trainlabel
		results.append((score, trainlabel))
		
	#sort similarity based on high scores (descending order)
	results.sort(reverse=True)
	
	#Classify based on the top 5 scores
	toplab = [x[1] for x in results[:10]]
	#number one
	numones = toplab.count(1)
	#negative number one
	numnegones = toplab.count(-1)
	prediction = 1
	
	
	flag = 0
	
	if (numones >= 6):
		if flag == 1:
			print "POSITIVE","+ve=%f -ve=%f %s" % ( numones, numnegones, line)
		print "Positive"
	elif (numones <= 4):
		if flag == 1:
			print "NEGATIVE","+ve=%f -ve=%f %s" % ( numones, numnegones, line)
		print "Negative"
	else:
		if flag == 1:	
			print "NEUTRAL","+ve=%f -ve=%f %s" % ( numones, numnegones, line)
		print "Neutral"
	
	

	
	
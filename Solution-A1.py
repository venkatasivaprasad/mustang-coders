from math import log, sqrt
from nltk.stem.porter import PorterStemmer
import re
import sys
from nltk import pos_tag, word_tokenize
from nltk.corpus import sentiwordnet

from os import listdir
from os.path import isfile, join

def LoadTrainSet():
	POSITIVEpath = "C:\Users\Administrator\Desktop\Testing\Postive"
	NEGATIVEpath = "C:\Users\Administrator\Desktop\Testing\Negative"
	
	onlyfiles = [ f for f in listdir(POSITIVEpath) if isfile(join(POSITIVEpath,f)) ]
	
	for f in onlyfiles:
		File = open(POSITIVEpath+ "\\"+f ,"r")		
		Content = File.read().splitlines()
		File.close()	

		for line in Content:
			PostiveLines.append(re.sub(r'[^A-Za-z0-9.\s]+', '',line))
			y = 1

	onlyfiles = [ f for f in listdir(NEGATIVEpath) if isfile(join(NEGATIVEpath,f)) ]			
			
	for f in onlyfiles:
		File = open(NEGATIVEpath+ "\\"+f ,"r")		
		Content = File.read().splitlines()
		File.close()	

		for line in Content:
			neglines.append(re.sub(r'[^A-Za-z0-9.\s]+', '',line))
			



stemmer = PorterStemmer()
#read in +ve, -ve  li

stopwordsFiles = open(r"C:\Users\Administrator\Desktop\Testing\stopwords.txt", "r")
tstopwords = stopwordsFiles.read().splitlines()
stopwordsFiles.close()

stopwords = [stemmer.stem(x.strip().lower()) for x in tstopwords]



#print stopwords
	





File = open(r'C:\Users\Administrator\Desktop\Testing\HackathonInput.txt',"r")		
TestContent = File.read().splitlines()
File.close()

File = open(r'C:\Users\Administrator\Desktop\Testing\training-data1.txt',"r")		
Content = File.read().splitlines()
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

LoadTrainSet()

#print len(PostiveLines), len(neglines), len(stopwords)


#there are more than 4800 positives and negatives
#take first 4800 as training set, leaving rest for validation
#N = 

poslinesTrain = PostiveLines[:len(PostiveLines)]
neglinesTrain = neglines[:len(neglines)]

#print len(poslinesTrain), len(neglinesTrain), len(stopwords)


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


#init stemmer for stemming (pruning words)
stemmer = PorterStemmer()


#create the train set and test set by attaching labels to text to form a list of tuples (sentence, label)
#Label or tag 1 is positive and -1 is negative
trainset = [(x, 1) for x in poslinesTrain] + [(x, -1) for x in neglinesTrain]

#testset = [(x, 1) for x in poslinesTest] + [(x, -1) for x in neglinesTest]


def getwords(sentence):
	"""
	this method returns important words from a sentence as list
	you can comment/uncomment lines as you experiment with results
	"""
	sentence = sentence.lower()
	
	w = sentence.split()
	
	#remove words which are lesser than 3 characters
	w = [ x for x in  w if len(x) > 2]
	
	#stem each words
	w = [stemmer.stem(x) for x in w]

	#get rid of all stopwords
	w = [ x for x in w if not x in stopwords]
	

	
	#add bigrams
	#w = w + [w([i] + ' ' + w[i + 1] for in in range(len(w) - 1)]
	
	#get rid of duplicates
	w = list(set(w))
	
	return w


if(0):
	for line in TestContent:
		print line,getwords(line)
		Words = getwords(line)
		for w in Words:
			print w, w in stopwords
		
	sys.exit(0)	

#compute frequency of every word in the train set. We will want common words
#to count for less in our later analysis
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
			#print word,freq[word] ,log(Ntr / freq[word])
			
		#print line,score, trainlabel
		results.append((score, trainlabel))
		
	#sort similarity based on high scores (descending order)
	results.sort(reverse=True)
	
	if(0):
		print testwords
		for word in testwords:
			if word in stopwords:
				print word, freq.get(word, 0)
	
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
	

	
	
import nltk
import os, operator, re
import random
import pickle
import os.path


#folder = "20_newsgroups/rec.motorcycles/"

def get_all_tokens(folder_name):
	folder = "20_newsgroups/" + folder_name + "/"
	all_tokens = []
	for f in os.listdir(folder):
		file = open(folder + f, 'r')
		temp = nltk.word_tokenize(file.read())
		all_tokens += temp
		file.close()

	return all_tokens

def get_uni_freq(all_tokens):
	uni_freq = {}
	for t in all_tokens:
		if t in uni_freq:
			uni_freq[t]+=1
		else:
			uni_freq[t]=1

	return uni_freq

def unigram_model(all_tokens, name):
	if os.path.isfile(name + "_unigram_model"):
		file = open(name + "_unigram_model", 'rb')
		unigram = pickle.load(file)
		file.close()
		return unigram
	# Unigram model
	uni_freq = get_uni_freq(all_tokens)
	unigram = sorted(uni_freq.items(), key=operator.itemgetter(1), reverse = True)
	file = open(name + "_unigram_model", 'wb')
	pickle.dump(unigram, file)
	file.close()
	return unigram


def unigram_sentence(all_tokens, name):
	unigram = unigram_model(all_tokens, name)
	total = len(all_tokens)

	print("Unigram sentence generation. (Choosing by max frequency)")
	# Unigram sentence generation
	th = 1
	uni_sentence = ""
	i = 0
	while pow(th, 1/float(i+1)) > 0.01:
		th *= float(unigram[i][1])/total
		word = re.search('[^A-z0-9]', unigram[i][0])
		if not word:
			uni_sentence += unigram[i][0] + " "
		i = i+1

	uni_sentence += "."
	print(uni_sentence)
	print("")

	th = 1
	i = 0
	uni_sentence = ""
	while pow(th,1/float(i+1)) > 0.00009:
		i = i+1
		index = random.randint(0, len(unigram))
		th *= float(unigram[index][1])/total
		if unigram[index][0] == "." or unigram[index][0] == "!" or unigram[index][0] == "?":
			uni_sentence += unigram[index][0]
			break
		uni_sentence += unigram[index][0] + " "

	if uni_sentence[-1] != ".":
		uni_sentence += "."

	print("Unigram sentence generation. (Choosing randomly)")
	print(uni_sentence)
	print("")

def get_bi_freq(all_tokens):
	bi_freq = {}
	for i in range(len(all_tokens)-1):
		token = all_tokens[i]
		next_token = all_tokens[i+1]
		if token != next_token:
			if token in bi_freq:
				if next_token in bi_freq[token]:
					bi_freq[token][next_token] +=1
				else:
					bi_freq[token][next_token] = 2 #add one smoothing
			else:
				bi_freq[token] = {}
				bi_freq[token][next_token] = 2 #add one smoothing

	return bi_freq


def bigram_model(all_tokens, name):
	# Bigram model
	if os.path.isfile(name + "_bigram_model"):
		file = open(name + "_bigram_model", 'rb')
		bigram = pickle.load(file)
		file.close()
		return bigram

	bi_freq = get_bi_freq(all_tokens)
	bigram = {}
	for token in bi_freq:
		bigram[token] = sorted(bi_freq[token].items(), key=operator.itemgetter(1), reverse = True)

	file = open(name + "_bigram_model", 'wb')
	pickle.dump(bigram, file)
	file.close()
	return bigram
	

def bigram_sentence(all_tokens, name):
	uni_freq = get_uni_freq(all_tokens)
	bigram = bigram_model(all_tokens, name)

	# Bigram sentence generation
	print("Bigram sentence generation")
	prev = "Consider"
	bi_sentence = prev + " "
	th = 1
	i = 0 
	while pow(th,1/float(i+1)) > 0.1:
		if prev in bigram and len(bigram[prev])>0:
			bi_sentence += bigram[prev][0][0] + " "
			th *= float(bigram[prev][0][1])/uni_freq[prev]
			temp = bigram[prev][0][0]
			del bigram[prev][0]
			prev = temp
			i = i+1
		else:
			break

	print(bi_sentence + "\n")


def trigram_model(all_tokens, name):
	# Trigram Model
	if os.path.isfile(name + "_trigram_model"):
		file = open(name + "_trigram_model", 'rb')
		trigram = pickle.load(file)
		file.close()
		return trigram


	tri_freq = {}
	for i in range(len(all_tokens) - 2):
		token = all_tokens[i] + " " + all_tokens[i+1]
		next_token = all_tokens[i+2]
		if token in tri_freq:
			if next_token in tri_freq[token]:
				tri_freq[token][next_token] +=1
			else:
				tri_freq[token][next_token] = 1
		else:
			tri_freq[token] = {}
			tri_freq[token][next_token] = 1

	trigram = {}
	for token in tri_freq:
		trigram[token] = sorted(tri_freq[token].items(), key=operator.itemgetter(1), reverse = True)

	file = open(name + "_trigram_model", 'wb')
	pickle.dump(trigram, file)
	file.close()

	return trigram

def trigram_sentence(all_tokens, name):
	
	trigram = trigram_model(all_tokens, name)
	# Trigram sentence generation
	print("Trigram sentence generation")
	prev = "You are"
	tri_sentence = prev + " "
	for i in range(20):
		if prev in trigram:
			tri_sentence += trigram[prev][0][0] + " "
			temp = prev.split()
			prev = temp[1] + " " + trigram[prev][0][0]

	if tri_sentence[-1] != ".":
		tri_sentence += "."

	print(tri_sentence + "\n")


def calculate_prob(unigram, bigram, words, total):
	prob = 1
	prev = words[0]
	V = len(unigram)
	if len(words) == 1:
		if words[0] in unigram:
			return float(unigram[words[0]])/total
		else:
			return 1.0/total
	for i in range(1, len(words)):
		if prev in bigram:
			if words[i] in bigram[prev]:
				prob *= float(bigram[prev][words[i]])/(unigram[prev] + V) 
			else:
				prob *= 1.0/(unigram[prev] + V)
			prev = words[i]
		else:
			prob *= 1.0/V 
			
	#print (prob)
	return prob



def discriminative_model(sentence, graphics, motorcycles):
	gp = get_bi_freq(graphics)
	mc = get_bi_freq(motorcycles)

	uni_gp = get_uni_freq(graphics)
	uni_mc = get_uni_freq(motorcycles)

	words = nltk.word_tokenize(sentence)
	prob_gp = calculate_prob(uni_gp, gp, words, len(graphics))
	prob_mc = calculate_prob(uni_mc, mc, words, len(motorcycles))

	if prob_mc>prob_gp:
		print("Belongs to motorcycles news group.")
	else:
		print("Belongs to graphics news group.")

def calculate_prob_unk(unigram, bigram, words):
	V = len(unigram)
	prob = 1
	prev = words[0]
	for i in range(1, len(words)):
		if prev in bigram:
			if words[i] in bigram[prev]:
				prob *= float(bigram[prev][words[i]])/(unigram[prev] + V)
				prev = words[i]
			else:
				if '<UNK>' in bigram[prev]:
					prob *= float(bigram[prev]['<UNK>'])/(unigram[prev] + V)
				else:
					prob *= 1.0/(unigram['<UNK>'] + V)
				prev = '<UNK>'		
		else:
			prob *= 1.0/(unigram['<UNK>'] + V)
			if words[i] in bigram:
				prev = words[i]
			else:
				prev = '<UNK>'
	return prob
	

def create_unk(all_tokens, sentence):
	total = len(all_tokens)
	unigram = get_uni_freq(all_tokens)
	new_unigram = {}
	uni_prob = {}

	for i in unigram:
		uni_prob[i] =  float(unigram[i])/total

	for i in range(total):
		if unigram[all_tokens[i]] < 2:
			if '<UNK>' in new_unigram:
				new_unigram['<UNK>'] += unigram[all_tokens[i]]
			else:
				new_unigram['<UNK>'] = unigram[all_tokens[i]]
			all_tokens[i] = '<UNK>'
		else:
			new_unigram[all_tokens[i]] = unigram[all_tokens[i]]

	bigram = get_bi_freq(all_tokens)

	words = nltk.word_tokenize(sentence)
	if len(words) == 1:
		if words[0] in new_unigram:
			prob = float(new_unigram[words[0]])/total
		else:
			prob = 1.0/total # can make it oneo
	else:
		prob = calculate_prob_unk(new_unigram, bigram, words)

	#print (total)
	#print (prob)
	return prob


def unk_model(sentence, graphics, motorcycles):
	prob_gp = create_unk(graphics, sentence)
	prob_mc = create_unk(motorcycles, sentence)

	if prob_mc>prob_gp:
		print("Belongs to motorcycles news group.")
	else:
		print("Belongs to graphics news group.")



motorcycles = get_all_tokens('rec.motorcycles')
graphics = get_all_tokens('comp.graphics')

unigram_sentence(motorcycles, "motorcycles")
unigram_sentence(graphics, "graphics")
bigram_sentence(motorcycles, "motorcycles")
bigram_sentence(graphics, "graphics")
trigram_sentence(motorcycles, "motorcycles")
trigram_sentence(graphics, "graphics")

discriminative_model("motorcycles are", graphics, motorcycles)
unk_model("motorcycles are", graphics, motorcycles)




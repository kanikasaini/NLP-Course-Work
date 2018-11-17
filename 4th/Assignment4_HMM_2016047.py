#Kanika Saini 2016047
import pickle

def train():
	folder = "Training set_HMM.txt"
	file = open(folder, 'r')
	data = file.read()

	sentences = data.split('\n\n')
	del(sentences[len(sentences)-1])

	tag_count = {}
	transition_prob = {}
	emission_prob = {}
	words = []

	prev_tag = 'start'
	for i in range(len(sentences)):
		s = sentences[i].split('\n')
		for j in range(len(s)):
			temp = s[j].split('\t')
			word = temp[0]
			tag = temp[1]

			if word not in words:
				words.append(word)

			if word in emission_prob:
				if tag in emission_prob[word]:
					emission_prob[word][tag] += 1
				else:
					emission_prob[word][tag] = 2
			else:
				emission_prob[word] = {}
				emission_prob[word][tag] = 2

			if tag in tag_count:
				tag_count[tag] +=1
			else:
				tag_count[tag] = 0

			if prev_tag in transition_prob:
				if tag in transition_prob[prev_tag]:
					transition_prob[prev_tag][tag] +=1
				else:
					transition_prob[prev_tag][tag] = 2
			else:
				transition_prob[prev_tag] = {}
				transition_prob[prev_tag][tag] = 2

			prev_tag = tag

	transition_file = open('transition_file', 'wb')
	emission_file = open('emission_file', 'wb')
	tag_file = open('tag_file', 'wb')
	vocab_file = open('vocab_file', 'wb')
	pickle.dump(transition_prob, transition_file)
	pickle.dump(emission_prob, emission_file)
	pickle.dump(tag_count, tag_file)
	pickle.dump(words, vocab_file)

	#dump models to files

def viterbi(sentence):
	transition_file = open('transition_file', 'rb')
	emission_file = open('emission_file', 'rb')
	tag_file = open('tag_file', 'rb')
	vocab_file = open('vocab_file', 'rb')

	transition_prob = pickle.load(transition_file)
	emission_prob = pickle.load(emission_file)
	tag_count = pickle.load(tag_file)
	vocab = pickle.load(vocab_file)
	V = len(vocab)

	s = sentence.split('\n')
	tags = list(tag_count.keys())
	total_tags = len(tags)
	dp = [[0 for i in range(len(s))] for i in range(len(tags))] #intialising the dp matrix with 0 values
	POStags = ['NULL' for i in range(len(s))]

	pointer = [[{'row':0, 'col':0} for i in range(len(s))] for i in range(len(tags))]

	for j in range(len(s)):
		for i in range(len(tags)):
			if j==0:
				if s[j] not in vocab:
					if tags[i] in transition_prob['start']:
						dp[i][j] = (transition_prob['start'][tags[i]]/(tag_count[tags[i]] + total_tags)) * 1.0/V
					else:
						dp[i][j] = (1.0/(tag_count[tags[i]] + total_tags)) * 1.0/V
				else:			
					if tags[i] not in emission_prob[s[j]]:
						dp[i][j] = 0
					elif tags[i] in transition_prob['start']:
						dp[i][j] = (transition_prob['start'][tags[i]]/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V)
					else:
						dp[i][j] = (1.0/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V)				
			else:
				for k in range(len(tags)):
					if s[j] not in vocab:
						if tags[i] in transition_prob[tags[k]]:
							if dp[i][j] < dp[k][j-1] * (transition_prob[tags[k]][tags[i]]/(tag_count[tags[i]] + total_tags)) * 1.0/V:
								pointer[i][j]['row'] = k
								pointer[i][j]['col'] = j-1
							dp[i][j] = max(dp[i][j], dp[k][j-1] * (transition_prob[tags[k]][tags[i]]/(tag_count[tags[i]] + total_tags)) * 1.0/V)
						else:
							if dp[i][j] < dp[k][j-1] * (1.0/(tag_count[tags[i]] + total_tags)) * 1.0/V:
								pointer[i][j]['row'] = k
								pointer[i][j]['col'] = j-1

							dp[i][j] = max(dp[i][j], dp[k][j-1] * (1.0/(tag_count[tags[i]] + total_tags)) * 1.0/V )


					else:
						if tags[i] not in emission_prob[s[j]]:
							dp[i][j] = 0
						elif tags[i] in transition_prob[tags[k]]:
							if dp[i][j] < dp[k][j-1] * (transition_prob[tags[k]][tags[i]]/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V):
								pointer[i][j]['row'] = k
								pointer[i][j]['col'] = j-1
							dp[i][j] = max(dp[i][j], dp[k][j-1] * (transition_prob[tags[k]][tags[i]]/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V))
						else:
							if dp[i][j] < dp[k][j-1] * (1.0/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V):
								pointer[i][j]['row'] = k
								pointer[i][j]['col'] = j-1
							dp[i][j] = max(dp[i][j], dp[k][j-1] * (1.0/(tag_count[tags[i]] + total_tags)) * emission_prob[s[j]][tags[i]]/(tag_count[tags[i]] + V))			

	row = 0
	col = len(s)-1
	maxdp = 0 
	for i in range(len(tags)):
		if dp[i][len(s)-1]>maxdp:
			maxdp = dp[i][len(s)-1]
			row = i

	POStags[len(s)-1] = s[-1]

	for i in range(len(s)-2, -1, -1):
		temp = pointer[row][col]
		POStags[i] = tags[temp['row']]
		row = temp['row']
		col = temp['col']

	for i in range(len(s)):
		print(POStags[i])

	return POStags

#train()
test_file = open('test.txt', 'r')
result_file = open('result.txt', 'w')
sentences = test_file.read().split('\n\n')

for i in range(len(sentences)):
	res = viterbi(sentences[i])
	words = sentences[i].split('\n')
	for j in range(len(res)):
		result_file.write(words[j] + '\t' + res[j] + '\n')
	result_file.write('\n')






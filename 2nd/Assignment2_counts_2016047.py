#Kanika Saini 2016047

import re;

def one(doc):
	para = re.findall('\n{2,}|[^a-zA-Z0-9\n]$', doc);
	print("Number of paragraphs: ", len(para));
	words = len(re.findall('\S+', doc)) - len(re.findall(' ([^a-zA-Z0-9 ]{1,}) ', doc));
	print("Number of words: ", words);
	sentences = len(re.findall('([!?\"\'] [A-Z])|(\. [A-Z\'\"])|(\n{2,}|[^a-zA-Z0-9\n]$)' , doc)) - len(re.findall('Dr\.|Mr\.|Mrs\.|Ms\.', doc));
	print("Number of sentences: ", sentences);


def two(doc, word):
	out = re.findall('(^' + word + ')|([.\'\"?!] ' + word + ')|([.\'\"?!] [\"\']' + word + ')|(\n' + word + ')', doc, re.IGNORECASE);
	print(len(out))

def three(doc, word):
	out =  re.findall(word + '(?=([!?\"\'] [A-Z])|(\. [A-Z\'\"])|([^a-zA-z0-9]*\n{2,}|[^a-zA-Z0-9\n]$))', doc);
	print(len(out));


def four(doc, word):	
	out = re.findall('(^|\\b)' + word + '($|\\b)', doc, re.IGNORECASE);
	print("Count of word: ", len(out));


file = open("37261", 'r');
doc = file.read();
flag = True;

while(flag):
	print("1. Number of paragraphs, sentences, and words contained in the article.\n");
	print("2. Given a word as input, number of sentences starting with the word.\n");
	print("3. Given a word as input, number of sentences ending with the word.\n");
	print("4. Given a word as input, count of that word in the input file.\n");
	print("5. Exit\n");
	option = int(input("Enter option: "));
	if (option == 1):
		one(doc);
	elif(option == 2):
		word = input("Enter the word: ");
		two(doc, word);
	elif(option == 3):
		word = input("Enter the word: ");
		three(doc, word);
	elif(option == 4):
		word = input("Enter the word: ");
		four(doc, word);
	else:
		flag = False;
	print("\n");

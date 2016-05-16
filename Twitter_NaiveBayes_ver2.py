import nltk;
import csv;
import json;

with open('train_new.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    all_tweets = []
    for row in reader:
        tweet_words = row['col2'].split()

        
        resultwords  = [word for word in tweet_words if not(word.lower().startswith('@'))]
        result = ' '.join(resultwords)

        #print result

       # json_obj = json.loads(row['col15'])
        #print(json_obj['label'])
        #tup = (result, json_obj['label'])
        tup = (result, row['col15'])
        all_tweets.append(tup)


print ('all_tweets list populated')


##        
##pos_tweets = [('I love this car', 'positive'),
##
##              ('This view is amazing', 'positive'),
##
##              ('I feel great this morning', 'positive'),
##
##              ('I am so excited about the concert', 'positive'),
##
##              ('He is my best friend', 'positive')]
##
##neg_tweets = [('I do not like this car', 'negative'),
##
##              ('This view is horrible', 'negative'),
##
##              ('I feel tired this morning', 'negative'),
##
##              ('I am not looking forward to the concert', 'negative'),
##
##              ('He is my enemy', 'negative')]



#################################
tweets = []

for (words, sentiment) in all_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

#print(tweets)



##Classifier


def get_words_in_tweets(tweets):
    all_words = []

    for (words, sentiment) in tweets:
        all_words.extend(words)

    return all_words

def get_word_features(wordlist):

    wordlist = nltk.FreqDist(wordlist)

    word_features = wordlist.keys()

    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))


def extract_features(document):

    document_words = set(document)

    features = {}

    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)

    return features


training_set = nltk.classify.apply_features(extract_features, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

print(word_features)

print(classifier.show_most_informative_features(32))


ofile  = open('final_new.csv','w',newline='')
writer = csv.writer(ofile)


with open('test_new.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    all_tweets = []
    for row in reader:
        tweet_words = row['col2'].split()

        
        resultwords  = [word for word in tweet_words if not(word.lower().startswith('@'))]
        result = ' '.join(resultwords)

        #print result

##        tweet = 'What I told you bout bullying my friend he dont like that https://t.co/0AV9dtF9Fg'
        

        resultwords  = [word for word in tweet_words if not(word.lower().startswith('@'))]
        result = ' '.join(resultwords)

        #print result

#        json_obj = json.loads(row['col15'])
       # print(json_obj['label'])
        
        writer.writerow([row['col1'],result,row['col3'],row['col4'],row['col5'],row['col6'],row['col7'],row['col8'],row['col9'],row['col10'],row['col11'],row['col12'],row['col13'],row['col14'],row['col15'],classifier.classify(extract_features(result.split()))])

        print(classifier.classify(extract_features(result.split())))


print("write completed")
ofile.close()

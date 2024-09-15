
import pandas as pd
import numpy as np
from collections import defaultdict
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sankey_test import make_sankey
from nltk.sentiment import SentimentIntensityAnalyzer
from exception_class import NLPError
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

class SentimentNLP:
    """
    class for analyzing text files using natural language processing
    """

    def __init__(self):
        # manage data about the different texts that
        # we register with the framework
        self.data = defaultdict(dict)
        self.Exception = NLPError()

    def _default_parser(self, filename):
        """
        Create a generic parser for simple text files
        :param filename (str): name of file
        :return results (dict): a dict of statistics for each text file, the state variable
        """
        # call the exceptions class which checks for exceptions in this function
        self.Exception._default_parser(filename)


        # read in txt file into string
        with open(filename) as f:
            content = f.read()

        # pre-process the content
        content = self.preprocess(content)

        # computes word count frequency for each text file
        wordcounts = SentimentNLP.count(content)

        # initializes nltk library
        sia = SentimentIntensityAnalyzer()

        # construct results dict to organize statistics for each file
        results = {
            'wordcount': wordcounts,
            'sentiment': sia.polarity_scores(content),
            'raw_text': content,
        }
        return results

    def preprocess(self, content):
        """
        cleans text file through pre-processing step
        :param content (str): the content of the file
        :return: text_data (str): cleaned version of content
        """
        # use NLTK for processing and cleaning
        text_data = content

        # take out punctuation and lowercase everything
        text_data = re.sub('[^a-zA-Z]', ' ', text_data)
        text_data = text_data.lower()
        text_data = text_data.split()

        # combine similar words
        wl = WordNetLemmatizer()

        # tale out non-english words and stop words
        text_data = [wl.lemmatize(word) for word in text_data if not word in set(stopwords.words('english'))]
        text_data = ' '.join(text_data)

        return text_data

    def count(content):
        """
        counts the number of words and appends into a dictionary
        (takes in a parsed/cleaned string from txt file)
        content (str): the contents of the file
        return: counts (dict): word count freq dictionary
        """

        # split the words
        counts = dict()
        words = content.split()

        # count the occurences of each word
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1

        return counts

    def _save_results(self, label, results):
        """ Integrate parsing results into internal state
        label (str): unique label for a text file that we parsed
        results: the data extracted from the file as a dictionary attribute-->raw data
        """
        # save the data in results to the object's dictionary, which holds all of the data for each file
        for k, v in results.items():
            self.data[k][label] = v

    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework, handles domain-specific parsers
        filename (str): name of the file
        label (str): unique label for a text file that we parsed
        parser (function): custom domain-specific parser to handle text file
         """

        # call the exceptions class which checks for exceptions in this function
        self.Exception.load_text(filename, label, parser)


        if parser is None:
            # do default parsing of standard .txt file
            results = self._default_parser(filename)

        else:
            # get the results using the user's parser
            results = parser(filename)

        # assign label to the filename if it was not given
        if label is None:
            label = filename

        # Save / integrate the data we extracted from the file
        # into the internal state of the framework
        self._save_results(label, results)

    def get_wordcount(self, word_list = None, k = 5):
        """
        filters word count dictionary based on user defined parameters
        :param word_list (lst): a list of words as string
        :param k (int): the k most common words across the files
        """

        # call the exceptions class which checks for exceptions in this function
        self.Exception.get_wordcount(word_list, k)

        # for default parameters
        if word_list == None:
            wordcount_dict = self.data["wordcount"]

            for filename in wordcount_dict:
                # extract k most common words
                temp_dict = dict(sorted(wordcount_dict[filename].items(), key=lambda x: x[1], reverse=True)[:k])
                wordcount_dict[filename] = temp_dict
        # for user defined parameters
        else:
            wordcount_dict = self.data["wordcount"]

            for filename in wordcount_dict:
                temp_dict = defaultdict(dict)
                # extract user defined set of words
                for key, value in wordcount_dict[filename].items():
                    if key in word_list:
                        temp_dict[key] = value

                wordcount_dict[filename] = temp_dict

        # save the new wordcounts to the object's data dictionary
        self.data["wordcount"] = wordcount_dict


    def wordcount_sankey(self, word_list=None, k=5):
        """
        create sankey visualization with user parameters
        :param word_list (lst): a list of words as string
        :param k (int): the k most common words across the files
        """
        # filter state variable with parameters
        self.get_wordcount(word_list, k)

        df_sankey = pd.DataFrame(columns=['text', 'word'])
        wordcount_dict = self.data["wordcount"]

        # iterate through dict to make dataframe
        for filename in wordcount_dict:
            for key, value in wordcount_dict[filename].items():
                for i in range(value):
                    new_row = pd.Series({'text': filename, 'word': key})
                    df_sankey = pd.concat([df_sankey, new_row.to_frame().T], ignore_index=True)

        # call sankey library
        make_sankey(df_sankey, df_sankey.columns, 0)

    def second_viz(self):
        """
        Create single visualization of a word cloud with subplots for each text file
        """

        # get the raw_text data to use for the plot
        text_content = self.data['raw_text']
        filename_lst = []
        text_lst = []

        # create list of text content
        for key, value in text_content.items():
            text_lst.append(value)
            filename_lst.append(key)

        # Create the figure and subplots
        fig, axs = plt.subplots(1, len(text_lst), figsize=(15, 5))

        # Create a word cloud for each subplot
        for i in range(len(text_lst)):
            ax = axs[i]
            wc = WordCloud(collocations=False, background_color="white").generate(text_lst[i])
            ax.imshow(wc, interpolation='bilinear')
            ax.set_title(filename_lst[i])
            ax.set_axis_off()

        # Adjust the layout
        plt.tight_layout()
        plt.show()



    def third_viz(self):
        """
        Create a multiple bar plot that compares positive vs negative sentiment scores for each file
        """

        # get the sentiment data to be used for the plot
        filenames = self.data["sentiment"].keys()
        pos_lst = []
        neg_lst = []

        # obtain pos and neg values for each file
        for filename in self.data["sentiment"]:
            pos_lst.append(self.data["sentiment"][filename]["pos"])
            neg_lst.append(self.data["sentiment"][filename]["neg"])

        # set width of bar
        barWidth = 0.25
        fig = plt.subplots(figsize=(12, 8))

        # Set position of bar on X axis
        br1 = np.arange(len(pos_lst))
        br2 = [x + barWidth for x in br1]

        # Make the plot
        plt.bar(br1, pos_lst, color='b', width=barWidth,
                edgecolor='grey', label='positive')
        plt.bar(br2, neg_lst, color='r', width=barWidth,
                edgecolor='grey', label='negative')

        # Add Xticks
        plt.xlabel('Text file', fontweight='bold', fontsize=15)
        plt.ylabel('Sentiment Score', fontweight='bold', fontsize=15)
        plt.xticks([r + barWidth for r in range(len(pos_lst))],
                   filenames)
        plt.title('Bar graph of sentiment scores for each file')
        plt.legend()
        plt.show()
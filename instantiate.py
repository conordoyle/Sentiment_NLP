"""
This file can be used to run Sentiment_NLP
"""

from Sentiment_NLP import SentimentNLP




object = SentimentNLP()

object.load_text('michael-jackson.txt')
object.load_text('lorde.txt')
object.load_text('rihanna.txt')
object.load_text('nirvana.txt')
object.load_text('amy-winehouse.txt')

# create sankey diagram
object.wordcount_sankey()

# create word cloud visualization
object.second_viz()

# create multiple bar plot
object.third_viz()








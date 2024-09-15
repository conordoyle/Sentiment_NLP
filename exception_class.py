"""
This exception class, NLPError, is reusable to test exceptions for different parsers
"""
from collections import defaultdict
import os
from sankey_test import make_sankey

class NLPError:
    """ A user-defined exception for signalling a
        grading application-specific issue """

    def __init__(self):
        self.data = defaultdict(dict)

    def _default_parser(self, filename):
        """ Creates generic parser for simple text files
        :param filename (str): name of file
        :return results (dict): a dict of statistics for each text file, the state variable
        """


        try:

            assert type(filename) == str, 'Expecting a file name'
            assert filename.endswith('.txt'), 'Not a txt file'
            assert os.path.isfile(filename), 'File does not exist'
            assert os.stat(filename).st_size != 0, 'Inputted file is empty'

        except AssertionError as ae:
            print("Parser error: ", str(ae))
            return None

        except Exception as e:
            print("Parser Exception: " + str(e))
            return None

        else:
            print('Success')

        finally:
            print('CLOSING CONNECTION')


    def load_text(self, filename, label = None, parser = None):


        if label is None:
            label = filename


        try:
            assert type(filename) == str, 'Filename not a string'
            assert filename.lower().endswith('.txt'), 'Not a valid txt file'
            assert label != None and type(label) == str, 'Label not a string'
            assert os.stat(filename).st_size != 0, 'Inputted file is empty'


        except AssertionError as ae:
            print("Loading text error: ", str(ae))

            return None

        else:
            print('Success')



        finally:
            print('CLOSING CONNECTION')



    def get_wordcount(self, word_list=None, k=None):


        try:
            if word_list != None:
                assert type(word_list) == list, 'Not a list'
            if word_list != None:
                assert len(word_list) != 0, 'List is empty'
            assert k!=None and type(k) == int, 'k not an integer'
            assert k >=1, 'k is too small'

        except AssertionError as ae:
            print("Parser error: ", str(ae))
            return None

        else:
            print('Success')

        finally:
            print('CLOSING CONNECTION')
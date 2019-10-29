import re
from pset_3.data import load_words, load_vectors
from functools import reduce


class WordEmbedding(object):
    def __init__(self, words, vecs):
        self.words = words
        self.vecs = vecs

    def __call__(self, word):

        """Embed a word
        :param word: string
        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """

        # first O(n) implementation - leaving in for discussion during Peer Review
        # count = 0
        # for i in self.words:
        #     j = i.rstrip("\n")
        #     try:
        #         if j == word:
        #             position_in_words = count
        #             break
        #         else:
        #             count += 1
        #     finally:
        #         if count == len(self.words):
        #             return None
        #
        # word_vector = self.vecs[position_in_words]
        # return word_vector

        processed_words = [x.rstrip("\n") for x in self.words]
        position_dict = {str(key): idx for idx, key in enumerate(processed_words)}
        word_position = position_dict.get(word, None)
        if word_position is None:
            return None
        else:
            word_vector = self.vecs[word_position]

        return word_vector

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instantiate an embedding from files
        Example::
            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')
        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))

    def tokenize(self, text):
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['hello', "i'm", 'scott']
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining
        :param str document: the document (one or more words) to get a vector
            representation for
        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        document_wordlist = self.tokenize(text)
        # create list of vectors of all words
        y = list(map(lambda x: self.__call__(x), document_wordlist))
        # filter out any None's
        z = [item for item in y if item is not None]
        # add all filtered vectors together
        resulting_vector = reduce(lambda a, b: a + b, z)

        return resulting_vector


if __name__ == "__main__":
    wordlist = "C:/Users/Boiiiiiii/2019fa-pset-3-patchcasey/data/words.txt"
    veclist = "C:/Users/Boiiiiiii/2019fa-pset-3-patchcasey/data/vectors.npy.gz"
    x = WordEmbedding.from_files(wordlist, veclist)
    y = x.__call__("qoduhqwodhiqwod")

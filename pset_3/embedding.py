import re
from pset_3.data import load_words, load_vectors
from functools import reduce

class WordEmbedding(object):
    def __init__(self, words, vecs):
        self.words = words
        self.vecs = vecs

    def __call__(self, word):
        """Embed a word
        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        # Consider how you implement the vocab lookup.  It should be O(1).

        #borrowing iterative process from pset-0
        #TODO - perhaps replace with iterator?
        count = 0
        for i in self.words:
            j = i.rstrip('\n')
            try:
                if j == word:
                    position_in_words = count
                    break
                else:
                    count += 1
            finally:
                if count == len(self.words):
                    return 0

        word_vector = self.vecs[position_in_words]
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
        y = map(lambda x: self.__call__(x), document_wordlist)
        resulting_vector = reduce(lambda a,b : a+b, y)
        return resulting_vector

if __name__ == "__main__":
    test = WordEmbedding(load_words('C:/Users/Boiiiiiii/2019fa-pset-3-patchcasey/data/words.txt'),
                  load_vectors('C:/Users/Boiiiiiii/2019fa-pset-3-patchcasey/data/vectors.npy.gz'))
    test.embed_document('the and a zjxchjc')
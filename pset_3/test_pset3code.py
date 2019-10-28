import os
from tempfile import TemporaryDirectory
from unittest import TestCase
import pandas as pd
import numpy as np
import tempfile
import fastparquet
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cossim

from .data import load_words, load_vectors, load_data
from .cosine_sim import cosine_similarity
from .embedding import WordEmbedding
from .find_friends import salted_hash, print_distancefile, calculate_distance


class FindFriendsTests(TestCase):
    def test_saltedhash(self):
        x = salted_hash("2019fa")
        self.assertEqual(x, "46a4bb62")

    def test_printdistancefile(self):
        with TemporaryDirectory() as tmp:
            tf = tempfile.NamedTemporaryFile(dir=tmp)
            # fp = tf.name
            with tf as f:
                assert os.path.exists(f.name)
                print_distancefile(f.name)
            assert not os.path.exists(tf.name)

    def test_calculate_distance(self):
        a = ["01d2743e"]
        b = ["test"]
        df = pd.DataFrame(data=b, index=a)
        x = calculate_distance(students_input=df)
        y = x.iloc[0]["01d2743e"]
        self.assertEqual(y, 0.028073)


class DataTests(TestCase):

    # TODO - maybe mock here if have time?

    def test_load_words(self):
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            with open(fp, "w") as f:
                f.write("test\n" "again\n" "testme\n")
            test_list = load_words(fp)
            self.assertEqual(test_list[0], "test\n")
            self.assertEqual(test_list[1], "again\n")
            self.assertEqual(test_list[2], "testme\n")

    # TODO - test this when pipenv install works
    def test_load_words_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            load_data("qpojdpoqjdp/qodhqoiwhd/oiwdhqoiwh.wiuegriuwer")

    def test_load_vectors(self):
        # with TemporaryDirectory() as tmp:
        #     # fp = os.path.join(tmp, "asdf.npy.gz")
        #     fp = tempfile.NamedTemporaryFile(delete=False, dir=tmp, suffix=".npy")
        test_np_array = np.array([0, 0, 0])
        fp = os.path.join(os.getcwd(), "testing_array_path.npy")
        np.save(fp, test_np_array)
        print(fp)
        testing_np_array = load_vectors(fp)
        self.assertEqual(testing_np_array.shape, (3,))

    def test_load_data(self):
        d = {"col1": [1, 2], "col2": [3, 4]}
        df = pd.DataFrame(d)
        fp = os.path.join(os.getcwd(), "outfile.parquet")
        df.to_parquet(fp, engine="fastparquet", compression=None)
        returned_df = load_data(fp)
        self.assertEqual(returned_df.shape, (2, 2))


class CosineTests(TestCase):
    def test_cosine_similarity(self):
        a = np.array([[5, 4, 3, 2, 1]])
        b = np.array([[4, 3, 2, 5, 1]])
        sklearn_output = sklearn_cossim(a, b)
        test_output = cosine_similarity(a.flatten(), b.flatten())
        self.assertAlmostEqual(sklearn_output.item(0, 0), test_output)


class EmbeddingTests(TestCase):
    # TODO - figure out why this isn't working - shouldn't these be callable throughout class?
    # def __init__(self, wordlist, veclist, data_dir):
    #     self.wordlist = os.path.join(data_dir, "words.txt")
    #     self.veclist = os.path.join(data_dir, "vectors.npy.gz")
    #     data_dir = os.path.abspath(os.path.join(os.getcwd(), '.', 'data'))

    def test_call(self):
        wordlist = ["the","test"]
        veclist1 = np.zeros(shape=(300))
        veclist2 = np.ones(shape=(300))
        veclist = [veclist1,veclist2]
        string_pos = "the"
        string_neg = "oiqwhdoqihfoweuhfouwehfow"

        x = WordEmbedding(wordlist, veclist)
        pos_result = x.__call__(string_pos)
        self.assertEqual(pos_result.shape, (300,))
        self.assertIsNone(x.__call__(string_neg))

    def test_tokenize(self):
        wordlist = ["the", "test"]
        veclist1 = np.zeros(shape=(300))
        veclist2 = np.ones(shape=(300))
        veclist = [veclist1, veclist2]
        listofwords = "test this sentence it's hard"
        tokenized_words = ["test", "this", "sentence", "it's", "hard"]
        x = WordEmbedding(wordlist, veclist)
        self.assertListEqual(x.tokenize(listofwords), tokenized_words)

    def test_embed_document(self):
        wordlist = ["the", "test"]
        veclist1 = np.array([1, 2])
        veclist2 = np.array([2, 3])
        veclist = [veclist1, veclist2]
        listofwords = "the test"

        x = WordEmbedding(wordlist, veclist)
        y = x.embed_document(listofwords)

        self.assertEqual(y[0], 3)
        self.assertEqual(y[1], 5)

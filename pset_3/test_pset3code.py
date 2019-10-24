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

class DataTests(TestCase):

    #TODO - maybe mock here if have time?

    def test_load_words(self):
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            with open(fp, "w") as f:
                f.write("test\n"
                        "again\n"
                        "testme\n"
                        )
            test_list = load_words(fp)
            self.assertEqual(test_list[0], "test\n")
            self.assertEqual(test_list[1], "again\n")
            self.assertEqual(test_list[2], "testme\n")

    def test_load_vectors(self):
        # with TemporaryDirectory() as tmp:
        #     # fp = os.path.join(tmp, "asdf.npy.gz")
        #     fp = tempfile.NamedTemporaryFile(delete=False, dir=tmp, suffix=".npy")
            test_np_array = np.array([0,0,0])
            fp = os.path.join(os.getcwd(),"testing_array_path.npy")
            np.save(fp,test_np_array)
            print(fp)
            testing_np_array = load_vectors(fp)
            self.assertEqual(testing_np_array.shape, (3,))

    def test_load_data(self):
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(d)
        fp = os.path.join(os.getcwd(), "outfile.parquet")
        df.to_parquet(fp,engine="fastparquet",compression=None)
        returned_df = load_data(fp)
        self.assertEqual(returned_df.shape, (2,2))

class DataTests(TestCase):

    def test_cosine_similarity(self):
        a = np.array([[5, 4, 3, 2, 1]])
        b = np.array([[4, 3, 2, 5, 1]])
        sklearn_output = sklearn_cossim(a,b)
        test_output = cosine_similarity(a.flatten(), b.flatten())
        self.assertEqual(round(sklearn_output.item(0,0), 15), round(test_output, 15))



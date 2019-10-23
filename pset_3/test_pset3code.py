import os
from tempfile import TemporaryDirectory
from unittest import TestCase
import pandas as pd
import numpy as np
import tempfile

from .data import load_words, load_vectors, load_data

class Data_tests(TestCase):
    #TODO - maybe mock here if have time?
    def test_load_words(self):
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            #TODO - replace with atomic_write
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


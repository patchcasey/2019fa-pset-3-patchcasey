import numpy as np
import pandas as pd
import os

def load_words(filename):
    """Load a file containing a list of words as a python list
    use case: data/words.txt
    :param str filename: path/name to file to load
    :rtype: list
    """
    if os.path.isfile(filename) is True:
        with open(filename, "r") as f:
            lines = f.readlines()
        results = [x for x in lines]
        return results
    else:
        raise FileNotFoundError

def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array
    use case: `data/vectors.npy.gz`
    :param str filename:
    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding
    :rtype: ndarray
    """

    vectors = np.load(filename,allow_pickle=True)
    return vectors

def load_data(filename):
    """Load student response data in parquet format
    use case: data/hashed.parquet
    :param str filename:
    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # You will probably need to fill a few NA's and set/sort the index via
    # pandas

    initial = pd.read_parquet(filename, engine='fastparquet')
    return initial
import numpy
from numpy.linalg import norm as LA
from .hash_str import hash_str, get_csci_salt


def cosine_similarity(a, b):
    """
    from sklearn.metrics.pairwise.cosine_similarity:
    Cosine similarity, or the cosine kernel, computes similarity as the normalized dot product of X and Y:
        K(X, Y) = <X, Y> / (||X||*||Y||)
    This function implements the dot product of x and y divided by norm of x and y
    :param a: array
    :param b: array
    :return: float
    """

    numerator = numpy.dot(a, b)
    denominator = LA(a) * LA(b)
    cos_sim = numerator / denominator
    return cos_sim

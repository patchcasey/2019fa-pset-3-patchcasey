# Pset 3

Add your build badge here!

Customizing our own cookiecutter repo, and using it to complete a Word2Vec
project.

Note: This problem set will involve submitting two separate repos:

(1) customized cookiecutter  
(2) pset 3  

Please submit both links to the Canvas assignments when you have completed!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Preface](#preface)
  - [Atomicity and utils](#atomicity-and-utils)
- [Problems](#problems)
  - [Use your cookiecutter to create your pset-3 repo](#use-your-cookiecutter-to-create-your-pset-3-repo)
    - [Push your pset 3 repo](#push-your-pset-3-repo)
  - [Student Embeddings](#student-embeddings)
    - [AWS Data](#aws-data)
    - [Loading the data](#loading-the-data)
    - [Embedding](#embedding)
    - [Cosine similarity](#cosine-similarity)
    - [Find your friends](#find-your-friends)
    - [An 'atomic' workflow](#an-atomic-workflow)
    - [Join and output](#join-and-output)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Preface

**DO NOT CLONE THIS REPO LOCALLY YET**.  We will manually create a repo and link
it.  If you have cloned this repo locally, simply delete
it (it's fine if it's already forked on github).

### Atomicity and utils

You'll be using your `atomic_write` function in this problem set. After you
initiate the repo, `pipenv install` your `pset_utils` repo as instructed
previously (see instructions for how to authenticate in Travis/Docker). Let us
know if you have issues here as this involves a bit more configuration than
ideal.  You can add the atomic write later if you are blocked.

## Problems

### Use your cookiecutter to create your pset-3 repo

In the directory above `2019fa-cookiecutter-csci-pset-YOUR_GITHUB_ID`, *do the
following*:

```bash
cookiecutter 2019fa-cookiecutter-csci-pset-YOUR_GITHUB_ID/
```

You have configured many things already such as name, github id, travis, etc.

In addition, for this project specifically, make sure to *do the following*:  

| Param | Value |  
|-|-|  
| project_name | `Pset 3` |  
| repo_name | (should default to `2019fa-pset-3-YOUR_GITHUB_ID`) |  
| project_slug | (should default to `pset_3`) |

#### Push your pset 3 repo

Now you can *push to your pset 3 repo* via:

```bash
cd <rendered pset folder>
git init
git add --all  # though nicer if you do this manually/via SourceTree
git commit -m "Add initial project skeleton."
git remote add origin git@github.com:csci-e-29/2019fa-pset-3-YOUR_GITHUB_ID.git
git fetch
git merge origin/master --allow-unrelated-histories
git push -u origin master
```

### Student Embeddings

#### AWS Data

Navigate into your pset 3 directory in terminal. Copy the `Makefile` from Pset 1
and modify it to download the following three files into your `data/` dir:

```bash
$ aws s3 ls s3://cscie29-data/<HASH_ID>/pset_3/
2019-10-18 02:34:52      48359 project.parquet
2019-10-18 02:16:54   11812928 vectors.npy.gz
2019-10-18 02:17:03      74745 words.txt
```

where `<HASH_ID>` is the first 8 digits of our semester code hashed with the
CSCI salt.  Semester codes are the year followed by either `sp` of `fa`, eg
`2019fa`.  (Hint - for `2019fa`, it starts `46a...` You may hard code the answer
in your Makefile.

(NB: normally you could use `--recursive`, but that does not currently work due
to permissions.  Listing the directory also does not currently work, but you
can download the files if you specify the name).

Use your new [Makefile](Makefile) to download the data, and ensure your travis
file uses it in the answer stage, similar to how it was in pset 1 (it should
only run on your master branch!).  If on Windows, you can of course download the
data manually (but still use Makefile for running on Travis).

You should now have a new folder called `data` with three files we'll use for
this problem set.

For these problems, we will use the three files you pulled from S3:

1. `data/words.txt` contains  a list of 9844 common words.

2. `data/vectors.npy.gz` is a 9844x300 embedding matrix. Each row of the matrix
is the 300-dimensional vector representation for the word at the same position
in the vocab list (first row <-> first word in list, ... etc).  You can load
this with `numpy.load`.

3. `data/project.parquet`, a dataframe containing hashed user ids, and
answers from your demographics survey about what you hope to learn from this
course.


#### Loading the data

You will need to write functions to load the three datasets; please implement
them in `pset_3.data`

You likely already have or need `awscli`, `pandas`, and `pyarrow` in your
Pipfile. You will likely also need `numpy`. As a reminder, you should install
such packages via `pipenv install numpy`.

```python
def load_words(filename):
    """Load a file containing a list of words as a python list

    use case: data/words.txt

    :param str filename: path/name to file to load
    :rtype: list
    """
    ...

def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array

    use case: `data/vectors.npy.gz`
    :param str filename:

    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding

    :rtype: ndarray
    """
    ...

def load_data(filename):
    """Load student response data in parquet format

    use case: data/hashed.parquet
    :param str filename:

    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """
    # You will probably need to fill a few NA's and set/sort the index via
    # pandas
    ...

```

#### Embedding

***Create a class*** called `WordEmbedding`, which is initialized with two
arguments: the word list and the vectors.  Implement the embedding as the
`__call__` method as well as a helper constructor to load from files (we do
this to help with testing).

You can implement this in `pset_3.embedding`:

```python
class WordEmbedding(object):
    def __init__(self, words, vecs):
        ...

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """

        # Consider how you implement the vocab lookup.  It should be O(1).
        ...

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instantiate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))
```

Finally, we need a way to combine embeddings for multiple words into a 'document
embedding', aka a single vector for an entire body of text.  

***Add a function*** (`embed_document`) that embeds documents using the simple
approach of just adding the vectors. Note that you will need to use the
`tokenize` function provided in order to get all "words" of a document.

```python
import re

class WordEmbedding(object):
    ...

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
            # Use tokenize(), maybe map(), functools.reduce, itertools.aggregate...
            # Assume any words not in the vocabulary are treated as 0's
            # Return a zero vector even if no words in the document are part
            # of the vocabulary
            ...
```

To wrap it all up, you can use [Pandas
apply](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.apply.html?highlight=apply#pandas.Series.apply)
to execute your code in a functional way.

Add something along these lines to `pset_3.cli` to execute everything
you've done so far.

```python
def main(args=None):
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the hashed student data
    data = load_data('data/hashed.parquet')

    # create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the index with vectors inside
    embeddings = data['project'].apply(embedding.embed_document)
```

#### Cosine similarity

Since words are being represented as vectors, we can compute a distance metric
to represent how "similar" two words are. There are a couple of distance metrics
we can use - [cosine
similarity](https://en.wikipedia.org/wiki/Cosine_similarity) is a commonly used
one. Cosine similarity is defined as:

![](https://latex.codecogs.com/svg.latex?similarity%28A%2C%20B%29%20%3D%20cos%28%5Ctheta%29%20%3D%20%5Cfrac%20%7BA%20%5Ccdot%20B%7D%20%7B%5Cleft%5C%7C%20A%20%5Cright%5C%7C%20%5Cleft%5C%7C%20B%20%5Cright%5C%7C%20%7D%20%3D%20%5Cfrac%20%7B%5Csum%20A_i%20B_i%7D%20%7B%20%5Csqrt%7B%5Csum%20A_i%5E2%7D%20%5Csqrt%7B%5Csum%20B_i%5E2%7D%20%7D)

***Implement a function*** `cosine_similarity(a, b)` that computes cosine
similarity for two vector inputs. Be sure to test it. Please use `numpy.dot`
and `numpy.linalg.norm` in your implementation.

Note: We did not provide starter code! Time to take control, it's your
application after all. Don't overthink it - it should just be a short snippet.
Create a home for the cosine function that makes sense and be sure to include a
doc string describing what it does.


#### Find your friends

The hashed ids are the salted hash of ***your name exactly as it appears in
Canvas***. You can double check how your name appears in Canvas in your
[profile](https://canvas.harvard.edu/profile).  You should convert your name to
lowercase before hashing.

***Calculate the distance*** between your response and those of other students
using your cosine similarity method.  Note that `distance(x,y) == 1 - cosine_similarity(x, y)`.

Persist this output as a new parquet file in `data/`

```python
def main(args=None):
    ...

    distance = ... # series or data frame

    # utilize atomic_write to export results to data/...
    filename = "data/distance_to_peers.parquet"

    # Ensure you are ***only*** writing the index and distance!
    distance.to_parquet(f)
```

#### An 'atomic' workflow

Go back and restructure your `main()` method to ***only calculate the distance
if the output file does not exist***.  If the file exists when the program
starts, assume it has already been calculated correctly (you can delete it
if you need to rerun!).  Be sure to also use your `atomic_write` function.

#### Join and output

After writing the distance if it doesn't already exist, read it back and print a
summary of the top five most similar students, including yourself.  The summary
should include the id, the distance, and the project text in some human readable
form.

```python
def main(args=None):
    ...
    distance = ... # load back from disk
    five_friends = ... # join distance to project data, sort and select

    for friend, row in five_friends.iterrows():
        # Print out a summary of the TA and the 4 closest students
        ...
```

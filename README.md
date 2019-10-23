# Pset 3

Add your build badge here!

Customizing our own cookiecutter repo, and using it to complete a Word2Vec
project.

Note: This problem set will involve submitting two separate repos:

(1) customized cookiecutter  
(2) pset 3  

Please submit both links to the Canvas assignments when you have completed!
>>>>>>> origin/master

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

<<<<<<< HEAD
- [Before you begin...](#before-you-begin)
  - [Document code and read documentation](#document-code-and-read-documentation)
  - [Docker shortcut](#docker-shortcut)
  - [Pipenv](#pipenv)
    - [Installation](#installation)
    - [Usage](#usage)
      - [Pipenv inside docker](#pipenv-inside-docker)
  - [Credentials and data](#credentials-and-data)
    - [Using `awscli`](#using-awscli)
      - [Installation (via pipenv)](#installation-via-pipenv)
    - [Configure `awscli`](#configure-awscli)
      - [Make a .env (say: dotenv) file](#make-a-env-say-dotenv-file)
      - [Other methods](#other-methods)
    - [Copy the data locally](#copy-the-data-locally)
    - [Set the Travis environment variables](#set-the-travis-environment-variables)
- [Problems (40 points)](#problems-40-points)
  - [Hashed strings (10 points)](#hashed-strings-10-points)
    - [Implement a standardized string hash (5 points)](#implement-a-standardized-string-hash-5-points)
    - [True salting (5 points)](#true-salting-5-points)
  - [Atomic writes (15 points)](#atomic-writes-15-points)
    - [Implement an atomic write (15 points)](#implement-an-atomic-write-15-points)
  - [Parquet (15 points)](#parquet-15-points)
  - [Your main script](#your-main-script)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Before you begin...

**Add your Travis and Code Climate badges** to the
top of this README, using the markdown template for your master branch.

### Document code and read documentation

For some problems we have provided starter code. Please look carefully at the
doc strings and follow all input and output specifications.

For other problems, we might ask you to create new functions, please document
them using doc strings! Documentation factors into the "python quality" portion
of your grade.

### Docker shortcut

See [drun_app](./drun_app):

```bash
docker-compose build
./drun_app python # Equivalent to docker-compose run app python
```

### Pipenv

This pset will require dependencies.  Rather than using a requirements.txt, we
will use [pipenv](https://pipenv.readthedocs.io/en/latest/) to give us a pure,
repeatable, application environment.

#### Installation

If you are using the Docker environment, you should be good to go.  Mac/windows
users should [install
pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today) into
their main python environment as instructed.  If you need a new python 3.7
environment, you can use a base
[conda](https://docs.conda.io/en/latest/miniconda.html) installation.

```bash
# Optionally create a new base python 3.7
conda create -n py37 python=3.7
conda activate py37
pip install pipenv
pipenv install ...
```

```bash
pipenv install --dev
pipenv run python some_python_file
```

If you get a TypeError, see [this
issue](https://github.com/pypa/pipenv/issues/3363)

#### Usage

Rather than `python some_file.py`, you should run `pipenv run python some_file.py`
or `pipenv shell` etc

***Never*** pip install something!  Instead you should `pipenv install
pandas` or `pipenv install --dev ipython`.  Use `--dev` if your app
only needs the dependency for development, not to actually do it's job.

Pycharm [works great with
pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html)

Be sure to commit any changes to your [Pipfile](./Pipfile) and
[Pipfile.lock](./Pipfile.lock)!

##### Pipenv inside docker

Because of the way docker freezes the operating system, installing a new package
within docker is a two-step process:

```bash
docker-compose build

# Now i want a new thing
./drun_app pipenv install pandas # Updates pipfile, but does not rebuild image
# running ./drun_app python -c "import pandas" will fail!

# Rebuild
docker-compose build
./drun_app python -c "import pandas" # Now this works
```

### Credentials and data

Git should be for code, not data, so we've created an S3 bucket for problem set
file distribution.  For this problem set, we've uploaded a data set of your
answers to the "experience demographics" quiz that you should have completed in
the first week. In order to access the data in S3, we need to install and
configure `awscli` both for running the code locally and running our tests in
Travis.

You should have created an IAM key in your AWS account.  DO NOT SHARE THE SECRET
KEY WITH ANYONE. It gives anyone access to the S3 bucket.  It must not be
committed to your code.

For more reference on security, see [Travis Best
Practices](https://docs.travis-ci.com/user/best-practices-security/#recommendations-on-how-to-avoid-leaking-secrets-to-build-logs)
and [Removing Sensitive
Data](https://help.github.com/articles/removing-sensitive-data-from-a-repository/).

#### Using `awscli`

AWS provides a [CLI
tool](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
that helps interact with the many different services they offer.

##### Installation (via pipenv)

We have already installed `awscli` into your pipenv.  It is available within
the pipenv shell and the docker container via the same mechanism.

```bash
pipenv run aws --help
./drun_app aws --help
```

#### Configure `awscli`

Now configure `awscli` to access the S3 bucket.

##### Make a .env (say: dotenv) file

Create a [.env](.env) file that looks something like this:

```
AWS_ACCESS_KEY_ID=XXXX
OTHER_ENV_VARIABLE=XXX
```

***DO NOT*** commit this file to the repo (it's already in your
[.gitignore](.gitignore))

Both docker and pipenv will automatically inject these variables into your
environment!  Whenever you need new env variables, add them to a dotenv.

See env refs for
[docker](https://docs.docker.com/compose/environment-variables/) and
[pipenv](https://pipenv.readthedocs.io/en/latest/advanced/#automatic-loading-of-env)
for more details.

##### Other methods

According to the
[documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
the easiest way is:

```bash
aws configure
AWS Access Key ID [None]: ACCESS_KEY
AWS Secret Access Key [None]: SECRET_KEY
Default region name [None]:
Default output format [None]:
```

There are other, more complicated, configurations outlined in the documentation.
Feel free to use a solution using environment variables, a credentials
file, a profile, etc.

#### Copy the data locally

Read the [Makefile](Makefile) and [.travis.yml](./.travis.yml) to see how to
copy the data locally.

Note that we are using a [Requestor
Pays](https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html)
bucket.  You are responsible for usage charges.

You should now have a new folder called `data` in your root directory with the
data we'll use for this problem set. You can find more details breaking down
this command at the [S3 Documentation
Site](https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html).

#### Set the Travis environment variables

This is Advanced Data Science, so of course we also want to automate our tests
and pset using CI/CD.  Unfortunately, we can't upload our .env or run  `aws
configure` and interactively enter the credentials for the Travis builds, so we
have to configure Travis to use the access credentials without compromising the
credentials in our git repo.

We've provided a working `.travis.yml` configuration that only requires the AWS
credentials when running on the master branch, but you will still need to the
final step of adding the variables for your specific pset repository.

To add environment variables to your Travis environment, you can use of the
following options:

* Navigating to the settings, eg https://travis-ci.com/csci-e-29/YOUR_PSET_REPO/settings
* The [Travis CLI](https://github.com/travis-ci/travis.rb)
* encrypting into the `.travis.yml` as instructed [here](https://docs.travis-ci.com/user/environment-variables/#defining-encrypted-variables-in-travisyml).

Preferably, you should only make your 'prod' credentials available on your
master branch: [Travis
Settings](https://docs.travis-ci.com/user/environment-variables/#defining-variables-in-repository-settings)

You can chose the method you think is most appropriate.  Our only requirement is
that ***THE KEYS SHOULD NOT BE COMMITTED TO YOUR REPO IN PLAIN TEXT ANYWHERE***.

For more information, check out the [Travis Documentation on Environment
Variables](https://docs.travis-ci.com/user/environment-variables/)

__*IMPORTANT*__: If you find yourself getting stuck or running into issues,
please post on Piazza and ask for help.  We've provided most of the instructions
necessary for this step and do not want you spinning your wheels too long just
trying to download the data.

## Problems (40 points)

### Hashed strings (10 points)

It can be extremely useful to ***hash*** a string or other data for various
reasons - to distribute/partition it, to anonymize it, or otherwise conceal the
content.

#### Implement a standardized string hash (5 points)

Use `sha256` as the backbone algorithm from
[hashlib](https://docs.python.org/3/library/hashlib.html).

A `salt` is a prefix that may be added to increase the randomness or otherwise
change the outcome.  It may be a `str` or `bytes` string, or empty.

Implement it in [hash_str.py](pset_1/hash_str.py), where the return value is the
`.digest()` of the hash, as a `bytes` array:

```python
def hash_str(some_val, salt=''):
    """Converts strings to hash digest

    :param str:
    :param str or bytes salt: string or bytes to add randomness to the hashing, defaults to ''

    :rtype: bytes
    """
```

Note you will need to `.encode()` string values into bytes.

As an example, `hash_str('world!', salt='hello, ').hex()[:6] == '68e656'`

Note that if we ever ask you for a bytes value in Canvas, the expectation is
the hexadecimal representation as illustrated above.

#### True salting (5 points)

Note, however, that hashing isn't very secure without a secure salt.  We
can take raw `bytes` to get something with more entropy than standard text
provides.

Let's designate an environment variable, `CSCI_SALT`, which will contain
hex-encoded bytes.  Implement the function `pset_utils.hash_str.get_csci_salt`
which pulls and decodes an environment variable.  In Canvas, you will be given
a random salt taken from [random.org](http://random.org) for real security.

### Atomic writes (15 points)

Use the module `pset_1.io`.  We will implement an atomic writer.

Atomic writes are used to ensure we never have an incomplete file output.
Basically, they perform the operations:

1. Create a temporary file which is unique (possibly involving a random file
   name)
2. Allow the code to take its sweet time writing to the file
3. Rename the file to the target destination name.

If the target and temporary file are on the same filesystem, the rename
operation is ***atomic*** - that is, it can only completely succeed or fail
entirely, and you can never be left with a bad file state.

See notes in
[Luigi](https://luigi.readthedocs.io/en/stable/luigi_patterns.html#atomic-writes-problem)
and the [Thanksgiving
Bug](https://www.arashrouhani.com/luigi-budapest-bi-oct-2015/#/21)

#### Implement an atomic write (15 points)

Start with the following in [io.py](./pset_1/io.py):

```python
@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write
    :param bool as_file:  if True, the yielded object is a :class:File.
        Otherwise, it will be the temporary file path string
    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """
    ...
```

 Key considerations:

 * You can use [tempfile](https://docs.python.org/3.6/library/tempfile.html),
   write to the same directory as the target, or both.
   What are the tradeoffs? Add code comments for anything critical
 * Ensure the file is deleted if the writing code fails
 * Ensure the temporary file has the same extension(s) as the target.  This is
   important for any code that may infer something from the path (eg, `.tar.gz`)
 * If the writing code fails and you try again, the temp file should be new -
   you don't want the context to reopen the same temp file.
 * Others?

 Ensure these considerations are reflected in your unit tests!

***Every file written in this class must be written atomically, via this
function or otherwise.***

### Parquet (15 points)

Excel is a very poor file format compared to modern column stores.  Use [Parquet
via
Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#parquet)
to transform the provided excel file into a better format.

The new file should keep the same name, but use the extension `.parquet`.

Ensure you use your atomic write.

Read back ***just the hashed id column*** and print it (don't read the entire
data set!).

### Your main script

Implement top level execution in [pset_1/\__main__.py](pset_1/__main__.py) to
show your work and answer the q's in the pset answers quiz.  It can be
invoked with `python -m pset_1`.
=======
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


from .embedding import WordEmbedding
from .data import load_data
from .hash_str import hash_str, get_csci_salt
from.cosine_sim import cosine_similarity
import pandas as pd
import os

# read in the hashed student data
cwd = os.getcwd()
data_dir = os.path.abspath(os.path.join(os.getcwd(), '.', 'data'))
file_to_use = os.path.join(data_dir, "project.parquet")
peer_distance_filename = os.path.join(data_dir, "distance_to_peers.parquet")
data = load_data(file_to_use)

# create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the index with vectors inside
embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
embeddings = data['project'].apply(embedding.embed_document)

def print_distancefile(path_to_file=peer_distance_filename):
    if os.path.exists(path_to_file):
        # this would be logged if Logging
        print("File already exists! Moving on...")
        pass
    else:
        # TODO - implement atomic_write
        print("Printing file...")
        distance.to_parquet(peer_distance_filename, compression=None)


def salted_hash(word, salt=None):
    if salt is not None:
        return hash_str(some_val=word, salt=salt).hex()[:8]
    else:
        return hash_str(some_val=word, salt=get_csci_salt()).hex()[:8]


def return_vector(student_name, calculated_embeddings=embeddings):
    return calculated_embeddings.loc[student_name]


def calculate_distance(myname="casey patch",students_input=data.index.values):
    myself = salted_hash(myname)
    myself_vector = return_vector(myself)

    students = students_input
    list_of_student_ids = list(students)
    students_vector = []
    for x in students:
        students_vector.append(return_vector(x))

    cos_sim_myselftostudents = list(map(lambda y: cosine_similarity(myself_vector, y), students_vector))

    distance_list = []
    for x in cos_sim_myselftostudents:
        distance_list.append(1 - x)

    distance = pd.DataFrame(distance_list, index=list_of_student_ids, columns=["distance"])
    return distance
from .embedding import WordEmbedding
from .data import load_data
from .hash_str import hash_str, get_csci_salt
from.cosine_sim import cosine_similarity
from .find_friends import calculate_distance, print_distancefile, salted_hash, return_vector
import pandas as pd
import os


def main(args=None):
    cwd = os.getcwd()
    data_dir = os.path.abspath(os.path.join(os.getcwd(), '.', 'data'))
    file_to_use = os.path.join(data_dir, "project.parquet")
    peer_distance_filename = os.path.join(data_dir, "distance_to_peers.parquet")
    data = load_data(file_to_use)

    # create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the index with vectors inside
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
    embeddings = data['project'].apply(embedding.embed_document)

    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')


    embeddings = data['project'].apply(embedding.embed_document)

    distance = calculate_distance()

    print_distancefile()

    loaded_distance = load_data(peer_distance_filename)
    merged_df = pd.merge(loaded_distance, data, left_index=True, right_index=True)
    print(merged_df)
    closest_5students = merged_df.nsmallest(5, ['distance'])
    # check to make sure I am in the list
    if salted_hash("casey patch") in closest_5students.index:
        pass
    else:
        #this might not be the correct error to raise?
        raise IndexError

    for friend, row in closest_5students.iterrows():
        print("\nStudent (first entry is me!)\n", "distance:\n", row['distance'], "\nresponse: \n", row['project'])
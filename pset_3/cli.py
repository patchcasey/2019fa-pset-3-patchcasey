from .embedding import WordEmbedding
from .data import load_data
from .hash_str import hash_str, get_csci_salt
from.cosine_sim import cosine_similarity
import os

def main(args=None):
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the hashed student data
    cwd = os.getcwd()
    data_dir = os.path.abspath(os.path.join(os.getcwd(), '.', 'data'))
    file_to_use = os.path.join(data_dir, "project.parquet")
    data = load_data(file_to_use)

    # create the vector representation for each survey entry
    # Note: this result will be a Series object preserving the index with vectors inside
    embeddings = data['project'].apply(embedding.embed_document)

    def salted_hash(input):
        return hash_str(some_val=input,salt=get_csci_salt()).hex()[:8]

    def return_vector(student_name, calculated_embeddings=embeddings):
        return calculated_embeddings.loc[student_name]

    def calculate_distance():
        myself = salted_hash("casey patch")
        myself_vector = return_vector(myself)
        print(myself_vector)
    #     students = data["user_id"]
    #     students_vector = []
    #     for x in students:
    #         students_vector.append(return_vector(x))
    #     print(students_vector[1])
    #     test = list(map(lambda x, y: cosine_similarity(myself, y), myself, students))
    #     print(test)
    calculate_distance()

    # distance = ...  # series or data frame
    #
    # # utilize atomic_write to export results to data/...
    # peer_distance_filename = os.path.join(data_dir, "distance_to_peers.parquet")
    #
    # # Ensure you are ***only*** writing the index and distance!
    # distance.to_parquet(peer_distance_filename)
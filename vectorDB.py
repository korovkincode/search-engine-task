import json
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

MOVIE_QUERY = "Serial killer"


with open("movies.json", encoding="utf-8") as moviesFile:
    moviesData = json.load(moviesFile)

movies_df = pd.DataFrame(moviesData)
movies_df = movies_df.dropna(subset=["overview"])
movies_df = movies_df[["id", "title", "overview"]]


model = SentenceTransformer("all-MiniLM-L6-v2")
descriptions = movies_df["overview"].tolist()
embeddings = model.encode(descriptions, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")


index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def search(query: str, limit: int = 5):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, limit)
    results = movies_df.iloc[indices[0]].copy()
    results["similarity_score"] = distances[0]
    return results[["title", "overview", "similarity_score"]]


print(search(MOVIE_QUERY, 5))
'''
Result:
             title                                           overview  similarity_score
1767  Suspect Zero  A killer is on the loose, and an FBI agent sif...          0.758932
1379      The Cell  A psychotherapist journeys inside a comatose s...          0.765101
2138       Copycat  An agoraphobic psychologist and a female detec...          0.856649
421         Zodiac  The true story of the investigation of 'The Zo...          0.900846
4291           Saw  Obsessed with teaching his victims the value o...          0.927669
'''
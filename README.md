# 🔍 Search Engine with Graph and Vector Databases

- A **Graph Database** (Neo4j) for relationship-based queries
- A **Vector Database** (FAISS) for semantic similarity search

## 🧠 Task Overview

I used the TMDB dataset to:

1. **Collect & Prepare Data**
   - `movies.json` and `credits.json` (from Kaggle)
2. **Build a Graph Database (Neo4j)**
   - Store movies, actors, and genres as connected nodes
3. **Build a Vector Database (FAISS)**
   - Store movie descriptions as text embeddings for similarity search
4. **Implement Search Queries**
   - Find movies by actor and genre (Neo4j)
   - Find similar movies by description (FAISS)

---

### `graphDB.py`
1. Loads data into Neo4j (set `FILL_DATABASE = True`)
2. Relationships: `(:Actor)-[:ACTED_IN]->(:Movie)-[:HAS_GENRE]->(:Genre)`
    
```python
Database.findMovies("Daniel Radcliffe", "Fantasy")
```

**Best for:**
- Exploring explicit relationships (e.g., actor → movie → genre)
- Path-based queries (e.g., co-actors, recommendation chains)
- Schema-rich, well-connected data


### `vectorDB.py`
1. Loads movie descriptions and computes embeddings using `SentenceTransformer`
2. Stores and indexes them with `FAISS` for semantic search

```python
search("Serial killer", 5)
```

**Best for:**
- Semantic similarity search (e.g., movies with similar themes or descriptions)
- Natural language queries (no schema or predefined relationships)
- Discovering hidden or abstract similarities in unstructured text data (e.g., synopsis)


## 🚀 Summary

| Feature                     | Graph DB (Neo4j)     | Vector DB (FAISS)       |
|-----------------------------|----------------------|--------------------------|
| Structured queries          | ✅ Strong             | ❌ Not applicable        |
| Fuzzy/semantic search       | ❌ Not built-in       | ✅ Excellent              |
| Relationship modeling       | ✅ Excellent          | ❌ None                  |
| Performance (structured)    | ✅ Optimized          | ❌ Irrelevant            |
| Performance (semantic)      | ❌ Limited            | ✅ ANN-optimized         |
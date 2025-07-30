import os
import json
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm


def create_vector_db():
    """ Load data from ./train/* (all subjects) and create a vector db using qdrant persistent database. Use BAAI/bge-small-en-v1.5 for embedding. """
    
    # Initialize Qdrant client with persistent storage
    client = QdrantClient(path="./qdrant_db")
    
    # Initialize the embedding model
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    
    # Create collection if it doesn't exist
    collection_name = "math_problems"
    try:
        client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists")
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # BGE-small-en-v1.5 has 384 dimensions
        )
        print(f"Created new collection '{collection_name}'")
    
    # Check if collection already has data
    collection_info = client.get_collection(collection_name)
    if collection_info.points_count > 0:
        print(f"Collection already contains {collection_info.points_count} points")
        return client, collection_name
    
    # Load data from all train directories
    train_base_dir = "./train"
    points = []
    
    if os.path.exists(train_base_dir):
        # First, count total files for progress bar
        total_files = 0
        subject_files = {}
        for subject_dir in os.listdir(train_base_dir):
            subject_path = os.path.join(train_base_dir, subject_dir)
            if os.path.isdir(subject_path):
                files = [f for f in os.listdir(subject_path) if f.endswith('.json')]
                subject_files[subject_dir] = files
                total_files += len(files)
        
        print(f"Found {total_files} files across {len(subject_files)} subjects")
        
        # Create progress bar
        with tqdm(total=total_files, desc="Loading and embedding problems") as pbar:
            for subject_dir, files in subject_files.items():
                subject_path = os.path.join(train_base_dir, subject_dir)
                pbar.set_postfix({"Subject": subject_dir})
                
                for filename in files:
                    file_path = os.path.join(subject_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                        # Combine problem and solution for embedding
                        text_for_embedding = f"Problem: {data['problem']} Solution: {data['solution']}"
                        
                        # Generate embedding
                        embedding = model.encode(text_for_embedding).tolist()
                        
                        # Create point
                        point = PointStruct(
                            id=len(points),
                            vector=embedding,
                            payload={
                                "problem": data['problem'],
                                "solution": data['solution'],
                                "level": data.get('level', ''),
                                "type": data.get('type', ''),
                                "subject": subject_dir,
                                "filename": filename
                            }
                        )
                        points.append(point)
                    
                    pbar.update(1)
    
    # Insert points into collection
    if points:
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Created vector database with {len(points)} math problems")
    else:
        print("No data found in ./train directory")
    
    return client, collection_name


def search_vector_db(query: str, client=None, collection_name="math_problems", top_k: int = 5):
    """ Search the vector db for the query. """
    
    if client is None:
        # Initialize client if not provided
        client = QdrantClient(path="./qdrant_db")
    
    # Initialize the embedding model
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')
    
    # Generate embedding for the query
    query_embedding = model.encode(query).tolist()
    
    # Search the collection
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )
    
    return search_results


def main():
    # Create the vector database
    client, collection_name = create_vector_db()
    
    # Example search
    query = "What is the area of the triangle with vertices (-1,4), (7,0), and (11,5)?"
    results = search_vector_db(query, client, collection_name)
    
    print(f"\nSearch results for: '{query}'")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result.score:.4f}")
        print(f"Subject: {result.payload.get('subject', 'N/A')}")
        print(f"Problem: {result.payload['problem']}...")
        print(f"Level: {result.payload['level']}")
        print(f"Type: {result.payload['type']}")


if __name__ == "__main__":
    main()
from knowledge_base import search_vector_db

def main():
    query = "Find Integral of tanx + sinx / sin^2 x"
    results = search_vector_db(query)
    print(type(results))
    print(f"\nSearch results for: '{query}'")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Score: {result.score:.4f}")
        print(f"Subject: {result.payload.get('subject', 'N/A')}")
        print(f"Problem: {result.payload['problem']}")
        print(f"Solution: {result.payload['solution']}")
        print(f"Level: {result.payload['level']}")
        print(f"Type: {result.payload['type']}")
        print("-" * 80)

if __name__ == "__main__":
    main()

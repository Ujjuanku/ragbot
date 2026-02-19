import time
import rag

print("Testing 'hr' query (Rule-based)...")
start = time.time()
response = rag.get_answer("hr")
end = time.time()
print(f"Response: {response[:50]}...")
print(f"Time taken: {end - start:.4f}s")

print("\n--------------------------------\n")

print("Testing 'What is AcmeFlow?' query (RAG)...")
start = time.time()
response = rag.get_answer("What is AcmeFlow?")
end = time.time()
print(f"Response: {response[:50]}...")
print(f"Time taken: {end - start:.4f}s")

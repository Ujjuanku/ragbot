#!/bin/bash

echo "Testing RAG Chatbot..."
echo "--------------------------------"
echo "Query: What is AcmeFlow?"
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is AcmeFlow?"}'
echo "\n\n--------------------------------"
echo "Query: Who is the CEO of Google? (Should be refused)"
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Who is the CEO of Google?"}'
echo "\n\n--------------------------------"
echo "Query: hr (Should return menu)"
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "hr"}'
echo "\n"

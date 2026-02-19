from pinecone import Pinecone
from openai import OpenAI
import config


# -------------------------------
# Initialize Clients
# -------------------------------
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)


# -------------------------------
# Query Normalization (Intent Expansion)
# Helps short vague queries retrieve context
# -------------------------------
def normalize_query(q: str) -> str:
    q = q.lower().strip()
    
    # Common typos handling
    typo_map = {
        "benifit": "benefits",
        "benifits": "benefits",
        "policys": "policies",
        "prodcuts": "products"
    }
    
    q = typo_map.get(q, q)

    shortcuts = {
        "hr": "human resources policy leave policy employee benefits work hours remote work",
        "leave": "employee leave policy vacation sick leave paid time off holidays",
        "benefits": "employee benefits insurance compensation perks health coverage",
        "company": "company overview history mission vision headquarters employees clients",
        "products": "company products services offerings solutions platform tools",
        "about": "company overview history mission vision what company does",
        "policy": "company hr policy employee rules benefits working hours",
        "product": "company products services"
    }

    return shortcuts.get(q, q)

def handle_special_scenarios(query: str):
    """
    Handle very broad or specific keyword-only queries with a guided response.
    This improves UX by guiding the user instead of just RAG-ing vague terms.
    """
    q_lower = query.lower().strip()
    
    if q_lower in ["hr", "human resources", "hr policy"]:
        return """Here are some key HR topics I can help you with:
1. **Leave Policy**: Ask about PTO, sick leave, or parental leave.
2. **Benefits**: Ask about health insurance, 401(k), or wellness stipends.
3. **Working Hours**: Ask about remote work or core hours.
4. **Onboarding**: Ask about the process for new hires.

Try asking: "What is the vacation policy?"""

    if q_lower in ["products", "product", "services", "what do you sell"]:
        return """Acme Tech Solutions offers 5 main products:
1. **AcmeFlow**: Project Management.
2. **AcmeSecure**: Cybersecurity.
3. **AcmeConnect**: Unified Communications.
4. **DataAcme**: Business Intelligence.
5. **CloudOne**: AI Infrastructure.

Try asking: "Tell me more about AcmeFlow" or "Explain all products briefly"."""
    
    return None

# -------------------------------
# Main RAG Function
# -------------------------------
def get_answer(query: str) -> str:
    """
    1. Check for special guided scenarios (Rule-based)
    2. Normalize user query
    3. Embed query
    4. Retrieve relevant chunks
    5. Build grounded prompt
    6. Generate answer
    """
    
    # ---- 1. Rule-based Guidance for broad queries ----
    direct_response = handle_special_scenarios(query)
    if direct_response:
        return direct_response

    # ---- 2. Normalize vague queries & Typos ----
    norm_query = normalize_query(query)

    # ---- 3. Embed Query ----
    query_embedding_response = openai_client.embeddings.create(
        input=norm_query,
        model=config.EMBEDDING_MODEL
    )
    query_vector = query_embedding_response.data[0].embedding

    # ---- 4. Retrieve Context ----
    # Increased top_k to catch more context for "all products" queries
    search_results = index.query(
        vector=query_vector,
        top_k=7, 
        include_metadata=True
    )

    contexts = [
        match["metadata"]["text"]
        for match in search_results["matches"]
        if match["score"] > 0.15 # Lowered slightly to be more inclusive
    ]

    if not contexts:
        return "I don't have enough information about that in the company documents."

    context_str = "\n\n---\n\n".join(contexts)

    # ---- 5. System Prompt ----
    system_prompt = """
You are an internal AI assistant for Acme Tech Solutions.

Rules:
- Answer ONLY using the provided context.
- If the user asks specifically about "all products", list them all based on the context.
- If answer is not present → say "I don't have enough information about that."
- Never use outside knowledge.
- Be professional and concise.
"""

    user_prompt = f"""
Context:
{context_str}

User Question:
{query}

Answer:
"""

    # ---- 6. Generate Answer ----
    response = openai_client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0.1
    )

    return response.choices[0].message.content

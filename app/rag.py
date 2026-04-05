import os
import re

documents = []

# 🔹 Load XML files
def load_documents():
    docs = []
    folder = "data/rules"

    for file in os.listdir(folder):
        if file.endswith(".xml"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                content = f.read()
                docs.append({
                    "content": content,
                    "filename": file
                })

    return docs


# 🔹 Extract keywords from query
def extract_keywords(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)

    # remove common words
    stopwords = {"the", "is", "to", "a", "for", "and", "of"}
    return [w for w in words if w not in stopwords]


# 🔹 Detect rule type
def detect_rule_type(query):
    query = query.lower()

    if "activity" in query:
        return "activity"
    elif "flow" in query:
        return "flow"
    elif "section" in query:
        return "section"
    
    return None


# 🔹 Build index (just load data)
def build_index():
    global documents
    documents = load_documents()
    print(f"Loaded {len(documents)} XML files")


# 🔹 Smart retrieval
def retrieve(query, k=3):
    keywords = extract_keywords(query)
    rule_type = detect_rule_type(query)

    scored_docs = []

    for doc in documents:
        text = doc["content"].lower()

        score = 0

        # 🔹 Keyword matching score
        for word in keywords:
            if word in text:
                score += 2

        # 🔹 Rule type boost
        if rule_type and rule_type in text:
            score += 5

        # 🔹 Filename boost
        if any(word in doc["filename"].lower() for word in keywords):
            score += 3

        scored_docs.append((score, doc["content"]))

    # Sort by score
    scored_docs.sort(reverse=True, key=lambda x: x[0])

    # Return top k
    return [doc for score, doc in scored_docs[:k] if score > 0]

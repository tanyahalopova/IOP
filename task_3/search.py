import re
def evaluate_query(query):
    tokens = re.findall(r'\w+|AND|OR|NOT|\(|\)', query)
    expression = []
    for token in tokens:
        token_lower = token.lower()
        if token_lower == "and":
            expression.append("&")
        elif token_lower == "or":
            expression.append("|")
        elif token_lower == "not":
            expression.append("all_docs -")
        elif token in ["(", ")"]:
            expression.append(token)
        else:
            docs = index.get(token_lower, set())
            expression.append(str(docs))
    expr = " ".join(expression)
    return eval(expr)


INDEX_FILE = "inverted_index.txt"
index = {}
all_docs = set()

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    for line in f:
        lemma, docs = line.strip().split(":")
        docs_set = set(docs.strip().split())
        index[lemma] = docs_set
        all_docs.update(docs_set)


while True:
    query = input("Введите запрос: ")
    result = evaluate_query(query)
    print("Документы:", result)
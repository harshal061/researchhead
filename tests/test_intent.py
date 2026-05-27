from agents.intent_agent import extract_intent

query = """
I want papers about low-data medical image classification using transformers
"""

result = extract_intent(query)

print(result)
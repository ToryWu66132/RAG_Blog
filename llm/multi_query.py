from llm.client import get_llm_client

client = get_llm_client()


def generate_multi_queries(query, n=3):
    prompt = f"""
You are an expert in search query optimization.

Generate {n} different search queries for the following user question.

Requirements:
- Keep the original intent
- Use different wording and perspectives
- Be concise
- Do not introduce unrelated concepts

Original Query:
{query}

Output format:
1. ...
2. ...
3. ...
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.7,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    queries = []
    for line in content.split("\n"):
        if line.strip():
            q = line.split(".", 1)[-1].strip()
            if q:
                queries.append(q)

    return queries
from llm.client import get_llm_client

# 实例化客户端
client = get_llm_client()


def rewrite_query(query):
    prompt = f"""
    You are an expert in search query optimization.

    Rewrite the user query to improve semantic retrieval quality.

    Requirements:
    - Keep original intent
    - Add relevant keywords if missing
    - Make it more specific and explicit
    - Do NOT introduce unrelated concepts

    Original Query:
    {query}

    Rewritten Query:
    """

    # 调用LLM
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

from llm.client import get_llm_client

client = get_llm_client()


def generate_blog(topic, context):
    prompt = f"""
    You are an expert technical writer.

    Write a structured blog post based ONLY on the provided context.

    Requirements:
    - Use only the information from the context
    - Do NOT add unsupported facts
    - Organize the article with clear sections and headings
    - Make the explanation clear and logical

    Context:
    {context}

    Topic:
    {topic}

    Output format:
    - Title
    - Introduction
    - Main Sections
    - Conclusion
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are a precise and factual writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

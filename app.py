import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from rag.chunker import chunk_text
from rag.embedder import Embedder
from rag.retriever import Retriever
from llm.generator import generate_blog
from llm.query_rewriter import rewrite_query
from rag.reranker import Reranker
from publish.feishu import upload_to_feishu
from llm.multi_query import generate_multi_queries


embedder = Embedder()
reranker = Reranker()
retriever = None

st.title("RAG博客生成器")

uploaded_file = st.file_uploader("请上传参考文件")

platform = st.selectbox("选择平台", ["飞书", "本地"])

auto_upload = st.checkbox("自动上传")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    chunks = chunk_text(text)
    embeddings = embedder.encode(chunks)

    retriever = Retriever(len(embeddings[0]))
    retriever.add(embeddings, chunks)

    st.success("Document processed!")

query = st.text_input("Enter topic")

if query and retriever:
    queries = [query]

    rewritten = rewrite_query(query)
    queries.append(rewritten)

    queries.extend(generate_multi_queries(query))

    queries = list(dict.fromkeys(queries))

    all_docs = []
    seen_docs = set()

    for q in queries:
        query_emb = embedder.encode([q])[0]
        docs = retriever.search(query_emb, k=5)

        for doc in docs:
            if doc not in seen_docs:
                all_docs.append(doc)
                seen_docs.add(doc)

    docs = reranker.rerank(query, all_docs, top_k=3)

    context = "\n".join(docs)

    blog = generate_blog(query, context)

    st.subheader("Generated Blog")
    st.write(blog)

    if auto_upload and platform == "飞书":
        url = upload_to_feishu(query, blog)
        st.success(f"已自动上传到飞书: {url}")

    if st.button("上传博客"):
        if platform == "飞书":
            url = upload_to_feishu(query, blog)
            st.success(f"上传成功: {url}")


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    # 主循环
    while start < len(text):
        # 切片
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        #移动窗口
        start += chunk_size - overlap

    return chunks
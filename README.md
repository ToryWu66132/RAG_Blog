# RAG_Blog
一个面向内容生成场景的轻量级 RAG 项目：用户上传参考资料，系统完成文本切分、向量化检索、查询重写、结果重排与博客生成，并支持将结果发布到飞书文档。

这个项目适合作为一个简洁清晰的 RAG 入门样例，也适合拿来演示“检索增强生成”在知识整理、技术写作和企业内容生产中的基本落地方式。

项目亮点
基于 Streamlit 提供可直接交互的 Web 界面
支持上传参考文档，按分块构建本地检索语料
使用 SentenceTransformer 完成文本向量化
基于 FAISS 实现向量召回
使用 LLM 对用户问题进行 Query Rewrite，提升检索质量
引入 CrossEncoder 进行重排，优化最终上下文
调用 DeepSeek Chat 生成结构化博客内容
支持将生成结果自动发布到飞书文档
提供简单的检索效果评估脚本，便于对比重排前后结果
适用场景
根据已有资料快速生成技术博客
将内部知识文档整理为对外可读内容
演示 RAG 系统的最小可运行闭环
作为课程作业、作品集或原型项目的基础模板
核心流程
上传文档
  -> 文本切分
  -> 向量编码
  -> FAISS 建库
  -> 用户输入主题
  -> Query Rewrite
  -> 向量召回
  -> Rerank 重排
  -> 拼接上下文
  -> LLM 生成博客
  -> 可选发布到飞书
技术栈
前端交互：Streamlit
向量模型：sentence-transformers/all-MiniLM-L6-v2
重排模型：cross-encoder/ms-marco-MiniLM-L-6-v2
向量检索：FAISS
大模型调用：OpenAI SDK + DeepSeek API
发布渠道：Feishu Open Platform
项目结构
RAG_Blog/
├── app.py                  # Streamlit 应用入口
├── rag/
│   ├── chunker.py          # 文本切分
│   ├── embedder.py         # 向量编码
│   ├── retriever.py        # FAISS 检索
│   └── reranker.py         # CrossEncoder 重排
├── llm/
│   ├── client.py           # DeepSeek 客户端封装
│   ├── query_rewriter.py   # 查询重写
│   ├── generator.py        # 博客生成
│   └── deepseek_llm.py     # 备用/实验性封装
├── publish/
│   └── feishu.py           # 飞书文档创建与写入
├── evaluation/
│   ├── evaluator.py        # 检索效果对比
│   └── run_eval.py         # 评估脚本入口
└── requirements.txt
快速开始
1. 安装依赖
pip install -r requirements.txt
2. 配置环境变量
在项目根目录创建 .env 文件：

API_KEY=your_deepseek_api_key
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
说明：

API_KEY 用于调用 DeepSeek 模型
FEISHU_APP_ID 和 FEISHU_APP_SECRET 用于发布到飞书
如果你只想本地生成博客，可以先只配置 API_KEY
3. 启动项目
streamlit run app.py
启动后你可以：

上传一份 UTF-8 编码的文本资料
输入想生成的博客主题
查看系统基于参考内容生成的博客结果
选择是否自动上传到飞书
功能说明
1. 文档切分
项目使用固定窗口和重叠策略对原始文本进行切分，避免检索时上下文过长，同时保留一定语义连续性。

2. 向量召回
切分后的文本块会被编码成向量并写入 FAISS 索引，用于后续相似度搜索。

3. Query Rewrite
用户输入主题后，系统会先用 LLM 改写查询，使检索请求更明确、更利于召回相关内容。

4. Rerank 重排
在初步召回多个候选片段后，项目通过 CrossEncoder 再次打分排序，选出更相关的上下文交给生成模型。

5. 博客生成
生成模块会要求模型“仅基于检索到的上下文”输出带有标题、引言、正文分节和结论的结构化博客，以降低内容幻觉。

6. 飞书发布
博客生成完成后，可调用飞书开放平台接口自动创建文档并写入内容，方便内部分享或沉淀。

评估方式
项目内置了一个简单的检索评估脚本，用于比较：

仅向量检索的结果
向量检索 + 重排后的结果
运行方式：

python evaluation/run_eval.py
注意：当前脚本默认读取 data/sample.txt，仓库中未包含该文件，使用前需要自行准备测试数据。

当前实现特点
这个项目的优势在于结构直观、链路完整、易于理解，特别适合：

学习 RAG 的基本组成模块
快速搭建一个可以演示的原型系统
在此基础上继续扩展为面向真实业务的知识生成工具
同时，目前版本也保持了明显的“轻量原型”特征，例如：

文档上传后默认按纯文本方式解析，暂未覆盖 PDF、Word 等复杂格式
“本地”发布选项已出现在界面中，但当前主要实现的是飞书上传链路
检索索引运行在内存中，未做持久化
提示词、切分策略、召回数量和重排数量仍可继续调优
可继续优化的方向
增加 PDF、Markdown、Word 等多格式文档解析
引入向量库持久化能力
支持多文档知识库管理
增加博客风格、语气与篇幅控制
完善本地导出能力，例如导出 Markdown 或 HTML
增加更完整的自动化评估指标
为发布模块增加更多平台适配
演示价值
如果你希望把它作为作品集项目来介绍，这个项目最有代表性的地方在于：

它不是单独调用大模型写文章，而是展示了“检索增强生成”的完整工程链路
它把生成质量提升拆成了多个具体环节：切分、召回、改写、重排、生成、发布
它兼顾了交互界面与后端流程，具备较强的演示性
一句话概括：

一个从参考资料到结构化博客、再到飞书发布的端到端 RAG 内容生成原型。

License
本项目可根据你的实际需求补充开源协议；如果计划公开发布，建议补充 MIT 或 Apache-2.0 等许可证说明。

# 轻量 RAG 检索系统

用 LangChain 向量检索从临床文本中查找关键信息，并模拟 LLM 生成回答。

## 脚本

| 文件 | 说明 |
|---|---|
| `rag_langchain.py` | LangChain RAG 管线：TextSplitter → Embedding → VectorStore → 检索 |
| `rag_qa.py` | 完整问答演示：写死的临床文本 + 模拟 LLM 回答 |

## 快速开始

```bash
python rag_langchain.py    # 向量检索
python rag_qa.py           # 检索 + 回答
```

## 示例输出

```
用户提问: 排除标准是什么？

[检索到 4 个相关文档块]

AI 回答:
根据临床方案，本研究的排除标准如下：

  - 排除标准：既往接受过全身化疗或胸部放疗，存在症状性脑转移，
    活动性自身免疫性疾病，妊娠期或哺乳期女性
```

## 原理：一行对照 LangChain + ChromaDB

| 步骤 | LangChain + ChromaDB | 本脚本等价实现 |
|---|---|---|
| 加载文本 | `TextLoader("file.txt").load()` | 写死在代码中 |
| 分句 | `RecursiveCharacterTextSplitter()` | 按句号/换行手动切分 |
| 向量化 | `OpenAIEmbeddings()` | sklearn `TfidfVectorizer` |
| 存入向量库 | `Chroma.from_documents(docs, embedding)` | `InMemoryVectorStore.from_documents()` |
| 检索 | `vector_store.similarity_search(query)` | 完全一样 |
| 回答 | 调用 GPT/Claude API | `fake_llm_answer()` 从检索结果提取 |

## 依赖

- `langchain` `langchain-core` `langchain-community`
- `scikit-learn`

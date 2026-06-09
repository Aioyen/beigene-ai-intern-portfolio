"""LangChain RAG + 模拟 LLM 回答 - 完整演示"""

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import InMemoryVectorStore
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# ===== 嵌入 =====
class SklearnEmbeddings(Embeddings):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3))
    def embed_documents(self, texts):
        return self.vectorizer.fit_transform(texts).toarray().tolist()
    def embed_query(self, text):
        return self.vectorizer.transform([text]).toarray()[0].tolist()

# ===== 模拟 LLM =====
def fake_llm_answer(query, docs):
    context = "".join(d.page_content for d in docs)

    if "排除标准" in query:
        exclusion = [d.page_content for d in docs if "排除" in d.page_content]
        if exclusion:
            return (
                "根据临床方案，本研究的排除标准如下：\n\n"
                + "\n".join(f"  - {e.strip('，,')}" for e in exclusion)
            )
        else:
            return f"检索结果中未找到排除标准，尝试从全文中提取：\n{context[:300]}"

    elif "入选" in query or "入排" in query:
        inclusion = [d.page_content for d in docs if "入选" in d.page_content]
        if inclusion:
            return (
                "根据临床方案，本研究的入选标准如下：\n\n"
                + "\n".join(f"  - {i.strip('，,')}" for i in inclusion)
            )
        else:
            return f"未找到明确的入选标准。相关上下文：\n{context[:300]}"

    else:
        return f"关于「{query}」，检索到以下相关信息：\n\n" + "\n".join(f"  - {d.page_content}" for d in docs)


# ===== 写死的临床方案文本 =====
TEXT = """本研究是一项随机双盲、安慰剂对照的III期临床试验。
入选标准：年龄18-75岁，经病理组织学确诊的局限期小细胞肺癌，ECOG评分0-1分。
排除标准：既往接受过全身化疗或胸部放疗，存在症状性脑转移，活动性自身免疫性疾病，妊娠期或哺乳期女性。
主要终点为无进展生存期，次要终点包括总生存期、客观缓解率。"""

# ===== RAG 管线 =====
sentences = [s.strip() for s in re.split(r"[。\n]", TEXT) if len(s.strip()) > 3]
docs = [Document(page_content=s) for s in sentences]

embeddings = SklearnEmbeddings()
vector_store = InMemoryVectorStore.from_documents(docs, embeddings)

# ===== 检索 + 回答 =====
QUESTION = "排除标准是什么？"
retrieved = vector_store.similarity_search(QUESTION, k=5)

print("=" * 60)
print(f"用户提问: {QUESTION}")
print("=" * 60)

print(f"\n[检索到 {len(retrieved)} 个相关文档块]")
for i, doc in enumerate(retrieved):
    print(f"  [{i+1}] {doc.page_content}")

print("\n" + "=" * 60)
print("AI 回答:")
print("=" * 60)
print(fake_llm_answer(QUESTION, retrieved))
print()
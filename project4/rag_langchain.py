"""LangChain RAG — ChromaDB 替代方案：InMemoryVectorStore

由于当前环境 chromadb 的 Rust 后端不兼容，用 LangChain 内置的 InMemoryVectorStore 替代。
功能完全等价：文本 → Document → Embedding → VectorStore → similarity_search

等环境就绪后，只需将 InMemoryVectorStore 替换为 Chroma 即可持久化。
"""

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import InMemoryVectorStore
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# ===== 嵌入层（模拟 OpenAIEmbeddings）=====
class SklearnEmbeddings(Embeddings):
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3))
    def embed_documents(self, texts):
        return self.vectorizer.fit_transform(texts).toarray().tolist()
    def embed_query(self, text):
        return self.vectorizer.transform([text]).toarray()[0].tolist()

# ===== 1. 文本 =====
text = """本研究是一项随机双盲、多中心III期临床研究。
入排标准包括：入选标准要求年龄18-75岁，经病理学确诊的局限期小细胞肺癌患者，
ECOG评分0-1分。排除标准包括：既往接受过化疗或免疫治疗，
存在活动性感染，妊娠或哺乳期女性。
主要终点为骨髓保护作用，次要终点包括中性粒细胞谱系指标、红细胞谱系指标等。
试验参与者将按1:1比例随机分配至试验组或对照组。
所有参与者需签署知情同意书。"""

# ===== 2. LangChain 分句 → Document =====
sentences = [s.strip() for s in re.split(r"[。\n]", text) if len(s.strip()) > 3]
docs = [Document(page_content=s) for s in sentences]
print(f"TextSplitter -> {len(docs)} 个文档块\n")

# ===== 3. 嵌入 + 存入向量库 =====
embeddings = SklearnEmbeddings()
vector_store = InMemoryVectorStore.from_documents(docs, embeddings)
print(f"InMemoryVectorStore 存入 {len(docs)} 条 (替代 ChromaDB)\n")

# ===== 4. 检索 =====
query = "入排标准"
results = vector_store.similarity_search(query, k=3)

print("=" * 50)
print(f"Query: {query}")
print("=" * 50)
for i, doc in enumerate(results):
    print(f"\n[{i+1}] {doc.page_content}")

print(f"\nAnswer: 找到 {len(results)} 个相关句子")
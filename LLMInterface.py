from langchain_openai import OpenAIEmbeddings, ChatOpenAI, OpenAI
import numpy as np


class LLMInterface():
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.llm = OpenAI()

    def embed_query(self, query: str) -> np.ndarray:
        return np.array(self.embeddings.embed_query(query))

    def generate(self, query: str) -> str:
        return self.llm.invoke(query)

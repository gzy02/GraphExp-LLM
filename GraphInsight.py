from LLMInterface import LLMInterface
from GraphTree import GraphNode
import networkx as nx

ALPHA = 0.5
BETA = 0.5


class GraphInsight:
    def __init__(self, name: str, description: str, subject: GraphNode, perspective: str):
        self.name = name
        self.description = description
        self.subject = subject
        self.perspective = perspective
        self.interestingness = self.getInterestingness()
        self.impact = self.getImpact()

    def __str__(self):
        return f"{self.subject.graph.name} in perspective {self.perspective} \n{self.name}:\n {self.description}"

    def getInterestingness(self):
        dataset = self.subject.get_dataset()
        graph = self.subject.graph

        return len(graph.nodes)/len(dataset.nodes)

    def getImpact(self) -> float:
        dataset = self.subject.get_dataset()
        graph = self.subject.graph

        max_degree = max(dict(dataset.degree).values())
        impact = 0
        for node in graph.nodes:
            impact += graph.degree[node]/max_degree
        return impact

    def similarity(self, s1: str, s2: str) -> float:
        """calculated using the cosine similarity between the vector representations of the user’s query 𝑄 and the insight 𝐼. This metric assesses the semantic alignment of the insight with the query."""
        interface = LLMInterface()
        vec1 = interface.embed_query(s1)
        vec2 = interface.embed_query(s2)

        return vec1 @ vec2

    def getRelevance(self, query: str):
        return self.similarity(query, self.description)

    def getScore(self) -> float:
        return (ALPHA * self.relevance + BETA * self.interestingness + (1 - ALPHA - BETA) * self.impact)*10

    def calculateScore(self, query: str):
        self.relevance = self.getRelevance(query)
        self.score = self.getScore()

from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from GraphSummary import GraphSummary


class NewlineSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a newline-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split("\n")


class GraphTemplate():
    def __init__(self):
        self.template = PromptTemplate(
            input_variables=["summary", "info", "perspective"],
            template="You are a helpful assistant that proposes helpful insights about a graph.\nHere is a summary of a graph:\n{summary}\nHere is the adjacency list information of this graph:\n```json\n{info}\n```\n\nPlease propose 3 valuable insights from the perspective of {perspective} for users to choose from. ONLY return a newline separated list, and nothing more.",
        )

    def generate(self, summary: GraphSummary, perspective: str) -> str:
        return self.template.format(summary=summary.summary(),
                                    info=summary.info(), perspective=perspective)

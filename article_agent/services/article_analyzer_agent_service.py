import os
from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from dotenv import load_dotenv
import os

load_dotenv()

class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    summary: str

class ArticleAnalyzerAgent:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def gpt_llm(self):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=self.openai_api_key)
        return llm

    def classification_node(self, state: State):
        """
        Classify the article into one of predefined categories:

        Parameters:
            state (State): The current state dictionary containing the text to classify.

        Returns:
            dict: A dictionary with the "classification" key containing the category result.

        Categories:
            - News: Actual reporting of current events.
            - Blog: Personal or informal web writting.
            - Research: Academic or scientific content.
            - Other: Content that does not fit into the above categories.
        """

        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Classify the following text into one of the following categories:News, Blog,Research, or Other. \n\nText: {text}\n\nCategory:
            """
        )

        message = HumanMessage(content=prompt.format(text=state["text"]))

        classification = self.gpt_llm().invoke([message]).content.strip()

        return {"classification": classification}
    
    def entity_extraction_node(self, state: State):
        """
        Function to identify and extract named entities from the text.
        Organized by caregory (Person, Organization, Location, etc.)
        """
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Extract all entities (Person, Organization, Location) from the following text. Provide the result as a comma-separated list. \n\nText: {text}\n\nEntities:
        """
        )

        message = HumanMessage(content=prompt.format(text=state["text"]))

        entities = self.gpt_llm().invoke([message]).content.strip(", ")

        return {"entities": entities}

    def summarize_node(self, state: State):
        # Create template for the summarization prompt
        summarization_prompt = PromptTemplate.from_template(
            """
            Summarize the following text in a few sentences. 
            \n\nText: {text}
            \n\nSummary:
            """
        )

        chain = summarization_prompt | self.gpt_llm()
        result = chain.invoke({"text": state["text"]})

        return {"summary": result.content}

    def agent_structure(self):
        """
        Define the structure of the agent using LangGraph StateGraph.
        """
        workflow = StateGraph(State)

        # Add nodes to the workflow
        workflow.add_node("classification_node", self.classification_node)
        workflow.add_node("entity_extraction", self.entity_extraction_node)
        workflow.add_node("summarization", self.summarize_node)

        #  Add edges to the workflow
        workflow.set_entry_point("classification_node")
        workflow.add_edge("classification_node", "entity_extraction")
        workflow.add_edge("entity_extraction", "summarization")
        workflow.add_edge("summarization", END)

        return workflow.compile()
        
        
        

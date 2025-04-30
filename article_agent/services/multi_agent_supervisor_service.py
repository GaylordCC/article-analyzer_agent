from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import uuid

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

load_dotenv()

class MultiAgentSupervisor:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=self.openai_api_key)
        self.checkpointer = InMemorySaver()
        self.store = InMemoryStore()

    def add(self, a: float, b: float) -> float:
        """
        Add two numbers together.
        """
        return a + b
    
    def multiply(self, a: float, b: float) -> float:
        """
        Multiply two numbers.
        """
        return a * b
    
    def web_search(self, query: str) -> str:
        """
        Search the web for information.
        """
        return (
            " Here are the headcounts for each of the FAANG companies in 2024: \n"
            "1. **Facebook**: 67,317 employees.\n"
            "2. **Apple**: 164,000 employees.\n"
            "3. **Amazon**: 1,551,000 employees.\n"
            "4. **Netflix**: 14,000 employees.\n"
            "5. **Google (Alphabet)**: 181,269 employees.\n"
        )
    
    def math_agent(self):
        """
        A math agent that can add, multiply, and search the web.
        """
        return create_react_agent(
            model=self.model,
            tools=[self.add, self.multiply],
            name="math_expert",
            prompt= "You are a math expert. Always use one tool at time"
        )
        
    def research_agent(self):
        """
        A web search agent that can search the web for information.
        """
        return create_react_agent(
            model=self.model,
            tools=[self.web_search],
            name="research_expert",
            prompt= "You are a World class research with access to web search. Do not do math."
        )
    
    def create_supervisor(self):
        workflow = create_supervisor(
            [self.math_agent(), self.research_agent()],
            model=self.model,
            prompt = (
                    "You are a team supervisor managing a research expert and math expert"
                    "For current event, use reserach-agent"
                    "For math problems, use math_agent"
                )
            )

        app = workflow.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )
        results = app.invoke({
            "messages": [
                {"role": "user",
                "content": "what is 234 times 568?"
                }
            ]
        },
        config={"thread_id": str(uuid.uuid4())}
        )
        return results
        
    
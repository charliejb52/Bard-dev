from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
import json
from langgraph.graph import StateGraph, START, END

load_dotenv()

if os.environ["OPENAI_API_KEY"]:
    print("OpenAI api key set")
else:
    raise ValueError("OpenAI api key is not set")

llm = ChatOpenAI(model="gpt-5.4")

# graph schema for scales agent:
class scale_agent_schema(BaseModel):
    measures: List = Field(description="a list of the measures to be analyzed")
    scale: List = Field(description="the underlying scale being outlined during the selected measures. Stored in the same format as the measures themselves")

# response schema for scales agent:
class llm_schema(BaseModel):
    scale: str = Field(description="the underlying scale being outlined during the selected measures. Stored in the same format as the measures themselves")

llm_with_schema = llm.with_structured_output(llm_schema)

llm_with_schema.invoke("give one measure of the pentatonic scale as a list of beats nested inside a measure dict")

def determine_scale(state: scale_agent_schema) -> scale_agent_schema:

    measures = ", ".join(json.dumps(measure) for measure in state.measures)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a guitar music theory expert who looks at the notes of a song and determines the scales being played"),
            ("human", "Determine the scale being played in this song:\n\n{measures}\n\nThen put all the notes of the underlying scale shape into your response in the same format as the input.")
        ]
    )

    chain = prompt | llm_with_schema

    response = chain.invoke({"measures": measures})

    state.scale = response.scale

    return state


def scale_agent_graph():
    # returns a scale agent graph
    graph = StateGraph(scale_agent_schema)

    graph.add_node("determine_scale", determine_scale)

    graph.add_edge(START, "determine_scale")
    graph.add_edge("determine_scale", END)

    return graph.compile()
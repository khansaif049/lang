from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

KB = {
    "langgraph": "LangGraph lets you build stateful workflows for LLM apps.",
    "node": "A node is one step in the graph.",
    "state": "State is shared data passed between nodes.",
}


class GraphState(TypedDict, total=False):
    user_query: str
    intent: Literal["greeting", "help", "question"]
    final_reply: str
    messages: list[str]
    is_valid: bool
    error_message: str

    context: str
    found_match: bool
    match_count: int


def validate_query_node(state:GraphState) -> GraphState:
    user_query = state.get("user_query", "").strip().lower()
    messages = state.get("messages", [])

    if not user_query:
        return {
            "is_valid": False,
            "error_message": "Query is missing",
            "messages": messages + ["validate failed"],
        }

    return {"is_valid":True, "messages": messages + ["validate passed"]}


def classify_query_node(state:GraphState) -> GraphState:
    user_query = state.get("user_query", "").strip().lower()
    messages = state.get("messages", [])
    list_of_greetings = ["hi", "hello", "hey"]
    list_of_help = ["help", "kaise", "samjha", "sikha"]

    if any(word in user_query for word in list_of_greetings):
        return {"intent":"greeting", "messages": messages + ["intent=greeting"]}

    if any(word in user_query for word in list_of_help):
        return {"intent":"help", "messages": messages + ["intent=help"]}

    return {"intent":"question", "messages": messages + ["intent=question"]}

def greeting_node(state:GraphState) -> GraphState:
    messages = state.get("messages", [])
    return {
        "final_reply":"Hello bhai, kaise help karu?",
        "messages": messages + ["greeting reply created"],
    }
    
def help_node(state:GraphState) -> GraphState:
    messages = state.get("messages", [])
    context = state.get("context", "")
    found_match = state.get("found_match", False)

    if found_match:
        return {
            "final_reply": f"Main help kar sakta hoon. {context}",
            "messages": messages + ["help reply created"],
        }
    else:
        return {
            "final_reply":"Main tumhe LangGraph basics step by step samjha sakta hoon",
            "messages": messages + ["help reply created"],
        }
        
    
def question_node(state:GraphState) -> GraphState:
    messages = state.get("messages", [])
    context = state.get("context", "")
    found_match = state.get("found_match", False)
    if found_match:
        return {
            "final_reply":f"Main is query ko handle kar raha hoon: {state['user_query']}  {context}",
            "messages": messages + ["question reply created"],
        }
    else:
        return {
            "final_reply":f"Main is query ko handle kar raha hoon: {state['user_query']}",
            "messages": messages + ["question reply created"],
        }


def fallback_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    return {
        "final_reply": "Iss topic ke liye mere paas enough context nahi mila. Thoda aur specific poochho.",
        "messages": messages + ["fallback reply created"],
    }


def error_node(state:GraphState) -> GraphState:
    messages = state.get("messages", [])
    return {
        "final_reply":f"Error: {state['error_message']}",
        "messages": messages + ["error reply created"],
    }

def lookup_node(state: GraphState) -> GraphState:
    query = state["user_query"].lower()
    messages = state.get("messages", [])

    for key, value in KB.items():
        if key in query:
            return {
                "context": value,
                "found_match": True,
                "match_count": 1,
                "messages": messages + [f"context found for {key}"],
            }

    return {
        "context": "",
        "found_match": False,
        "match_count": 0,
        "messages": messages + ["no context found"],
    }



def validate_route(state: GraphState) -> str:
    if state["is_valid"]:
        return "ok"
    return "error"

def intent_route(state: GraphState) -> str:
    return state["intent"]

def lookup_quality_route(state: GraphState) -> str:
    if state.get("match_count", 0) > 0:
        return "match"
    return "fallback"

def post_lookup_route(state: GraphState) -> str:
    return state["intent"]

graph = StateGraph(GraphState)

graph.add_node("validate_query_node",validate_query_node)
graph.add_node("classify_query_node",classify_query_node)
graph.add_node("greeting_node",greeting_node)
graph.add_node("help_node",help_node)
graph.add_node("question_node",question_node)
graph.add_node("fallback_node",fallback_node)
graph.add_node("error_node",error_node)
graph.add_node("lookup_node",lookup_node)

graph.add_edge(START, "validate_query_node")

graph.add_conditional_edges(
    "validate_query_node",
    validate_route,
    {
        "ok": "classify_query_node",
        "error": "error_node",
    },
)

graph.add_conditional_edges(
    "classify_query_node",
    intent_route,
    {
        "greeting": "greeting_node",
        "help": "lookup_node",
        "question": "lookup_node"
    },
)

graph.add_conditional_edges(
    "lookup_node",
    lookup_quality_route,
    {
        "match":"classify_query_node_after_lookup",
        "fallback":"fallback_node"
    }
)

graph.add_node("classify_query_node_after_lookup", lambda state: {})

graph.add_conditional_edges(
    "classify_query_node_after_lookup",
    post_lookup_route,
    {
        "help":"help_node",
        "question":"question_node"
    }
)

graph.add_edge("greeting_node",END)
graph.add_edge("help_node",END)
graph.add_edge("question_node",END)
graph.add_edge("fallback_node",END)
graph.add_edge("error_node",END)

app = graph.compile()

print("\nBuilt-in graph view:\n")
print(app.get_graph().draw_ascii())

if __name__ == "__main__":
    initial_state: GraphState = {"user_query": "langgraph kaise kaam karta hai", "messages": []}

    for step in app.stream(initial_state):
        print(step)

    result = app.invoke(initial_state)
    print("\nFinal messages:")
    for msg in result["messages"]:
        print(f"- {msg}")

    print("\nFinal reply:")
    print(result["final_reply"])

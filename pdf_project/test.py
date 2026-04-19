from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict, total=False):
    name: str
    mood: str
    time_of_day:str
    route: Literal["happy", "serious","angry"]
    response_style: Literal["short", "normal"]
    reply: str
    final_reply:str
    is_valid:bool
    error_message:str
    advice:str
    messages: list[str]

def validate_node(state: GraphState) -> GraphState:
    mood = state.get("mood", "").strip().lower()
    name = state.get("name", "").strip()
    messages = state.get("messages", [])

    if not name or not mood:
        return {
            "is_valid": False,
            "error_message": "Name or mood is missing",
            "messages": messages + ["validate failed"]
        }
    else:
        return {"is_valid":True,"messages": messages + ["validate passed"]}

def error_node(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    return {
        "final_reply": f"Error: {state['error_message']}",
        "messages": messages + ["error reply created"],
    }

def tool_node(state:GraphState) -> GraphState:
    route = state["route"].lower()
    messages = state.get("messages", [])
    if route == "happy":
        return {
            "advice": "Keep this momentum going.",
            "messages": messages + ["tool advice added"],
        }
    if route == "serious":
        return {
            "advice": "Break the work into small steps.",
            "messages": messages + ["tool advice added"],
        }
    return {
        "advice": "Take a breath and slow down.",
        "messages": messages + ["tool advice added"],
    }

def summary_node(state: GraphState) -> GraphState:
    text = state["final_reply"]
    short_text = " ".join(text.split()[:6]) + "..."
    messages = state.get("messages", [])
    return {
        "final_reply": short_text,
        "messages": messages + ["summary applied"],
    }

def style_route(state: GraphState) -> str:
    # response_style = state["response_style"].lower()
    # # if response_style == "short":
    # #     response_style
    return state["response_style"]


def decide_route(state: GraphState) -> GraphState:
    mood = state["mood"].lower()
    route: Literal["happy", "serious", "angry"]
    messages = state.get("messages", [])

    if mood in {"happy", "excited"}:
        route = "happy"
    elif mood in {"angry", "frustrated"}:
        route = "angry"
    else:
        route = "serious"

    return {"route": route, "messages": messages + [f"route={route}"]}


def happy_node(state: GraphState) -> GraphState:
    reply = f"Hi {state['name']}! Aaj energy kaafi achchi lag rahi hai."
    messages = state.get("messages", [])
    return {"reply": reply, "messages": messages + ["happy reply created"]}


def serious_node(state: GraphState) -> GraphState:
    reply = f"Hi {state['name']}. Chalo calmly step by step kaam karte hain."
    messages = state.get("messages", [])
    return {"reply": reply, "messages": messages + ["serious reply created"]}


def angry_node(state:GraphState) -> GraphState:
    reply = f"Hi {state['name']}. kya bhai langgraph sikh raha hai angry mode me"
    messages = state.get("messages", [])
    return {"reply":reply, "messages": messages + ["angry reply created"]}

def add_time_node(state: GraphState) -> GraphState:
    time_of_day = state["time_of_day"].lower()
    reply = state["reply"]
    advice = state["advice"]
    messages = state.get("messages", [])

    if time_of_day == "morning":
        final_reply = f"Good morning! {reply} {advice}"
    elif time_of_day == "afternoon":
        final_reply = f"Good afternoon! {reply} {advice}"
    elif time_of_day == "night":
        final_reply = f"Good night! {reply} {advice}"
    else:
        final_reply = f"{reply} {advice}"

    return {
        "final_reply": final_reply,
        "messages": messages + [f"time style applied: {time_of_day}"],
    }



def route_next(state: GraphState) -> str:
    return state["route"]


graph = StateGraph(GraphState)

graph.add_node("validate_node",validate_node)

graph.add_node("summary_node",summary_node)
# graph.add_node("style_route",style_route)

graph.add_node("decide_route", decide_route)

graph.add_node("happy_node", happy_node)
graph.add_node("serious_node", serious_node)
graph.add_node("angry_node", angry_node)
graph.add_node("tool_node",tool_node)


graph.add_node("add_time_node",add_time_node)
graph.add_node("error_node",error_node)

graph.add_edge(START, "validate_node")

def validate_route(state: GraphState) -> str:
    if state["is_valid"]:
        return "ok"
    return "error"



graph.add_conditional_edges(
    "validate_node",
    validate_route,
    {
        "ok": "decide_route",
        "error": "error_node",
    },
)

# graph.ad
graph.add_conditional_edges(
    "decide_route",
    route_next,
    {
        "happy": "happy_node",
        "serious": "serious_node",
        "angry": "angry_node"
    },
)




graph.add_edge("happy_node", "tool_node")
graph.add_edge("serious_node", "tool_node")
graph.add_edge("angry_node", "tool_node")

graph.add_edge("tool_node", "add_time_node")

graph.add_conditional_edges(
    "add_time_node",
    style_route,
    {
        "short": "summary_node",
        "normal": END,
    },
)

graph.add_edge("summary_node",END)
graph.add_edge("error_node",END)

app = graph.compile()

print("\nBuilt-in graph view:\n")
print(app.get_graph().draw_ascii())


if __name__ == "__main__":
    initial_state: GraphState = {
        "name": "saif",
        "mood": "angry",
        "time_of_day":"morning",
        "response_style": "short",
        "messages": [],
    }


    print("\nStream output:")
    for step in app.stream(initial_state):
        print(step)

    result = app.invoke(initial_state)

    print("\nFinal messages:")
    for msg in result["messages"]:
        print(f"- {msg}")

    print("\nFinal reply:")
    print(result["final_reply"])

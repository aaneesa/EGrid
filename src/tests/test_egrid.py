from src.agent.graph import app
from langchain_core.messages import HumanMessage

def run_agent_test(query: str):
    print(f"\n{'='*60}")
    print(f"🚀 TESTING QUERY: {query}")
    print(f"{'='*60}")

    # The input must now be a list of messages
    inputs = {"messages": [HumanMessage(content=query)]}

    # Stream the output to see the "Thought Process"
    for event in app.stream(inputs, stream_mode="values"):
        message = event["messages"][-1]
        
        # Check if the Agent is calling a tool
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                print(f"🛠️  AGENT ACTION: Calling Tool [{tool_call['name']}]")
                print(f"    Arguments: {tool_call['args']}")
        
        # Check if a tool is returning data
        if message.type == "tool":
            print(f"📥 TOOL RESPONSE: Data received from {message.name}")

    print("\n✅ FINAL ENGINEERING MANDATE:")
    print(event["messages"][-1].content)
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # TEST 1: Standard Analysis (Triggers ML + RAG)
    run_agent_test("Provide a mandate for a 35°C Monday at 6 PM in Chicago.")

    # TEST 2: Pure Policy (Should skip ML, only call RAG)
    run_agent_test("What are the GS-CRIT-03 grid standards?")

    # TEST 3: Simulation (Triggers the Scenario Engine)
    run_agent_test("What if EV adoption triples and we have a 5 degree temp rise?")
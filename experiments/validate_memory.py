"""
Validation script for Agent Memory.
"""
from agentblueprint_core import Agent, SimpleMemory

def test_memory():
    print("\n🧪 Testing Agent Memory...")
    
    memory = SimpleMemory()
    agent = Agent(
        name="mem_agent",
        model="mock",
        memory=memory
    )
    
    # 1. First run
    print("Run 1: Hello")
    res1 = agent.run("Hello")
    print(f"Response: {res1}")
    
    # 2. Verify memory
    history = memory.get_history()
    print(f"History after 1: {history}")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    
    # 3. Second run
    print("Run 2: World")
    res2 = agent.run("World")
    print(f"Response: {res2}")
    
    # 4. Verify context accumulation
    context = memory.get_context()
    print(f"Full Context:\n{context}")
    
    assert "USER: Hello" in context
    assert "ASSISTANT: ECHO [mem_agent]: Hello" in context
    assert "USER: World" in context
    
    print("✅ Memory validation successful")

if __name__ == "__main__":
    test_memory()

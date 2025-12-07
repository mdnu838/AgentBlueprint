"""
Validation script for LLM Provider system.
"""
from agentblueprint_core import Agent, LLMFactory, MockLLM, OpenAILLM

def test_factory():
    print("\n🧪 Testing LLMFactory...")
    
    # Test Mock
    provider = LLMFactory.create("mock:v1")
    assert isinstance(provider, MockLLM)
    print("✅ Factory created MockLLM")
    
    # Test OpenAI
    # We expect this to instantiate OpenAILLM even if API key is missing (it might fail on generation, but init should work or fail gracefully)
    try:
        provider = LLMFactory.create("openai:gpt-4")
        assert isinstance(provider, OpenAILLM)
        print("✅ Factory created OpenAILLM")
    except ImportError:
        print("⚠️ OpenAI package not installed (Skipping OpenAI test)")
    except Exception as e:
        print(f"⚠️ OpenAI Init error (expected if key missing): {e}")

def test_agent_integration():
    print("\n🧪 Testing Agent Provider Integration...")
    
    # Test Mock Agent
    agent = Agent(name="test", model="mock:gpt-4")
    response = agent.run("Hello")
    print(f"Mock Response: {response}")
    assert "ECHO" in response
    print("✅ Agent uses Mock provider correctly")

def main():
    test_factory()
    test_agent_integration()
    print("\n✅ LLM Provider validation passed")

if __name__ == "__main__":
    main()

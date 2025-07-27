#!/usr/bin/env python3
"""
Simple test script to verify the Telecom Sales Agent works correctly
"""

import json
from datetime import datetime

def test_models():
    """Test that all models can be imported and instantiated"""
    print("🧪 Testing models...")
    
    try:
        from src.models.customer_profile import (
            CustomerProfile, TelecomPlan, PlanComparison, 
            CustomerNeeds, UsageData, Priority, UsagePattern, CustomerSegment
        )
        
        # Test CustomerNeeds
        needs = CustomerNeeds(
            cost_sensitivity=Priority.HIGH,
            data_priority=Priority.CRITICAL,
            voice_priority=Priority.MEDIUM,
            network_quality=Priority.HIGH,
            customer_service=Priority.MEDIUM,
            flexibility=Priority.LOW
        )
        
        # Test UsageData
        usage = UsageData(
            data_usage_gb=25.5,
            voice_minutes=800,
            sms_count=1200,
            international_usage=True,
            roaming_usage=False,
            peak_usage_hours=[9, 17, 18]
        )
        
        # Test CustomerProfile
        profile = CustomerProfile(
            customer_id="test_001",
            name="Test Customer",
            location="Test City",
            segment=CustomerSegment.INDIVIDUAL,
            usage_pattern=UsagePattern.MODERATE,
            current_monthly_spend=75.0,
            usage_data=usage,
            needs=needs
        )
        
        # Test TelecomPlan
        plan = TelecomPlan(
            plan_id="test_plan",
            name="Test Plan",
            price=80.0,
            data_allowance=20.0,
            voice_minutes="unlimited",
            sms_allowance="unlimited"
        )
        
        print("✅ All models imported and instantiated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {str(e)}")
        return False


def test_agents():
    """Test that all agent classes can be imported and instantiated"""
    print("🤖 Testing agents...")
    
    try:
        from src.agents.customer_profiler import CustomerProfiler
        from src.agents.plan_analyzer import PlanAnalyzer
        from src.agents.pitch_generator import PitchGenerator
        
        # Test instantiation
        profiler = CustomerProfiler()
        analyzer = PlanAnalyzer()
        generator = PitchGenerator()
        
        print("✅ All agents imported and instantiated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {str(e)}")
        return False


def test_basic_functionality():
    """Test basic functionality without requiring OpenAI API"""
    print("⚙️ Testing basic functionality...")
    
    try:
        from src.agents.customer_profiler import CustomerProfiler
        from src.models.customer_profile import Priority, UsagePattern
        
        profiler = CustomerProfiler()
        
        # Test basic profiler functionality
        conversation = "I need unlimited data and am price sensitive"
        usage_data = {"data_usage_gb": 45.0, "voice_minutes": 1200, "sms_count": 100}
        
        # Test that the profiler can run without errors
        result = profiler._run(conversation, usage_data)
        
        # Just verify we get a non-empty result (JSON string)
        assert isinstance(result, str) and len(result) > 0
        
        # Test that we can parse the result as JSON
        profile_data = json.loads(result)
        assert "needs" in profile_data
        assert "usage_pattern" in profile_data
        
        print("✅ Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False


def test_workflow_structure():
    """Test that the LangGraph agent structure is correctly set up"""
    print("🔄 Testing workflow structure...")
    
    try:
        from src.langgraph_agent import TelecomSalesAgent, AgentState
        
        # Test that agent can be instantiated (even with dummy key)
        agent = TelecomSalesAgent("dummy-key")
        
        # Test that workflow is built
        assert agent.workflow is not None
        assert agent.app is not None
        
        # Test that required tools are available
        assert len(agent.tools) == 3
        
        print("✅ Workflow structure test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow structure test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("🚀 TELECOM SALES AGENT - TESTING SUITE")
    print("=" * 50)
    
    tests = [
        ("Models", test_models),
        ("Agents", test_agents), 
        ("Basic Functionality", test_basic_functionality),
        ("Workflow Structure", test_workflow_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The agent is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run: streamlit run streamlit_app.py")
        print("3. Or run: python example_usage.py")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
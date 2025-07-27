#!/usr/bin/env python3
"""
Example usage of the Telecom Sales Agent

This script demonstrates how to use the LangGraph-based GenAI agent
to analyze customer profiles, compare telecom plans, and generate
personalized sales pitches.
"""

import os
import json
from datetime import datetime, timedelta

from src.langgraph_agent import TelecomSalesAgent


def create_sample_data():
    """Create sample customer data for demonstration"""
    
    # Sample customer conversation
    customer_conversation = """
    Hi, I'm looking at my phone bill and it seems really high. I'm currently paying $85 per month 
    and I feel like I'm not getting good value. I use my phone a lot for work - lots of video calls 
    and I'm always streaming music during my commute. I travel internationally about twice a year 
    for business and the roaming charges are killing me. My current plan only gives me 15GB of data 
    and I'm constantly hitting the limit. I need unlimited data or at least way more than I have now. 
    The coverage at my office downtown is also pretty spotty - calls drop frequently. I've been with 
    my current carrier for 3 years but I'm ready to switch if I can get better value and reliability.
    I'd prefer not to be locked into a long contract if possible.
    """
    
    # Current plan details
    current_plan = {
        "plan_id": "current_basic_15gb",
        "name": "Business Basic 15GB",
        "price": 85.0,
        "data_allowance": 15.0,
        "voice_minutes": "unlimited",
        "sms_allowance": "unlimited",
        "international_included": False,
        "roaming_included": False,
        "hotspot_data": 5.0,
        "network_priority": "standard",
        "features": ["Visual Voicemail", "Mobile Hotspot"],
        "contract_length": 24,
        "setup_fee": 35.0
    }
    
    # Target plan to pitch
    target_plan = {
        "plan_id": "premium_unlimited",
        "name": "Premium Unlimited Pro",
        "price": 75.0,
        "data_allowance": "unlimited",
        "voice_minutes": "unlimited", 
        "sms_allowance": "unlimited",
        "international_included": True,
        "roaming_included": True,
        "hotspot_data": 50.0,
        "network_priority": "premium",
        "features": [
            "Premium Network Priority",
            "50GB Mobile Hotspot",
            "International Calling & Text",
            "Free Roaming in 200+ Countries",
            "Advanced Security Features",
            "24/7 Premium Support"
        ],
        "contract_length": 12,
        "setup_fee": 0.0,
        "promotional_discount": 20.0,
        "promotional_duration": 6
    }
    
    # Customer usage data
    usage_data = {
        "customer_id": "cust_12345",
        "name": "Sarah Johnson",
        "location": "Downtown Seattle",
        "current_spend": 85.0,
        "data_usage_gb": 18.5,
        "voice_minutes": 850,
        "sms_count": 1200,
        "international_usage": True,
        "roaming_usage": True,
        "peak_usage_hours": [8, 9, 17, 18, 19],
        "business_user": True
    }
    
    return customer_conversation, current_plan, target_plan, usage_data


def demo_basic_usage():
    """Demonstrate basic usage of the sales agent"""
    print("🚀 TELECOM SALES AGENT DEMO - BASIC USAGE")
    print("=" * 60)
    
    # Set up API key (you'll need to set this environment variable)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("⚠️  Warning: OPENAI_API_KEY not set. Using placeholder...")
        openai_api_key = "your-openai-api-key-here"
    
    # Initialize the agent
    print("🤖 Initializing Telecom Sales Agent...")
    agent = TelecomSalesAgent(openai_api_key=openai_api_key)
    
    # Get sample data
    customer_conversation, current_plan, target_plan, usage_data = create_sample_data()
    
    print(f"👤 Processing customer: {usage_data['name']}")
    print(f"📍 Location: {usage_data['location']}")
    print(f"💰 Current spend: ${usage_data['current_spend']}/month")
    print()
    
    try:
        # Process the customer (synchronous version for demo)
        result = agent.process_customer_sync(
            customer_conversation=customer_conversation,
            current_plan=current_plan,
            target_plan=target_plan,
            usage_data=usage_data
        )
        
        if result["success"]:
            print("✅ Analysis completed successfully!")
            print()
            
            # Display customer profile insights
            profile = result["customer_profile"]
            print("👤 CUSTOMER PROFILE INSIGHTS:")
            print(f"• Segment: {profile['segment']}")
            print(f"• Usage Pattern: {profile['usage_pattern']}")
            print(f"• Cost Sensitivity: {profile['needs']['cost_sensitivity']}")
            print(f"• Data Priority: {profile['needs']['data_priority']}")
            print(f"• Network Quality Priority: {profile['needs']['network_quality']}")
            if profile['pain_points']:
                print(f"• Pain Points: {', '.join(profile['pain_points'])}")
            print()
            
            # Display plan comparison
            comparison = result["plan_comparison"]
            print("📊 PLAN COMPARISON SUMMARY:")
            print(f"• Monthly Savings: ${comparison['monthly_savings']:.2f}")
            print(f"• Annual Savings: ${comparison['annual_savings']:.2f}")
            print(f"• Data Change: {comparison['data_difference']}")
            print(f"• Voice Change: {comparison['voice_difference']}")
            print(f"• Suitability Score: {comparison['suitability_score']:.1f}/10")
            if comparison['feature_improvements']:
                print("• New Features:")
                for feature in comparison['feature_improvements'][:3]:
                    print(f"  - {feature}")
            print()
            
            # Display formatted pitch
            print("🎯 FORMATTED SALES PITCH:")
            print("=" * 60)
            formatted_pitch = agent.format_pitch_for_sales_rep(result)
            print(formatted_pitch)
            
        else:
            print(f"❌ Error: {result['error']}")
            
    except Exception as e:
        print(f"💥 Demo failed: {str(e)}")


def demo_multiple_customers():
    """Demonstrate processing multiple customer scenarios"""
    print("\n\n🎭 MULTIPLE CUSTOMER SCENARIOS DEMO")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Budget-Conscious Family",
            "conversation": """
            We're a family of four and our phone bills are getting out of hand. We're paying almost $200 
            per month total and need to cut costs. The kids mainly use WiFi at home and school, and we 
            don't travel much. We just need reliable service for calls and basic internet when we're out.
            Cost is our biggest concern right now.
            """,
            "usage_data": {
                "customer_id": "family_001",
                "name": "The Martinez Family", 
                "location": "Suburban Phoenix",
                "current_spend": 180.0,
                "data_usage_gb": 25.0,
                "voice_minutes": 600,
                "sms_count": 2000,
                "international_usage": False,
                "roaming_usage": False,
                "business_user": False
            },
            "target_plan": {
                "plan_id": "family_value_30gb",
                "name": "Family Value 30GB",
                "price": 120.0,
                "data_allowance": 30.0,
                "voice_minutes": "unlimited",
                "sms_allowance": "unlimited",
                "international_included": False,
                "roaming_included": False,
                "hotspot_data": 10.0,
                "network_priority": "standard",
                "features": ["Family Sharing", "Parental Controls", "4 Lines Included"],
                "contract_length": 12,
                "setup_fee": 0.0,
                "promotional_discount": 25.0,
                "promotional_duration": 12
            }
        },
        
        {
            "name": "Heavy Data User", 
            "conversation": """
            I'm a content creator and I'm constantly uploading videos, streaming, and working on the go. 
            I probably use 80-100GB per month and I need the fastest speeds possible. Money isn't really 
            an issue - I just want the best performance. I also travel a lot for shoots so I need good 
            coverage everywhere and international options would be great.
            """,
            "usage_data": {
                "customer_id": "creator_001",
                "name": "Alex Thompson",
                "location": "Los Angeles",
                "current_spend": 95.0,
                "data_usage_gb": 95.0,
                "voice_minutes": 400,
                "sms_count": 800,
                "international_usage": True,
                "roaming_usage": True,
                "business_user": True
            },
            "target_plan": {
                "plan_id": "ultra_premium",
                "name": "Ultra Premium Unlimited",
                "price": 120.0,
                "data_allowance": "unlimited",
                "voice_minutes": "unlimited",
                "sms_allowance": "unlimited", 
                "international_included": True,
                "roaming_included": True,
                "hotspot_data": 100.0,
                "network_priority": "premium",
                "features": [
                    "5G Ultra-Fast Network",
                    "100GB Premium Hotspot",
                    "Global Roaming",
                    "Priority Customer Support",
                    "Entertainment Bundle Included"
                ],
                "contract_length": 6,
                "setup_fee": 0.0
            }
        }
    ]
    
    # Process each scenario
    agent = TelecomSalesAgent("placeholder-key")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📱 SCENARIO {i}: {scenario['name']}")
        print("-" * 40)
        
        # Use the basic current plan for all scenarios
        _, current_plan, _, _ = create_sample_data()
        
        try:
            result = agent.process_customer_sync(
                customer_conversation=scenario["conversation"],
                current_plan=current_plan,
                target_plan=scenario["target_plan"],
                usage_data=scenario["usage_data"]
            )
            
            if result["success"]:
                profile = result["customer_profile"]
                comparison = result["plan_comparison"]
                pitch = result["personalized_pitch"]
                
                print(f"✅ {scenario['usage_data']['name']} - Analysis Complete")
                print(f"🎯 Suitability Score: {comparison['suitability_score']:.1f}/10")
                print(f"💰 Monthly Impact: ${comparison['monthly_savings']:.2f}")
                print(f"🗣️  Opening Hook: {pitch['opening_hook'][:100]}...")
                print(f"🎁 Top Feature: {pitch['feature_highlights'][0] if pitch['feature_highlights'] else 'N/A'}")
                
            else:
                print(f"❌ Error processing {scenario['name']}: {result['error']}")
                
        except Exception as e:
            print(f"💥 Error in scenario {i}: {str(e)}")


def main():
    """Run the complete demo"""
    print("🌟 TELECOM SALES AGENT - COMPREHENSIVE DEMO")
    print("=" * 70)
    print("This demo showcases a LangGraph-based GenAI agent that:")
    print("• Analyzes customer conversations and usage patterns")
    print("• Compares current vs target telecom plans")
    print("• Generates personalized sales pitches")
    print("• Provides actionable insights for sales representatives")
    print()
    
    # Run demos
    demo_basic_usage()
    demo_multiple_customers()
    
    print("\n\n🎉 DEMO COMPLETE!")
    print("=" * 70)
    print("The Telecom Sales Agent successfully demonstrated:")
    print("✅ Customer needs profiling from conversation analysis")
    print("✅ Intelligent plan comparison with suitability scoring")
    print("✅ Personalized pitch generation with objection handling")
    print("✅ Multiple customer scenario support")
    print()
    print("Ready for integration into your sales workflow! 🚀")


if __name__ == "__main__":
    main()
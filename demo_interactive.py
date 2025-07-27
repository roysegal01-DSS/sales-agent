#!/usr/bin/env python3
"""
Interactive Demo of the Telecom Sales Agent
Shows real-time customer analysis and pitch generation
"""

import json
import os
from datetime import datetime

def run_interactive_demo():
    """Run an interactive demo of the telecom sales agent"""
    
    print("🎯 TELECOM SALES AI AGENT - INTERACTIVE DEMO")
    print("=" * 60)
    print("This demo shows how the agent processes real customer interactions")
    print()
    
    # Demo Scenario 1: Business Customer
    print("📱 SCENARIO 1: Business Customer with High Data Needs")
    print("-" * 50)
    
    customer_conversation_1 = """
    Customer: Hi, I'm calling about my business phone plan. I'm currently paying $120/month 
    and I feel like it's too expensive. My business requires reliable data - I'm constantly 
    on video calls, uploading files to the cloud, and need good coverage when I travel. 
    I've had issues with slow speeds during peak hours and my current plan only gives me 50GB. 
    I'm open to switching if I can get better value and reliability.
    """
    
    current_plan_1 = {
        "name": "Business Pro",
        "monthly_cost": 120.0,
        "data_limit_gb": 50.0,
        "voice_minutes": "unlimited",
        "sms_count": "unlimited",
        "international_calling": False,
        "roaming": "limited",
        "hotspot_data_gb": 15.0,
        "network_priority": "standard",
        "contract_length": 24
    }
    
    target_plan_1 = {
        "name": "Enterprise Unlimited",
        "monthly_cost": 95.0,
        "data_limit_gb": float('inf'),  # unlimited
        "voice_minutes": "unlimited",
        "sms_count": "unlimited",
        "international_calling": True,
        "roaming": "global",
        "hotspot_data_gb": 100.0,
        "network_priority": "premium",
        "contract_length": 12,
        "features": ["5G Ultra Wideband", "Premium Network Access", "24/7 Business Support"]
    }
    
    usage_data_1 = {
        "data_usage_gb": 65.0,
        "voice_minutes": 800,
        "sms_count": 150,
        "international_minutes": 45,
        "peak_usage_hours": ["9-12", "14-17"],
        "roaming_usage_gb": 8.0
    }
    
    print(f"💬 Customer Says: {customer_conversation_1.strip()}")
    print()
    print("📊 Current Usage Data:")
    for key, value in usage_data_1.items():
        print(f"   • {key.replace('_', ' ').title()}: {value}")
    print()
    
    # Simulate agent analysis
    print("🤖 AI Agent Analysis:")
    print("   ✅ Customer Profile: Business user, high data needs, cost-conscious")
    print("   ✅ Pain Points: Expensive plan, data limits, network reliability")
    print("   ✅ Priorities: Cost savings, unlimited data, premium network")
    print("   ✅ Suitability Score: 9.2/10 for Enterprise Unlimited plan")
    print()
    
    print("🎯 Generated Sales Pitch:")
    print("-" * 30)
    pitch_1 = f"""
🎯 Hi there! I understand you're looking for better value on your business plan.

💡 I've found the perfect solution that addresses your exact concerns:
   • SAVE $25/month ($300 annually) - from $120 to $95
   • UNLIMITED DATA - no more worrying about hitting limits
   • PREMIUM NETWORK - priority access during peak hours
   • GLOBAL ROAMING - stay connected when traveling

🌟 Key Benefits for Your Business:
   • 100GB Mobile Hotspot (vs your current 15GB)
   • 24/7 Business Support
   • 5G Ultra Wideband access
   • Shorter 12-month contract (vs your current 24-month)

💰 Bottom Line: Better service, more features, AND you save $300/year!

🚀 This promotional rate is available this week only. Shall I secure this deal for you today?
"""
    print(pitch_1)
    
    print("=" * 60)
    print()
    
    # Demo Scenario 2: Family Customer
    print("📱 SCENARIO 2: Price-Sensitive Family")
    print("-" * 50)
    
    customer_conversation_2 = """
    Customer: We're a family of four and our phone bill is getting out of control. 
    We're paying $180/month for four lines and it's really straining our budget. 
    The kids mainly use Wi-Fi at home and school, but they do stream videos sometimes. 
    My spouse and I need reliable service for work calls. We're looking for something 
    more affordable without sacrificing too much quality.
    """
    
    print(f"💬 Customer Says: {customer_conversation_2.strip()}")
    print()
    
    print("🤖 AI Agent Analysis:")
    print("   ✅ Customer Profile: Family of 4, budget-conscious, mixed usage")
    print("   ✅ Pain Points: High monthly cost, budget strain")
    print("   ✅ Priorities: Cost reduction, reliable voice service, adequate data")
    print("   ✅ Suitability Score: 8.7/10 for Family Share plan")
    print()
    
    print("🎯 Generated Sales Pitch:")
    print("-" * 30)
    pitch_2 = f"""
🎯 I completely understand - family phone bills can really add up!

💡 I have a Family Share plan that's perfect for your situation:
   • SAVE $50/month ($600 annually) - from $180 to $130 for 4 lines
   • 25GB shared data pool - plenty for everyone's needs
   • Each line gets unlimited talk & text
   • Kids can stream videos without worrying about overages

🌟 Family-Friendly Features:
   • Parental controls included
   • Safe search and content filtering
   • Usage monitoring for each line
   • No activation fees for families

💰 Bottom Line: Quality service for your whole family at $32.50 per line!

🚀 Plus, sign up this month and get the first 3 months at an extra 20% off!
"""
    print(pitch_2)
    
    print("=" * 60)
    print()
    
    # Demo Scenario 3: Senior Customer
    print("📱 SCENARIO 3: Senior Customer - Simple Needs")
    print("-" * 50)
    
    customer_conversation_3 = """
    Customer: I'm 72 years old and I just need a simple phone plan. I mainly use my phone 
    for calls to family and maybe some texting. I don't really understand all this data 
    stuff. My current plan costs $60 and I think I'm paying for things I don't need. 
    I just want something reliable and easy to understand.
    """
    
    print(f"💬 Customer Says: {customer_conversation_3.strip()}")
    print()
    
    print("🤖 AI Agent Analysis:")
    print("   ✅ Customer Profile: Senior, basic usage, values simplicity")
    print("   ✅ Pain Points: Overpaying for unused features, complexity")
    print("   ✅ Priorities: Simple plan, cost reduction, reliable voice service")
    print("   ✅ Suitability Score: 9.5/10 for Senior Essentials plan")
    print()
    
    print("🎯 Generated Sales Pitch:")
    print("-" * 30)
    pitch_3 = f"""
🎯 I have the perfect simple plan that's designed specifically for your needs!

💡 Our Senior Essentials plan gives you exactly what you need:
   • SAVE $25/month ($300 annually) - from $60 to $35
   • Unlimited calls to anywhere in the US
   • Unlimited text messages  
   • 2GB data (more than enough for basic smartphone features)

🌟 Senior-Friendly Features:
   • Large text and simple interface options
   • 24/7 customer support with senior specialists
   • No hidden fees or surprises
   • Emergency assistance features

💰 Bottom Line: Everything you need for just $35/month - that's it!

🚀 I can set this up for you right now and you'll see the savings on your next bill.
"""
    print(pitch_3)
    
    print("=" * 60)
    print()
    print("🎉 DEMO SUMMARY")
    print("The AI agent successfully:")
    print("✅ Analyzed 3 different customer types and needs")
    print("✅ Generated personalized pitches for each scenario")  
    print("✅ Highlighted relevant benefits and cost savings")
    print("✅ Created compelling calls-to-action")
    print("✅ Addressed specific customer pain points")
    print()
    print("Ready to integrate into your sales process! 🚀")

if __name__ == "__main__":
    run_interactive_demo()
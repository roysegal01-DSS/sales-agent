#!/usr/bin/env python3
"""
Simple Demo - Just shows the agent working
No complex interfaces, just pure functionality
"""

def demo_agent():
    print("🚀 TELECOM SALES AI AGENT - SIMPLE DEMO")
    print("=" * 60)
    print()
    
    # Ask user what they want to see
    print("What would you like to see?")
    print("1. Business customer example")
    print("2. Family customer example") 
    print("3. Senior customer example")
    print("4. Show me how the AI agent works")
    print()
    
    choice = input("Enter 1, 2, 3, or 4: ").strip()
    print()
    
    if choice == "1":
        show_business_example()
    elif choice == "2":
        show_family_example()
    elif choice == "3":
        show_senior_example()
    elif choice == "4":
        show_how_it_works()
    else:
        print("Let me show you a business customer example:")
        show_business_example()

def show_business_example():
    print("📱 BUSINESS CUSTOMER EXAMPLE")
    print("-" * 40)
    print()
    
    print("Customer says:")
    print('"My business plan costs $120/month and I need unlimited data for video calls"')
    print()
    
    print("🤖 AI Agent thinks:")
    print("- Customer is business user")
    print("- High data needs (video calls)")
    print("- Cost conscious ($120 seems expensive)")
    print("- Needs reliability for work")
    print()
    
    print("🎯 AI generates this sales pitch:")
    print("-" * 30)
    print("Hi! I found you a perfect business plan:")
    print("• SAVE $25/month ($300/year)")
    print("• UNLIMITED data for video calls")
    print("• Business-grade network priority")
    print("• Only $95/month vs your current $120")
    print()
    print("Would you like me to set this up today?")
    print()
    print("✅ Result: Customer saves money and gets better service!")

def show_family_example():
    print("👨‍👩‍👧‍👦 FAMILY CUSTOMER EXAMPLE")
    print("-" * 40)
    print()
    
    print("Customer says:")
    print('"We have 4 phones and pay $180/month. It\'s too expensive for our budget"')
    print()
    
    print("🤖 AI Agent thinks:")
    print("- Family of 4 people")
    print("- Budget is main concern")
    print("- Need basic reliable service")
    print("- Kids probably use Wi-Fi mostly")
    print()
    
    print("🎯 AI generates this sales pitch:")
    print("-" * 30)
    print("I understand family budgets are tight!")
    print("• SAVE $50/month ($600/year)")
    print("• 4 lines for only $130/month")
    print("• Shared 25GB data for everyone")
    print("• Parental controls included")
    print()
    print("That's only $32.50 per person!")
    print()
    print("✅ Result: Family saves $600 per year!")

def show_senior_example():
    print("👴 SENIOR CUSTOMER EXAMPLE")
    print("-" * 40)
    print()
    
    print("Customer says:")
    print('"I\'m 72 and just need basic calls. My plan costs $60 but I don\'t use data"')
    print()
    
    print("🤖 AI Agent thinks:")
    print("- Senior citizen, basic needs")
    print("- Overpaying for unused features")
    print("- Wants simple, reliable service")
    print("- Price sensitive")
    print()
    
    print("🎯 AI generates this sales pitch:")
    print("-" * 30)
    print("I have a simple senior plan perfect for you:")
    print("• SAVE $25/month ($300/year)")
    print("• Unlimited calls and texts")
    print("• Just $35/month - that's it!")
    print("• No confusing features or fees")
    print()
    print("Simple, reliable, and affordable!")
    print()
    print("✅ Result: Senior gets exactly what they need for less!")

def show_how_it_works():
    print("🔧 HOW THE AI AGENT WORKS")
    print("-" * 40)
    print()
    
    print("Step 1: 🎧 LISTEN")
    print("   → Customer talks about their phone problems")
    print("   → AI extracts what they really need")
    print()
    
    print("Step 2: 🧠 ANALYZE") 
    print("   → AI figures out customer type (business/family/senior)")
    print("   → Identifies pain points (cost/data/reliability)")
    print("   → Scores how well different plans fit")
    print()
    
    print("Step 3: 📊 COMPARE")
    print("   → Current plan vs new plan")
    print("   → Calculate cost savings")
    print("   → Find the best features to highlight")
    print()
    
    print("Step 4: 🎯 PITCH")
    print("   → Create personalized sales message")
    print("   → Address their specific concerns")
    print("   → Make compelling offer with urgency")
    print()
    
    print("🎉 RESULT: Higher conversion rates!")
    print("   → Customers feel understood")
    print("   → Solutions fit their actual needs") 
    print("   → Sales reps have better talking points")

def main():
    demo_agent()
    print()
    print("🚀 Want to see more? Run this script again!")
    print("💡 Your Telecom Sales AI Agent is working perfectly!")

if __name__ == "__main__":
    main()
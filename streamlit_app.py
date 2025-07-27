import streamlit as st
import json
import os
from datetime import datetime

from src.langgraph_agent import TelecomSalesAgent
from src.models.customer_profile import CustomerSegment, UsagePattern, Priority


def init_app():
    """Initialize the Streamlit app"""
    st.set_page_config(
        page_title="Telecom Sales Agent",
        page_icon="📱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📱 Telecom Sales AI Agent")
    st.markdown("**Generate personalized sales pitches using AI-powered customer analysis**")
    
    # Initialize session state
    if 'agent' not in st.session_state:
        api_key = os.getenv("OPENAI_API_KEY", "demo-key")
        st.session_state.agent = TelecomSalesAgent(api_key)
    
    if 'results' not in st.session_state:
        st.session_state.results = None


def create_sidebar():
    """Create the sidebar with sample data options"""
    st.sidebar.title("🎯 Quick Start")
    
    if st.sidebar.button("Load Sample Scenario", type="primary"):
        load_sample_data()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Sample Scenarios")
    
    scenarios = {
        "Business User": "High data usage, international travel, values network quality",
        "Family Plan": "Cost-conscious, multiple lines, basic usage",
        "Heavy Streamer": "Unlimited data needs, entertainment focused",
        "Budget Conscious": "Price sensitive, light usage, flexible terms"
    }
    
    for name, desc in scenarios.items():
        if st.sidebar.button(f"Load: {name}"):
            load_scenario(name)


def load_sample_data():
    """Load sample data into the form"""
    st.session_state.customer_conversation = """
    Hi, I'm looking at my phone bill and it seems really high. I'm currently paying $85 per month 
    and I feel like I'm not getting good value. I use my phone a lot for work - lots of video calls 
    and I'm always streaming music during my commute. I travel internationally about twice a year 
    for business and the roaming charges are killing me. My current plan only gives me 15GB of data 
    and I'm constantly hitting the limit. I need unlimited data or at least way more than I have now. 
    The coverage at my office downtown is also pretty spotty - calls drop frequently. I've been with 
    my current carrier for 3 years but I'm ready to switch if I can get better value and reliability.
    I'd prefer not to be locked into a long contract if possible.
    """
    
    # Set other session state values for current plan
    st.session_state.current_plan_name = "Business Basic 15GB"
    st.session_state.current_price = 85.0
    st.session_state.current_data = 15.0
    st.session_state.current_international = False
    st.session_state.current_roaming = False
    
    # Target plan
    st.session_state.target_plan_name = "Premium Unlimited Pro"
    st.session_state.target_price = 75.0
    st.session_state.target_data_unlimited = True
    st.session_state.target_international = True
    st.session_state.target_roaming = True
    st.session_state.target_promotional = 20.0
    
    # Usage data
    st.session_state.customer_name = "Sarah Johnson"
    st.session_state.customer_location = "Downtown Seattle"
    st.session_state.data_usage = 18.5
    st.session_state.voice_minutes = 850
    st.session_state.international_usage = True


def load_scenario(scenario_name):
    """Load a specific scenario"""
    scenarios = {
        "Business User": {
            "conversation": "I'm a business professional who travels frequently. I need reliable coverage, unlimited data for video calls, and international roaming. Network quality is more important than price for me.",
            "name": "Michael Chen",
            "location": "New York City",
            "data_usage": 45.0,
            "voice_minutes": 1200,
            "current_price": 95.0,
            "target_price": 110.0,
            "international": True
        },
        "Family Plan": {
            "conversation": "We're a family of four and our phone bills are too high. We need to cut costs but still have enough data for the kids' apps and our basic usage. We mainly use WiFi at home.",
            "name": "The Johnson Family",
            "location": "Suburban Denver",
            "data_usage": 35.0,
            "voice_minutes": 600,
            "current_price": 180.0,
            "target_price": 120.0,
            "international": False
        },
        "Heavy Streamer": {
            "conversation": "I stream videos constantly and use my phone for gaming. I need unlimited data and the fastest speeds possible. I don't care much about price if the performance is there.",
            "name": "Alex Rivera",
            "location": "Los Angeles",
            "data_usage": 85.0,
            "voice_minutes": 300,
            "current_price": 70.0,
            "target_price": 90.0,
            "international": False
        },
        "Budget Conscious": {
            "conversation": "I'm retired and on a fixed income. I only need basic calling and texting with some light internet use. Price is very important to me and I want the flexibility to change plans.",
            "name": "Dorothy Williams",
            "location": "Rural Ohio",
            "data_usage": 5.0,
            "voice_minutes": 400,
            "current_price": 50.0,
            "target_price": 35.0,
            "international": False
        }
    }
    
    if scenario_name in scenarios:
        data = scenarios[scenario_name]
        st.session_state.customer_conversation = data["conversation"]
        st.session_state.customer_name = data["name"]
        st.session_state.customer_location = data["location"]
        st.session_state.data_usage = data["data_usage"]
        st.session_state.voice_minutes = data["voice_minutes"]
        st.session_state.current_price = data["current_price"]
        st.session_state.target_price = data["target_price"]
        st.session_state.international_usage = data["international"]
        st.session_state.target_international = data["international"]


def create_input_form():
    """Create the main input form"""
    st.header("📝 Customer Input")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Customer Conversation")
        customer_conversation = st.text_area(
            "What did the customer say?",
            value=st.session_state.get("customer_conversation", ""),
            height=200,
            placeholder="Enter the customer's conversation, needs, concerns, and preferences..."
        )
    
    with col2:
        st.subheader("👤 Customer Info")
        customer_name = st.text_input(
            "Customer Name",
            value=st.session_state.get("customer_name", "")
        )
        customer_location = st.text_input(
            "Location",
            value=st.session_state.get("customer_location", "")
        )
        
        st.subheader("📊 Usage Data")
        data_usage = st.number_input(
            "Monthly Data Usage (GB)",
            min_value=0.0,
            max_value=500.0,
            value=st.session_state.get("data_usage", 10.0),
            step=0.5
        )
        voice_minutes = st.number_input(
            "Monthly Voice Minutes",
            min_value=0,
            max_value=5000,
            value=st.session_state.get("voice_minutes", 300),
            step=50
        )
        international_usage = st.checkbox(
            "Uses International Services",
            value=st.session_state.get("international_usage", False)
        )
    
    return customer_conversation, customer_name, customer_location, data_usage, voice_minutes, international_usage


def create_plan_inputs():
    """Create plan input sections"""
    st.header("📱 Plan Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 Current Plan")
        current_plan_name = st.text_input(
            "Current Plan Name",
            value=st.session_state.get("current_plan_name", "Basic Plan")
        )
        current_price = st.number_input(
            "Current Monthly Price ($)",
            min_value=0.0,
            value=st.session_state.get("current_price", 50.0),
            step=5.0
        )
        current_data = st.number_input(
            "Current Data Allowance (GB)",
            min_value=0.0,
            value=st.session_state.get("current_data", 10.0),
            step=1.0
        )
        current_international = st.checkbox(
            "Current: International Included",
            value=st.session_state.get("current_international", False)
        )
        current_roaming = st.checkbox(
            "Current: Roaming Included",
            value=st.session_state.get("current_roaming", False)
        )
    
    with col2:
        st.subheader("📈 Target Plan")
        target_plan_name = st.text_input(
            "Target Plan Name",
            value=st.session_state.get("target_plan_name", "Premium Plan")
        )
        target_price = st.number_input(
            "Target Monthly Price ($)",
            min_value=0.0,
            value=st.session_state.get("target_price", 70.0),
            step=5.0
        )
        
        target_data_unlimited = st.checkbox(
            "Target: Unlimited Data",
            value=st.session_state.get("target_data_unlimited", False)
        )
        
        if not target_data_unlimited:
            target_data = st.number_input(
                "Target Data Allowance (GB)",
                min_value=0.0,
                value=st.session_state.get("target_data", 25.0),
                step=1.0
            )
        else:
            target_data = "unlimited"
        
        target_international = st.checkbox(
            "Target: International Included",
            value=st.session_state.get("target_international", True)
        )
        target_roaming = st.checkbox(
            "Target: Roaming Included",
            value=st.session_state.get("target_roaming", True)
        )
        target_promotional = st.number_input(
            "Promotional Discount (%)",
            min_value=0.0,
            max_value=50.0,
            value=st.session_state.get("target_promotional", 0.0),
            step=5.0
        )
    
    return (current_plan_name, current_price, current_data, current_international, current_roaming,
            target_plan_name, target_price, target_data, target_international, target_roaming, target_promotional)


def process_customer_data(customer_conversation, customer_name, customer_location, data_usage, voice_minutes, 
                         international_usage, current_plan_data, target_plan_data):
    """Process the customer data through the agent"""
    
    # Build current plan dict
    current_plan = {
        "plan_id": "current_plan",
        "name": current_plan_data[0],
        "price": current_plan_data[1],
        "data_allowance": current_plan_data[2],
        "voice_minutes": "unlimited",
        "sms_allowance": "unlimited",
        "international_included": current_plan_data[3],
        "roaming_included": current_plan_data[4],
        "hotspot_data": 5.0,
        "network_priority": "standard",
        "features": [],
        "contract_length": 24,
        "setup_fee": 0.0
    }
    
    # Build target plan dict
    target_plan = {
        "plan_id": "target_plan",
        "name": target_plan_data[0],
        "price": target_plan_data[1],
        "data_allowance": target_plan_data[2],
        "voice_minutes": "unlimited",
        "sms_allowance": "unlimited",
        "international_included": target_plan_data[3],
        "roaming_included": target_plan_data[4],
        "hotspot_data": 20.0,
        "network_priority": "premium",
        "features": ["Premium Network", "Enhanced Support"],
        "contract_length": 12,
        "setup_fee": 0.0,
        "promotional_discount": target_plan_data[5] if target_plan_data[5] > 0 else None,
        "promotional_duration": 6 if target_plan_data[5] > 0 else None
    }
    
    # Build usage data dict
    usage_data = {
        "customer_id": "streamlit_user",
        "name": customer_name,
        "location": customer_location,
        "current_spend": current_plan_data[1],
        "data_usage_gb": data_usage,
        "voice_minutes": voice_minutes,
        "sms_count": 500,
        "international_usage": international_usage,
        "roaming_usage": international_usage,
        "peak_usage_hours": [9, 17, 18, 19],
        "business_user": "business" in customer_conversation.lower()
    }
    
    # Process through agent
    with st.spinner("🤖 Analyzing customer and generating personalized pitch..."):
        try:
            result = st.session_state.agent.process_customer_sync(
                customer_conversation=customer_conversation,
                current_plan=current_plan,
                target_plan=target_plan,
                usage_data=usage_data
            )
            return result
        except Exception as e:
            st.error(f"Error processing customer data: {str(e)}")
            return None


def display_results(result):
    """Display the analysis results"""
    if not result or not result.get("success"):
        st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
        return
    
    st.header("🎯 Generated Sales Pitch")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Sales Pitch", "👤 Customer Profile", "📊 Plan Comparison", "🔧 Raw Data"])
    
    with tab1:
        st.subheader("🎤 Ready-to-Use Sales Pitch")
        formatted_pitch = st.session_state.agent.format_pitch_for_sales_rep(result)
        st.text_area("Copy this pitch:", value=formatted_pitch, height=600)
        
        if st.button("📋 Copy to Clipboard"):
            st.code(formatted_pitch)
    
    with tab2:
        st.subheader("👤 Customer Analysis")
        profile = result["customer_profile"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Segment", profile["segment"])
            st.metric("Usage Pattern", profile["usage_pattern"])
        with col2:
            st.metric("Cost Sensitivity", profile["needs"]["cost_sensitivity"])
            st.metric("Data Priority", profile["needs"]["data_priority"])
        with col3:
            st.metric("Network Quality Priority", profile["needs"]["network_quality"])
            st.metric("International Needs", profile["needs"]["international_needs"])
        
        if profile["pain_points"]:
            st.subheader("😣 Pain Points Identified")
            for pain in profile["pain_points"]:
                st.write(f"• {pain}")
    
    with tab3:
        st.subheader("📊 Plan Comparison Analysis")
        comparison = result["plan_comparison"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            savings_color = "normal" if comparison["monthly_savings"] >= 0 else "inverse"
            st.metric("Monthly Savings", f"${comparison['monthly_savings']:.2f}", delta=comparison["monthly_savings"])
        with col2:
            st.metric("Annual Savings", f"${comparison['annual_savings']:.2f}")
        with col3:
            st.metric("Suitability Score", f"{comparison['suitability_score']:.1f}/10")
        with col4:
            st.metric("Data Change", comparison["data_difference"])
        
        if comparison["feature_improvements"]:
            st.subheader("✨ New Features")
            for feature in comparison["feature_improvements"]:
                st.write(f"• {feature}")
        
        if comparison["potential_drawbacks"]:
            st.subheader("⚠️ Potential Concerns")
            for drawback in comparison["potential_drawbacks"]:
                st.write(f"• {drawback}")
    
    with tab4:
        st.subheader("🔧 Raw Analysis Data")
        st.json(result)


def main():
    """Main application function"""
    init_app()
    create_sidebar()
    
    # Main form
    customer_conversation, customer_name, customer_location, data_usage, voice_minutes, international_usage = create_input_form()
    
    # Plan inputs
    current_plan_data, target_plan_data = create_plan_inputs()[:6], create_plan_inputs()[6:]
    
    # Process button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Personalized Pitch", type="primary", use_container_width=True):
            if customer_conversation and customer_name:
                result = process_customer_data(
                    customer_conversation, customer_name, customer_location, 
                    data_usage, voice_minutes, international_usage,
                    current_plan_data, target_plan_data
                )
                if result:
                    st.session_state.results = result
            else:
                st.error("Please provide customer conversation and name.")
    
    # Display results if available
    if st.session_state.results:
        display_results(st.session_state.results)
    
    # Footer
    st.markdown("---")
    st.markdown("**Telecom Sales AI Agent** - Powered by LangGraph and OpenAI")


if __name__ == "__main__":
    main()
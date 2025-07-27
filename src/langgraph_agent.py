import json
from typing import Dict, List, Any, TypedDict, Annotated
from datetime import datetime
import operator

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import BaseTool

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain.schema import BaseMessage
from typing import Annotated
import operator

from .agents.customer_profiler import CustomerProfiler
from .agents.plan_analyzer import PlanAnalyzer
from .agents.pitch_generator import PitchGenerator
from .models.customer_profile import CustomerProfile, TelecomPlan


class AgentState(TypedDict):
    """State shared across the LangGraph agent"""
    messages: Annotated[List[Dict], operator.add]
    customer_conversation: str
    current_plan: Dict[str, Any]
    target_plan: Dict[str, Any]
    usage_data: Dict[str, Any]
    customer_profile: Dict[str, Any]
    plan_comparison: Dict[str, Any]
    personalized_pitch: Dict[str, Any]
    step: str
    error: str


class TelecomSalesAgent:
    """LangGraph-based telecom sales agent for personalized plan pitches"""
    
    def __init__(self, openai_api_key: str = None):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        
        # Initialize tools
        self.tools = [
            CustomerProfiler(),
            PlanAnalyzer(),
            PitchGenerator()
        ]
        
        self.tool_node = ToolNode(self.tools)
        
        # Build the graph
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_customer", self._analyze_customer)
        workflow.add_node("compare_plans", self._compare_plans)
        workflow.add_node("generate_pitch", self._generate_pitch)
        workflow.add_node("validate_inputs", self._validate_inputs)
        workflow.add_node("error_handler", self._handle_error)
        
        # Define the flow
        workflow.set_entry_point("validate_inputs")
        
        # Conditional routing from validation
        workflow.add_conditional_edges(
            "validate_inputs",
            self._route_after_validation,
            {
                "analyze": "analyze_customer",
                "error": "error_handler"
            }
        )
        
        # Sequential flow through main process
        workflow.add_edge("analyze_customer", "compare_plans")
        workflow.add_edge("compare_plans", "generate_pitch")
        workflow.add_edge("generate_pitch", END)
        workflow.add_edge("error_handler", END)
        
        return workflow
    
    def _validate_inputs(self, state: AgentState) -> AgentState:
        """Validate required inputs before processing"""
        try:
            required_fields = [
                "customer_conversation",
                "current_plan", 
                "target_plan",
                "usage_data"
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in state or not state[field]:
                    missing_fields.append(field)
            
            if missing_fields:
                state["error"] = f"Missing required fields: {', '.join(missing_fields)}"
                state["step"] = "error"
            else:
                state["step"] = "validation_passed"
                state["error"] = ""
                
            return state
            
        except Exception as e:
            state["error"] = f"Validation error: {str(e)}"
            state["step"] = "error"
            return state
    
    def _route_after_validation(self, state: AgentState) -> str:
        """Route based on validation results"""
        if state.get("error"):
            return "error"
        return "analyze"
    
    def _analyze_customer(self, state: AgentState) -> AgentState:
        """Analyze customer conversation and usage to build profile"""
        try:
            profiler = CustomerProfiler()
            
            # Run customer profiling
            profile_result = profiler._run(
                customer_conversation=state["customer_conversation"],
                usage_data=state["usage_data"],
                existing_profile=state.get("customer_profile", {})
            )
            
            if profile_result.startswith("Error"):
                state["error"] = profile_result
                state["step"] = "error"
            else:
                state["customer_profile"] = json.loads(profile_result)
                state["step"] = "customer_analyzed"
                state["messages"].append({
                    "role": "assistant",
                    "content": f"✅ Customer profile analyzed successfully. Identified as {state['customer_profile']['segment']} segment with {state['customer_profile']['usage_pattern']} usage pattern."
                })
            
            return state
            
        except Exception as e:
            state["error"] = f"Customer analysis error: {str(e)}"
            state["step"] = "error"
            return state
    
    def _compare_plans(self, state: AgentState) -> AgentState:
        """Compare current and target plans"""
        try:
            analyzer = PlanAnalyzer()
            
            # Run plan comparison
            comparison_result = analyzer._run(
                current_plan=state["current_plan"],
                target_plan=state["target_plan"],
                customer_profile=state["customer_profile"]
            )
            
            if comparison_result.startswith("Error"):
                state["error"] = comparison_result
                state["step"] = "error"
            else:
                state["plan_comparison"] = json.loads(comparison_result)
                state["step"] = "plans_compared"
                
                # Extract key insights for message
                comparison = state["plan_comparison"]
                savings = comparison["monthly_savings"]
                suitability = comparison["suitability_score"]
                
                if savings > 0:
                    savings_msg = f"saves ${savings:.2f}/month"
                elif savings < 0:
                    savings_msg = f"costs ${abs(savings):.2f}/month more"
                else:
                    savings_msg = "same cost"
                
                state["messages"].append({
                    "role": "assistant", 
                    "content": f"📊 Plan comparison completed. Target plan {savings_msg} with {suitability:.1f}/10 suitability score."
                })
            
            return state
            
        except Exception as e:
            state["error"] = f"Plan comparison error: {str(e)}"
            state["step"] = "error"
            return state
    
    def _generate_pitch(self, state: AgentState) -> AgentState:
        """Generate personalized sales pitch"""
        try:
            pitch_generator = PitchGenerator()
            
            # Generate personalized pitch
            pitch_result = pitch_generator._run(
                customer_profile=state["customer_profile"],
                plan_comparison=state["plan_comparison"],
                sales_context=""
            )
            
            if pitch_result.startswith("Error"):
                state["error"] = pitch_result
                state["step"] = "error"
            else:
                state["personalized_pitch"] = json.loads(pitch_result)
                state["step"] = "pitch_generated"
                state["messages"].append({
                    "role": "assistant",
                    "content": "🎯 Personalized sales pitch generated successfully!"
                })
            
            return state
            
        except Exception as e:
            state["error"] = f"Pitch generation error: {str(e)}"
            state["step"] = "error"
            return state
    
    def _handle_error(self, state: AgentState) -> AgentState:
        """Handle errors in processing"""
        state["messages"].append({
            "role": "assistant",
            "content": f"❌ Error occurred: {state['error']}"
        })
        return state
    
    async def process_customer(
        self,
        customer_conversation: str,
        current_plan: Dict[str, Any],
        target_plan: Dict[str, Any],
        usage_data: Dict[str, Any],
        existing_profile: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a customer interaction and generate personalized pitch
        
        Args:
            customer_conversation: Text from customer interaction
            current_plan: Current telecom plan details
            target_plan: Target plan to pitch
            usage_data: Customer usage statistics
            existing_profile: Optional existing customer profile
            
        Returns:
            Dictionary containing analysis results and personalized pitch
        """
        
        # Initialize state
        initial_state = AgentState(
            messages=[],
            customer_conversation=customer_conversation,
            current_plan=current_plan,
            target_plan=target_plan,
            usage_data=usage_data,
            customer_profile=existing_profile or {},
            plan_comparison={},
            personalized_pitch={},
            step="start",
            error=""
        )
        
        # Run the workflow
        result = await self.app.ainvoke(initial_state)
        
        return {
            "customer_profile": result.get("customer_profile", {}),
            "plan_comparison": result.get("plan_comparison", {}),
            "personalized_pitch": result.get("personalized_pitch", {}),
            "messages": result.get("messages", []),
            "success": not bool(result.get("error")),
            "error": result.get("error", "")
        }
    
    def process_customer_sync(
        self,
        customer_conversation: str,
        current_plan: Dict[str, Any], 
        target_plan: Dict[str, Any],
        usage_data: Dict[str, Any],
        existing_profile: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Synchronous version of process_customer
        """
        
        # Initialize state
        initial_state = AgentState(
            messages=[],
            customer_conversation=customer_conversation,
            current_plan=current_plan,
            target_plan=target_plan,
            usage_data=usage_data,
            customer_profile=existing_profile or {},
            plan_comparison={},
            personalized_pitch={},
            step="start",
            error=""
        )
        
        # Run the workflow synchronously
        result = self.app.invoke(initial_state)
        
        return {
            "customer_profile": result.get("customer_profile", {}),
            "plan_comparison": result.get("plan_comparison", {}),
            "personalized_pitch": result.get("personalized_pitch", {}),
            "messages": result.get("messages", []),
            "success": not bool(result.get("error")),
            "error": result.get("error", "")
        }
    
    def format_pitch_for_sales_rep(self, result: Dict[str, Any]) -> str:
        """
        Format the generated pitch for easy use by sales representatives
        """
        if not result["success"]:
            return f"❌ Error generating pitch: {result['error']}"
        
        pitch = result["personalized_pitch"]
        customer = result["customer_profile"]
        comparison = result["plan_comparison"]
        
        formatted_pitch = f"""
🎯 PERSONALIZED SALES PITCH FOR {customer['name'].upper()}

📞 OPENING:
{pitch['opening_hook']}

💡 ADDRESS THEIR CONCERNS:
{pitch['pain_point_address']}

🌟 VALUE PROPOSITION:
{pitch['value_proposition']}

⭐ KEY FEATURES TO HIGHLIGHT:
"""
        for feature in pitch['feature_highlights']:
            formatted_pitch += f"• {feature}\n"
        
        formatted_pitch += f"""
💰 COST BENEFITS:
{pitch['cost_benefit_analysis']}

🛡️ OBJECTION HANDLING:
"""
        for objection, response in pitch['objection_handling'].items():
            formatted_pitch += f"• {objection.replace('_', ' ').title()}: {response}\n"
        
        formatted_pitch += f"""
🚀 CALL TO ACTION:
{pitch['call_to_action']}

⏰ URGENCY FACTORS:
"""
        for factor in pitch['urgency_factors']:
            formatted_pitch += f"• {factor}\n"
        
        formatted_pitch += f"""
👤 PERSONAL TOUCHES:
"""
        for note in pitch['personalization_notes']:
            formatted_pitch += f"• {note}\n"
        
        formatted_pitch += f"""
📊 PLAN COMPARISON SUMMARY:
• Monthly savings: ${comparison['monthly_savings']:.2f}
• Annual savings: ${comparison['annual_savings']:.2f}
• Data: {comparison['data_difference']}
• Voice: {comparison['voice_difference']}
• Suitability Score: {comparison['suitability_score']:.1f}/10
"""
        
        return formatted_pitch
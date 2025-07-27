from typing import Dict, List, Any
import json
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ..models.customer_profile import CustomerProfile, PlanComparison, Priority


class PitchGeneratorInput(BaseModel):
    customer_profile: Dict[str, Any] = Field(description="Customer profile information")
    plan_comparison: Dict[str, Any] = Field(description="Plan comparison analysis")
    sales_context: str = Field(default="", description="Additional sales context or goals")


class PitchResult(BaseModel):
    opening_hook: str = Field(description="Attention-grabbing opening statement")
    pain_point_address: str = Field(description="How the solution addresses customer pain points")
    value_proposition: str = Field(description="Main value proposition tailored to customer")
    feature_highlights: List[str] = Field(description="Key features to emphasize")
    cost_benefit_analysis: str = Field(description="Cost and savings explanation")
    objection_handling: Dict[str, str] = Field(description="Potential objections and responses")
    call_to_action: str = Field(description="Compelling call to action")
    urgency_factors: List[str] = Field(description="Reasons to act now")
    personalization_notes: List[str] = Field(description="Personal touches based on customer profile")


class PitchGenerator(BaseTool):
    name: str = "pitch_generator"
    description: str = "Generates personalized sales pitches based on customer profile and plan comparison"
    args_schema = PitchGeneratorInput
    
    def _run(self, customer_profile: Dict, plan_comparison: Dict, sales_context: str = "") -> str:
        """Generate a personalized sales pitch for the customer."""
        try:
            # Parse inputs
            customer = CustomerProfile(**customer_profile)
            comparison = PlanComparison(**plan_comparison)
            
            # Generate pitch components
            pitch = PitchResult(
                opening_hook=self._generate_opening_hook(customer, comparison),
                pain_point_address=self._address_pain_points(customer, comparison),
                value_proposition=self._create_value_proposition(customer, comparison),
                feature_highlights=self._highlight_key_features(customer, comparison),
                cost_benefit_analysis=self._explain_cost_benefits(customer, comparison),
                objection_handling=self._prepare_objection_handling(customer, comparison),
                call_to_action=self._create_call_to_action(customer, comparison),
                urgency_factors=self._identify_urgency_factors(customer, comparison),
                personalization_notes=self._add_personal_touches(customer, comparison)
            )
            
            return json.dumps(pitch.dict(), indent=2)
            
        except Exception as e:
            return f"Error generating pitch: {str(e)}"
    
    def _generate_opening_hook(self, customer: CustomerProfile, comparison: PlanComparison) -> str:
        """Generate attention-grabbing opening based on customer's top priorities."""
        
        # Cost-focused opening
        if customer.needs.cost_sensitivity in [Priority.HIGH, Priority.CRITICAL]:
            if comparison.monthly_savings > 0:
                return f"Hi {customer.name}, I have great news! I found a way to save you ${comparison.monthly_savings:.2f} every month on your phone bill - that's ${comparison.annual_savings:.2f} per year!"
            else:
                return f"Hi {customer.name}, I know keeping costs down is important to you. Let me show you how you can get significantly more value for just a small increase in your monthly spend."
        
        # Data-focused opening
        elif customer.needs.data_priority in [Priority.HIGH, Priority.CRITICAL]:
            if "unlimited" in comparison.data_difference.lower():
                return f"Hi {customer.name}, imagine never worrying about data limits again. I have a plan that gives you unlimited data for your streaming and browsing needs."
            elif "increase" in comparison.data_difference.lower():
                return f"Hi {customer.name}, I noticed you're a heavy data user. I found a plan that gives you {comparison.data_difference} - perfect for your usage patterns!"
        
        # Coverage/quality focused opening
        elif customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
            return f"Hi {customer.name}, I understand reliable coverage is crucial for you. I have a solution that will give you premium network priority and improved coverage where you need it most."
        
        # Generic but personalized opening
        else:
            return f"Hi {customer.name}, I've been analyzing your current plan and usage patterns, and I believe I've found a much better fit for your specific needs."
    
    def _address_pain_points(self, customer: CustomerProfile, comparison: PlanComparison) -> str:
        """Address specific pain points mentioned by the customer."""
        if not customer.pain_points:
            return "I understand you're looking for better value and service from your telecom provider."
        
        pain_solutions = {
            'poor coverage': "The new plan includes access to our premium network with 99.9% coverage and priority data speeds.",
            'expensive bill': f"This plan will reduce your monthly costs by ${comparison.monthly_savings:.2f}, giving you more value for less money.",
            'slow internet': "You'll get premium network priority, which means faster data speeds even during peak hours.",
            'poor customer service': "Our premium customers get access to dedicated support with average wait times under 2 minutes.",
            'contract issues': "This plan offers flexible terms so you're not locked into something that doesn't work for you.",
            'billing issues': "We've simplified our billing and you'll have a dedicated account manager to ensure clarity.",
            'overage charges': "With this plan's generous allowances, you'll never have to worry about overage charges again."
        }
        
        addressed_points = []
        for pain_point in customer.pain_points:
            if pain_point in pain_solutions:
                addressed_points.append(pain_solutions[pain_point])
        
        if addressed_points:
            return "I specifically chose this plan because it addresses your concerns: " + " ".join(addressed_points)
        else:
            return "This plan is designed to eliminate the frustrations you've experienced with your current service."
    
    def _create_value_proposition(self, customer: CustomerProfile, comparison: PlanComparison) -> str:
        """Create main value proposition based on customer priorities."""
        value_points = []
        
        # Cost value
        if customer.needs.cost_sensitivity in [Priority.HIGH, Priority.CRITICAL] and comparison.monthly_savings > 0:
            value_points.append(f"Save ${comparison.annual_savings:.2f} annually")
        
        # Data value
        if customer.needs.data_priority in [Priority.HIGH, Priority.CRITICAL]:
            if "unlimited" in comparison.data_difference.lower():
                value_points.append("Unlimited data for worry-free usage")
            elif "increase" in comparison.data_difference.lower():
                value_points.append(f"More data ({comparison.data_difference})")
        
        # Feature value
        if comparison.feature_improvements:
            top_features = comparison.feature_improvements[:2]  # Take top 2 features
            value_points.extend(top_features)
        
        # Quality value
        if customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
            if any("premium" in feature.lower() for feature in comparison.feature_improvements):
                value_points.append("Premium network quality and priority")
        
        if value_points:
            return f"This plan gives you exactly what matters most to you: {', '.join(value_points)}."
        else:
            return f"This plan is perfectly tailored to your usage pattern and provides better overall value than your current plan (suitability score: {comparison.suitability_score:.1f}/10)."
    
    def _highlight_key_features(self, customer: CustomerProfile, comparison: PlanComparison) -> List[str]:
        """Select and highlight features most relevant to the customer."""
        relevant_features = []
        
        # Prioritize features based on customer needs
        for feature in comparison.feature_improvements:
            feature_lower = feature.lower()
            
            # International features
            if customer.needs.international_needs in [Priority.HIGH, Priority.CRITICAL]:
                if "international" in feature_lower:
                    relevant_features.insert(0, feature)  # High priority
                    continue
            
            # Data-related features
            if customer.needs.data_priority in [Priority.HIGH, Priority.CRITICAL]:
                if any(word in feature_lower for word in ["data", "unlimited", "hotspot"]):
                    relevant_features.insert(0, feature)
                    continue
            
            # Network quality features
            if customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
                if any(word in feature_lower for word in ["premium", "priority", "speed", "coverage"]):
                    relevant_features.insert(0, feature)
                    continue
            
            # Cost-related features (discounts, promotions)
            if customer.needs.cost_sensitivity in [Priority.HIGH, Priority.CRITICAL]:
                if any(word in feature_lower for word in ["discount", "promotion", "save", "%"]):
                    relevant_features.insert(0, feature)
                    continue
            
            # Add other features at the end
            relevant_features.append(feature)
        
        # Return top 5 most relevant features
        return relevant_features[:5]
    
    def _explain_cost_benefits(self, customer: CustomerProfile, comparison: PlanComparison) -> str:
        """Explain cost benefits in a way that resonates with the customer."""
        if comparison.monthly_savings > 0:
            if customer.needs.cost_sensitivity == Priority.CRITICAL:
                return f"You'll save ${comparison.monthly_savings:.2f} every month - that's ${comparison.annual_savings:.2f} per year! Over a 2-year period, you'd save ${comparison.annual_savings * 2:.2f}. That's real money back in your pocket."
            else:
                return f"Not only do you get better service, but you'll also save ${comparison.monthly_savings:.2f} monthly (${comparison.annual_savings:.2f} annually)."
        elif comparison.monthly_savings < 0:
            additional_cost = abs(comparison.monthly_savings)
            if customer.needs.cost_sensitivity == Priority.LOW:
                return f"For just ${additional_cost:.2f} more per month, you get significantly better service and features - excellent value for the upgrade."
            else:
                return f"While this plan is ${additional_cost:.2f} more per month, the additional value you receive makes it worth every penny."
        else:
            return "You get all these improvements at the same price you're paying now - it's like getting a free upgrade!"
    
    def _prepare_objection_handling(self, customer: CustomerProfile, comparison: PlanComparison) -> Dict[str, str]:
        """Prepare responses to likely objections."""
        objections = {}
        
        # Cost objection
        if comparison.monthly_savings < 0:
            objections["cost_concern"] = f"I understand cost is important. While this is ${abs(comparison.monthly_savings):.2f} more monthly, you're getting {len(comparison.feature_improvements)} new features and better service. It's actually better value per dollar."
        
        # Contract concern
        if customer.needs.flexibility in [Priority.HIGH, Priority.CRITICAL]:
            objections["contract_flexibility"] = "I know flexibility is important to you. This plan offers options to adjust your service as your needs change."
        
        # Coverage concern
        if 'poor coverage' in customer.pain_points:
            objections["coverage_doubt"] = "I completely understand your coverage concerns. This plan includes access to our premium network with 99.9% coverage and we offer a 30-day satisfaction guarantee."
        
        # Switching hassle
        objections["switching_hassle"] = "I know switching providers can seem like a hassle, but I'll personally handle the entire transition for you. You'll keep your phone number and there's no downtime."
        
        # Current plan satisfaction
        objections["current_plan_ok"] = f"Your current plan might seem fine, but you're missing out on {', '.join(comparison.feature_improvements[:3])}. Why settle for 'okay' when you can have exactly what you need?"
        
        return objections
    
    def _create_call_to_action(self, customer: CustomerProfile, comparison: PlanComparison) -> str:
        """Create compelling call to action based on customer profile."""
        
        # High urgency for cost-sensitive customers with savings
        if customer.needs.cost_sensitivity in [Priority.HIGH, Priority.CRITICAL] and comparison.monthly_savings > 0:
            return f"Let's get you started today so you can begin saving ${comparison.monthly_savings:.2f} immediately. I can have your new service active within 24 hours. What's the best time to complete the switch?"
        
        # Promotional urgency
        if any("discount" in feature.lower() for feature in comparison.feature_improvements):
            return "This promotional offer is available for a limited time. Let me secure this deal for you today before it expires. Shall we proceed with the activation?"
        
        # Quality-focused CTA
        if customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
            return "You deserve reliable, fast service. Let's get you switched over to our premium network today. I can start the process right now and you'll notice the difference immediately."
        
        # General urgency
        return f"This plan is perfectly matched to your needs with a {comparison.suitability_score:.1f}/10 fit score. Let's get you set up today so you can start enjoying these benefits right away."
    
    def _identify_urgency_factors(self, customer: CustomerProfile, comparison: PlanComparison) -> List[str]:
        """Identify reasons why the customer should act now."""
        urgency_factors = []
        
        # Promotional offers
        if any("discount" in feature.lower() or "%" in feature for feature in comparison.feature_improvements):
            urgency_factors.append("Limited-time promotional pricing expires soon")
        
        # Contract end date
        if customer.contract_end_date:
            urgency_factors.append("Perfect timing - your current contract allows for changes")
        
        # High savings
        if comparison.monthly_savings > 20:
            urgency_factors.append(f"Start saving ${comparison.monthly_savings:.2f}/month immediately")
        
        # Pain points
        if customer.pain_points:
            urgency_factors.append("Stop dealing with current service issues")
        
        # High suitability
        if comparison.suitability_score >= 8:
            urgency_factors.append("This plan is an excellent fit for your needs")
        
        # Availability
        urgency_factors.append("Plan availability subject to change")
        
        return urgency_factors
    
    def _add_personal_touches(self, customer: CustomerProfile, comparison: PlanComparison) -> List[str]:
        """Add personal touches based on customer profile."""
        personal_notes = []
        
        # Loyalty recognition
        if customer.loyalty_years > 2:
            personal_notes.append(f"As a valued {customer.loyalty_years}-year customer, you deserve our best service")
        
        # Usage pattern recognition
        if customer.usage_pattern.value == "heavy":
            personal_notes.append("I can see you're a power user - this plan is designed for people like you")
        elif customer.usage_pattern.value == "business":
            personal_notes.append("This business-grade plan matches your professional needs")
        
        # Segment-specific notes
        if customer.segment.value == "family":
            personal_notes.append("Perfect for keeping your family connected with shared benefits")
        elif customer.segment.value == "business":
            personal_notes.append("Designed for business reliability and professional features")
        
        # Location-specific
        if customer.location:
            personal_notes.append(f"Excellent coverage in the {customer.location} area")
        
        # Payment history recognition
        if customer.payment_history == "good":
            personal_notes.append("Your excellent payment history qualifies you for our best rates")
        
        return personal_notes
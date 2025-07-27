from typing import Dict, List, Any
import json
import re
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ..models.customer_profile import CustomerProfile, CustomerNeeds, UsageData, Priority, UsagePattern, CustomerSegment


class CustomerProfilerInput(BaseModel):
    customer_conversation: str = Field(description="Conversation or interaction with customer")
    usage_data: Dict[str, Any] = Field(description="Customer usage statistics")
    existing_profile: Dict[str, Any] = Field(default={}, description="Existing customer profile if available")


class CustomerProfiler(BaseTool):
    name: str = "customer_profiler"
    description: str = "Analyzes customer conversations and usage data to create or update customer needs profile"
    args_schema = CustomerProfilerInput
    
    def _run(self, customer_conversation: str, usage_data: Dict, existing_profile: Dict = None) -> str:
        """Analyze customer conversation and usage data to build comprehensive profile."""
        try:
            # Extract needs from conversation
            needs = self._extract_needs_from_conversation(customer_conversation)
            
            # Analyze usage patterns
            usage_pattern = self._analyze_usage_pattern(usage_data)
            
            # Determine customer segment
            segment = self._determine_customer_segment(customer_conversation, usage_data)
            
            # Extract pain points
            pain_points = self._extract_pain_points(customer_conversation)
            
            # Build or update profile
            if existing_profile:
                profile = CustomerProfile(**existing_profile)
                # Update with new insights
                profile.needs = needs
                profile.usage_pattern = usage_pattern
                profile.pain_points = pain_points
                profile.usage_data = UsageData(**usage_data)
            else:
                # Create new profile with minimal required info
                profile = CustomerProfile(
                    customer_id=usage_data.get('customer_id', 'unknown'),
                    name=usage_data.get('name', 'Customer'),
                    location=usage_data.get('location', 'Unknown'),
                    segment=segment,
                    usage_pattern=usage_pattern,
                    current_monthly_spend=usage_data.get('current_spend', 0),
                    usage_data=UsageData(**usage_data),
                    needs=needs,
                    pain_points=pain_points
                )
            
            return json.dumps(profile.dict(), indent=2, default=str)
            
        except Exception as e:
            return f"Error profiling customer: {str(e)}"
    
    def _extract_needs_from_conversation(self, conversation: str) -> CustomerNeeds:
        """Extract customer needs and priorities from conversation text."""
        conversation_lower = conversation.lower()
        
        # Initialize with default medium priorities
        needs = CustomerNeeds(
            cost_sensitivity=Priority.MEDIUM,
            data_priority=Priority.MEDIUM,
            voice_priority=Priority.MEDIUM,
            network_quality=Priority.MEDIUM,
            customer_service=Priority.MEDIUM,
            flexibility=Priority.MEDIUM
        )
        
        # Cost sensitivity indicators
        cost_keywords = {
            Priority.CRITICAL: ['expensive', 'too much', 'cant afford', 'budget tight', 'cheaper', 'save money', 'cost cutting'],
            Priority.HIGH: ['pricey', 'cost', 'budget', 'affordable', 'reasonable price'],
            Priority.LOW: ['dont care about price', 'money no object', 'premium service', 'best available']
        }
        
        for priority, keywords in cost_keywords.items():
            if any(keyword in conversation_lower for keyword in keywords):
                needs.cost_sensitivity = priority
                break
        
        # Data priority indicators
        data_keywords = {
            Priority.CRITICAL: ['unlimited data', 'lots of data', 'stream videos', 'heavy user', 'work from home', 'online gaming'],
            Priority.HIGH: ['data', 'internet', 'streaming', 'social media', 'apps'],
            Priority.LOW: ['dont use data', 'wifi mostly', 'basic phone', 'calls only']
        }
        
        for priority, keywords in data_keywords.items():
            if any(keyword in conversation_lower for keyword in keywords):
                needs.data_priority = priority
                break
        
        # Voice priority indicators
        voice_keywords = {
            Priority.CRITICAL: ['unlimited calls', 'talk a lot', 'business calls', 'long conversations'],
            Priority.HIGH: ['calls', 'talking', 'voice', 'minutes'],
            Priority.LOW: ['dont call much', 'text mostly', 'rarely call']
        }
        
        for priority, keywords in voice_keywords.items():
            if any(keyword in conversation_lower for keyword in keywords):
                needs.voice_priority = priority
                break
        
        # Network quality indicators
        network_keywords = {
            Priority.CRITICAL: ['poor coverage', 'dropped calls', 'slow internet', 'need reliability', 'coverage issues'],
            Priority.HIGH: ['good coverage', 'fast internet', 'reliable', 'network quality'],
            Priority.LOW: ['coverage ok', 'dont mind slow']
        }
        
        for priority, keywords in network_keywords.items():
            if any(keyword in conversation_lower for keyword in keywords):
                needs.network_quality = priority
                break
        
        # International needs
        international_keywords = ['international', 'overseas', 'abroad', 'foreign', 'global', 'travel']
        if any(keyword in conversation_lower for keyword in international_keywords):
            needs.international_needs = Priority.HIGH
        
        # Family sharing needs
        family_keywords = ['family plan', 'multiple lines', 'kids', 'spouse', 'shared', 'family']
        if any(keyword in conversation_lower for keyword in family_keywords):
            needs.family_sharing = Priority.HIGH
        
        # Business features
        business_keywords = ['business', 'work', 'company', 'enterprise', 'professional']
        if any(keyword in conversation_lower for keyword in business_keywords):
            needs.business_features = Priority.HIGH
        
        # Flexibility needs
        flexibility_keywords = ['flexible', 'change plans', 'no contract', 'month to month', 'cancel anytime']
        if any(keyword in conversation_lower for keyword in flexibility_keywords):
            needs.flexibility = Priority.HIGH
        
        return needs
    
    def _analyze_usage_pattern(self, usage_data: Dict) -> UsagePattern:
        """Determine usage pattern based on usage statistics."""
        data_gb = usage_data.get('data_usage_gb', 0)
        voice_minutes = usage_data.get('voice_minutes', 0)
        
        # Business pattern indicators
        if (data_gb > 50 and voice_minutes > 1000) or usage_data.get('business_user', False):
            return UsagePattern.BUSINESS
        
        # Heavy user pattern
        elif data_gb > 30 or voice_minutes > 800:
            return UsagePattern.HEAVY
        
        # Moderate user pattern
        elif data_gb > 10 or voice_minutes > 300:
            return UsagePattern.MODERATE
        
        # Light user pattern
        else:
            return UsagePattern.LIGHT
    
    def _determine_customer_segment(self, conversation: str, usage_data: Dict) -> CustomerSegment:
        """Determine customer segment based on conversation and usage."""
        conversation_lower = conversation.lower()
        
        # Enterprise indicators
        enterprise_keywords = ['enterprise', 'corporation', 'company plan', 'bulk lines', 'business account']
        if any(keyword in conversation_lower for keyword in enterprise_keywords):
            return CustomerSegment.ENTERPRISE
        
        # Business indicators
        business_keywords = ['business', 'work', 'professional', 'office']
        if any(keyword in conversation_lower for keyword in business_keywords):
            return CustomerSegment.BUSINESS
        
        # Family indicators
        family_keywords = ['family', 'kids', 'children', 'spouse', 'multiple lines', 'family plan']
        if any(keyword in conversation_lower for keyword in family_keywords):
            return CustomerSegment.FAMILY
        
        # Default to individual
        return CustomerSegment.INDIVIDUAL
    
    def _extract_pain_points(self, conversation: str) -> List[str]:
        """Extract current pain points from customer conversation."""
        pain_points = []
        conversation_lower = conversation.lower()
        
        pain_indicators = {
            'poor coverage': ['poor coverage', 'no signal', 'dropped calls', 'coverage issues'],
            'expensive bill': ['expensive', 'high bill', 'too much money', 'overpriced'],
            'slow internet': ['slow internet', 'slow data', 'poor speed', 'buffering'],
            'poor customer service': ['bad service', 'poor support', 'unhelpful staff', 'long wait times'],
            'contract issues': ['locked in', 'cant change', 'stuck with plan', 'contract problems'],
            'billing issues': ['billing error', 'wrong charge', 'unexpected fees', 'billing confusion'],
            'overage charges': ['overage', 'extra charges', 'exceeded limit', 'surprise charges']
        }
        
        for pain_point, keywords in pain_indicators.items():
            if any(keyword in conversation_lower for keyword in keywords):
                pain_points.append(pain_point)
        
        return pain_points
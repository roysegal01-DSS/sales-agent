from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from enum import Enum
from datetime import datetime


class UsagePattern(str, Enum):
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    BUSINESS = "business"


class CustomerSegment(str, Enum):
    INDIVIDUAL = "individual"
    FAMILY = "family"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UsageData(BaseModel):
    data_usage_gb: float = Field(description="Monthly data usage in GB")
    voice_minutes: int = Field(description="Monthly voice minutes used")
    sms_count: int = Field(description="Monthly SMS count")
    international_usage: bool = Field(default=False, description="Uses international services")
    roaming_usage: bool = Field(default=False, description="Uses roaming services")
    peak_usage_hours: List[int] = Field(default=[], description="Hours of peak usage (0-23)")


class CustomerNeeds(BaseModel):
    cost_sensitivity: Priority = Field(description="How price-sensitive the customer is")
    data_priority: Priority = Field(description="Importance of data allowance")
    voice_priority: Priority = Field(description="Importance of voice minutes")
    network_quality: Priority = Field(description="Importance of network coverage/speed")
    customer_service: Priority = Field(description="Importance of customer support")
    flexibility: Priority = Field(description="Need for plan flexibility/changes")
    international_needs: Priority = Field(default=Priority.LOW, description="International calling needs")
    family_sharing: Priority = Field(default=Priority.LOW, description="Need for family plan sharing")
    business_features: Priority = Field(default=Priority.LOW, description="Need for business features")


class CustomerProfile(BaseModel):
    customer_id: str = Field(description="Unique customer identifier")
    name: str = Field(description="Customer name")
    age: Optional[int] = Field(default=None, description="Customer age")
    location: str = Field(description="Customer location/region")
    segment: CustomerSegment = Field(description="Customer segment")
    usage_pattern: UsagePattern = Field(description="Overall usage pattern")
    current_monthly_spend: float = Field(description="Current monthly spending")
    contract_end_date: Optional[datetime] = Field(default=None, description="Current contract end date")
    
    # Usage data
    usage_data: UsageData = Field(description="Customer usage statistics")
    
    # Needs profile
    needs: CustomerNeeds = Field(description="Customer needs and priorities")
    
    # Additional context
    pain_points: List[str] = Field(default=[], description="Current issues with service")
    preferences: Dict[str, Union[str, int, float]] = Field(default={}, description="Additional preferences")
    satisfaction_score: Optional[float] = Field(default=None, description="Current satisfaction score (1-10)")
    
    # Behavioral insights
    payment_history: str = Field(default="good", description="Payment history: good, average, poor")
    loyalty_years: int = Field(default=0, description="Years as customer")
    support_tickets: int = Field(default=0, description="Number of support tickets in last 12 months")


class TelecomPlan(BaseModel):
    plan_id: str = Field(description="Unique plan identifier")
    name: str = Field(description="Plan name")
    price: float = Field(description="Monthly price")
    data_allowance: Union[float, str] = Field(description="Data allowance in GB or 'unlimited'")
    voice_minutes: Union[int, str] = Field(description="Voice minutes or 'unlimited'")
    sms_allowance: Union[int, str] = Field(description="SMS allowance or 'unlimited'")
    
    # Features
    international_included: bool = Field(default=False)
    roaming_included: bool = Field(default=False)
    hotspot_data: Optional[float] = Field(default=None, description="Hotspot data in GB")
    network_priority: str = Field(default="standard", description="Network priority level")
    
    # Additional features
    features: List[str] = Field(default=[], description="Additional plan features")
    contract_length: int = Field(default=12, description="Contract length in months")
    setup_fee: float = Field(default=0.0, description="One-time setup fee")
    
    # Promotional offers
    promotional_discount: Optional[float] = Field(default=None, description="Promotional discount percentage")
    promotional_duration: Optional[int] = Field(default=None, description="Promotional period in months")


class PlanComparison(BaseModel):
    current_plan: TelecomPlan
    target_plan: TelecomPlan
    monthly_savings: float = Field(description="Monthly cost difference")
    annual_savings: float = Field(description="Annual cost difference")
    data_difference: str = Field(description="Data allowance comparison")
    voice_difference: str = Field(description="Voice minutes comparison")
    feature_improvements: List[str] = Field(description="New/improved features")
    potential_drawbacks: List[str] = Field(description="Potential disadvantages")
    suitability_score: float = Field(description="How well the plan fits customer needs (1-10)")
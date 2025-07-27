from typing import Dict, List, Any
import json
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from ..models.customer_profile import CustomerProfile, TelecomPlan, PlanComparison, Priority


class PlanAnalyzerInput(BaseModel):
    current_plan: Dict[str, Any] = Field(description="Current telecom plan details")
    target_plan: Dict[str, Any] = Field(description="Target telecom plan details")
    customer_profile: Dict[str, Any] = Field(description="Customer profile information")


class PlanAnalyzer(BaseTool):
    name: str = "plan_analyzer"
    description: str = "Analyzes and compares telecom plans to determine suitability for a customer"
    args_schema = PlanAnalyzerInput
    
    def _run(self, current_plan: Dict, target_plan: Dict, customer_profile: Dict) -> str:
        """Compare current and target plans for a specific customer."""
        try:
            # Parse inputs
            current = TelecomPlan(**current_plan)
            target = TelecomPlan(**target_plan)
            customer = CustomerProfile(**customer_profile)
            
            # Calculate cost differences
            monthly_savings = current.price - target.price
            annual_savings = monthly_savings * 12
            
            # Apply promotional discount if applicable
            if target.promotional_discount and target.promotional_duration:
                promotional_savings = target.price * (target.promotional_discount / 100)
                effective_target_price = target.price - promotional_savings
                monthly_savings = current.price - effective_target_price
            
            # Compare data allowances
            data_diff = self._compare_data(current.data_allowance, target.data_allowance)
            
            # Compare voice minutes
            voice_diff = self._compare_voice(current.voice_minutes, target.voice_minutes)
            
            # Identify feature improvements
            feature_improvements = self._identify_improvements(current, target, customer)
            
            # Identify potential drawbacks
            drawbacks = self._identify_drawbacks(current, target, customer)
            
            # Calculate suitability score
            suitability = self._calculate_suitability(current, target, customer)
            
            comparison = PlanComparison(
                current_plan=current,
                target_plan=target,
                monthly_savings=monthly_savings,
                annual_savings=annual_savings,
                data_difference=data_diff,
                voice_difference=voice_diff,
                feature_improvements=feature_improvements,
                potential_drawbacks=drawbacks,
                suitability_score=suitability
            )
            
            return json.dumps(comparison.dict(), indent=2, default=str)
            
        except Exception as e:
            return f"Error analyzing plans: {str(e)}"
    
    def _compare_data(self, current_data, target_data) -> str:
        """Compare data allowances between plans."""
        if current_data == "unlimited" and target_data == "unlimited":
            return "Both plans offer unlimited data"
        elif current_data == "unlimited":
            return f"Downgrade from unlimited to {target_data}GB"
        elif target_data == "unlimited":
            return f"Upgrade from {current_data}GB to unlimited data"
        else:
            diff = float(target_data) - float(current_data)
            if diff > 0:
                return f"Increase of {diff}GB data ({current_data}GB → {target_data}GB)"
            elif diff < 0:
                return f"Decrease of {abs(diff)}GB data ({current_data}GB → {target_data}GB)"
            else:
                return "Same data allowance"
    
    def _compare_voice(self, current_voice, target_voice) -> str:
        """Compare voice minutes between plans."""
        if current_voice == "unlimited" and target_voice == "unlimited":
            return "Both plans offer unlimited voice minutes"
        elif current_voice == "unlimited":
            return f"Downgrade from unlimited to {target_voice} minutes"
        elif target_voice == "unlimited":
            return f"Upgrade from {current_voice} to unlimited voice minutes"
        else:
            diff = int(target_voice) - int(current_voice)
            if diff > 0:
                return f"Increase of {diff} voice minutes ({current_voice} → {target_voice})"
            elif diff < 0:
                return f"Decrease of {abs(diff)} voice minutes ({current_voice} → {target_voice})"
            else:
                return "Same voice minutes allowance"
    
    def _identify_improvements(self, current: TelecomPlan, target: TelecomPlan, customer: CustomerProfile) -> List[str]:
        """Identify feature improvements in the target plan."""
        improvements = []
        
        # Check international features
        if not current.international_included and target.international_included:
            if customer.needs.international_needs in [Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]:
                improvements.append("International calling now included")
        
        # Check roaming features
        if not current.roaming_included and target.roaming_included:
            improvements.append("Roaming services now included")
        
        # Check hotspot data
        if (not current.hotspot_data or current.hotspot_data == 0) and target.hotspot_data:
            improvements.append(f"Mobile hotspot with {target.hotspot_data}GB included")
        elif current.hotspot_data and target.hotspot_data and target.hotspot_data > current.hotspot_data:
            improvements.append(f"Increased hotspot data ({current.hotspot_data}GB → {target.hotspot_data}GB)")
        
        # Check network priority
        if current.network_priority == "standard" and target.network_priority == "premium":
            if customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
                improvements.append("Premium network priority for faster speeds")
        
        # Check additional features
        current_features = set(current.features)
        target_features = set(target.features)
        new_features = target_features - current_features
        for feature in new_features:
            improvements.append(f"New feature: {feature}")
        
        # Check promotional offers
        if target.promotional_discount:
            improvements.append(f"{target.promotional_discount}% discount for {target.promotional_duration} months")
        
        return improvements
    
    def _identify_drawbacks(self, current: TelecomPlan, target: TelecomPlan, customer: CustomerProfile) -> List[str]:
        """Identify potential drawbacks in the target plan."""
        drawbacks = []
        
        # Check for feature downgrades
        if current.international_included and not target.international_included:
            drawbacks.append("Loss of included international calling")
        
        if current.roaming_included and not target.roaming_included:
            drawbacks.append("Loss of included roaming services")
        
        if current.hotspot_data and target.hotspot_data and target.hotspot_data < current.hotspot_data:
            drawbacks.append(f"Reduced hotspot data ({current.hotspot_data}GB → {target.hotspot_data}GB)")
        
        # Check contract length
        if target.contract_length > current.contract_length:
            if customer.needs.flexibility in [Priority.HIGH, Priority.CRITICAL]:
                drawbacks.append(f"Longer contract commitment ({current.contract_length} → {target.contract_length} months)")
        
        # Check setup fees
        if target.setup_fee > current.setup_fee:
            drawbacks.append(f"Setup fee of ${target.setup_fee}")
        
        return drawbacks
    
    def _calculate_suitability(self, current: TelecomPlan, target: TelecomPlan, customer: CustomerProfile) -> float:
        """Calculate how suitable the target plan is for the customer (1-10 scale)."""
        score = 5.0  # Base score
        
        # Cost sensitivity evaluation
        monthly_savings = current.price - target.price
        if customer.needs.cost_sensitivity == Priority.CRITICAL:
            if monthly_savings > 0:
                score += min(2.0, monthly_savings / 10)  # Up to 2 points for savings
            else:
                score -= min(2.0, abs(monthly_savings) / 10)  # Deduct for higher cost
        elif customer.needs.cost_sensitivity == Priority.HIGH:
            if monthly_savings > 0:
                score += min(1.5, monthly_savings / 15)
            else:
                score -= min(1.5, abs(monthly_savings) / 15)
        
        # Data needs evaluation
        if customer.needs.data_priority in [Priority.HIGH, Priority.CRITICAL]:
            current_data = 0 if current.data_allowance == "unlimited" else float(current.data_allowance) if current.data_allowance != "unlimited" else 1000
            target_data = 0 if target.data_allowance == "unlimited" else float(target.data_allowance) if target.data_allowance != "unlimited" else 1000
            
            if target.data_allowance == "unlimited":
                score += 1.5
            elif isinstance(target.data_allowance, (int, float)) and customer.usage_data.data_usage_gb <= target.data_allowance:
                score += 1.0
            elif isinstance(target.data_allowance, (int, float)) and customer.usage_data.data_usage_gb > target.data_allowance:
                score -= 1.5
        
        # Voice needs evaluation
        if customer.needs.voice_priority in [Priority.HIGH, Priority.CRITICAL]:
            if target.voice_minutes == "unlimited":
                score += 1.0
            elif isinstance(target.voice_minutes, int) and customer.usage_data.voice_minutes <= target.voice_minutes:
                score += 0.5
            elif isinstance(target.voice_minutes, int) and customer.usage_data.voice_minutes > target.voice_minutes:
                score -= 1.0
        
        # International needs
        if customer.needs.international_needs in [Priority.HIGH, Priority.CRITICAL]:
            if target.international_included:
                score += 1.0
            else:
                score -= 0.5
        
        # Network quality
        if customer.needs.network_quality in [Priority.HIGH, Priority.CRITICAL]:
            if target.network_priority == "premium":
                score += 1.0
            elif target.network_priority == "standard":
                score -= 0.5
        
        # Ensure score is within 1-10 range
        return max(1.0, min(10.0, score))
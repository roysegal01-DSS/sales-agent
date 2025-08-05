const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8501;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Mock data for demonstration
const mockCustomerProfiles = {
  business: {
    segment: "Business",
    needs: ["High data usage", "Reliable network", "Cost optimization"],
    currentPlan: "Basic Business 50GB",
    painPoints: ["Network drops during calls", "Exceeding data limits"],
    budget: "Cost-conscious but willing to pay for reliability"
  },
  family: {
    segment: "Family",
    needs: ["Multiple lines", "Shared data", "Parental controls"],
    currentPlan: "Individual plans for 4 members",
    painPoints: ["High monthly costs", "Complex billing"],
    budget: "Budget-focused, looking for savings"
  },
  senior: {
    segment: "Senior",
    needs: ["Simple plan", "Good customer service", "Emergency features"],
    currentPlan: "Unlimited Premium",
    painPoints: ["Paying for unused features", "Complex interface"],
    budget: "Fixed income, wants value"
  }
};

const mockPlans = {
  business: {
    name: "Business Pro 100GB",
    price: "$89/month",
    features: ["100GB data", "Priority network", "24/7 support"],
    score: 9.2
  },
  family: {
    name: "Family Share 4-Line",
    price: "$140/month (4 lines)",
    features: ["Unlimited shared data", "Parental controls", "Multi-device"],
    score: 8.8
  },
  senior: {
    name: "Senior Essentials",
    price: "$35/month",
    features: ["5GB data", "Emergency button", "Simple interface"],
    score: 9.5
  }
};

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/api/analyze-customer', (req, res) => {
  const { conversation, customerType = 'business' } = req.body;
  
  // Mock analysis based on customer type
  const profile = mockCustomerProfiles[customerType] || mockCustomerProfiles.business;
  const recommendedPlan = mockPlans[customerType] || mockPlans.business;
  
  // Generate mock pitch
  const pitch = generateMockPitch(profile, recommendedPlan);
  
  // Generate detailed analysis
  const detailedAnalysis = generateDetailedAnalysis(profile, recommendedPlan, customerType);
  
  res.json({
    customerProfile: profile,
    recommendedPlan: recommendedPlan,
    pitch: pitch,
    confidence: 0.85,
    detailedAnalysis: detailedAnalysis
  });
});

app.get('/api/sample-scenarios', (req, res) => {
  res.json({
    business: "Hi, I'm calling about our business phone plan. We're a small consulting firm with 8 employees. Our current plan keeps running out of data and we're experiencing dropped calls during important client meetings. We need something more reliable but we're also watching our costs carefully.",
    family: "Hello, we're a family of four looking to consolidate our phone plans. Right now we each have individual plans and it's costing us almost $200 a month. The kids are always running out of data and we'd like better parental controls. We're hoping to save some money while getting better service.",
    senior: "Good morning, I'm 72 years old and I think I'm paying too much for my phone plan. I have this unlimited plan that costs $85 a month but I barely use any data. I mainly just make calls and send a few texts. I'd like something simpler and less expensive, but I do want to make sure I can reach help if I need it."
  });
});

function generateMockPitch(profile, plan) {
  const pitches = {
    business: `Based on your business needs, I recommend our ${plan.name} plan at ${plan.price}. This addresses your key concerns:

🎯 **Reliability**: Priority network access ensures no more dropped calls during client meetings
📊 **Data**: 100GB monthly allowance eliminates overage concerns  
💰 **Value**: 24/7 business support included, saving on IT costs
🚀 **Growth**: Easily scalable as your team expands

This plan will save you approximately $30/month compared to your current overages while providing enterprise-grade reliability.`,

    family: `Perfect! Our ${plan.name} at ${plan.price} is designed exactly for families like yours:

👨‍👩‍👧‍👦 **Family Focused**: All 4 lines on one simple bill
💰 **Savings**: Save $60/month compared to your current individual plans
🛡️ **Parental Controls**: Built-in content filtering and screen time management
📱 **Flexibility**: Shared data pool means no one runs out unexpectedly

You'll get better service, more features, and significant savings - it's a win-win!`,

    senior: `I have the perfect solution for you! Our ${plan.name} at ${plan.price} is specifically designed for customers who want simplicity and value:

✨ **Simple**: Easy-to-use interface, no complicated features
💰 **Affordable**: Save $50/month compared to your current plan
🆘 **Peace of Mind**: One-touch emergency button connects to 24/7 help
📞 **What You Need**: 5GB data is perfect for calls, texts, and light browsing

This plan gives you exactly what you use while keeping money in your pocket.`
  };

  return pitches[profile.segment.toLowerCase()] || pitches.business;
}

function generateDetailedAnalysis(profile, plan, customerType) {
  const analyses = {
    family: {
      customerProfiling: {
        extractedKeywords: [
          { category: "Family indicators", keywords: "\"family of four\", \"kids\"" },
          { category: "Cost concerns", keywords: "\"costing us almost $200\", \"save some money\"" },
          { category: "Usage issues", keywords: "\"running out of data\"" },
          { category: "Feature needs", keywords: "\"parental controls\"" },
          { category: "Service goals", keywords: "\"better service\", \"consolidate\"" }
        ],
        intentClassification: {
          primary: "Cost Reduction",
          secondary: "Service Consolidation", 
          tertiary: "Feature Enhancement"
        },
        priorityAnalysis: {
          costSensitivity: { score: 9.5, level: "CRITICAL", color: "critical" },
          dataPriority: { score: 7.5, level: "HIGH", color: "high" },
          familyFeatures: { score: 8.0, level: "HIGH", color: "high" },
          networkQuality: { score: 6.0, level: "MEDIUM", color: "medium" },
          flexibility: { score: 5.5, level: "MEDIUM", color: "medium" }
        },
        segmentation: {
          primarySegment: "Family (4 lines)",
          usagePattern: "Mixed Usage",
          budgetCategory: "Cost-Conscious",
          decisionMaker: "Primary Account Holder"
        },
        painPoints: [
          { issue: "High Monthly Costs", description: "Currently paying ~$200/month for 4 individual plans" },
          { issue: "Data Limitations", description: "Children frequently exceed data allowances" },
          { issue: "Lack of Control", description: "No parental controls on current individual plans" },
          { issue: "Plan Complexity", description: "Managing 4 separate bills and plans" }
        ]
      },
      benefitsComparison: {
        costAnalysis: {
          currentCost: 200,
          recommendedCost: 140,
          monthlySavings: 60,
          annualSavings: 720,
          savingsPercentage: 30
        },
        featureComparison: [
          { feature: "Monthly Cost", current: "$200/month (4 individual plans)", recommended: "$140/month (Family Share 4-Line)", benefit: "Save $60/month", type: "savings" },
          { feature: "Annual Savings", current: "$2,400/year", recommended: "$1,680/year", benefit: "Save $720/year", type: "savings" },
          { feature: "Data Allowance", current: "4 × 10GB = 40GB total (separate)", recommended: "50GB shared pool", benefit: "+10GB total, flexible sharing", type: "improvement" },
          { feature: "Parental Controls", current: "❌ Not available", recommended: "✅ Full parental control suite", benefit: "Content filtering, time limits", type: "new" },
          { feature: "Billing", current: "4 separate bills", recommended: "1 consolidated bill", benefit: "Simplified management", type: "improvement" },
          { feature: "Account Management", current: "4 separate accounts", recommended: "1 family account", benefit: "Centralized control", type: "improvement" }
        ]
      },
      suitabilityScoring: {
        overall: 8.8,
        breakdown: {
          costFit: { score: 9.5, label: "Cost Fit" },
          featureMatch: { score: 9.0, label: "Feature Match" },
          usageAlignment: { score: 8.0, label: "Usage Alignment" },
          familyNeeds: { score: 9.5, label: "Family Needs" }
        },
        reasoning: [
          "Cost Optimization: 30% monthly savings addresses primary concern",
          "Data Flexibility: Shared pool prevents individual overages", 
          "Family Features: Built-in parental controls and management",
          "Simplification: One bill, one account, easier management"
        ]
      },
      personalization: {
        messagingStrategy: [
          "Lead with savings: Emphasize $60/month reduction",
          "Address pain points: Mention data sharing and controls",
          "Family focus: Use family-centric language",
          "Simplicity emphasis: Highlight consolidated billing",
          "Value proposition: Better service for less money"
        ],
        objectionHandling: [
          { objection: "What if we need more data?", response: "The shared 50GB pool is actually 10GB more than your current total, and if anyone needs extra, the whole family benefits from the shared allowance." },
          { objection: "Will service quality decrease?", response: "You'll get the same network quality, but with better family features and significant cost savings." }
        ]
      },
      roiAnalysis: {
        yearOne: 720,
        yearTwo: 1440,
        yearThree: 2160,
        additionalValue: [
          "Parental control features (value: ~$10/month = $120/year)",
          "Simplified billing management (time savings: ~2 hours/month)",
          "Reduced overage risk (potential savings: $50-100/month)"
        ]
      }
    }
  };

  return analyses[customerType] || null;
}

app.listen(PORT, () => {
  console.log(`🚀 Telecom Sales Agent running at http://localhost:${PORT}`);
  console.log(`📱 Web interface available in your browser`);
  console.log(`🤖 AI-powered sales pitch generation ready!`);
});
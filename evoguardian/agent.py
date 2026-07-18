import json
import random
import time
import os

# Simulated dataset of scams and normal messages for local evaluation
DATASET = [
    {"text": "URGENT: Your account at Wells Fargo is locked due to suspicious activity. Click here to verify: http://wellsfargo-verify.com", "label": "scam", "category": "phishing"},
    {"text": "Hi Mom, I dropped my phone in the toilet and it's broken. This is my temporary number. Can you transfer $500 for my taxi? Please.", "label": "scam", "category": "impersonation"},
    {"text": "Congratulations! You have won a $1000 Amazon gift card. Claim it now at http://win-amazon-rewards.xyz", "label": "scam", "category": "gift_card"},
    {"text": "Hey, are we still meeting for lunch at 1 PM today at the usual Italian restaurant?", "label": "normal", "category": "personal"},
    {"text": "Your package from DHL is arriving today between 2 PM and 5 PM. Track details: http://dhl.com/track/129384", "label": "normal", "category": "delivery"},
    {"text": "Dad, can you send me the recipe for the lasagna you made last week? Thanks!", "label": "normal", "category": "personal"},
    {"text": "IRS Alert: You have unpaid taxes of $3,450. A warrant is out for your arrest. Pay immediately via Bitcoin: http://irs-tax-gov.com", "label": "scam", "category": "tax_threat"},
    {"text": "Hi, this is Netflix. Your payment failed and your subscription will end. Update payment details here: http://netflix-billing-update.info", "label": "scam", "category": "subscription_phishing"},
]

# Simple rule-based heuristics that can be mutated (evolved) by the optimizer
DEFAULT_PROMPT = {
    "system_instructions": "Identify if the message is a scam. Look for links.",
    "rules": [
        "If it has a link, flag it.",
    ]
}

# Mutation candidate pool (Simulated LLM Proposer outputs)
MUTATION_OPTIONS = [
    {
        "system_instructions": "Classify the message. Scams often use urgent language, threats, impersonation of family, suspicious links, or promotional discount offers.",
        "rules": [
            "Flag if it has urgent words like 'URGENT', 'Congrats', 'Congratulations', 'failed'.",
            "Flag if it requests urgent money transfers (e.g. 'transfer $500').",
            "Flag if it threatens legal action or tax arrests.",
            "Flag links that do not match official domains (e.g. netflix-billing-update.info vs netflix.com).",
            "Flag promotional offers containing discount keywords like 'off', 'discount', or 'free'."
        ]
    },
    {
        "system_instructions": "Evaluate the message safety. Look for high-pressure requests, banking threats, impersonations, or fake gift cards.",
        "rules": [
            "Check for familial impersonations ('Hi Mom', 'Hi Dad') followed by urgent money requests.",
            "Flag tax or government authority claims with links or non-standard payment options.",
            "Analyze links: distinguish between official ones (dhl.com) and suspicious ones (irs-tax-gov.com).",
            "Flag promotional claims with keywords like 'discount', 'free', or 'gift card'."
        ]
    },
    {
        "system_instructions": "Analyze the message for signs of social engineering, panic induction, phishing links, and prize scams.",
        "rules": [
            "Flag high-urgency notifications about bank accounts, package deliveries, or subscription cancellations.",
            "Identify urgent money requests from unknown numbers posing as family.",
            "Exclude benign package tracking links that match known reputable companies (e.g. dhl.com).",
            "Flag discount offers containing words like 'off', 'cupcake', or 'free'."
        ]
    }
]

class ScamGuardianAgent:
    def __init__(self, prompt_config=None):
        self.config = prompt_config or DEFAULT_PROMPT

    def analyze(self, text):
        text_lower = text.lower()
        reasoning_steps = []
        is_scam = False
        confidence = 0.5

        reasoning_steps.append(f"Applying system prompt: '{self.config['system_instructions']}'")
        
        # Apply the current active rules
        matched_rules = 0
        for rule in self.config["rules"]:
            rule_lower = rule.lower()
            
            # Simulated rule application logic
            if "link" in rule_lower and "http" in text_lower:
                # Check if it is a safe link (dhl.com/track/129384)
                if "dhl.com" in text_lower and "exclude benign" in rule_lower:
                    reasoning_steps.append("Rule Match: DHL link detected but excluded as benign.")
                elif "netflix-billing" in text_lower or "irs-tax" in text_lower or "wellsfargo" in text_lower or "win-amazon" in text_lower:
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append(f"Rule Match: Flagged suspicious domain in link.")
                elif "http" in text_lower and not ("dhl.com" in text_lower):
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append("Rule Match: Generic link detected.")
                    
            if "urgent" in rule_lower or "urgency" in rule_lower:
                if any(x in text_lower for x in ["urgent", "congrats", "congratulations", "failed", "immediate"]):
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append("Rule Match: High urgency language detected.")
                    
            if "money" in rule_lower or "impersonation" in rule_lower:
                if ("mom" in text_lower or "dad" in text_lower or "temporary number" in text_lower) and ("transfer" in text_lower or "$" in text_lower or "money" in text_lower):
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append("Rule Match: Family impersonation combined with urgent money/transfer request.")
                    
            if "threat" in rule_lower or "tax" in rule_lower:
                if "tax" in text_lower or "irs" in text_lower or "arrest" in text_lower:
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append("Rule Match: Legal threat or authority pressure detected.")

            if "promo" in rule_lower or "discount" in rule_lower:
                if any(x in text_lower for x in ["off", "discount", "free", "win", "gift card", "cupcake"]):
                    is_scam = True
                    matched_rules += 1
                    reasoning_steps.append("Rule Match: Promotional offer or discount keyword detected.")

        if is_scam:
            confidence = min(0.5 + (0.15 * matched_rules), 0.99)
            classification = "scam"
        else:
            confidence = 0.85
            classification = "normal"

        return {
            "classification": classification,
            "confidence": confidence,
            "reasoning": reasoning_steps
        }

class EvoSkillOptimizer:
    def __init__(self):
        self.current_config = DEFAULT_PROMPT
        self.history = []

    def evaluate(self, config):
        agent = ScamGuardianAgent(config)
        correct = 0
        total = len(DATASET)
        failures = []

        for idx, item in enumerate(DATASET):
            res = agent.analyze(item["text"])
            is_correct = res["classification"] == item["label"]
            if is_correct:
                correct += 1
            else:
                failures.append({
                    "text": item["text"],
                    "expected": item["label"],
                    "predicted": res["classification"],
                    "reasoning": res["reasoning"]
                })

        accuracy = correct / total
        return accuracy, failures

    def run_evolution_step(self, iteration):
        current_acc, failures = self.evaluate(self.current_config)
        
        if current_acc == 1.0 or iteration > len(MUTATION_OPTIONS):
            return {
                "iteration": iteration,
                "config": self.current_config,
                "accuracy": current_acc,
                "mutated": False,
                "failures": failures
            }

        new_config = MUTATION_OPTIONS[iteration - 1]
        new_acc, new_failures = self.evaluate(new_config)

        if new_acc > current_acc:
            self.current_config = new_config
            accuracy_result = new_acc
            mutated = True
            selected_failures = new_failures
        else:
            accuracy_result = current_acc
            mutated = False
            selected_failures = failures

        step_info = {
            "iteration": iteration,
            "config": self.current_config,
            "accuracy": accuracy_result,
            "mutated": mutated,
            "failures": selected_failures
        }
        self.history.append(step_info)
        return step_info

if __name__ == "__main__":
    print("Testing EvoSkill Optimizer locally...")
    optimizer = EvoSkillOptimizer()
    
    acc, failures = optimizer.evaluate(DEFAULT_PROMPT)
    print(f"Initial Agent Accuracy: {acc*100}%")
    
    for i in range(1, 4):
        result = optimizer.run_evolution_step(i)
        print(f"Iteration {i} - Accuracy: {result['accuracy']*100}% (Mutated: {result['mutated']})")

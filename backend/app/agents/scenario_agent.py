from typing import List, Dict, Any
from app.services.groq_service import groq_service
import json
import logging

logger = logging.getLogger(__name__)


async def scenario_agent(company_name: str, company_context: str) -> List[Dict[str, Any]]:
    """
    Scenario Agent: Generate 4 diverse future scenarios
    
    Args:
        company_name: Name of the company
        company_context: Research context about the company
        
    Returns:
        List of 4 scenario dictionaries
    """
    logger.info(f"Scenario Agent: Generating scenarios for {company_name}")
    
    scenario_prompt = f"""Based on the following company context for {company_name}, generate 4 diverse future scenarios.

Company Context:
{company_context}

Generate 4 scenarios that explore different combinations of:
1. Technology evolution: incremental vs breakthrough
2. Market dynamics: concentration vs fragmentation
3. Regulatory environment: permissive vs restrictive
4. Economic conditions: growth vs constraint

Each scenario should be distinct and cover different strategic possibilities. For each scenario, provide:
- title: A descriptive title (max 100 chars)
- description: 2-3 paragraphs describing the scenario
- timeline: When this scenario might unfold (e.g., "2025-2030", "Next 3-5 years")
- key_assumptions: Key assumptions underlying this scenario
- likelihood: A probability estimate between 0.0 and 1.0

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Scenario Title",
    "description": "2-3 paragraphs...",
    "timeline": "2025-2030",
    "key_assumptions": "Key assumptions...",
    "likelihood": 0.25
  }},
  ...
]

Ensure scenarios are diverse and cover different strategic futures.
"""
    
    try:
        response = await groq_service.generate(
            prompt=scenario_prompt,
            system_prompt="You are a strategic futurist. Generate diverse, plausible future scenarios based on research.",
            temperature=0.8,
            max_tokens=3000
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw Groq response (first 500 chars): {response[:500]}")
        
        # Parse scenarios from response
        scenarios_text = response.strip()
        
        # Remove markdown code blocks if present
        if scenarios_text.startswith("```"):
            # Find the closing ```
            parts = scenarios_text.split("```")
            if len(parts) >= 3:
                scenarios_text = parts[1]  # Take content between first pair of ```
                if scenarios_text.startswith("json"):
                    scenarios_text = scenarios_text[4:]
            else:
                # Malformed markdown, try to extract JSON
                scenarios_text = scenarios_text.replace("```json", "").replace("```", "")
        
        scenarios_text = scenarios_text.strip()
        
        # Try to extract JSON array from text if there's extra content
        # Look for the first '[' and last ']'
        first_bracket = scenarios_text.find('[')
        last_bracket = scenarios_text.rfind(']')
        
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            scenarios_text = scenarios_text[first_bracket:last_bracket + 1]
        
        if not scenarios_text or scenarios_text.strip() == "":
            raise ValueError("Empty response from Groq")
        
        scenarios = json.loads(scenarios_text)
        if not isinstance(scenarios, list):
            raise ValueError("Scenarios response is not a list")
        
        # Ensure we have exactly 4 scenarios
        if len(scenarios) < 4:
            logger.warning(f"Only got {len(scenarios)} scenarios, expected 4")
        elif len(scenarios) > 4:
            scenarios = scenarios[:4]
        
        # Validate and clean scenarios
        for i, scenario in enumerate(scenarios):
            if "scenario_number" not in scenario:
                scenario["scenario_number"] = i + 1
            if "likelihood" not in scenario:
                scenario["likelihood"] = 0.25
            elif not isinstance(scenario["likelihood"], (int, float)):
                scenario["likelihood"] = 0.25
        
        logger.info(f"Generated {len(scenarios)} scenarios")
        return scenarios
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error for scenarios: {e}")
        logger.error(f"Response text (first 1000 chars): {response[:1000] if 'response' in locals() else 'N/A'}")
        raise
    except Exception as e:
        logger.error(f"Error generating scenarios: {e}")
        logger.error(f"Response text (first 1000 chars): {response[:1000] if 'response' in locals() else 'N/A'}")
        # Fallback scenarios
        return [
            {
                "scenario_number": 1,
                "title": f"Incremental Growth Scenario for {company_name}",
                "description": "A scenario where the company experiences steady, incremental growth with gradual technological adoption and stable market conditions.",
                "timeline": "2025-2030",
                "key_assumptions": "Stable market conditions, gradual technology adoption, moderate regulatory changes",
                "likelihood": 0.3
            },
            {
                "scenario_number": 2,
                "title": f"Disruptive Technology Scenario for {company_name}",
                "description": "A scenario where breakthrough technologies fundamentally reshape the industry, creating both opportunities and challenges.",
                "timeline": "2024-2027",
                "key_assumptions": "Rapid technology adoption, market disruption, new competitive entrants",
                "likelihood": 0.25
            },
            {
                "scenario_number": 3,
                "title": f"Regulatory Constraint Scenario for {company_name}",
                "description": "A scenario where increased regulatory oversight and restrictions impact business operations and strategic options.",
                "timeline": "2025-2028",
                "key_assumptions": "Increased regulation, compliance requirements, restricted market access",
                "likelihood": 0.2
            },
            {
                "scenario_number": 4,
                "title": f"Market Consolidation Scenario for {company_name}",
                "description": "A scenario where market dynamics lead to consolidation, with winners and losers clearly defined.",
                "timeline": "2026-2030",
                "key_assumptions": "Market consolidation, competitive pressure, strategic acquisitions",
                "likelihood": 0.25
            }
        ]


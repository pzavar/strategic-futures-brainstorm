from typing import List, Dict, Any
from app.services.groq_service import groq_service
import json
import logging
import re

logger = logging.getLogger(__name__)


def sanitize_json_string(text: str) -> str:
    """
    Sanitize a JSON string by escaping control characters
    that can cause JSON parsing errors.
    """
    # First, temporarily mark already-escaped characters
    text = text.replace('\\n', '\x00ESCAPED_NEWLINE\x00')
    text = text.replace('\\t', '\x00ESCAPED_TAB\x00')
    text = text.replace('\\r', '\x00ESCAPED_RETURN\x00')
    text = text.replace('\\\\', '\x00ESCAPED_BACKSLASH\x00')
    
    # Now escape actual control characters (including \n, \t, \r)
    # Replace newlines with escaped newlines
    text = text.replace('\n', '\\n')
    text = text.replace('\r', '\\r')
    text = text.replace('\t', '\\t')
    
    # Remove any other control characters (ASCII 0-31 except those we just handled)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', text)
    
    # Restore the already-escaped characters
    text = text.replace('\x00ESCAPED_BACKSLASH\x00', '\\\\')
    text = text.replace('\x00ESCAPED_NEWLINE\x00', '\\n')
    text = text.replace('\x00ESCAPED_TAB\x00', '\\t')
    text = text.replace('\x00ESCAPED_RETURN\x00', '\\r')
    
    return text


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

Each scenario should be distinct and cover different strategic possibilities.

IMPORTANT: 
- Use the specific financial data and metrics from the company context in your scenarios
- Reference current revenue, growth rates, and market position when describing future trajectories
- Scenarios should be grounded in the company's actual financial situation and market position

You must return a JSON object with a "scenarios" array. Each scenario must have these fields:
- title: A descriptive title (max 100 chars)
- description: 2-3 paragraphs describing the scenario
- timeline: When this scenario might unfold (e.g., "2025-2030", "Next 3-5 years")
- key_assumptions: Key assumptions underlying this scenario
- likelihood: A probability estimate between 0.0 and 1.0

Return valid JSON in this exact structure:
{{
  "scenarios": [
    {{
      "title": "Scenario Title Here",
      "description": "Description paragraphs here",
      "timeline": "2025-2030",
      "key_assumptions": "Key assumptions here",
      "likelihood": 0.25
    }}
  ]
}}

Ensure all string values are properly quoted and escaped. Generate exactly 4 diverse scenarios.
"""
    
    try:
        response = await groq_service.generate(
            prompt=scenario_prompt,
            system_prompt="You are a strategic futurist. You must return valid JSON only.",
            temperature=0.8,
            max_tokens=3000,
            json_mode=True
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw Groq response (first 500 chars): {response[:500]}")
        
        # Parse scenarios from response
        scenarios_text = response.strip()
        
        logger.info(f"[PARSE] Original response length: {len(scenarios_text)} chars")
        logger.info(f"[PARSE] Response preview: {scenarios_text[:200]}")
        
        # JSON mode should return clean JSON, but still validate
        if not scenarios_text:
            raise ValueError("Empty response from Groq")
        
        # Parse the JSON response
        data = json.loads(scenarios_text)
        
        # Extract scenarios array from the response
        if isinstance(data, dict) and "scenarios" in data:
            scenarios = data["scenarios"]
        elif isinstance(data, list):
            # Fallback: if it's already a list
            scenarios = data
        else:
            raise ValueError(f"Unexpected response structure: {type(data)}")
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


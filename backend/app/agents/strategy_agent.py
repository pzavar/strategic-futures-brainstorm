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


async def strategy_agent(
    company_name: str,
    company_context: str,
    scenario: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Strategy Agent: Propose 2-3 strategies for a given scenario
    
    Args:
        company_name: Name of the company
        company_context: Research context about the company
        scenario: The scenario dictionary
        
    Returns:
        List of strategy dictionaries
    """
    logger.info(f"Strategy Agent: Generating strategies for scenario: {scenario.get('title', 'Unknown')}")
    
    strategy_prompt = f"""Based on the company context and future scenario below, propose 2-3 concrete strategic recommendations for {company_name}.

Company Context:
{company_context}

Future Scenario:
Title: {scenario.get('title', 'Unknown')}
Description: {scenario.get('description', 'N/A')}
Timeline: {scenario.get('timeline', 'N/A')}
Key Assumptions: {scenario.get('key_assumptions', 'N/A')}

You must return a JSON object with a "strategies" array. Each strategy must have these fields:
- name: A clear, actionable strategy name (max 100 chars)
- description: Detailed description of the strategy (2-3 paragraphs)
- expected_impact: What impact this strategy would have (1-2 paragraphs) - INCLUDE QUANTIFIED ESTIMATES (revenue impact, cost savings, market share changes, etc.)
- key_risks: Key risks and challenges (1 paragraph)

IMPORTANT:
- Reference the company's current financial position (revenue, margins, growth rates) from the context
- Quantify expected impacts where possible (e.g., "could increase revenue by 10-15%", "reduce costs by $X million")
- Ground strategies in the company's actual scale and resources

Return valid JSON in this exact structure:
{{
  "strategies": [
    {{
      "name": "Strategy Name Here",
      "description": "Detailed description here",
      "expected_impact": "Impact description here with quantified estimates",
      "key_risks": "Risk description here"
    }}
  ]
}}

Ensure all string values are properly quoted and escaped. Provide 2-3 distinct, actionable strategies.
"""
    
    try:
        response = await groq_service.generate(
            prompt=strategy_prompt,
            system_prompt="You are a strategic consultant. You must return valid JSON only.",
            temperature=0.7,
            max_tokens=4000,
            json_mode=True
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw Groq response (first 500 chars): {response[:500]}")
        
        # Parse strategies from response
        strategies_text = response.strip()
        
        logger.info(f"[PARSE] Original response length: {len(strategies_text)} chars")
        logger.info(f"[PARSE] Response preview: {strategies_text[:200]}")
        
        # JSON mode should return clean JSON, but still validate
        if not strategies_text:
            raise ValueError("Empty response from Groq")
        
        # Parse the JSON response
        data = json.loads(strategies_text)
        
        # Extract strategies array from the response
        if isinstance(data, dict) and "strategies" in data:
            strategies = data["strategies"]
        elif isinstance(data, list):
            # Fallback: if it's already a list
            strategies = data
        else:
            raise ValueError(f"Unexpected response structure: {type(data)}")
        if not isinstance(strategies, list):
            raise ValueError("Strategies response is not a list")
        
        # Ensure we have 2-3 strategies
        if len(strategies) < 2:
            logger.warning(f"Only got {len(strategies)} strategies, expected 2-3")
        elif len(strategies) > 3:
            strategies = strategies[:3]
        
        logger.info(f"Generated {len(strategies)} strategies for scenario")
        return strategies
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error for strategies: {e}")
        logger.error(f"Response text (first 1000 chars): {response[:1000] if 'response' in locals() else 'N/A'}")
        raise
    except Exception as e:
        logger.error(f"Error generating strategies: {e}")
        logger.error(f"Response text (first 1000 chars): {response[:1000] if 'response' in locals() else 'N/A'}")
        raise


from typing import List, Dict, Any
from app.services.groq_service import groq_service
import json
import logging

logger = logging.getLogger(__name__)


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

For each strategy, provide:
- name: A clear, actionable strategy name (max 100 chars)
- description: Detailed description of the strategy (2-3 paragraphs)
- expected_impact: What impact this strategy would have (1-2 paragraphs)
- key_risks: Key risks and challenges (1 paragraph)

Return ONLY a JSON array with this exact structure:
[
  {{
    "name": "Strategy Name",
    "description": "Detailed description...",
    "expected_impact": "Impact description...",
    "key_risks": "Risk description..."
  }},
  ...
]

Provide 2-3 distinct, actionable strategies that would help the company navigate this scenario.
"""
    
    try:
        response = await groq_service.generate(
            prompt=strategy_prompt,
            system_prompt="You are a strategic consultant. Propose concrete, actionable strategies based on scenarios.",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Log the raw response for debugging
        logger.debug(f"Raw Groq response (first 500 chars): {response[:500]}")
        
        # Parse strategies from response
        strategies_text = response.strip()
        
        # Remove markdown code blocks if present
        if strategies_text.startswith("```"):
            # Find the closing ```
            parts = strategies_text.split("```")
            if len(parts) >= 3:
                strategies_text = parts[1]  # Take content between first pair of ```
                if strategies_text.startswith("json"):
                    strategies_text = strategies_text[4:]
            else:
                # Malformed markdown, try to extract JSON
                strategies_text = strategies_text.replace("```json", "").replace("```", "")
        
        strategies_text = strategies_text.strip()
        
        # Try to extract JSON array from text if there's extra content
        # Look for the first '[' and last ']'
        first_bracket = strategies_text.find('[')
        last_bracket = strategies_text.rfind(']')
        
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            strategies_text = strategies_text[first_bracket:last_bracket + 1]
        
        if not strategies_text or strategies_text.strip() == "":
            raise ValueError("Empty response from Groq")
        
        strategies = json.loads(strategies_text)
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
        # Fallback strategies
        return [
            {
                "name": f"Adaptive Strategy for {scenario.get('title', 'Scenario')}",
                "description": "A flexible approach that allows the company to adapt to changing conditions while maintaining core capabilities.",
                "expected_impact": "This strategy would help the company remain competitive and responsive to market changes.",
                "key_risks": "Risk of spreading resources too thin or losing focus on core competencies."
            },
            {
                "name": f"Proactive Positioning Strategy",
                "description": "An aggressive strategy to position the company as a leader in the scenario's context.",
                "expected_impact": "Could establish market leadership but requires significant investment.",
                "key_risks": "High investment requirements and uncertainty about scenario unfolding as predicted."
            }
        ]


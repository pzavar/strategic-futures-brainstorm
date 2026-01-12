from typing import List, Dict, Any
from app.services.groq_service import groq_service
from app.services.tavily_service import tavily_service
import json
import logging
import asyncio

logger = logging.getLogger(__name__)


async def research_agent(company_name: str) -> Dict[str, Any]:
    """
    Research Agent: Generate research questions and search for information
    
    Args:
        company_name: Name of the company to research
        
    Returns:
        Dictionary with research_questions, search_results, and company_context
    """
    logger.info(f"Research Agent: Starting research for {company_name}")
    
    # Step 1: Generate strategic research questions
    questions_prompt = f"""Generate 5-7 strategic research questions about {company_name} that would help understand:
1. Business model and revenue streams
2. Competitive landscape and market position
3. Emerging technologies affecting the industry
4. Regulatory environment and compliance requirements
5. Strategic priorities and growth opportunities
6. Market trends and disruptions
7. Key threats and challenges

Return ONLY a JSON array of question strings, no other text.
Example format: ["Question 1?", "Question 2?", ...]
"""
    
    try:
        questions_response = await groq_service.generate(
            prompt=questions_prompt,
            system_prompt="You are a strategic research analyst. Generate focused, actionable research questions.",
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse questions from response
        questions_text = questions_response.strip()
        # Remove markdown code blocks if present
        if questions_text.startswith("```"):
            questions_text = questions_text.split("```")[1]
            if questions_text.startswith("json"):
                questions_text = questions_text[4:]
        questions_text = questions_text.strip()
        
        # Try to extract JSON array from text if there's extra content
        # Look for the first '[' and last ']'
        first_bracket = questions_text.find('[')
        last_bracket = questions_text.rfind(']')
        
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            questions_text = questions_text[first_bracket:last_bracket + 1]
        
        research_questions = json.loads(questions_text)
        if not isinstance(research_questions, list):
            raise ValueError("Questions response is not a list")
        
        logger.info(f"Generated {len(research_questions)} research questions")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error for questions: {e}")
        logger.error(f"Response text (first 1000 chars): {questions_response[:1000] if 'questions_response' in locals() else 'N/A'}")
        raise
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        logger.error(f"Response text (first 1000 chars): {questions_response[:1000] if 'questions_response' in locals() else 'N/A'}")
        # Fallback questions
        research_questions = [
            f"What is {company_name}'s business model and revenue streams?",
            f"Who are {company_name}'s main competitors?",
            f"What emerging technologies are affecting {company_name}'s industry?",
            f"What regulatory challenges does {company_name} face?",
            f"What are {company_name}'s strategic priorities?"
        ]
    
    # Step 2: Search for each question
    search_results = {}
    for i, question in enumerate(research_questions):
        try:
            logger.info(f"Searching for question {i+1}/{len(research_questions)}: {question}")
            results = await tavily_service.search(query=question, max_results=5)
            search_results[question] = results
        except asyncio.CancelledError as e:
            logger.error(f"[RESEARCH] Search cancelled for question '{question}': {e}", exc_info=True)
            search_results[question] = []
        except Exception as e:
            logger.error(f"[RESEARCH] Error searching for question '{question}': {type(e).__name__}: {str(e)}", exc_info=True)
            search_results[question] = []
    
    # Step 3: Synthesize findings into company context
    # Truncate search results to avoid token limit issues
    # Summarize each search result to key points only
    summarized_results = {}
    for question, results in search_results.items():
        if isinstance(results, list) and len(results) > 0:
            # Take only the first 2 results and limit content length
            summarized_results[question] = []
            for result in results[:2]:
                if isinstance(result, dict):
                    summary = {
                        "title": result.get("title", "")[:200],
                        "url": result.get("url", ""),
                        "content": result.get("content", "")[:500] if result.get("content") else ""
                    }
                    summarized_results[question].append(summary)
        else:
            summarized_results[question] = results
    
    synthesis_prompt = f"""Based on the following research about {company_name}, synthesize a comprehensive company context.

Research Questions and Findings:
{json.dumps(summarized_results, indent=2)}

Create a comprehensive company context covering:
1. Industry and market position
2. Business model and revenue streams
3. Competitive landscape
4. Emerging technologies and trends
5. Regulatory environment
6. Strategic priorities
7. Key threats and opportunities

Format as a well-structured text document (2-3 pages equivalent).
"""
    
    try:
        company_context = await groq_service.generate(
            prompt=synthesis_prompt,
            system_prompt="You are a strategic analyst synthesizing research into actionable insights.",
            temperature=0.7,
            max_tokens=2000
        )
        logger.info("Successfully synthesized company context")
    except Exception as e:
        logger.error(f"Error synthesizing context: {e}")
        logger.error(f"Search results size: {len(json.dumps(search_results))} chars")
        company_context = f"Research completed for {company_name}. Analysis of {len(research_questions)} research areas."
    
    return {
        "research_questions": research_questions,
        "search_results": search_results,
        "company_context": company_context
    }


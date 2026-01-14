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
1. Financial performance (revenue, earnings, profit margins, growth rates)
2. Business model and revenue streams
3. Competitive landscape and market position
4. Emerging technologies affecting the industry
5. Regulatory environment and compliance requirements
6. Strategic priorities and growth opportunities
7. Market trends and disruptions
8. Key threats and challenges

Return a JSON object with a "questions" array.
Format: {{"questions": ["Question 1?", "Question 2?", ...]}}
"""
    
    try:
        questions_response = await groq_service.generate(
            prompt=questions_prompt,
            system_prompt="You are a strategic research analyst for S&P 500 companies and all-things tech/finance/economy expert. You must return valid JSON only.",
            temperature=0.7,
            max_tokens=700,
            json_mode=True
        )
        
        # Parse questions from response
        questions_text = questions_response.strip()
        
        if not questions_text:
            raise ValueError("Empty response from Groq")
        
        # Parse the JSON response
        data = json.loads(questions_text)
        
        # Extract questions array from the response
        if isinstance(data, dict) and "questions" in data:
            research_questions = data["questions"]
        elif isinstance(data, list):
            # Fallback: if it's already a list
            research_questions = data
        else:
            raise ValueError(f"Unexpected response structure: {type(data)}")
            
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
            f"What is {company_name}'s latest financial performance including revenue, earnings, and profit margins?",
            f"What is {company_name}'s business model and revenue streams?",
            f"Who are {company_name}'s main competitors and market share?",
            f"What emerging technologies are affecting {company_name}'s industry?",
            f"What regulatory challenges does {company_name} face?",
            f"What are {company_name}'s strategic priorities and recent initiatives?"
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
    # Prepare search results with URLs preserved for citations
    summarized_results = {}
    for question, results in search_results.items():
        if isinstance(results, list) and len(results) > 0:
            # Take first 3 results to get more data including financial info
            summarized_results[question] = []
            for result in results[:3]:
                if isinstance(result, dict):
                    summary = {
                        "title": result.get("title", "")[:300],
                        "url": result.get("url", ""),  # Keep full URL for citations
                        "content": result.get("content", "")[:800] if result.get("content") else ""  # Increased for financial data
                    }
                    summarized_results[question].append(summary)
        else:
            summarized_results[question] = results
    
    synthesis_prompt = f"""Based on the following research about {company_name}, synthesize a comprehensive company context.

Research Questions and Findings:
{json.dumps(summarized_results, indent=2)}

Create a comprehensive company context covering:
1. **Financial Performance**: Include specific numbers - revenue, earnings, profit margins, growth rates, market cap (with year/quarter)
2. **Industry and Market Position**: Market share percentages, ranking, competitive positioning
3. **Business Model and Revenue Streams**: Breakdown of revenue sources with percentages if available
4. **Competitive Landscape**: Key competitors with market share data
5. **Emerging Technologies and Trends**: Specific technologies and adoption rates
6. **Regulatory Environment**: Specific regulations and compliance requirements
7. **Strategic Priorities**: Recent announcements, initiatives, investments
8. **Key Threats and Opportunities**: Data-driven analysis

CRITICAL REQUIREMENTS:
- Include specific financial metrics and numbers wherever possible
- Cite sources by including the URL in parentheses after key facts: "Company revenue was $X billion (source: url)"
- Use data from the research results, not generic statements
- Include dates for financial data (e.g., "Q3 2024", "FY 2023")
- Format citations as: (Source: [url])

Format as a well-structured markdown document with clear sections.
"""
    
    try:
        company_context = await groq_service.generate(
            prompt=synthesis_prompt,
            system_prompt="You are a strategic business analyst with a deep understanding of industry analysis and market research. Include specific financial metrics and cite sources with URLs.",
            temperature=0.7,
            max_tokens=4000  # Increased to accommodate financial data and citations
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


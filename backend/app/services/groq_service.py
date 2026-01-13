import httpx
import asyncio
from typing import Optional, Dict, Any
from app.core.config import settings
import time
import logging

logger = logging.getLogger(__name__)


class GroqService:
    """Service for interacting with Groq API (Llama 3.1 8B Instant)"""
    
    BASE_URL = "https://api.groq.com/openai/v1"
    MODEL = "llama-3.1-8b-instant"  # Fast, reliable model - commonly available
    MAX_RETRIES = 5  # Increased for rate limiting
    RETRY_DELAY = 2  # seconds - increased base delay for rate limits
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False
    ) -> str:
        """
        Generate text using Groq API with retry logic
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            json_mode: If True, forces the model to return valid JSON
            
        Returns:
            Generated text
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Hardcode model name to avoid any caching issues
        model_name = "llama-3.1-8b-instant"  # Hardcoded to ensure it's used
        logger.info(f"[GROQ] Using model: {model_name} for request (JSON mode: {json_mode})")
        
        payload = {
            "model": model_name,  # Hardcoded model name
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Enable JSON mode if requested
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.debug(f"[GROQ] Attempt {attempt + 1}/{self.MAX_RETRIES} - Max tokens: {max_tokens}")
                response = await self.client.post("/chat/completions", json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                # Log the actual error response from Groq
                error_detail = ""
                try:
                    error_detail = e.response.text
                    error_json = e.response.json() if e.response.headers.get("content-type", "").startswith("application/json") else None
                    if error_json:
                        error_detail = f"JSON: {error_json}"
                except Exception as parse_error:
                    error_detail = f"Could not parse error response: {parse_error}"
                
                status_code = e.response.status_code
                
                if status_code == 429:  # Rate limit
                    wait_time = self.RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"[GROQ] Rate limited (429), waiting {wait_time}s before retry {attempt + 1}/{self.MAX_RETRIES}")
                    logger.debug(f"[GROQ] Rate limit response: {error_detail}")
                    await asyncio.sleep(wait_time)
                    continue
                elif status_code >= 500:  # Server error
                    if attempt < self.MAX_RETRIES - 1:
                        wait_time = self.RETRY_DELAY * (2 ** attempt)
                        logger.warning(f"[GROQ] Server error ({status_code}), retrying in {wait_time}s")
                        logger.debug(f"[GROQ] Server error response: {error_detail}")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"[GROQ] Server error ({status_code}) after all retries: {error_detail}")
                elif status_code >= 400:  # Client error (400-499)
                    # For 400 errors, log detailed info and don't retry
                    logger.error(f"[GROQ] Client error ({status_code}): {error_detail}")
                    logger.error(f"[GROQ] Request payload: model={model_name}, temperature={temperature}, max_tokens={max_tokens}")
                    logger.error(f"[GROQ] Messages count: {len(messages)}, System prompt: {'Yes' if system_prompt else 'No'}")
                    logger.error(f"[GROQ] User prompt length: {len(prompt)} chars")
                    # Don't retry client errors (400-499) as they won't succeed on retry
                    raise
                
                # For other status codes, log and raise
                logger.error(f"[GROQ] HTTP error ({status_code}): {error_detail}")
                raise
            except Exception as e:
                logger.error(f"[GROQ] Unexpected error calling Groq API: {type(e).__name__}: {str(e)}", exc_info=True)
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (2 ** attempt))
                    continue
                raise
        
        raise Exception("Failed to generate after all retries")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance
groq_service = GroqService()


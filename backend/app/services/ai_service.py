"""
AI service for chat, analysis, and intent classification.
Supports both Ollama (local) and Groq API (free tier).
"""
import httpx
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from uuid import UUID
import json

from app.core.config import settings
from app.schemas.schemas import ChatResponse, AnalysisReport


class AIService:
    """Service for AI-powered analysis and conversation."""
    
    def __init__(self):
        self.ollama_url = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.groq_api_key = settings.GROQ_API_KEY
        self.groq_model = settings.GROQ_MODEL
        self.provider = settings.LLM_PROVIDER
    
    async def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Call local Ollama LLM."""
        url = f"{self.ollama_url}/api/generate"
        
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 1024
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                return result.get("response", "I apologize, but I couldn't generate a response.")
        except Exception as e:
            print(f"Ollama error: {e}")
            raise
    
    async def _call_groq(self, messages: List[Dict[str, str]]) -> str:
        """Call Groq API."""
        if not self.groq_api_key:
            raise ValueError("Groq API key not configured")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.groq_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq error: {e}")
            raise
    
    async def _call_llm(self, prompt: str, system_prompt: str = "", messages: Optional[List[Dict[str, str]]] = None) -> str:
        """Call LLM with fallback logic."""
        if messages:
            # Use message format for Groq
            if self.provider == "groq" and self.groq_api_key:
                return await self._call_groq(messages)
            else:
                # Convert messages to prompt for Ollama
                full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
                return await self._call_ollama(full_prompt, system_prompt)
        else:
            # Use simple prompt format
            if self.provider == "groq" and self.groq_api_key:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                return await self._call_groq(messages)
            else:
                return await self._call_ollama(prompt, system_prompt)
    
    def _get_intent_classification_prompt(self, user_message: str) -> str:
        """Generate prompt for intent classification."""
        return f"""
Analyze the following user query about financial markets and extract:
1. The primary INTENT (choose from: STOCK_ANALYSIS, IPO_ANALYSIS, PORTFOLIO_REVIEW, MARKET_RESEARCH, SWING_TRADING, INTRADAY_TRADING, LONG_TERM_INVESTING, COMPARISON, VALUATION_CHECK, OPPORTUNITY_SCAN, GENERAL_QUESTION)
2. The TIME_HORIZON (intraday, swing, positional, long_term, or unspecified)
3. Any mentioned STOCK SYMBOLS (as a list)
4. Any specific ASPECTS requested (fundamentals, technicals, valuation, risks, etc.)

User query: "{user_message}"

Respond ONLY with valid JSON in this exact format:
{{
    "intent": "INTENT_TYPE",
    "time_horizon": "horizon_or_unspecified",
    "symbols": ["SYMBOL1", "SYMBOL2"],
    "aspects": ["aspect1", "aspect2"]
}}
"""
    
    async def classify_intent(self, user_message: str) -> Dict[str, Any]:
        """Classify user intent and extract entities."""
        system_prompt = "You are a financial intent classifier. Extract structured information from user queries."
        
        try:
            response = await self._call_llm(
                self._get_intent_classification_prompt(user_message),
                system_prompt
            )
            
            # Parse JSON response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {
                    "intent": "GENERAL_QUESTION",
                    "time_horizon": "unspecified",
                    "symbols": [],
                    "aspects": []
                }
        except Exception as e:
            print(f"Intent classification error: {e}")
            return {
                "intent": "GENERAL_QUESTION",
                "time_horizon": "unspecified",
                "symbols": [],
                "aspects": []
            }
    
    def _get_analysis_prompt(self, symbol: str, time_horizon: str, data: Dict[str, Any], context: str = "") -> Tuple[str, str]:
        """Generate prompt for stock analysis."""
        
        system_prompt = """You are a professional equity research analyst. Your role is to provide balanced, evidence-based analysis of stocks.

IMPORTANT GUIDELINES:
1. NEVER claim certainty about future price movements
2. Always distinguish between FACTS (data), INTERPRETATIONS, and OPINIONS
3. Acknowledge uncertainty and limitations
4. Consider multiple scenarios (bull case, base case, bear case)
5. Highlight both positives AND risks
6. Adapt your analysis depth based on time horizon
7. It's okay to say "insufficient data" or "no clear opportunity"
8. Never give definitive BUY/SELL recommendations - instead discuss risk/reward

For INTRADAY/SWING: Focus on technical setup, momentum, volume, catalysts
For LONG_TERM: Focus on business quality, financials, competitive position, valuation"""

        user_prompt = f"""Analyze {symbol} for a {time_horizon.replace('_', ' ')} perspective.

AVAILABLE DATA:
{json.dumps(data, indent=2, default=str)}

USER CONTEXT: {context if context else "None"}

Provide a structured analysis with these sections:

1. BUSINESS OVERVIEW (what does the company do?)
2. FINANCIAL PERFORMANCE (revenue, earnings, margins, growth)
3. VALUATION ASSESSMENT (is it expensive or cheap? compare to peers/history)
4. TECHNICAL POSITION (only if relevant for the time horizon)
5. KEY CATALYSTS (what could drive performance?)
6. MAIN RISKS (what could go wrong?)
7. CONCLUSION with confidence level (High/Medium/Low)

Format your response clearly with section headers. Be concise but thorough."""

        return user_prompt, system_prompt
    
    async def analyze_stock(
        self, 
        symbol: str, 
        time_horizon: str,
        market_data: Dict[str, Any],
        fundamentals: Optional[Dict[str, Any]] = None,
        context: str = ""
    ) -> AnalysisReport:
        """Generate comprehensive stock analysis."""
        
        # Prepare data for LLM
        data = {
            "symbol": symbol,
            "market_data": market_data,
            "fundamentals": fundamentals or {}
        }
        
        user_prompt, system_prompt = self._get_analysis_prompt(symbol, time_horizon, data, context)
        
        try:
            response = await self._call_llm(user_prompt, system_prompt)
            
            return AnalysisReport(
                symbol=symbol,
                time_horizon=time_horizon,
                business_overview=self._extract_section(response, "BUSINESS OVERVIEW"),
                financial_performance=self._extract_section(response, "FINANCIAL PERFORMANCE"),
                valuation=self._extract_section(response, "VALUATION"),
                technical_position=self._extract_section(response, "TECHNICAL POSITION"),
                catalysts=self._extract_list(response, "CATALYSTS"),
                risks=self._extract_list(response, "RISKS"),
                conclusion=self._extract_section(response, "CONCLUSION"),
                confidence_level=self._extract_confidence(response),
                generated_at=datetime.utcnow()
            )
        except Exception as e:
            print(f"Analysis error: {e}")
            return AnalysisReport(
                symbol=symbol,
                time_horizon=time_horizon,
                conclusion=f"Unable to complete analysis due to technical error: {str(e)}",
                confidence_level="Low",
                generated_at=datetime.utcnow()
            )
    
    def _extract_section(self, text: str, section_name: str) -> Optional[str]:
        """Extract a section from analysis text."""
        import re
        pattern = rf"{section_name}[:\s]*(.*?)(?=\n\d\.|\n[A-Z]|\Z)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else None
    
    def _extract_list(self, text: str, section_name: str) -> Optional[List[str]]:
        """Extract a bulleted list from analysis text."""
        import re
        pattern = rf"{section_name}[:\s]*\n(.*?)(?=\n\d\.|\n[A-Z]|\Z)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1)
            items = re.findall(r'[-•*]\s*(.+)', content)
            return [item.strip() for item in items] if items else None
        return None
    
    def _extract_confidence(self, text: str) -> str:
        """Extract confidence level from analysis."""
        import re
        pattern = r"confidence level[:\s]*(High|Medium|Low)"
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else "Medium"
    
    async def chat(
        self, 
        message: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> ChatResponse:
        """Handle general chat queries."""
        
        # First classify intent
        intent_info = await self.classify_intent(message)
        
        system_prompt = """You are a helpful AI assistant specializing in financial markets and investment research. 

GUIDELINES:
- Provide evidence-based answers
- Acknowledge uncertainty
- Distinguish facts from opinions
- Never guarantee returns
- Encourage further research
- Be honest about data limitations
- Adapt to the user's time horizon and objectives"""

        # Build conversation
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history[-5:])  # Last 5 messages for context
        
        if context_data:
            messages.append({
                "role": "system", 
                "content": f"Context data: {json.dumps(context_data, default=str)}"
            })
        
        messages.append({"role": "user", "content": message})
        
        try:
            response_text = await self._call_llm("", "", messages)
            
            return ChatResponse(
                response=response_text,
                conversation_id=UUID(int=1),  # Will be replaced with actual ID
                intent=intent_info.get("intent"),
                entities={
                    "symbols": intent_info.get("symbols", []),
                    "time_horizon": intent_info.get("time_horizon")
                },
                confidence="Medium",
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            return ChatResponse(
                response=f"I apologize, but I encountered an error processing your request: {str(e)}",
                conversation_id=UUID(int=1),
                intent=intent_info.get("intent"),
                timestamp=datetime.utcnow()
            )


# Singleton instance
ai_service = AIService()

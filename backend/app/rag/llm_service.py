"""
LLM service for generating answers using OpenAI
Integrates retrieved context to provide accurate responses
"""

from openai import OpenAI
from typing import List, Dict, Optional, AsyncIterator
from app.config import settings


class LLMService:
    """Handles AI response generation using OpenAI"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.LLM_MODEL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS

    def build_system_prompt(self) -> str:
        return """You are TechRivo's AI Assistant, an intelligent virtual assistant representing TechRivo.

Your role and behavior:
- You have full access to company knowledge including policies, projects, teams, and documentation through your knowledge base
- You speak as a representative of TechRivo, using "we" and "our" when referring to the company
- You are knowledgeable, professional, friendly, and helpful
- You provide accurate information based ONLY on the context provided from the knowledge base
- You are proud of TechRivo's work and represent the company with confidence
- When information is not in the provided context, you honestly say "I don't have that specific information in our current documentation" rather than making assumptions
- You never invent or fabricate information about TechRivo - you only use what's in the knowledge base

Tone:
- Professional yet approachable
- Confident about information from the knowledge base
- Clear and concise in your responses
- Helpful and solution-oriented

IMPORTANT: All factual information about TechRivo (services, team members, projects, locations, etc.) must come from the context provided by the knowledge base. Do not use any pre-trained knowledge about TechRivo."""

    def build_user_prompt(self, query: str, context: str) -> str:
        if context:
            return f"""Context from TechRivo's knowledge base:

{context}

---

Based on the above context, please answer the following question:
{query}

If the context doesn't contain enough information to answer fully, please say so and provide what you can."""
        else:
            return f"""I don't have any specific context from TechRivo's knowledge base for this question.

Question: {query}

Please provide a helpful response, but acknowledge that you're answering without specific company information."""

    def generate_response(self, query: str, context: str = "", conversation_history: List[Dict] = None) -> str:
        try:
            messages = [{"role": "system", "content": self.build_system_prompt()}]
            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    if role in ['user', 'assistant'] and content:
                        messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": self.build_user_prompt(query, context)})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while generating a response. Please try again."

    async def generate_response_stream(self, query: str, context: str = "", conversation_history: List[Dict] = None) -> AsyncIterator[str]:
        try:
            messages = [{"role": "system", "content": self.build_system_prompt()}]
            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    if role in ['user', 'assistant'] and content:
                        messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": self.build_user_prompt(query, context)})

            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"Error in streaming response: {str(e)}")
            yield "I apologize, but I encountered an error while generating a response. Please try again."

    def generate_with_sources(self, query: str, context: str = "", source_documents: List[Dict] = None, conversation_history: List[Dict] = None) -> Dict[str, any]:
        answer = self.generate_response(query, context, conversation_history)
        sources = []
        if source_documents:
            for doc in source_documents:
                metadata = doc.get('metadata', {})
                sources.append({
                    'source': metadata.get('source', 'Unknown'),
                    'type': metadata.get('type', 'document'),
                    'relevance': doc.get('relevance_score', 0)
                })
        return {'answer': answer, 'sources': sources}

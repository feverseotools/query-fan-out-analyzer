"""
AI Client for OpenAI Integration
Supports OpenAI GPT models with multilingual capabilities
"""

import openai
from typing import List, Dict, Optional
import json
import time
from dataclasses import dataclass

@dataclass
class AIResponse:
    predictions: List[Dict]
    reasoning: str
    confidence: float
    processing_time: float

class MultilingualAIClient:
    
    def __init__(self, provider: str, api_key: str, language: str = "en", settings: dict = None):
        # Only support OpenAI now
        if provider.lower() != "openai":
            raise ValueError("Only OpenAI provider is supported")
            
        self.provider = "openai"
        self.api_key = api_key
        self.language = language
        self.settings = settings or {}
        
        # Get AI settings from user configuration
        ai_settings = self.settings.get("ai_settings", {})
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        self.model = ai_settings.get("openai_model", "gpt-4")
        
        # Set generation parameters
        self.temperature = ai_settings.get("temperature", 0.7)
        self.max_predictions = ai_settings.get("max_predictions", 8)
        self.fallback_enabled = ai_settings.get("fallback_enabled", True)
    
    def generate_fanout_predictions(self, query: str, query_analysis: Dict) -> AIResponse:
        """Generate fan-out predictions using real AI APIs"""
        start_time = time.time()
        
        try:
            # Create language-specific prompt
            prompt = self._create_multilingual_prompt(query, query_analysis)
            
            # Call OpenAI API
            response = self._call_openai(prompt)
            
            # Parse response
            parsed_predictions = self._parse_ai_response(response, query)
            
            processing_time = time.time() - start_time
            
            return AIResponse(
                predictions=parsed_predictions,
                reasoning=f"Generated using OpenAI API in {self.language}",
                confidence=0.85,
                processing_time=processing_time
            )
            
        except Exception as e:
            # Fallback response
            return AIResponse(
                predictions=self._create_fallback_predictions(query),
                reasoning=f"Fallback due to error: {str(e)}",
                confidence=0.5,
                processing_time=time.time() - start_time
            )
    
    def _create_multilingual_prompt(self, query: str, analysis: Dict) -> str:
        """Create language-specific prompts for AI APIs"""
        
        # Language-specific instructions
        language_instructions = {
            "en": {
                "instruction": "Generate realistic sub-queries that Google's AI would create for this main query",
                "format": "Return JSON format with sub-queries, probabilities, facets, and reasoning",
                "context": "You are an expert SEO analyzing Google's query fan-out behavior"
            },
            "es": {
                "instruction": "Genera sub-consultas realistas que la IA de Google crearía para esta consulta principal",
                "format": "Devuelve formato JSON con sub-consultas, probabilidades, facetas y razonamiento",
                "context": "Eres un experto en SEO analizando el comportamiento de expansión de consultas de Google"
            },
            "fr": {
                "instruction": "Générez des sous-requêtes réalistes que l'IA de Google créerait pour cette requête principale",
                "format": "Retournez au format JSON avec sous-requêtes, probabilités, facettes et raisonnement",
                "context": "Vous êtes un expert SEO analysant le comportement d'expansion de requêtes de Google"
            },
            "de": {
                "instruction": "Generieren Sie realistische Unter-Abfragen, die Googles KI für diese Hauptabfrage erstellen würde",
                "format": "Geben Sie JSON-Format mit Unter-Abfragen, Wahrscheinlichkeiten, Facetten und Begründung zurück",
                "context": "Sie sind ein SEO-Experte, der Googles Query-Fan-Out-Verhalten analysiert"
            },
            "it": {
                "instruction": "Genera sotto-query realistiche che l'IA di Google creerebbe per questa query principale",
                "format": "Restituisci formato JSON con sotto-query, probabilità, faccette e ragionamento",
                "context": "Sei un esperto SEO che analizza il comportamento di espansione delle query di Google"
            }
        }
        
        lang_config = language_instructions.get(self.language, language_instructions["en"])
        
        prompt = f"""
{lang_config['context']}.

{lang_config['instruction']}: "{query}"

Query Analysis:
- Intent: {analysis.get('intent_type', 'unknown')}
- Category: {analysis.get('category', 'general')}
- Commercial Intent: {analysis.get('commercial_intent', 0.5):.0%}
- Language: {self.language}

Generate {self.max_predictions} realistic sub-queries that represent how Google's AI Mode would expand this query. Consider:

1. **Intent-based variations**: Based on user search intent
2. **Entity-specific queries**: Focusing on key entities in the original query
3. **Contextual extensions**: Industry/category-specific variations  
4. **Competitive analysis**: Market research variations
5. **User journey stages**: Different stages of user decision process

{lang_config['format']}:

{{
  "predictions": [
    {{
      "sub_query": "exact sub-query text in {self.language}",
      "probability": 0.85,
      "facet": "category name",
      "intent_type": "informational|transactional|navigational|commercial_investigation",
      "reasoning": "brief explanation why this sub-query would be generated"
    }}
  ],
  "analysis_summary": "brief summary of the fan-out strategy used"
}}

Important: Generate sub-queries in {self.language} language that are natural and realistic for {self.language}-speaking users.
"""
        
        return prompt
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO and query analysis specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _parse_ai_response(self, response: str, original_query: str) -> List[Dict]:
        """Parse AI response and extract predictions"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                predictions = parsed.get('predictions', [])
                
                # Validate and clean predictions
                cleaned_predictions = []
                for pred in predictions:
                    if self._is_valid_prediction(pred, original_query):
                        cleaned_predictions.append({
                            'sub_query': pred.get('sub_query', ''),
                            'probability': float(pred.get('probability', 0.5)),
                            'facet': pred.get('facet', 'AI Generated'),
                            'intent_type': pred.get('intent_type', 'mixed'),
                            'reasoning': pred.get('reasoning', 'AI generated prediction')
                        })
                
                return cleaned_predictions[:self.max_predictions]  # Limit based on settings
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._create_fallback_predictions(original_query)
    
    def _is_valid_prediction(self, prediction: Dict, original_query: str) -> bool:
        """Validate prediction quality"""
        sub_query = prediction.get('sub_query', '').strip()
        
        # Basic validation
        if not sub_query or len(sub_query) < 5:
            return False
        
        # Don't include exact duplicates of original query
        if sub_query.lower() == original_query.lower():
            return False
        
        # Check probability is reasonable
        prob = prediction.get('probability', 0)
        if not (0.1 <= prob <= 0.95):
            return False
        
        return True
    
    def _create_fallback_predictions(self, query: str) -> List[Dict]:
        """Create fallback predictions if AI fails"""
        
        # Language-specific fallback templates
        fallback_templates = {
            "en": [
                f"{query} reviews",
                f"{query} comparison", 
                f"best {query}",
                f"how to choose {query}",
                f"{query} guide"
            ],
            "es": [
                f"{query} reseñas",
                f"{query} comparación",
                f"mejor {query}",
                f"cómo elegir {query}",
                f"{query} guía"
            ],
            "fr": [
                f"{query} avis",
                f"{query} comparaison",
                f"meilleur {query}",
                f"comment choisir {query}",
                f"{query} guide"
            ],
            "de": [
                f"{query} bewertungen",
                f"{query} vergleich",
                f"bester {query}",
                f"wie man {query} wählt",
                f"{query} leitfaden"
            ],
            "it": [
                f"{query} recensioni",
                f"{query} confronto",
                f"migliore {query}",
                f"come scegliere {query}",
                f"{query} guida"
            ]
        }
        
        templates = fallback_templates.get(self.language, fallback_templates["en"])
        
        predictions = []
        for i, template in enumerate(templates):
            predictions.append({
                'sub_query': template,
                'probability': 0.7 - (i * 0.05),
                'facet': 'Fallback',
                'intent_type': 'mixed',
                'reasoning': f'Fallback prediction in {self.language}'
            })
        
        return predictions

    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            test_prompt = "Hello, this is a connection test. Please respond with 'OK'."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use cheaper model for testing
                messages=[{"role": "user", "content": test_prompt}],
                max_tokens=10
            )
            return "ok" in response.choices[0].message.content.lower()
                
        except Exception:
            return False

"""
Professional Fan-Out Prediction Engine
Advanced query analysis and sub-query generation with multilingual support
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
import random

@dataclass
class SubQueryPrediction:
    query: str
    probability: float
    facet: str
    intent_type: str
    reasoning: str

@dataclass
class QueryAnalysis:
    original_query: str
    entities: List[str]
    intent_type: str
    category: str
    commercial_intent: float
    query_complexity: str
    language: str

class ProfessionalFanOutEngine:
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.intent_patterns = self._load_intent_patterns()
        self.facet_templates = self._load_facet_templates()
        self.entity_types = self._load_entity_types()
        self.semantic_variations = self._load_semantic_variations()
    
    def set_language(self, language: str):
        """Set the language for analysis"""
        self.language = language
    
    def analyze_query(self, query: str) -> QueryAnalysis:
        """Comprehensive query analysis with language support"""
        query = query.lower().strip()
        
        # Extract entities
        entities = self._extract_entities(query)
        
        # Determine intent type
        intent_type = self._classify_intent(query)
        
        # Categorize query
        category = self._categorize_query(query, entities)
        
        # Calculate commercial intent
        commercial_intent = self._calculate_commercial_intent(query)
        
        # Assess complexity
        complexity = self._assess_complexity(query)
        
        return QueryAnalysis(
            original_query=query,
            entities=entities,
            intent_type=intent_type,
            category=category,
            commercial_intent=commercial_intent,
            query_complexity=complexity,
            language=self.language
        )
    
    def generate_fanout_predictions(self, query: str) -> List[SubQueryPrediction]:
        """Generate professional fan-out predictions"""
        analysis = self.analyze_query(query)
        predictions = []
        
        # Generate predictions based on analysis
        predictions.extend(self._generate_intent_based_predictions(analysis))
        predictions.extend(self._generate_entity_based_predictions(analysis))
        predictions.extend(self._generate_contextual_predictions(analysis))
        predictions.extend(self._generate_competitive_predictions(analysis))
        
        # Score and rank predictions
        scored_predictions = self._score_predictions(predictions, analysis)
        
        # Return top predictions
        return sorted(scored_predictions, key=lambda x: x.probability, reverse=True)[:8]
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract key entities from query"""
        entities = []
        
        # Product/brand patterns
        product_patterns = [
            r'\b(iphone|samsung|apple|google|microsoft|tesla|nike|adidas)\b',
            r'\b(macbook|laptop|smartphone|car|shoes|camera)\b',
            r'\b(\d{4})\b',  # Years
        ]
        
        for pattern in product_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            entities.extend(matches)
        
        # Extract potential product names (capitalized words)
        words = query.split()
        for word in words:
            if len(word) > 3 and not word.lower() in ['best', 'good', 'cheap', 'expensive']:
                entities.append(word)
        
        return list(set(entities))
    
    def _classify_intent(self, query: str) -> str:
        """Classify query intent with multilingual support"""
        
        intent_keywords = {
            "en": {
                "informational": ['what', 'how', 'why', 'when', 'where', 'definition', 'meaning', 'guide'],
                "transactional": ['buy', 'purchase', 'order', 'price', 'cost', 'cheap', 'deal', 'discount'],
                "navigational": ['website', 'login', 'official', 'homepage'],
                "commercial": ['best', 'top', 'review', 'comparison', 'vs', 'alternative']
            },
            "es": {
                "informational": ['qué', 'cómo', 'por qué', 'cuándo', 'dónde', 'definición', 'significado', 'guía'],
                "transactional": ['comprar', 'compra', 'pedir', 'precio', 'costo', 'barato', 'oferta', 'descuento'],
                "navigational": ['sitio web', 'página', 'oficial', 'inicio'],
                "commercial": ['mejor', 'mejores', 'reseña', 'comparación', 'vs', 'alternativa']
            },
            "fr": {
                "informational": ['quoi', 'comment', 'pourquoi', 'quand', 'où', 'définition', 'signification', 'guide'],
                "transactional": ['acheter', 'achat', 'commander', 'prix', 'coût', 'pas cher', 'offre', 'remise'],
                "navigational": ['site web', 'connexion', 'officiel', 'accueil'],
                "commercial": ['meilleur', 'top', 'avis', 'comparaison', 'vs', 'alternative']
            },
            "de": {
                "informational": ['was', 'wie', 'warum', 'wann', 'wo', 'definition', 'bedeutung', 'anleitung'],
                "transactional": ['kaufen', 'kauf', 'bestellen', 'preis', 'kosten', 'günstig', 'angebot', 'rabatt'],
                "navigational": ['website', 'anmeldung', 'offiziell', 'startseite'],
                "commercial": ['beste', 'top', 'bewertung', 'vergleich', 'vs', 'alternative']
            },
            "it": {
                "informational": ['cosa', 'come', 'perché', 'quando', 'dove', 'definizione', 'significato', 'guida'],
                "transactional": ['comprare', 'acquisto', 'ordinare', 'prezzo', 'costo', 'economico', 'offerta', 'sconto'],
                "navigational": ['sito web', 'login', 'ufficiale', 'homepage'],
                "commercial": ['migliore', 'top', 'recensione', 'confronto', 'vs', 'alternativa']
            }
        }
        
        lang_keywords = intent_keywords.get(self.language, intent_keywords["en"])
        
        for intent, keywords in lang_keywords.items():
            if any(kw in query for kw in keywords):
                if intent == "commercial":
                    return "commercial_investigation"
                return intent
        
        return 'mixed'
    
    def _categorize_query(self, query: str, entities: List[str]) -> str:
        """Categorize query by domain/industry with multilingual support"""
        
        category_keywords = {
            "en": {
                'technology': ['tech', 'software', 'app', 'computer', 'phone', 'laptop', 'ai', 'digital'],
                'ecommerce': ['buy', 'shop', 'store', 'product', 'brand', 'price'],
                'health': ['health', 'medical', 'doctor', 'treatment', 'symptoms', 'disease'],
                'education': ['learn', 'course', 'school', 'university', 'study', 'tutorial'],
                'travel': ['travel', 'hotel', 'flight', 'vacation', 'trip', 'destination'],
                'food': ['recipe', 'restaurant', 'food', 'cooking', 'meal', 'diet'],
                'finance': ['money', 'investment', 'bank', 'loan', 'insurance', 'financial']
            },
            "es": {
                'technology': ['tecnología', 'software', 'app', 'ordenador', 'teléfono', 'portátil', 'ia', 'digital'],
                'ecommerce': ['comprar', 'tienda', 'producto', 'marca', 'precio'],
                'health': ['salud', 'médico', 'doctor', 'tratamiento', 'síntomas', 'enfermedad'],
                'education': ['aprender', 'curso', 'escuela', 'universidad', 'estudiar', 'tutorial'],
                'travel': ['viajar', 'hotel', 'vuelo', 'vacaciones', 'viaje', 'destino'],
                'food': ['receta', 'restaurante', 'comida', 'cocinar', 'comida', 'dieta'],
                'finance': ['dinero', 'inversión', 'banco', 'préstamo', 'seguro', 'financiero']
            },
            "fr": {
                'technology': ['technologie', 'logiciel', 'app', 'ordinateur', 'téléphone', 'portable', 'ia', 'numérique'],
                'ecommerce': ['acheter', 'magasin', 'produit', 'marque', 'prix'],
                'health': ['santé', 'médical', 'docteur', 'traitement', 'symptômes', 'maladie'],
                'education': ['apprendre', 'cours', 'école', 'université', 'étudier', 'tutoriel'],
                'travel': ['voyager', 'hôtel', 'vol', 'vacances', 'voyage', 'destination'],
                'food': ['recette', 'restaurant', 'nourriture', 'cuisiner', 'repas', 'régime'],
                'finance': ['argent', 'investissement', 'banque', 'prêt', 'assurance', 'financier']
            },
            "de": {
                'technology': ['technologie', 'software', 'app', 'computer', 'telefon', 'laptop', 'ki', 'digital'],
                'ecommerce': ['kaufen', 'geschäft', 'produkt', 'marke', 'preis'],
                'health': ['gesundheit', 'medizinisch', 'arzt', 'behandlung', 'symptome', 'krankheit'],
                'education': ['lernen', 'kurs', 'schule', 'universität', 'studieren', 'tutorial'],
                'travel': ['reisen', 'hotel', 'flug', 'urlaub', 'reise', 'ziel'],
                'food': ['rezept', 'restaurant', 'essen', 'kochen', 'mahlzeit', 'diät'],
                'finance': ['geld', 'investition', 'bank', 'kredit', 'versicherung', 'finanziell']
            },
            "it": {
                'technology': ['tecnologia', 'software', 'app', 'computer', 'telefono', 'laptop', 'ia', 'digitale'],
                'ecommerce': ['comprare', 'negozio', 'prodotto', 'marca', 'prezzo'],
                'health': ['salute', 'medico', 'dottore', 'trattamento', 'sintomi', 'malattia'],
                'education': ['imparare', 'corso', 'scuola', 'università', 'studiare', 'tutorial'],
                'travel': ['viaggiare', 'hotel', 'volo', 'vacanze', 'viaggio', 'destinazione'],
                'food': ['ricetta', 'ristorante', 'cibo', 'cucinare', 'pasto', 'dieta'],
                'finance': ['denaro', 'investimento', 'banca', 'prestito', 'assicurazione', 'finanziario']
            }
        }
        
        lang_categories = category_keywords.get(self.language, category_keywords["en"])
        
        for category, keywords in lang_categories.items():
            if any(kw in query for kw in keywords):
                return category
        
        return 'general'
    
    def _calculate_commercial_intent(self, query: str) -> float:
        """Calculate commercial intent score (0-1)"""
        commercial_signals = [
            'buy', 'purchase', 'price', 'cost', 'cheap', 'expensive', 'deal', 'discount',
            'best', 'top', 'review', 'comparison', 'vs', 'alternative', 'recommend'
        ]
        
        score = sum(1 for signal in commercial_signals if signal in query)
        return min(score / 3, 1.0)  # Normalize to 0-1
    
    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity"""
        word_count = len(query.split())
        
        if word_count <= 2:
            return 'simple'
        elif word_count <= 4:
            return 'medium'
        else:
            return 'complex'
    
    def _generate_intent_based_predictions(self, analysis: QueryAnalysis) -> List[SubQueryPrediction]:
        """Generate predictions based on query intent"""
        predictions = []
        query = analysis.original_query
        
        if analysis.intent_type == 'commercial_investigation':
            templates = [
                f"{query} reviews",
                f"{query} pros and cons",
                f"{query} comparison",
                f"is {query} worth it",
                f"{query} alternatives",
                f"{query} vs competitors"
            ]
        elif analysis.intent_type == 'transactional':
            templates = [
                f"where to buy {query}",
                f"{query} discount",
                f"{query} free shipping",
                f"cheapest {query}",
                f"{query} coupon code"
            ]
        elif analysis.intent_type == 'informational':
            templates = [
                f"how to use {query}",
                f"{query} tutorial",
                f"{query} guide",
                f"what is {query}",
                f"{query} benefits"
            ]
        else:
            templates = [
                f"{query} information",
                f"{query} details",
                f"about {query}"
            ]
        
        for template in templates:
            predictions.append(SubQueryPrediction(
                query=template,
                probability=random.uniform(0.6, 0.9),
                facet="Intent-based",
                intent_type=analysis.intent_type,
                reasoning=f"Generated based on {analysis.intent_type} intent"
            ))
        
        return predictions
    
    def _generate_entity_based_predictions(self, analysis: QueryAnalysis) -> List[SubQueryPrediction]:
        """Generate predictions based on extracted entities"""
        predictions = []
        
        for entity in analysis.entities[:3]:  # Limit to top 3 entities
            if entity.isdigit():  # Year
                predictions.extend([
                    SubQueryPrediction(
                        query=f"best {analysis.original_query.replace(entity, '')} {entity}",
                        probability=random.uniform(0.7, 0.85),
                        facet="Temporal",
                        intent_type=analysis.intent_type,
                        reasoning=f"Year-specific variation for {entity}"
                    ),
                    SubQueryPrediction(
                        query=f"{analysis.original_query} {int(entity)+1} release date",
                        probability=random.uniform(0.5, 0.7),
                        facet="Future Planning",
                        intent_type="informational",
                        reasoning=f"Future version inquiry for {entity}"
                    )
                ])
            else:  # Product/brand entity
                predictions.extend([
                    SubQueryPrediction(
                        query=f"{entity} specifications",
                        probability=random.uniform(0.6, 0.8),
                        facet="Technical Details",
                        intent_type="informational",
                        reasoning=f"Technical specs for {entity}"
                    ),
                    SubQueryPrediction(
                        query=f"{entity} problems",
                        probability=random.uniform(0.5, 0.75),
                        facet="Issues & Support",
                        intent_type="informational",
                        reasoning=f"Common issues with {entity}"
                    )
                ])
        
        return predictions
    
    def _generate_contextual_predictions(self, analysis: QueryAnalysis) -> List[SubQueryPrediction]:
        """Generate context-aware predictions"""
        predictions = []
        
        category_templates = {
            'technology': [
                f"{analysis.original_query} setup",
                f"{analysis.original_query} compatibility",
                f"{analysis.original_query} security features",
                f"{analysis.original_query} updates"
            ],
            'ecommerce': [
                f"{analysis.original_query} warranty",
                f"{analysis.original_query} return policy",
                f"{analysis.original_query} customer service",
                f"{analysis.original_query} shipping time"
            ],
            'health': [
                f"{analysis.original_query} side effects",
                f"{analysis.original_query} dosage",
                f"{analysis.original_query} natural alternatives"
            ]
        }
        
        templates = category_templates.get(analysis.category, [
            f"{analysis.original_query} tips",
            f"{analysis.original_query} recommendations"
        ])
        
        for template in templates:
            predictions.append(SubQueryPrediction(
                query=template,
                probability=random.uniform(0.5, 0.8),
                facet=f"{analysis.category.title()} Context",
                intent_type=analysis.intent_type,
                reasoning=f"Context-specific for {analysis.category} category"
            ))
        
        return predictions
    
    def _generate_competitive_predictions(self, analysis: QueryAnalysis) -> List[SubQueryPrediction]:
        """Generate competitive analysis predictions"""
        predictions = []
        
        if analysis.commercial_intent > 0.5:
            competitive_templates = [
                f"{analysis.original_query} market share",
                f"{analysis.original_query} industry analysis",
                f"top competitors {analysis.original_query}",
                f"{analysis.original_query} market trends"
            ]
            
            for template in competitive_templates:
                predictions.append(SubQueryPrediction(
                    query=template,
                    probability=random.uniform(0.4, 0.7),
                    facet="Market Intelligence",
                    intent_type="commercial_investigation",
                    reasoning="Competitive analysis for commercial queries"
                ))
        
        return predictions
    
    def _score_predictions(self, predictions: List[SubQueryPrediction], analysis: QueryAnalysis) -> List[SubQueryPrediction]:
        """Score and adjust prediction probabilities"""
        for prediction in predictions:
            # Adjust based on query complexity
            if analysis.query_complexity == 'complex':
                prediction.probability *= 1.1
            elif analysis.query_complexity == 'simple':
                prediction.probability *= 0.9
            
            # Adjust based on commercial intent
            if 'price' in prediction.query or 'buy' in prediction.query:
                prediction.probability *= (0.5 + analysis.commercial_intent)
            
            # Ensure probability stays in valid range
            prediction.probability = min(max(prediction.probability, 0.1), 0.95)
        
        return predictions
    
    # Data loading methods (simplified for MVP)
    def _load_intent_patterns(self):
        return {}
    
    def _load_facet_templates(self):
        return {}
    
    def _load_entity_types(self):
        return {}
    
    def _load_semantic_variations(self):
        return {}

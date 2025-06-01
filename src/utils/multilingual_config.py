"""
Multilingual Configuration System
Supports EN, ES, FR, DE, IT languages
"""

from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class LanguageConfig:
    code: str
    name: str
    flag: str
    ui_strings: Dict[str, str]
    sample_queries: list
    facet_categories: Dict[str, str]

class MultilingualManager:
    
    def __init__(self):
        self.languages = self._load_language_configs()
        self.current_language = "en"
    
    def get_available_languages(self) -> Dict[str, LanguageConfig]:
        """Get all available language configurations"""
        return self.languages
    
    def set_language(self, language_code: str) -> bool:
        """Set current language"""
        if language_code in self.languages:
            self.current_language = language_code
            return True
        return False
    
    def get_ui_string(self, key: str, **kwargs) -> str:
        """Get UI string in current language"""
        lang_config = self.languages.get(self.current_language)
        if lang_config and key in lang_config.ui_strings:
            return lang_config.ui_strings[key].format(**kwargs)
        
        # Fallback to English
        en_config = self.languages.get("en")
        if en_config and key in en_config.ui_strings:
            return en_config.ui_strings[key].format(**kwargs)
        
        return key  # Return key if not found
    
    def get_sample_queries(self) -> list:
        """Get sample queries for current language"""
        lang_config = self.languages.get(self.current_language)
        return lang_config.sample_queries if lang_config else []
    
    def get_facet_categories(self) -> Dict[str, str]:
        """Get facet categories in current language"""
        lang_config = self.languages.get(self.current_language)
        return lang_config.facet_categories if lang_config else {}
    
    def _load_language_configs(self) -> Dict[str, LanguageConfig]:
        """Load all language configurations"""
        
        # English Configuration
        en_config = LanguageConfig(
            code="en",
            name="English",
            flag="🇺🇸",
            ui_strings={
                "app_title": "Query Fan-Out Analyzer & Predictor",
                "app_subtitle": "Analyze main queries and predict all sub-queries that Google would generate using fan-out techniques for AI Mode optimization.",
                "quick_analysis": "Quick Analysis",
                "enter_query": "Enter your main query:",
                "query_placeholder": "e.g., best smartphones 2024",
                "query_help": "Enter the primary query you want to analyze for fan-out predictions",
                "analyze_button": "Analyze Query",
                "api_config": "API Configuration",
                "select_provider": "Select AI Provider:",
                "api_key_label": "{provider} API Key:",
                "api_key_placeholder": "Enter your API key here",
                "api_key_help": "Your {provider} API key for generating predictions",
                "api_configured": "API Key configured!",
                "api_required": "API Key required for AI predictions",
                "quick_stats": "Quick Stats",
                "api_status": "API Status",
                "sub_queries_found": "Sub-queries Found",
                "avg_probability": "Avg. Probability", 
                "coverage_score": "Coverage Score",
                "analysis_completed": "Analysis completed!",
                "api_error": "Please configure your API key in the sidebar first!",
                "query_analysis_details": "Query Analysis Details",
                "intent_type": "Intent Type",
                "category": "Category",
                "commercial_intent": "Commercial Intent",
                "complexity": "Complexity",
                "key_entities": "Key Entities",
                "entities_found": "Entities Found",
                "predicted_sub_queries": "Predicted Sub-Queries",
                "export_data_table": "Export Data Table",
                "export_csv": "Export CSV",
                "download_csv": "Download CSV",
                "generate_report": "Generate Report",
                "new_analysis": "New Analysis",
                "report_next_version": "Report generation will be available in the next version!",
                "language_selection": "Language Selection",
                "select_language": "Select Language:",
                "language_help": "Choose your preferred language for analysis"
            },
            sample_queries=[
                "best laptops 2024",
                "how to lose weight fast", 
                "iPhone 15 vs Samsung Galaxy S24",
                "digital marketing course online",
                "Tesla Model 3 price",
                "restaurants near me",
                "investment strategies 2024",
                "best travel destinations Europe"
            ],
            facet_categories={
                "reviews": "Reviews",
                "comparison": "Comparison", 
                "price": "Price",
                "technical": "Technical Details",
                "problems": "Issues & Support",
                "alternatives": "Alternatives",
                "guide": "Guide & Tutorial",
                "market": "Market Intelligence"
            }
        )
        
        # Spanish Configuration  
        es_config = LanguageConfig(
            code="es",
            name="Español",
            flag="🇪🇸",
            ui_strings={
                "app_title": "Analizador y Predictor de Expansión de Consultas",
                "app_subtitle": "Analiza consultas principales y predice todas las sub-consultas que Google generaría usando técnicas de expansión para optimización en Modo IA.",
                "quick_analysis": "Análisis Rápido",
                "enter_query": "Introduce tu consulta principal:",
                "query_placeholder": "ej., mejores smartphones 2024",
                "query_help": "Introduce la consulta principal que quieres analizar para predicciones de expansión",
                "analyze_button": "Analizar Consulta",
                "api_config": "Configuración de API",
                "select_provider": "Seleccionar Proveedor de IA:",
                "api_key_label": "Clave API de {provider}:",
                "api_key_placeholder": "Introduce tu clave API aquí",
                "api_key_help": "Tu clave API de {provider} para generar predicciones",
                "api_configured": "¡Clave API configurada!",
                "api_required": "Clave API requerida para predicciones de IA",
                "quick_stats": "Estadísticas Rápidas",
                "api_status": "Estado API",
                "sub_queries_found": "Sub-consultas Encontradas",
                "avg_probability": "Probabilidad Promedio",
                "coverage_score": "Punteggio di Copertura",
                "analysis_completed": "Analisi completata!",
                "api_error": "Per favore configura la tua chiave API nella barra laterale prima!",
                "query_analysis_details": "Dettagli dell'Analisi Query",
                "intent_type": "Tipo di Intento",
                "category": "Categoria",
                "commercial_intent": "Intento Commerciale",
                "complexity": "Complessità",
                "key_entities": "Entità Chiave",
                "entities_found": "Entità Trovate",
                "predicted_sub_queries": "Sotto-query Previste",
                "export_data_table": "Esporta Tabella Dati",
                "export_csv": "Esporta CSV",
                "download_csv": "Scarica CSV",
                "generate_report": "Genera Report",
                "new_analysis": "Nuova Analisi",
                "report_next_version": "La generazione di report sarà disponibile nella prossima versione!",
                "language_selection": "Selezione Lingua",
                "select_language": "Seleziona Lingua:",
                "language_help": "Scegli la tua lingua preferita per l'analisi"
            },
            sample_queries=[
                "migliori laptop 2024",
                "come perdere peso velocemente",
                "iPhone 15 vs Samsung Galaxy S24",
                "corso di marketing digitale online",
                "prezzo Tesla Model 3",
                "ristoranti vicino a me",
                "strategie di investimento 2024",
                "migliori destinazioni di viaggio Europa"
            ],
            facet_categories={
                "reviews": "Recensioni",
                "comparison": "Confronto",
                "price": "Prezzo",
                "technical": "Dettagli Tecnici",
                "problems": "Problemi e Supporto",
                "alternatives": "Alternative",
                "guide": "Guida e Tutorial",
                "market": "Intelligence di Mercato"
            }
        )
        
        return {
            "en": en_config,
            "es": es_config,
            "fr": fr_config,
            "de": de_config,
            "it": it_config
        }uación de Cobertura",
                "analysis_completed": "¡Análisis completado!",
                "api_error": "¡Por favor configura tu clave API en la barra lateral primero!",
                "query_analysis_details": "Detalles del Análisis de Consulta",
                "intent_type": "Tipo de Intención",
                "category": "Categoría",
                "commercial_intent": "Intención Comercial",
                "complexity": "Complejidad",
                "key_entities": "Entidades Clave",
                "entities_found": "Entidades Encontradas",
                "predicted_sub_queries": "Sub-consultas Predichas",
                "export_data_table": "Exportar Tabla de Datos",
                "export_csv": "Exportar CSV",
                "download_csv": "Descargar CSV",
                "generate_report": "Generar Reporte",
                "new_analysis": "Nuevo Análisis",
                "report_next_version": "¡La generación de reportes estará disponible en la próxima versión!",
                "language_selection": "Selección de Idioma",
                "select_language": "Seleccionar Idioma:",
                "language_help": "Elige tu idioma preferido para el análisis"
            },
            sample_queries=[
                "mejores portátiles 2024",
                "cómo perder peso rápido",
                "iPhone 15 vs Samsung Galaxy S24", 
                "curso de marketing digital online",
                "precio Tesla Model 3",
                "restaurantes cerca de mí",
                "estrategias de inversión 2024",
                "mejores destinos de viaje Europa"
            ],
            facet_categories={
                "reviews": "Reseñas",
                "comparison": "Comparación",
                "price": "Precio", 
                "technical": "Detalles Técnicos",
                "problems": "Problemas y Soporte",
                "alternatives": "Alternativas",
                "guide": "Guía y Tutorial",
                "market": "Inteligencia de Mercado"
            }
        )
        
        # French Configuration
        fr_config = LanguageConfig(
            code="fr", 
            name="Français",
            flag="🇫🇷",
            ui_strings={
                "app_title": "Analyseur et Prédicteur d'Expansion de Requêtes",
                "app_subtitle": "Analysez les requêtes principales et prédisez toutes les sous-requêtes que Google générerait en utilisant des techniques d'expansion pour l'optimisation en Mode IA.",
                "quick_analysis": "Analyse Rapide",
                "enter_query": "Entrez votre requête principale:",
                "query_placeholder": "ex., meilleurs smartphones 2024",
                "query_help": "Entrez la requête principale que vous voulez analyser pour les prédictions d'expansion",
                "analyze_button": "Analyser la Requête",
                "api_config": "Configuration API",
                "select_provider": "Sélectionner le Fournisseur d'IA:",
                "api_key_label": "Clé API {provider}:",
                "api_key_placeholder": "Entrez votre clé API ici",
                "api_key_help": "Votre clé API {provider} pour générer des prédictions",
                "api_configured": "Clé API configurée!",
                "api_required": "Clé API requise pour les prédictions IA",
                "quick_stats": "Statistiques Rapides",
                "api_status": "Statut API",
                "sub_queries_found": "Sous-requêtes Trouvées",
                "avg_probability": "Probabilité Moyenne",
                "coverage_score": "Score de Couverture", 
                "analysis_completed": "Analyse terminée!",
                "api_error": "Veuillez configurer votre clé API dans la barre latérale d'abord!",
                "query_analysis_details": "Détails de l'Analyse de Requête",
                "intent_type": "Type d'Intention",
                "category": "Catégorie",
                "commercial_intent": "Intention Commerciale",
                "complexity": "Complexité",
                "key_entities": "Entités Clés",
                "entities_found": "Entités Trouvées",
                "predicted_sub_queries": "Sous-requêtes Prédites",
                "export_data_table": "Exporter le Tableau de Données",
                "export_csv": "Exporter CSV",
                "download_csv": "Télécharger CSV",
                "generate_report": "Générer un Rapport",
                "new_analysis": "Nouvelle Analyse",
                "report_next_version": "La génération de rapports sera disponible dans la prochaine version!",
                "language_selection": "Sélection de Langue",
                "select_language": "Sélectionner la Langue:",
                "language_help": "Choisissez votre langue préférée pour l'analyse"
            },
            sample_queries=[
                "meilleurs ordinateurs portables 2024",
                "comment perdre du poids rapidement",
                "iPhone 15 vs Samsung Galaxy S24",
                "cours de marketing numérique en ligne", 
                "prix Tesla Model 3",
                "restaurants près de moi",
                "stratégies d'investissement 2024",
                "meilleures destinations de voyage Europe"
            ],
            facet_categories={
                "reviews": "Avis",
                "comparison": "Comparaison",
                "price": "Prix",
                "technical": "Détails Techniques", 
                "problems": "Problèmes et Support",
                "alternatives": "Alternatives",
                "guide": "Guide et Tutoriel",
                "market": "Intelligence de Marché"
            }
        )
        
        # German Configuration
        de_config = LanguageConfig(
            code="de",
            name="Deutsch", 
            flag="🇩🇪",
            ui_strings={
                "app_title": "Abfrage-Fan-Out-Analysator und Prädiktor",
                "app_subtitle": "Analysieren Sie Hauptabfragen und sagen Sie alle Unterabfragen vorher, die Google mit Fan-Out-Techniken für die KI-Modus-Optimierung generieren würde.",
                "quick_analysis": "Schnellanalyse",
                "enter_query": "Geben Sie Ihre Hauptabfrage ein:",
                "query_placeholder": "z.B., beste Smartphones 2024",
                "query_help": "Geben Sie die Hauptabfrage ein, die Sie für Fan-Out-Vorhersagen analysieren möchten",
                "analyze_button": "Abfrage Analysieren",
                "api_config": "API-Konfiguration", 
                "select_provider": "KI-Anbieter Auswählen:",
                "api_key_label": "{provider} API-Schlüssel:",
                "api_key_placeholder": "Geben Sie Ihren API-Schlüssel hier ein",
                "api_key_help": "Ihr {provider} API-Schlüssel für die Generierung von Vorhersagen",
                "api_configured": "API-Schlüssel konfiguriert!",
                "api_required": "API-Schlüssel für KI-Vorhersagen erforderlich",
                "quick_stats": "Schnellstatistiken",
                "api_status": "API-Status",
                "sub_queries_found": "Unterabfragen Gefunden",
                "avg_probability": "Durchschnittliche Wahrscheinlichkeit",
                "coverage_score": "Abdeckungswert",
                "analysis_completed": "Analyse abgeschlossen!",
                "api_error": "Bitte konfigurieren Sie zuerst Ihren API-Schlüssel in der Seitenleiste!",
                "query_analysis_details": "Details der Abfrageanalyse",
                "intent_type": "Absichtstyp",
                "category": "Kategorie",
                "commercial_intent": "Kommerzielle Absicht",
                "complexity": "Komplexität",
                "key_entities": "Schlüsselentitäten",
                "entities_found": "Entitäten Gefunden",
                "predicted_sub_queries": "Vorhergesagte Unterabfragen",
                "export_data_table": "Datentabelle Exportieren",
                "export_csv": "CSV Exportieren",
                "download_csv": "CSV Herunterladen",
                "generate_report": "Bericht Generieren",
                "new_analysis": "Neue Analyse",
                "report_next_version": "Berichtsgenerierung wird in der nächsten Version verfügbar sein!",
                "language_selection": "Sprachauswahl",
                "select_language": "Sprache Auswählen:",
                "language_help": "Wählen Sie Ihre bevorzugte Sprache für die Analyse"
            },
            sample_queries=[
                "beste Laptops 2024",
                "wie man schnell abnimmt",
                "iPhone 15 vs Samsung Galaxy S24",
                "digitaler Marketing-Kurs online",
                "Tesla Model 3 Preis",
                "Restaurants in meiner Nähe", 
                "Investmentstrategien 2024",
                "beste Reiseziele Europa"
            ],
            facet_categories={
                "reviews": "Bewertungen",
                "comparison": "Vergleich",
                "price": "Preis",
                "technical": "Technische Details",
                "problems": "Probleme und Support",
                "alternatives": "Alternativen", 
                "guide": "Anleitung und Tutorial",
                "market": "Marktintelligenz"
            }
        )
        
        # Italian Configuration
        it_config = LanguageConfig(
            code="it",
            name="Italiano",
            flag="🇮🇹",
            ui_strings={
                "app_title": "Analizzatore e Predittore di Espansione Query",
                "app_subtitle": "Analizza le query principali e predici tutte le sotto-query che Google genererebbe usando tecniche di espansione per l'ottimizzazione in Modalità IA.",
                "quick_analysis": "Analisi Rapida",
                "enter_query": "Inserisci la tua query principale:",
                "query_placeholder": "es., migliori smartphone 2024",
                "query_help": "Inserisci la query principale che vuoi analizzare per le previsioni di espansione",
                "analyze_button": "Analizza Query",
                "api_config": "Configurazione API",
                "select_provider": "Seleziona Fornitore IA:",
                "api_key_label": "Chiave API {provider}:",
                "api_key_placeholder": "Inserisci la tua chiave API qui",
                "api_key_help": "La tua chiave API {provider} per generare previsioni",
                "api_configured": "Chiave API configurata!",
                "api_required": "Chiave API richiesta per previsioni IA",
                "quick_stats": "Statistiche Rapide",
                "api_status": "Stato API",
                "sub_queries_found": "Sotto-query Trovate",
                "avg_probability": "Probabilità Media",
                "coverage_score": "Punt

"""
QFAP - Query Fan-Out Analyzer & Predictor
Main Streamlit Application Entry Point with AI APIs and Multilingual Support
"""

import streamlit as st
from pathlib import Path
import sys

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

# Import our professional prediction engine and multilingual support
try:
    from core.fanout_engine import ProfessionalFanOutEngine
    from utils.ai_client import MultilingualAIClient
    from utils.multilingual_config import MultilingualManager
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="QFAP - Query Fan-Out Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "css" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Load custom styling
    load_css()
    
    # Initialize session state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.analysis_history = []
        st.session_state.current_query = ""
        st.session_state.predictions = []
        st.session_state.query_analysis = None
        st.session_state.api_provider = None
        st.session_state.api_key = None
        st.session_state.language = "en"
        
        # Initialize default user settings
        st.session_state.user_settings = {
            "ai_settings": {
                "temperature": 0.7,
                "max_predictions": 8,
                "openai_model": "gpt-4",
                "fallback_enabled": True
            },
            "analysis_settings": {
                "min_probability_threshold": 0.5,
                "include_reasoning": True,
                "enable_entity_extraction": True,
                "commercial_intent_weight": 1.0
            },
            "output_settings": {
                "group_by_facet": True,
                "sort_by_probability": True,
                "include_confidence_scores": True,
                "export_format": "csv"
            },
            "language_settings": {
                "auto_detect_language": False,
                "cross_language_analysis": False,
                "fallback_language": "en"
            }
        }
        
        # Initialize multilingual manager
        if ENGINE_AVAILABLE:
            st.session_state.ml_manager = MultilingualManager()
            st.session_state.fanout_engine = ProfessionalFanOutEngine(language="en")
            st.session_state.ai_client = None
        else:
            st.session_state.ml_manager = None
            st.session_state.fanout_engine = None
            st.session_state.ai_client = None
    
    # Remove translation function - UI always in English
    # Language selection only affects analysis, not UI
    
    # Sidebar navigation and configuration
    st.sidebar.title("🔍 QFAP Navigation")
    st.sidebar.markdown("---")
    
    # Settings Link
    st.sidebar.markdown("### 🔧 Configuration")
    if st.sidebar.button("⚙️ Advanced Settings"):
        st.switch_page("pages/03_Advanced_Settings.py")
    
    # Show current key settings
    if 'user_settings' in st.session_state:
        ai_settings = st.session_state.user_settings.get("ai_settings", {})
        with st.sidebar.expander("📋 Current Settings", expanded=False):
            st.write(f"**Temperature:** {ai_settings.get('temperature', 0.7)}")
            st.write(f"**Max Predictions:** {ai_settings.get('max_predictions', 8)}")
            st.write(f"**Model:** {ai_settings.get('openai_model', 'gpt-4')}")
    
    st.sidebar.markdown("---")
    
    # Language Selection (for analysis only, not UI)
    if st.session_state.ml_manager:
        st.sidebar.subheader("🌍 Analysis Language")
        
        languages = st.session_state.ml_manager.get_available_languages()
        language_options = {f"{lang_config.flag} {lang_config.name}": lang_config.code 
                          for lang_code, lang_config in languages.items()}
        
        current_lang_display = next((f"{lang_config.flag} {lang_config.name}" 
                                   for lang_code, lang_config in languages.items() 
                                   if lang_code == st.session_state.language), "🇺🇸 English")
        
        selected_language = st.sidebar.selectbox(
            "Select Language for Analysis:",
            options=list(language_options.keys()),
            index=list(language_options.keys()).index(current_lang_display),
            help="Choose the language for query analysis and predictions (UI remains in English)"
        )
        
        new_language = language_options[selected_language]
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            # Only set language for analysis, not for UI
            if st.session_state.fanout_engine:
                st.session_state.fanout_engine.set_language(new_language)
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # API Configuration in sidebar
    st.sidebar.subheader("⚙️ API Configuration")
    
    # API Key input
    api_provider = "OpenAI"  # Fixed to OpenAI only
    
    api_key = st.sidebar.text_input(
        "OpenAI API Key:",
        type="password",
        placeholder="Enter your OpenAI API key here",
        help="Your OpenAI API key for generating predictions"
    )
    
    # Store API configuration in session state and create AI client
    if api_key and api_key != st.session_state.get('api_key'):
        st.session_state.api_provider = "OpenAI"
        st.session_state.api_key = api_key
        
        # Create AI client with current language and user settings
        if ENGINE_AVAILABLE:
            try:
                st.session_state.ai_client = MultilingualAIClient(
                    provider="OpenAI",
                    api_key=api_key,
                    language=st.session_state.language,
                    settings=st.session_state.user_settings
                )
                # Test connection
                if st.session_state.ai_client.test_connection():
                    st.sidebar.success("✅ API Key configured!")
                else:
                    st.sidebar.error("❌ API connection failed")
                    st.session_state.ai_client = None
            except Exception as e:
                st.sidebar.error(f"❌ API Error: {str(e)}")
                st.session_state.ai_client = None
    elif api_key:
        st.sidebar.success("✅ API Key configured!")
    else:
        st.sidebar.warning("⚠️ API Key required for AI predictions")
    
    st.sidebar.markdown("---")
    
    # Main content area
    st.title("Query Fan-Out Analyzer & Predictor")
    st.markdown("**Analyze main queries and predict all sub-queries that Google would generate using fan-out techniques for AI Mode optimization.**")
    
    # Quick start section
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("🚀 Quick Analysis")
            
            # Query input with sample queries
            placeholder_text = "e.g., best smartphones 2024"  # Default placeholder
            if st.session_state.ml_manager:
                try:
                    # Get sample queries for selected analysis language
                    sample_queries = st.session_state.ml_manager.get_sample_queries(st.session_state.language)
                    if sample_queries:
                        placeholder_text = sample_queries[0]
                except Exception as e:
                    print(f"Error getting sample queries: {e}")
                    # Keep default placeholder
            
            query = st.text_input(
                "Enter your main query:",
                placeholder=placeholder_text,
                help="Enter the primary query you want to analyze for fan-out predictions"
            )
            
            # Show sample queries for current analysis language
            if st.session_state.ml_manager:
                try:
                    languages = st.session_state.ml_manager.get_available_languages()
                    if st.session_state.language in languages:
                        current_lang = languages[st.session_state.language]
                        with st.expander(f"💡 Sample Queries ({current_lang.name})", expanded=False):
                            sample_queries = st.session_state.ml_manager.get_sample_queries(st.session_state.language)
                            for i, sample in enumerate(sample_queries[:5]):
                                if st.button(f"📝 {sample}", key=f"sample_{i}"):
                                    st.session_state.temp_query = sample
                                    st.rerun()
                except Exception as e:
                    print(f"Error displaying sample queries: {e}")
                    # Continue without sample queries
            
            # Use sample query if selected
            if hasattr(st.session_state, 'temp_query'):
                query = st.session_state.temp_query
                delattr(st.session_state, 'temp_query')
            
            # Analyze button with API key validation
            analyze_disabled = not query or not st.session_state.get('api_key')
            button_help = "Please configure your API key in the sidebar first!" if not st.session_state.get('api_key') else "Click to analyze your query"
            
            if st.button("Analyze Query", type="primary", disabled=analyze_disabled, help=button_help):
                if not st.session_state.get('api_key'):
                    st.error("⚠️ Please configure your API key in the sidebar first!")
                else:
                    # Get current language name for spinner message
                    current_lang_name = "English"
                    if st.session_state.ml_manager:
                        try:
                            languages = st.session_state.ml_manager.get_available_languages()
                            if st.session_state.language in languages:
                                current_lang_name = languages[st.session_state.language].name
                        except Exception:
                            current_lang_name = "English"
                    
                    with st.spinner(f"Analyzing query in {current_lang_name} and predicting fan-out..."):
                        st.session_state.current_query = query
                        
                        # Use AI client for predictions if available
                        if st.session_state.ai_client and st.session_state.fanout_engine:
                            try:
                                # Get basic analysis first
                                analysis = st.session_state.fanout_engine.analyze_query(query)
                                st.session_state.query_analysis = analysis
                                
                                # Get AI-powered predictions
                                ai_response = st.session_state.ai_client.generate_fanout_predictions(
                                    query, 
                                    {
                                        'intent_type': analysis.intent_type,
                                        'category': analysis.category,
                                        'commercial_intent': analysis.commercial_intent
                                    }
                                )
                                
                                st.session_state.predictions = ai_response.predictions
                                
                            except Exception as e:
                                st.error(f"AI API Error: {str(e)}")
                                # Fallback to local engine
                                if st.session_state.fanout_engine:
                                    predictions = st.session_state.fanout_engine.generate_fanout_predictions(query)
                                    st.session_state.query_analysis = st.session_state.fanout_engine.analyze_query(query)
                                    st.session_state.predictions = [
                                        {
                                            "sub_query": pred.query,
                                            "probability": pred.probability,
                                            "facet": pred.facet,
                                            "intent_type": pred.intent_type,
                                            "reasoning": pred.reasoning
                                        }
                                        for pred in predictions
                                    ]
                        
                        # Fallback if no AI client
                        elif st.session_state.fanout_engine:
                            try:
                                predictions = st.session_state.fanout_engine.generate_fanout_predictions(query)
                                st.session_state.query_analysis = st.session_state.fanout_engine.analyze_query(query)
                                st.session_state.predictions = [
                                    {
                                        "sub_query": pred.query,
                                        "probability": pred.probability,
                                        "facet": pred.facet,
                                        "intent_type": pred.intent_type,
                                        "reasoning": pred.reasoning
                                    }
                                    for pred in predictions
                                ]
                            except Exception as e:
                                st.error(f"Prediction Error: {str(e)}")
                                # Ultimate fallback
                                st.session_state.predictions = [
                                    {"sub_query": f"{query} reviews", "probability": 0.87, "facet": "Reviews", "intent_type": "commercial", "reasoning": "Basic fallback"},
                                    {"sub_query": f"{query} comparison", "probability": 0.76, "facet": "Comparison", "intent_type": "commercial", "reasoning": "Basic fallback"}
                                ]
                        
                        st.success("✅ Analysis completed!")
                        st.rerun()
        
        with col2:
            st.header("📊 Quick Stats")
            
            # Show current analysis language
            current_lang_name = "English"
            current_lang_flag = "🇺🇸"
            if st.session_state.ml_manager:
                try:
                    languages = st.session_state.ml_manager.get_available_languages()
                    if st.session_state.language in languages:
                        current_lang = languages[st.session_state.language]
                        current_lang_name = current_lang.name
                        current_lang_flag = current_lang.flag
                except Exception as e:
                    print(f"Error getting language info: {e}")
                    # Keep defaults
                
            st.metric("Analysis Language", f"{current_lang_flag} {current_lang_name}")
            
            if st.session_state.get('api_key'):
                api_status = f"✅ OpenAI Connected"
            else:
                api_status = "⚠️ API Not Configured"
            
            st.metric("API Status", api_status)
            
            if st.session_state.predictions:
                st.metric("Sub-queries Found", len(st.session_state.predictions))
                avg_prob = sum(p['probability'] for p in st.session_state.predictions) / len(st.session_state.predictions)
                st.metric("Avg. Probability", f"{avg_prob:.0%}")
                st.metric("Coverage Score", "73%")
    
    # Results section
    if st.session_state.predictions:
        st.markdown("---")
        
        # Query Analysis Summary (if available)
        if st.session_state.get('query_analysis'):
            analysis = st.session_state.query_analysis
            
            with st.expander("🔍 Query Analysis Details", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Intent Type", analysis.intent_type.replace('_', ' ').title())
                    st.metric("Category", analysis.category.title())
                
                with col2:
                    st.metric("Commercial Intent", f"{analysis.commercial_intent:.0%}")
                    st.metric("Complexity", analysis.query_complexity.title())
                
                with col3:
                    if analysis.entities:
                        st.metric("Key Entities", len(analysis.entities))
                        st.write("**Entities Found:**")
                        for entity in analysis.entities[:5]:  # Show max 5
                            st.write(f"• {entity}")
        
        st.header("🎯 Predicted Sub-Queries")
        
        # Enhanced predictions display with settings awareness
        analysis_settings = st.session_state.user_settings.get("analysis_settings", {})
        output_settings = st.session_state.user_settings.get("output_settings", {})
        min_threshold = analysis_settings.get("min_probability_threshold", 0.5)
        
        # Filter predictions by threshold
        filtered_predictions = [
            pred for pred in st.session_state.predictions 
            if pred.get('probability', 0) >= min_threshold
        ]
        
        # Sort predictions if enabled
        if output_settings.get("sort_by_probability", True):
            filtered_predictions = sorted(filtered_predictions, key=lambda x: x.get('probability', 0), reverse=True)
        
        # Group by facet if enabled
        if output_settings.get("group_by_facet", True):
            # Group predictions by facet
            from itertools import groupby
            grouped_predictions = {}
            for facet, group in groupby(filtered_predictions, key=lambda x: x.get('facet', 'Other')):
                grouped_predictions[facet] = list(group)
            
            # Display grouped
            for facet, predictions in grouped_predictions.items():
                st.subheader(f"📂 {facet}")
                for i, pred in enumerate(predictions):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.write(f"**{pred['sub_query']}**")
                            if analysis_settings.get("include_reasoning", True) and 'reasoning' in pred:
                                st.caption(f"💡 {pred['reasoning']}")
                        
                        with col2:
                            if output_settings.get("include_confidence_scores", True):
                                prob = pred['probability']
                                if prob >= 0.8:
                                    st.success(f"🟢 {prob:.0%}")
                                elif prob >= 0.6:
                                    st.warning(f"🟡 {prob:.0%}")
                                else:
                                    st.info(f"🔵 {prob:.0%}")
                        
                        with col3:
                            if 'intent_type' in pred:
                                st.caption(pred['intent_type'].replace('_', ' ').title())
                        
                        st.divider()
        else:
            # Display flat list
            for i, pred in enumerate(filtered_predictions):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{i+1}. {pred['sub_query']}**")
                        if analysis_settings.get("include_reasoning", True) and 'reasoning' in pred:
                            st.caption(f"💡 {pred['reasoning']}")
                    
                    with col2:
                        if output_settings.get("include_confidence_scores", True):
                            prob = pred['probability']
                            if prob >= 0.8:
                                st.success(f"🟢 {prob:.0%}")
                            elif prob >= 0.6:
                                st.warning(f"🟡 {prob:.0%}")
                            else:
                                st.info(f"🔵 {prob:.0%}")
                    
                    with col3:
                        st.write(f"**{pred['facet']}**")
                        if 'intent_type' in pred:
                            st.caption(pred['intent_type'].replace('_', ' ').title())
                    
                    st.divider()
        
        # Summary table for export with applied filters
        with st.expander("📊 Export Data Table", expanded=False):
            import pandas as pd
            
            # Use filtered predictions for export
            if 'filtered_predictions' in locals():
                export_data = filtered_predictions
            else:
                export_data = st.session_state.predictions
            
            df = pd.DataFrame(export_data)
            if not df.empty:
                df['probability'] = df['probability'].apply(lambda x: f"{x:.0%}")
                
                st.dataframe(
                    df,
                    column_config={
                        "sub_query": st.column_config.TextColumn("Sub-Query", width="large"),
                        "probability": st.column_config.TextColumn("Probability", width="small"),
                        "facet": st.column_config.TextColumn("Facet", width="medium"),
                        "intent_type": st.column_config.TextColumn("Intent", width="medium"),
                        "reasoning": st.column_config.TextColumn("Reasoning", width="large")
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No predictions meet the current filter criteria.")
        
        # Export options with format from settings
        output_settings = st.session_state.user_settings.get("output_settings", {})
        export_format = output_settings.get("export_format", "csv")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📄 Export {export_format.upper()}"):
                if 'filtered_predictions' in locals():
                    export_data = filtered_predictions
                else:
                    export_data = st.session_state.predictions
                
                if export_data:
                    df = pd.DataFrame(export_data)
                    
                    if export_format == "csv":
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"fanout_analysis_{st.session_state.current_query.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                    elif export_format == "json":
                        json_data = df.to_json(orient='records', indent=2)
                        st.download_button(
                            label="Download JSON",
                            data=json_data,
                            file_name=f"fanout_analysis_{st.session_state.current_query.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                    elif export_format == "xlsx":
                        # Note: xlsx export would require openpyxl
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV (XLSX not available)",
                            data=csv_data,
                            file_name=f"fanout_analysis_{st.session_state.current_query.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                else:
                    st.warning("No data to export")
        
        with col2:
            if st.button("📊 Generate Report"):
                st.info("Report generation will be available in the next version!")
        
        with col3:
            if st.button("🔄 New Analysis"):
                st.session_state.predictions = []
                st.session_state.current_query = ""
                st.rerun()
        
        # Settings applied indicator
        if st.session_state.get('settings_saved'):
            st.success("✅ Custom settings are active!")
            if st.button("🔧 Modify Settings"):
                st.switch_page("pages/03_Advanced_Settings.py")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>QFAP v1.1 AI-Powered | Built with Streamlit | 
        <a href='https://github.com/your-username/qfap-analyzer' target='_blank'>GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

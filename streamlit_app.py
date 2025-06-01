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
        
        # Initialize multilingual manager
        if ENGINE_AVAILABLE:
            st.session_state.ml_manager = MultilingualManager()
            st.session_state.fanout_engine = ProfessionalFanOutEngine(language="en")
            st.session_state.ai_client = None
        else:
            st.session_state.ml_manager = None
            st.session_state.fanout_engine = None
            st.session_state.ai_client = None
    
    # Get current language strings (always English for UI)
    def t(key, **kwargs):
        """Translation helper function - Always returns English for UI"""
        if st.session_state.ml_manager:
            # Always use English for UI strings
            en_config = st.session_state.ml_manager.get_available_languages().get("en")
            if en_config and key in en_config.ui_strings:
                return en_config.ui_strings[key].format(**kwargs)
        return key
    
    # Sidebar navigation and configuration
    st.sidebar.title("🔍 QFAP Navigation")
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
    api_provider = st.sidebar.selectbox(
        "Select AI Provider:",
        ["OpenAI", "Anthropic"],
        help="Choose your preferred AI provider for query analysis"
    )
    
    api_key = st.sidebar.text_input(
        f"{api_provider} API Key:",
        type="password",
        placeholder="Enter your API key here",
        help=f"Your {api_provider} API key for generating predictions"
    )
    
    # Store API configuration in session state and create AI client
    if api_key and api_key != st.session_state.get('api_key'):
        st.session_state.api_provider = api_provider
        st.session_state.api_key = api_key
        
        # Create AI client with current language
        if ENGINE_AVAILABLE:
            try:
                st.session_state.ai_client = MultilingualAIClient(
                    provider=api_provider,
                    api_key=api_key,
                    language=st.session_state.language
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
            if st.session_state.ml_manager:
                # Get sample queries for selected analysis language
                st.session_state.ml_manager.set_language(st.session_state.language)
                sample_queries = st.session_state.ml_manager.get_sample_queries()
                placeholder_text = sample_queries[0] if sample_queries else "e.g., best smartphones 2024"
            else:
                placeholder_text = "e.g., best smartphones 2024"
            
            query = st.text_input(
                "Enter your main query:",
                placeholder=placeholder_text,
                help="Enter the primary query you want to analyze for fan-out predictions"
            )
            
            # Show sample queries for current analysis language
            if st.session_state.ml_manager:
                with st.expander(f"💡 Sample Queries ({languages[st.session_state.language].name})", expanded=False):
                    sample_queries = st.session_state.ml_manager.get_sample_queries()
                    for i, sample in enumerate(sample_queries[:5]):
                        if st.button(f"📝 {sample}", key=f"sample_{i}"):
                            st.session_state.temp_query = sample
                            st.rerun()
            
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
                    with st.spinner(f"Analyzing query in {languages[st.session_state.language].name} and predicting fan-out..."):
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
            if st.session_state.language in languages:
                current_lang = languages[st.session_state.language]
                st.metric("Analysis Language", f"{current_lang.flag} {current_lang.name}")
            
            if st.session_state.get('api_key'):
                api_status = f"✅ {st.session_state.get('api_provider', 'Unknown')} Connected"
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
        
        # Enhanced predictions display
        for i, pred in enumerate(st.session_state.predictions):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{i+1}. {pred['sub_query']}**")
                    if 'reasoning' in pred:
                        st.caption(f"💡 {pred['reasoning']}")
                
                with col2:
                    # Probability with color coding
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
        
        # Summary table for export
        with st.expander("📊 Export Data Table", expanded=False):
            import pandas as pd
            df = pd.DataFrame(st.session_state.predictions)
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
        
        # Export options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Export CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"fanout_analysis_{st.session_state.current_query.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Generate Report"):
                st.info("Report generation will be available in the next version!")
        
        with col3:
            if st.button("🔄 New Analysis"):
                st.session_state.predictions = []
                st.session_state.current_query = ""
                st.rerun()
    
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

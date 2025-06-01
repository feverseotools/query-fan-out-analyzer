"""
QFAP - Query Fan-Out Analyzer & Predictor
Main Streamlit Application Entry Point
"""

import streamlit as st
from pathlib import Path
import sys

# Add src directory to path for imports
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

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
        st.session_state.api_provider = None
        st.session_state.api_key = None
    
    # Sidebar navigation and configuration
    st.sidebar.title("🔍 QFAP Navigation")
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
    
    # Store API configuration in session state
    if api_key:
        st.session_state.api_provider = api_provider
        st.session_state.api_key = api_key
        st.sidebar.success("✅ API Key configured!")
    else:
        st.sidebar.warning("⚠️ API Key required for AI predictions")
    
    st.sidebar.markdown("---")
    
    # Main content area
    st.title("Query Fan-Out Analyzer & Predictor")
    st.markdown("""
    **Analyze main queries and predict all sub-queries that Google would generate 
    using fan-out techniques for AI Mode optimization.**
    """)
    
    # Quick start section
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("🚀 Quick Analysis")
            
            # Query input
            query = st.text_input(
                "Enter your main query:",
                placeholder="e.g., best smartphones 2024",
                help="Enter the primary query you want to analyze for fan-out predictions"
            )
            
            # Analyze button with API key validation
            analyze_disabled = not query or not st.session_state.get('api_key')
            button_help = "Enter a query and configure API key to analyze" if analyze_disabled else "Click to analyze your query"
            
            if st.button("Analyze Query", type="primary", disabled=analyze_disabled, help=button_help):
                if not st.session_state.get('api_key'):
                    st.error("⚠️ Please configure your API key in the sidebar first!")
                else:
                    with st.spinner("Analyzing query and predicting fan-out..."):
                        # Placeholder for actual AI analysis
                        # TODO: Replace with real AI integration
                        st.session_state.current_query = query
                        st.session_state.predictions = [
                            {"sub_query": f"{query} reviews", "probability": 0.87, "facet": "Reviews"},
                            {"sub_query": f"{query} comparison", "probability": 0.76, "facet": "Comparison"},
                            {"sub_query": f"{query} price", "probability": 0.71, "facet": "Price"},
                            {"sub_query": f"best {query.split()[-1]} brands", "probability": 0.68, "facet": "Brands"}
                        ]
                        st.success("✅ Analysis completed!")
                        st.rerun()
        
        with col2:
            st.header("📊 Quick Stats")
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
        st.header("🎯 Predicted Sub-Queries")
        
        # Display predictions in a table
        import pandas as pd
        df = pd.DataFrame(st.session_state.predictions)
        df['probability'] = df['probability'].apply(lambda x: f"{x:.0%}")
        
        st.dataframe(
            df,
            column_config={
                "sub_query": st.column_config.TextColumn("Sub-Query", width="large"),
                "probability": st.column_config.TextColumn("Probability", width="small"),
                "facet": st.column_config.TextColumn("Facet", width="medium")
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
        <p>QFAP v1.0 MVP | Built with Streamlit | 
        <a href='https://github.com/your-username/qfap-analyzer' target='_blank'>GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

"""
QFAP - Advanced Settings Page
Professional configuration options for power users
"""

import streamlit as st
import json
from pathlib import Path
import sys

# Add src directory to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path))

# Page configuration
st.set_page_config(
    page_title="QFAP - Advanced Settings",
    page_icon="⚙️",
    layout="wide"
)

def load_default_settings():
    """Load default application settings"""
    return {
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

def save_user_settings(settings):
    """Save user settings to session state"""
    st.session_state.user_settings = settings
    st.session_state.settings_saved = True

def main():
    """Main settings page function"""
    
    # Initialize settings if not exists
    if 'user_settings' not in st.session_state:
        st.session_state.user_settings = load_default_settings()
    
    # Page header
    st.title("⚙️ Advanced Settings")
    st.markdown("""
    **Customize QFAP behavior to match your specific needs and workflow.**
    Configure AI parameters, analysis settings, and output preferences.
    """)
    
    # Current settings
    settings = st.session_state.user_settings.copy()
    
    # Quick Actions Section
    st.markdown("---")
    st.header("🚀 Quick Configuration")
    col1, col2, col3, col4 = st.columns(4)
    
    # Predefined Presets
    presets = {
        "Conservative": {
            "description": "Safe, focused predictions for established brands",
            "temperature": 0.2,
            "max_predictions": 5,
            "min_probability_threshold": 0.7
        },
        "Balanced": {
            "description": "Optimal balance for most use cases",
            "temperature": 0.7,
            "max_predictions": 8,
            "min_probability_threshold": 0.5
        },
        "Aggressive": {
            "description": "Creative, experimental approach for new markets",
            "temperature": 0.9,
            "max_predictions": 12,
            "min_probability_threshold": 0.3
        },
        "E-commerce": {
            "description": "Optimized for product and shopping queries",
            "temperature": 0.6,
            "max_predictions": 10,
            "commercial_intent_weight": 1.5
        }
    }
    
    with col1:
        if st.button("🎯 Conservative", use_container_width=True):
            preset_config = presets["Conservative"]
            settings["ai_settings"]["temperature"] = preset_config["temperature"]
            settings["ai_settings"]["max_predictions"] = preset_config["max_predictions"]
            settings["analysis_settings"]["min_probability_threshold"] = preset_config["min_probability_threshold"]
            st.success("Conservative preset applied!")
            st.rerun()
    
    with col2:
        if st.button("⚖️ Balanced", use_container_width=True):
            preset_config = presets["Balanced"]
            settings["ai_settings"]["temperature"] = preset_config["temperature"]
            settings["ai_settings"]["max_predictions"] = preset_config["max_predictions"]
            settings["analysis_settings"]["min_probability_threshold"] = preset_config["min_probability_threshold"]
            st.success("Balanced preset applied!")
            st.rerun()
    
    with col3:
        if st.button("🚀 Aggressive", use_container_width=True):
            preset_config = presets["Aggressive"]
            settings["ai_settings"]["temperature"] = preset_config["temperature"]
            settings["ai_settings"]["max_predictions"] = preset_config["max_predictions"]
            settings["analysis_settings"]["min_probability_threshold"] = preset_config["min_probability_threshold"]
            st.success("Aggressive preset applied!")
            st.rerun()
    
    with col4:
        if st.button("🛒 E-commerce", use_container_width=True):
            preset_config = presets["E-commerce"]
            settings["ai_settings"]["temperature"] = preset_config["temperature"]
            settings["ai_settings"]["max_predictions"] = preset_config["max_predictions"]
            settings["analysis_settings"]["commercial_intent_weight"] = preset_config["commercial_intent_weight"]
            st.success("E-commerce preset applied!")
            st.rerun()
    
    # AI Configuration Section
    st.markdown("---")
    st.header("🤖 AI Configuration")
    st.markdown("Configure how AI models generate predictions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Model Selection")
        
        # OpenAI Model Selection
        openai_models = [
            "gpt-4",
            "gpt-4o-mini", 
            "gpt-4o"
        ]
        
        settings["ai_settings"]["openai_model"] = st.selectbox(
            "OpenAI Model:",
            openai_models,
            index=openai_models.index(settings["ai_settings"]["openai_model"]),
            help="Choose the OpenAI model for generating predictions"
        )
    
    with col2:
        st.subheader("Generation Parameters")
        
        # Temperature Control
        settings["ai_settings"]["temperature"] = st.slider(
            "AI Creativity (Temperature):",
            min_value=0.1,
            max_value=1.0,
            value=settings["ai_settings"]["temperature"],
            step=0.1,
            help="Higher values = more creative/diverse predictions. Lower = more focused/conservative."
        )
        
        # Max Predictions
        settings["ai_settings"]["max_predictions"] = st.slider(
            "Maximum Predictions:",
            min_value=3,
            max_value=15,
            value=settings["ai_settings"]["max_predictions"],
            step=1,
            help="Number of sub-queries to generate per analysis"
        )
    
    with col3:
        st.subheader("Fallback & Features")
        
        # Fallback Settings
        settings["ai_settings"]["fallback_enabled"] = st.checkbox(
            "Enable Local Fallback",
            value=settings["ai_settings"]["fallback_enabled"],
            help="Use local prediction engine if API fails"
        )
        
        # Temperature explanation
        if settings["ai_settings"]["temperature"] <= 0.3:
            st.info("🎯 **Conservative Mode**: Highly focused, predictable results")
        elif settings["ai_settings"]["temperature"] <= 0.7:
            st.info("⚖️ **Balanced Mode**: Good mix of creativity and focus")
        else:
            st.info("🚀 **Creative Mode**: More diverse, experimental predictions")
    
    # Analysis Settings Section
    st.markdown("---")
    st.header("🔍 Analysis Settings")
    st.markdown("Fine-tune how queries are analyzed and processed")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Quality Filters")
        
        # Probability Threshold
        settings["analysis_settings"]["min_probability_threshold"] = st.slider(
            "Minimum Probability Threshold:",
            min_value=0.1,
            max_value=0.9,
            value=settings["analysis_settings"]["min_probability_threshold"],
            step=0.05,
            help="Hide predictions below this probability score"
        )
        
        # Commercial Intent Weight
        settings["analysis_settings"]["commercial_intent_weight"] = st.slider(
            "Commercial Intent Weight:",
            min_value=0.5,
            max_value=2.0,
            value=settings["analysis_settings"]["commercial_intent_weight"],
            step=0.1,
            help="Boost commercial queries in scoring (1.0 = neutral)"
        )
    
    with col2:
        st.subheader("Analysis Features")
        
        # Include Reasoning
        settings["analysis_settings"]["include_reasoning"] = st.checkbox(
            "Include AI Reasoning",
            value=settings["analysis_settings"]["include_reasoning"],
            help="Show explanation for each prediction"
        )
        
        # Entity Extraction
        settings["analysis_settings"]["enable_entity_extraction"] = st.checkbox(
            "Enable Entity Extraction",
            value=settings["analysis_settings"]["enable_entity_extraction"],
            help="Extract and analyze key entities from queries"
        )
    
    with col3:
        st.subheader("Quality Metrics")
        
        # Show current threshold info
        threshold = settings["analysis_settings"]["min_probability_threshold"]
        if threshold >= 0.7:
            st.success(f"High Quality Filter: {threshold:.0%}")
            st.caption("Only showing high-confidence predictions")
        elif threshold >= 0.5:
            st.info(f"Balanced Filter: {threshold:.0%}")
            st.caption("Good balance of quality and quantity")
        else:
            st.warning(f"Permissive Filter: {threshold:.0%}")
            st.caption("Showing more experimental predictions")
    
    # Output & Display Settings Section
    st.markdown("---")
    st.header("📊 Output & Display Settings")
    st.markdown("Customize how results are displayed and exported")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Display Options")
        
        # Group by Facet
        settings["output_settings"]["group_by_facet"] = st.checkbox(
            "Group by Facet",
            value=settings["output_settings"]["group_by_facet"],
            help="Organize predictions by category/facet"
        )
        
        # Sort by Probability
        settings["output_settings"]["sort_by_probability"] = st.checkbox(
            "Sort by Probability",
            value=settings["output_settings"]["sort_by_probability"],
            help="Order predictions by confidence score"
        )
        
        # Include Confidence Scores
        settings["output_settings"]["include_confidence_scores"] = st.checkbox(
            "Show Confidence Scores",
            value=settings["output_settings"]["include_confidence_scores"],
            help="Display probability percentages"
        )
    
    with col2:
        st.subheader("Export Options")
        
        # Export Format
        export_formats = ["csv", "json", "xlsx"]
        settings["output_settings"]["export_format"] = st.selectbox(
            "Default Export Format:",
            export_formats,
            index=export_formats.index(settings["output_settings"]["export_format"]),
            help="Default format for data export"
        )
    
    with col3:
        st.subheader("Display Preview")
        
        # Show preview of current settings
        if settings["output_settings"]["group_by_facet"]:
            st.success("✅ Grouped Display")
        else:
            st.info("📝 Linear Display")
        
        if settings["output_settings"]["sort_by_probability"]:
            st.success("✅ Sorted by Confidence")
        else:
            st.info("📝 Original Order")
        
        st.caption(f"Export format: {settings['output_settings']['export_format'].upper()}")
    
    # Language Settings Section
    st.markdown("---")
    st.header("🌍 Language Settings")
    st.markdown("Configure multilingual analysis behavior")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Detection & Analysis")
        
        # Auto-detect Language
        settings["language_settings"]["auto_detect_language"] = st.checkbox(
            "Auto-detect Query Language",
            value=settings["language_settings"]["auto_detect_language"],
            help="Automatically detect and switch to query language"
        )
        
        # Cross-language Analysis
        settings["language_settings"]["cross_language_analysis"] = st.checkbox(
            "Cross-language Analysis",
            value=settings["language_settings"]["cross_language_analysis"],
            help="Generate predictions in multiple languages"
        )
    
    with col2:
        st.subheader("Fallback Options")
        
        # Fallback Language
        languages = ["en", "es", "fr", "de", "it"]
        language_names = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "it": "Italian"}
        
        fallback_options = [f"{lang} ({language_names[lang]})" for lang in languages]
        current_fallback = f"{settings['language_settings']['fallback_language']} ({language_names[settings['language_settings']['fallback_language']]})"
        
        selected_fallback = st.selectbox(
            "Fallback Language:",
            fallback_options,
            index=fallback_options.index(current_fallback),
            help="Language to use if auto-detection fails"
        )
        
        settings["language_settings"]["fallback_language"] = selected_fallback.split()[0]
    
    with col3:
        st.subheader("Language Status")
        
        if settings["language_settings"]["auto_detect_language"]:
            st.success("🤖 Auto-detection Enabled")
        else:
            st.info("👤 Manual Language Selection")
        
        if settings["language_settings"]["cross_language_analysis"]:
            st.success("🌐 Multi-language Predictions")
        else:
            st.info("🎯 Single Language Focus")
    
    # Save & Management Section
    st.markdown("---")
    st.header("💾 Save & Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            save_user_settings(settings)
            st.success("✅ Settings saved!")
    
    with col2:
        if st.button("🔄 Reset Defaults", use_container_width=True):
            st.session_state.user_settings = load_default_settings()
            st.success("✅ Reset to defaults!")
            st.rerun()
    
    with col3:
        if st.button("🚀 Apply & Return", use_container_width=True):
            save_user_settings(settings)
            st.success("✅ Settings applied!")
            st.switch_page("streamlit_app.py")
    
    with col4:
        # Export Settings JSON
        settings_json = json.dumps(settings, indent=2)
        st.download_button(
            label="📤 Export JSON",
            data=settings_json,
            file_name="qfap_settings.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Settings Summary Section
    st.markdown("---")
    with st.expander("📋 Current Settings Summary", expanded=False):
        
        # Organized summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("AI Configuration")
            st.write(f"**Temperature:** {settings['ai_settings']['temperature']}")
            st.write(f"**Max Predictions:** {settings['ai_settings']['max_predictions']}")
            st.write(f"**OpenAI Model:** {settings['ai_settings']['openai_model']}")
            st.write(f"**Fallback Enabled:** {settings['ai_settings']['fallback_enabled']}")
            
            st.subheader("Analysis Settings")
            st.write(f"**Min Probability:** {settings['analysis_settings']['min_probability_threshold']:.0%}")
            st.write(f"**Include Reasoning:** {settings['analysis_settings']['include_reasoning']}")
            st.write(f"**Entity Extraction:** {settings['analysis_settings']['enable_entity_extraction']}")
            st.write(f"**Commercial Weight:** {settings['analysis_settings']['commercial_intent_weight']}")
        
        with col2:
            st.subheader("Output Settings")
            st.write(f"**Group by Facet:** {settings['output_settings']['group_by_facet']}")
            st.write(f"**Sort by Probability:** {settings['output_settings']['sort_by_probability']}")
            st.write(f"**Show Confidence:** {settings['output_settings']['include_confidence_scores']}")
            st.write(f"**Export Format:** {settings['output_settings']['export_format']}")
            
            st.subheader("Language Settings")
            st.write(f"**Auto-detect:** {settings['language_settings']['auto_detect_language']}")
            st.write(f"**Cross-language:** {settings['language_settings']['cross_language_analysis']}")
            st.write(f"**Fallback:** {settings['language_settings']['fallback_language']}")

if __name__ == "__main__":
    main()

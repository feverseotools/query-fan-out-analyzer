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
            "anthropic_model": "claude-3-sonnet-20240229",
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
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🤖 AI Configuration",
        "🔍 Analysis Settings", 
        "📊 Output Settings",
        "🌍 Language Settings",
        "💾 Presets & Export"
    ])
    
    # Current settings
    settings = st.session_state.user_settings.copy()
    
    # Tab 1: AI Configuration
    with tab1:
        st.header("🤖 AI Configuration")
        st.markdown("Configure how AI models generate predictions")
        
        col1, col2 = st.columns(2)
        
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
            
            # Anthropic Model Selection
            anthropic_models = [
                "claude-3-sonnet-20240229",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240307"
            ]
            
            settings["ai_settings"]["anthropic_model"] = st.selectbox(
                "Anthropic Model:",
                anthropic_models,
                index=anthropic_models.index(settings["ai_settings"]["anthropic_model"]),
                help="Choose the Anthropic model for generating predictions"
            )
            
            # Fallback Settings
            settings["ai_settings"]["fallback_enabled"] = st.checkbox(
                "Enable Local Fallback",
                value=settings["ai_settings"]["fallback_enabled"],
                help="Use local prediction engine if API fails"
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
            
            # Temperature explanation
            if settings["ai_settings"]["temperature"] <= 0.3:
                st.info("🎯 **Conservative Mode**: Highly focused, predictable results")
            elif settings["ai_settings"]["temperature"] <= 0.7:
                st.info("⚖️ **Balanced Mode**: Good mix of creativity and focus")
            else:
                st.info("🚀 **Creative Mode**: More diverse, experimental predictions")
    
    # Tab 2: Analysis Settings
    with tab2:
        st.header("🔍 Analysis Settings")
        st.markdown("Fine-tune how queries are analyzed and processed")
        
        col1, col2 = st.columns(2)
        
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
    
    # Tab 3: Output Settings
    with tab3:
        st.header("📊 Output Settings")
        st.markdown("Customize how results are displayed and exported")
        
        col1, col2 = st.columns(2)
        
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
    
    # Tab 4: Language Settings
    with tab4:
        st.header("🌍 Language Settings")
        st.markdown("Configure multilingual analysis behavior")
        
        col1, col2 = st.columns(2)
        
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
    
    # Tab 5: Presets & Export
    with tab5:
        st.header("💾 Presets & Export")
        st.markdown("Save configurations and load predefined presets")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Configuration Presets")
            
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
            
            # Preset Selection
            preset_options = list(presets.keys())
            selected_preset = st.selectbox(
                "Load Preset:",
                ["Custom"] + preset_options,
                help="Load predefined configuration"
            )
            
            if selected_preset != "Custom":
                if st.button(f"Load {selected_preset} Preset"):
                    preset_config = presets[selected_preset]
                    
                    # Apply preset values
                    settings["ai_settings"]["temperature"] = preset_config.get("temperature", 0.7)
                    settings["ai_settings"]["max_predictions"] = preset_config.get("max_predictions", 8)
                    settings["analysis_settings"]["min_probability_threshold"] = preset_config.get("min_probability_threshold", 0.5)
                    
                    if "commercial_intent_weight" in preset_config:
                        settings["analysis_settings"]["commercial_intent_weight"] = preset_config["commercial_intent_weight"]
                    
                    st.success(f"✅ {selected_preset} preset loaded!")
                    st.rerun()
                
                # Show preset description
                if selected_preset in presets:
                    st.info(f"**{selected_preset}**: {presets[selected_preset]['description']}")
        
        with col2:
            st.subheader("Save & Export")
            
            # Save Settings
            if st.button("💾 Save Current Settings", type="primary"):
                save_user_settings(settings)
                st.success("✅ Settings saved successfully!")
            
            # Reset to Defaults
            if st.button("🔄 Reset to Defaults"):
                st.session_state.user_settings = load_default_settings()
                st.success("✅ Settings reset to defaults!")
                st.rerun()
            
            # Export Settings
            if st.button("📤 Export Settings JSON"):
                settings_json = json.dumps(settings, indent=2)
                st.download_button(
                    label="Download Settings",
                    data=settings_json,
                    file_name="qfap_settings.json",
                    mime="application/json"
                )
    
    # Apply Settings Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Apply Settings", type="primary", use_container_width=True):
            save_user_settings(settings)
            st.success("✅ Settings applied successfully! Go back to the main page to see changes.")
    
    # Settings Summary
    with st.expander("📋 Current Settings Summary", expanded=False):
        st.json(settings)

if __name__ == "__main__":
    main()

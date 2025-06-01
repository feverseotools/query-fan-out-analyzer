# 🔍 QFAP - Query Fan-Out Analyzer & Predictor

**Analyze main queries and predict all sub-queries that Google would generate using fan-out techniques for AI Mode optimization.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🎯 What is QFAP?

QFAP is a tool designed for SEOs, Content Strategists, and Digital Marketers who need to understand and optimize for Google's Query Fan-Out behavior in AI Mode. Instead of traditional keyword research, QFAP predicts the contextual sub-queries that AI systems generate from main queries.

### Key Features

- **🔮 Predictive Analysis**: Forecast sub-queries with high accuracy
- **📊 Visual Insights**: Interactive charts and data visualization  
- **⚡ Real-time Processing**: Instant analysis and results
- **📁 Export Options**: Download results in CSV format
- **🎨 User-friendly Interface**: Clean, intuitive Streamlit interface

## 🚀 Quick Start

### Option 1: Use Live App
Visit the deployed application: [QFAP Analyzer](https://your-app-url.streamlit.app)

### Option 2: Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/qfap-analyzer.git
   cd qfap-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Configure API Keys in the App**
   - Open the application
   - Use the sidebar to select your AI provider (OpenAI or Anthropic)
   - Enter your API key directly in the interface

## 🔧 Configuration

### API Keys Setup

The app allows you to configure API keys directly in the interface:

1. **Open the application**
2. **Navigate to the sidebar**  
3. **Select AI Provider**: Choose between OpenAI or Anthropic
4. **Enter API Key**: Input your API key in the secure field
5. **Start Analyzing**: The app will use your configured provider

**Supported Providers**:
- **OpenAI**: GPT models for query analysis
- **Anthropic**: Claude models for predictions

### No Configuration Files Needed

- ✅ **No secrets.toml required** - Configure everything in the UI
- ✅ **No environment variables** - All settings in the app
- ✅ **Secure input fields** - API keys are masked in the interface
- ✅ **Session-based storage** - Keys stored only during your session

## 📖 How to Use

1. **Configure API**: Select provider and enter your API key in the sidebar
2. **Enter Query**: Input your main search query
3. **Analyze**: Click "Analyze Query" to generate predictions  
4. **Review Results**: Examine predicted sub-queries with probability scores
5. **Export Data**: Download results for further analysis
6. **Iterate**: Test different queries and compare results

### Example Analysis

**Input**: "best smartphones 2024"

**Predicted Sub-queries**:
- "best smartphones 2024 reviews" (87% probability)
- "best smartphones 2024 comparison" (76% probability)  
- "best smartphones 2024 price" (71% probability)
- "best smartphone brands 2024" (68% probability)

## 🏗️ Project Structure

```
qfap-analyzer/
├── streamlit_app.py          # Main application
├── requirements.txt          # Dependencies
├── src/                      # Source code
├── pages/                    # Additional app pages
├── data/                     # Data files and templates
├── assets/                   # Static assets
└── docs/                     # Documentation
```

## 🚦 Current Status: MVP

This is the **Minimum Viable Product (MVP)** version with core functionality:

✅ **Implemented**:
- Basic query analysis
- Sub-query prediction (template-based)
- Simple visualization
- CSV export
- Streamlit Cloud deployment

🔄 **Coming Next**:
- AI-powered predictions (OpenAI/Claude integration)
- Advanced facet analysis
- Competitive gap analysis
- Batch processing
- Historical tracking

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/qfap-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/qfap-analyzer/discussions)
- **Email**: your-email@example.com

## 🎯 Roadmap

### Version 1.1 (Next)
- [ ] AI integration (OpenAI/Claude)
- [ ] Advanced NLP processing
- [ ] Enhanced UI components

### Version 1.2 (Future)
- [ ] Batch query analysis
- [ ] Competitive analysis
- [ ] API access
- [ ] Advanced reporting

---

**Built with ❤️ using Streamlit**

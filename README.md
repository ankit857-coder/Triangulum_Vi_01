# 🔮 Triangulum_Vi_01

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

An advanced AI research assistant powered by Google's Gemini model, designed to streamline academic research and information gathering across multiple domains.

## 🌟 Key Features

- **Multi-Source Research Integration**
  - Wikipedia for foundational knowledge
  - DuckDuckGo for real-time information
  - Google Scholar for academic papers
  - ArXiv for scientific publications
  - PubMed for medical research

- **Intelligent Query Processing**
  - Context-aware search routing
  - Automated source selection
  - Natural language understanding
  - Research synthesis

- **Advanced Research Tools**
  - Citation tracking
  - Paper summarization
  - Real-time data analysis
  - Cross-reference verification

## 📋 Prerequisites

- Python 3.9 or higher
- Google API key for Gemini model
- Internet connection

## 🚀 Quick Start

1. **Installation**
```bash
# Clone the repository
git clone https://github.com/ankit857-coder/Triangulum_Vi_01.git
cd Triangulum_Vi_01

# Install the package
pip install -e .
```

2. **Configuration**
```bash
# Create .env file
echo "Gemini_API=your_api_key_here" > .env
```

3. **Running the Assistant**
```bash
# Method 1: Using the CLI
triangulum

# Method 2: Running directly
python -m triangulum.main
```

## 💡 Usage Examples

```python
# Example queries:
"Compare the latest machine learning approaches in medical imaging"
"Find recent papers about quantum computing breakthroughs"
"What are the current developments in renewable energy?"
```

## 🛠️ Development Setup

1. **Install Development Dependencies**
```bash
pip install -r dev-requirements.txt
```

2. **Run Tests**
```bash
pytest tests/
```

3. **Code Quality**
```bash
# Format code
black triangulum/
isort triangulum/

# Type checking
mypy triangulum/
```

## 📚 Project Structure

```
triangulum/
├── __init__.py      # Package initialization
├── main.py          # Core application logic
├── tools_and_plugins.py  # Research tools implementation
└── requirements.txt  # Package dependencies
```

## 🔧 Research Tools

### 1. Wikipedia Tool
- General knowledge retrieval
- Historical information
- Conceptual explanations

### 2. DuckDuckGo Tool
- Real-time information
- Current events
- Market data

### 3. Google Scholar Tool
- Academic paper search
- Citation metrics
- Author tracking

### 4. ArXiv Tool
- Scientific preprints
- Latest research papers
- Cross-disciplinary search

### 5. PubMed Tool
- Medical research
- Clinical studies
- Biomedical literature

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 📝 Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions focused and modular
- Add unit tests for new features

## 🔄 Continuous Integration

- Automated testing on push
- Code quality checks
- Type checking validation
- Documentation generation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini for the language model
- LangChain for the agent framework
- Research databases and APIs
- Open source community

## 📞 Contact & Support

- Create an Issue for bugs
- Start a Discussion for questions
- Pull Requests welcome

## 🔮 Future Roadmap

- [ ] Enhanced query understanding
- [ ] PDF parsing and analysis
- [ ] Citation management system
- [ ] Research paper summarization
- [ ] Automated literature review
- [ ] Custom research agents
- [ ] Collaborative research features

---
Built with ❤️ by Triangulum_Vi_01
#!/bin/bash

echo "🚀 Telecom Sales Agent - Startup Options"
echo "========================================"
echo ""
echo "Available commands:"
echo "1. Run Tests:        ./start_demo.sh test"
echo "2. Run CLI Demo:     ./start_demo.sh demo"
echo "3. Start Web App:    ./start_demo.sh web"
echo "4. Show Help:        ./start_demo.sh help"
echo ""

# Activate virtual environment
source venv/bin/activate

case "$1" in
    "test")
        echo "🧪 Running all tests..."
        python3 test_agent.py
        ;;
    "demo")
        echo "🎯 Running CLI demo..."
        python3 example_usage.py
        ;;
    "web")
        echo "🌐 Starting Streamlit web app..."
        echo "Note: You'll need to set OPENAI_API_KEY for full functionality"
        streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
        ;;
    "help"|*)
        echo "Usage: $0 {test|demo|web|help}"
        echo ""
        echo "Commands:"
        echo "  test  - Run the test suite to verify everything works"
        echo "  demo  - Run a comprehensive CLI demonstration"
        echo "  web   - Start the Streamlit web interface"
        echo "  help  - Show this help message"
        echo ""
        echo "Requirements:"
        echo "- Set OPENAI_API_KEY environment variable for full LLM functionality"
        echo "- Virtual environment should be created: python3 -m venv venv"
        echo "- Dependencies installed: pip install -r requirements.txt"
        ;;
esac
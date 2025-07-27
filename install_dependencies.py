#!/usr/bin/env python3
"""
Install Dependencies - Handles version conflicts automatically
"""

import subprocess
import sys

def run_pip_install(packages):
    """Install packages using pip"""
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    return True

def main():
    print("🚀 Installing Telecom Sales Agent Dependencies")
    print("=" * 60)
    
    # Install in specific order to avoid conflicts
    core_packages = [
        "pip>=24.0",
        "pydantic>=2.7.0",
        "python-dotenv>=1.0.0"
    ]
    
    langchain_packages = [
        "langchain-core>=0.2.0",
        "langchain>=0.2.0",
        "langchain-openai>=0.1.8"
    ]
    
    langgraph_packages = [
        "langgraph>=0.1.0"
    ]
    
    other_packages = [
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "streamlit>=1.30.0"
    ]
    
    print("📦 Installing core packages...")
    if not run_pip_install(core_packages):
        return False
    
    print("\n📦 Installing LangChain packages...")
    if not run_pip_install(langchain_packages):
        return False
    
    print("\n📦 Installing LangGraph packages...")
    if not run_pip_install(langgraph_packages):
        return False
    
    print("\n📦 Installing other packages...")
    if not run_pip_install(other_packages):
        return False
    
    print("\n🎉 All dependencies installed successfully!")
    print("✅ Your Telecom Sales Agent is ready to use!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Some packages failed to install.")
        print("💡 Try running: pip install --upgrade pip")
        print("💡 Then run this script again.")
        sys.exit(1)
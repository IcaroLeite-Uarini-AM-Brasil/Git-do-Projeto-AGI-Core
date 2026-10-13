from setuptools import setup, find_packages

setup(
    name="agi_core",
    version="0.1.0",
    description="AGI Core - Modular Mega Framework (example)",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "torch>=2.0.0",
        "gymnasium>=0.28.1",
        "ray[default]>=2.5.0",
        "neo4j>=5.8.0",
        "streamlit>=1.22.0",
        "numpy>=1.24.0",
        "pyyaml>=6.0",
        "plotly>=5.14.0",
    ],
    python_requires=">=3.8",
)

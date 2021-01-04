from setuptools import setup, find_packages

setup(
    name="frex",
    version="0.4",
    description="Package for Explainable Recommender Framework.",
    url="git@github.com:solashirai/ExplainableRecommenderFramework.git",
    author="Sola S.D. Shirai",
    packages=find_packages(include=['frex', 'frex.*']),
    install_requires=[
        "dataclasses-json",
        "numpy",
        "pytest",
        "rdflib",
        "scipy",
        "sklearn",
        "SPARQLWrapper",
        "ortools",
    ]
)

from setuptools import setup

setup(
    name="frex",
    version="0.4",
    description="Package for Explainable Recommender Framework.",
    url="git@github.com:solashirai/ExplainableRecommenderFramework.git",
    author="Sola S.D. Shirai",
    packages=[
        "frex",
        "frex.models",
        "frex.pipelines",
        "frex.stores",
        "frex.utils",
        "frex.utils.constraints",
        "frex.pipeline_stages",
        "frex.pipeline_stages.candidate_generators",
        "frex.pipeline_stages.filters",
        "frex.pipeline_stages.scorers",
    ],
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

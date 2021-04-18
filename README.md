# FREx
FREx (the **F**ramework for **R**ecommendations with **Ex**planations) is a Python package to support the development of recommender systems that use rule-based or knowledge-based steps in the recommendation process. 

## Usage

FREx is developed for Python 3.8

You can use FREx by installing it via pip
```bash
$ pip install git+https://github.com/solashirai/FREx@master#egg=frex
```
Note that one of the requirements, [ortools](https://pypi.org/project/ortools/), might require you to be using a 64-bit installation of Python. If you see installation errors related to ortools, consider swapping to a 64-bit Python (if you were using 32-bit) or checking that your pip is upgraded.

You will now be able to use FREx in your project like any other Python package, with `import frex`.

## Additional Information

More documentation about the project is available [here](https://tetherless-world.github.io/FREx/).

The main classes and modules can be found in the frex/ directory. A toy example demonstrating the use of frex can be seen in the [examples/ramen_rec](https://github.com/solashirai/ExplainableRecommenderFramework/tree/master/examples/ramen_rec) directory.

Documentation generated using [Sphinx](https://www.sphinx-doc.org/en/master/) can be found at [https://solashirai.github.io/FREx](https://solashirai.github.io/FREx).

An example of running this toy example can be seen in the [jupyter notebook](https://github.com/solashirai/ExplainableRecommenderFramework/blob/master/examples/ramen_rec/example_run.ipynb).

Data source: https://www.kaggle.com/residentmario/ramen-ratings

This is a toy example using the explainable recommender framework to recommend ramen products.

To run the toy example, run a command of the following forms
- python -m examples.ramen_rec RAMEN \<ramen_uri\>
- python -m examples.ramen_rec EATER \<ramen_eater_uri\m>
where <uri> is either a ramen URI or a ramen eater (user) URI.

Ramen URIs are of the form http://www.frex.com/examples/ramen/1 . There is currently only one ramen eater in the data (http://www.frex.com/examples/USR01).

Calling examples.ramen_rec with the RAMEN argument will give recommendations for other ramens that are similar to the input ramen uri.

Calling examples.ramen_rec with the EATER argument will give ramen recommendations for the input ramen eater. 

The similarity and ranking metrics used in the toy example are fairly arbitrary. Since there is no real user data to apply, this toy example uses some very basic content-based filtering and ranking strategies. 

A jupyter notebook running this example can be seen in example_run.ipynb

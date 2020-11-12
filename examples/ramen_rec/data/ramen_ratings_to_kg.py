import rdflib
from rdflib.namespace import RDF, RDFS, XSD
import csv
import random


def convert():
    """
    One-off code to convert the ramen-raitings-csv file into RDF triples using very basic transformations.
    Don't look to this KG as an example of a good KG...
    """
    random.seed(
        1
    )  # seed random var, since we're just using random to tack on a fake 'price' to ramens.
    ramen_data = []
    with open("ramen-ratings.csv", "r", encoding="utf-8") as f:
        next(f)  # skip first line, header for CSV
        for line in f:
            # Review #,Brand,Variety,Style,Country,Stars,Top Ten
            ramen_content = line.strip().split(",")[:-1]
            if len(ramen_content) != 6:
                continue
            ramen_data.append(tuple(ramen_content))

    ramen_ns = rdflib.Namespace("http://www.frex.com/examples/ramen/")
    ramen_onto_ns = rdflib.Namespace("http://www.frex.com/examples/ramenOnto/")
    output_graph = rdflib.Graph()
    for ramen_content in ramen_data:
        output_graph.add(
            (ramen_ns[ramen_content[0]], RDF["type"], ramen_onto_ns["ramen"])
        )
        output_graph.add(
            (
                ramen_ns[ramen_content[0]],
                ramen_onto_ns["brand"],
                rdflib.Literal(ramen_content[1]),
            )
        )
        output_graph.add(
            (
                ramen_ns[ramen_content[0]],
                RDFS["label"],
                rdflib.Literal(ramen_content[2]),
            )
        )
        output_graph.add(
            (
                ramen_ns[ramen_content[0]],
                ramen_onto_ns["style"],
                rdflib.Literal(ramen_content[3]),
            )
        )
        output_graph.add(
            (
                ramen_ns[ramen_content[0]],
                ramen_onto_ns["country"],
                rdflib.Literal(ramen_content[4]),
            )
        )
        output_graph.add(
            (
                ramen_ns[ramen_content[0]],
                ramen_onto_ns[
                    "price"
                ],  # a random 'price' which will be used to demonstrate some constraints
                rdflib.Literal(round(random.uniform(0.5, 5.0), 2), datatype=XSD.float),
            )
        )
        if ramen_content[5] == "Unrated":
            # there's a few cases of unrated ramens, we'll just convert those to 2.5 for this toy example
            output_graph.add(
                (
                    ramen_ns[ramen_content[0]],
                    ramen_onto_ns["rating"],
                    rdflib.Literal(2.5, datatype=XSD.float),
                )
            )
        else:
            output_graph.add(
                (
                    ramen_ns[ramen_content[0]],
                    ramen_onto_ns["rating"],
                    rdflib.Literal(ramen_content[5], datatype=XSD.float),
                )
            )

    output_graph.serialize("ramen-ratings.ttl", format="ttl")


if __name__ == "__main__":
    convert()

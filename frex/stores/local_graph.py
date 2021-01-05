from rdflib import Graph
from rdflib.query import Result
from pathlib import Path
from typing import Tuple
from frex.stores import SparqlQueryable


class LocalGraph(SparqlQueryable):
    """
    LocalGraph should be used to store and access rdf graphs locally.
    """

    def __init__(self, *, file_paths: Tuple[Path, ...]):
        self.graph = Graph()
        for file_path in file_paths:
            self.load_graph_file(file_path=file_path)

    def load_graph_file(self, *, file_path: Path):
        """
        Load a piece of an RDF graph from a file.

        :param file_path: the path to the file containing the RDF graph to load.
        :return: None
        """
        self.__parse_ttl_file(file_path=file_path)

    def __parse_ttl_file(self, *, file_path: Path) -> None:

        return self.graph.parse(str(file_path), format="ttl")

    def query(self, *, sparql: str) -> Result:
        """
        Query the local graph object.

        :param sparql: A string containing valid SPARQL to query the graph.
        :return: A Result containing the result from calling the SPARQL query.
        """
        return self.graph.query(sparql)

    def get_graph(self) -> Graph:
        """
        Get the local Graph object.

        :return: The local Graph object
        """
        return self.graph

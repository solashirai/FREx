from rdflib import Graph
from rdflib.query import Result
from pathlib import Path
from typing import List
from frex.stores import SparqlQueryable


class LocalGraph(SparqlQueryable):

    def __init__(self, *, file_paths: List[Path]):
        self.graph = Graph()
        for file_path in file_paths:
            self.load_graph_file(file_path=file_path)

    def load_graph_file(self, *, file_path: Path):
        self.__parse_ttl_file(file_path=file_path)

    def __parse_ttl_file(self, *, file_path: Path) -> None:

        return self.graph.parse(str(file_path), format='ttl')

    def query(self, *, sparql: str) -> Result:
        return self.graph.query(sparql)

    def get_graph(self) -> Graph:
        return self.graph

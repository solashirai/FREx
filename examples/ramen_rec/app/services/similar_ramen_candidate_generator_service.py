from FREx.services.candidate_generator_service import CandidateGeneratorService
from typing import Tuple, FrozenSet, Dict
from rdflib import URIRef
from FREx.models import Explanation, Candidate
from examples.ramen_rec.app.models import RamenContext, RamenCandidate
from examples.ramen_rec.app.services import RamenQueryService
import pickle


class SimilarRamenCandidateGeneratorService(CandidateGeneratorService):

    def __init__(self, *, ramen_vector_file: str,
                 ramen_query_service: RamenQueryService):
        with open(ramen_vector_file, 'rb') as f:
            self.ramen_vector_dict: Dict[URIRef, FrozenSet] = pickle.load(f)
        self.ramen_query_service = ramen_query_service

    def get_candidates(self, *, context: RamenContext) -> Tuple[Candidate, ...]:
        ramen_sim_scores = dict()
        this_ramen_uri = context.target_ramen.uri
        this_ramen_content = self.ramen_vector_dict[this_ramen_uri]

        for other_ramen_uri in self.ramen_vector_dict.keys():
            if other_ramen_uri == this_ramen_uri:
                continue
            other_ramen_content = self.ramen_vector_dict[other_ramen_uri]
            # get jaccard index
            score = len(this_ramen_content.intersection(other_ramen_content)) / \
                    len(this_ramen_content.union(other_ramen_content))
            ramen_sim_scores[other_ramen_uri] = score

        sorted_uris = sorted(ramen_sim_scores.items(), key=lambda item: item[1], reverse=True)
        # for this system, we'll just say we return the top 50 ramens as candidates
        sorted_uris = [tup[0] for tup in sorted_uris[:50]]

        ramens = self.ramen_query_service.get_all_ramens_by_uri(ramen_uris=sorted_uris)
        return tuple(
            RamenCandidate(
                domain_object=ramen,
                applied_explanations=[
                    Explanation(explanation_string=f'This ramen is identified as being similar to the target ramen.')
                ],
                applied_scores=[0])
            for ramen in ramens)

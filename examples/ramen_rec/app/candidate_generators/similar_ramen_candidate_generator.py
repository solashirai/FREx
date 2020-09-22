from frex.pipeline_stages.candidate_generators import CandidateGenerator
from frex.utils import VectorSimilarityUtils
from typing import Dict, List, Generator, Optional
from rdflib import URIRef
from frex.models import Explanation, Candidate
from examples.ramen_rec.app.models import RamenContext, RamenCandidate
from examples.ramen_rec.app.services import GraphRamenQueryService
import numpy as np
import pickle
from pathlib import Path


class SimilarRamenCandidateGenerator(CandidateGenerator):
    def __init__(
        self, *, ramen_vector_file: Path, ramen_query_service: GraphRamenQueryService,
            **kwargs
    ):
        with open(str(ramen_vector_file), "rb") as f:
            self.ramen_vector_dict: Dict[URIRef, np.ndarray] = pickle.load(f)
        self.ramen_query_service = ramen_query_service

        CandidateGenerator.__init__(self, **kwargs)

    def __call__(
        self,
        *,
        candidates: Generator[Candidate, None, None] = None,
        context: RamenContext
    ) -> Generator[Candidate, None, None]:
        target_ramen_uri = context.target_ramen.uri
        target_ramen_vector = self.ramen_vector_dict[target_ramen_uri]

        comp_ramen_uris, comp_ramen_vectors = [], []
        for ram_uri, ram_vec in self.ramen_vector_dict.items():
            if ram_uri != target_ramen_uri:
                comp_ramen_uris.append(ram_uri)
                comp_ramen_vectors.append(ram_vec)

        ramen_sim_scores = VectorSimilarityUtils.get_item_vector_similarity(
            target_item=target_ramen_uri,
            target_vector=target_ramen_vector,
            comparison_items=comp_ramen_uris,
            comparison_contents=comp_ramen_vectors,
        )

        # for this system, we'll just say we return the top 50 ramens as candidates
        sorted_uris = VectorSimilarityUtils.get_top_n_candidates(
            candidate_score_dict=ramen_sim_scores, top_n=50
        )
        sorted_uris = [tup[0] for tup in sorted_uris]

        ramens = self.ramen_query_service.get_ramens_by_uri(ramen_uris=sorted_uris)
        for ramen in ramens:
            yield RamenCandidate(
                context=context,
                domain_object=ramen,
                applied_explanations=[
                    self.generator_explanation
                ],
                applied_scores=[0],
            )

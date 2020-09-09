from abc import abstractmethod
from frex.models.context import Context
from typing import Tuple, Any, List, Generator
from frex.models import Candidate, DomainObject
from frex.pipeline_stages import _Pipeline
import numpy as np
from scipy.sparse import csr_matrix, lil_matrix


class CandidateGenerator(_Pipeline):

    @staticmethod
    def sparse_l2_norm(mat: csr_matrix):
        return np.sqrt(np.sum(mat.multiply(mat), axis=1))

    @staticmethod
    def cosine_sim(*, comparison_vector: np.array, comparison_matrix: np.array) -> np.array:
        if isinstance(comparison_vector, csr_matrix):
            # sparse matrices seem to be very slow or require a ton of memory to call np.linalg.norm, so
            # compute using csr_matrix functions here.
            return comparison_vector.dot(comparison_matrix.T) / \
                   (CandidateGenerator.sparse_l2_norm(comparison_vector).dot(
                       CandidateGenerator.sparse_l2_norm(comparison_matrix).T))
        else:
            return np.dot(comparison_vector, comparison_matrix.T) / \
                   (np.linalg.norm(comparison_vector) * np.linalg.norm(comparison_matrix, axis=1).T)

    @staticmethod
    def get_item_vector_similarity(*, target_item: Any,
                                   target_vector: np.array,
                                   comparison_items: List[Any],
                                   comparison_contents: List[np.array]) -> List[Tuple[Any, float]]:
        """
        Convert a tuple of comparison_items and their corresponding vectors into a matrix and return a list of
        items and scores.
        The shape of item content vectors is expected to be (1, N) for each item.
        The target item and its vector should not be contained in comparison_items or comparison_contents.
        """
        ind_to_item = dict()
        content_matrix = np.zeros(shape=(len(comparison_items), target_vector.shape[1]))
        content_matrix = lil_matrix(content_matrix)
        for item_ind, item in enumerate(comparison_items):
            ind_to_item[item_ind] = item
            content_matrix[item_ind] = comparison_contents[item_ind]

        content_matrix = content_matrix.tocsr()
        cosine_sims: List[float] = CandidateGenerator.cosine_sim(comparison_vector=target_vector,
                                                                 comparison_matrix=content_matrix).tolist()[0]

        return list(zip(comparison_items, cosine_sims))

    @staticmethod
    def get_top_n_candidates(*, candidate_score_dict: List[Tuple[Any, float]], top_n: int) -> List[Any]:
        sorted_uris = sorted(candidate_score_dict, key=lambda item: item[1], reverse=True)
        return [tup[0] for tup in sorted_uris[:top_n]]

    @abstractmethod
    def get_candidates(self, *, context: Context) -> Generator[Candidate, None, None]:
        pass

    def execute(self, *, context: Context, candidates: Generator[Candidate, None, None]) -> \
            Generator[Candidate, None, None]:
        return self.get_candidates(context=context)

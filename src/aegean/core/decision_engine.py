"""
Decision engine for evaluating consensus conditions.

Based on paper Section 5.2: Refinement Decision Engine
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
from collections import Counter
from aegean.core.models import Solution
from aegean.core.answer_normalizer import AnswerNormalizer

logger = logging.getLogger(__name__)


class DecisionEngine(ABC):
    """
    Abstract base class for consensus decision engines.

    The decision engine evaluates whether consensus has been reached
    and determines when to terminate the protocol.
    """

    @abstractmethod
    def evaluate(
        self,
        solutions: List[Solution],
        round_num: int,
        previous_candidate: Optional[Solution] = None
    ) -> Tuple[Optional[Solution], bool]:
        """
        Evaluate solutions and determine if consensus is reached.
        """
        pass


class DefaultDecisionEngine(DecisionEngine):
    """
    Default decision engine implementing the Aegean protocol.
    """

    def __init__(
        self,
        quorum_size: int,
        stability_horizon: int,
        similarity_threshold: float = 0.9,
        answer_normalizer: Optional[AnswerNormalizer] = None,
        normalization_context: Optional[Dict] = None,
    ):
        self.quorum_size = quorum_size
        self.stability_horizon = stability_horizon
        self.similarity_threshold = similarity_threshold
        self.answer_normalizer = answer_normalizer
        self.normalization_context = normalization_context or {}
        self.stability_counter = 0
        self.previous_candidate: Optional[Solution] = None

    def evaluate(
        self,
        solutions: List[Solution],
        round_num: int,
        previous_candidate: Optional[Solution] = None
    ) -> Tuple[Optional[Solution], bool]:
        if not solutions:
            return None, False

        answer_votes, normalized_map = self._count_votes(solutions)
        candidate_answer, vote_count = max(answer_votes.items(), key=lambda x: x[1])

        if vote_count < self.quorum_size:
            self.stability_counter = 0
            self.previous_candidate = None
            return None, False

        candidate_solution = self._pick_best_solution_for_answer(
            solutions, candidate_answer, normalized_map
        )

        if self._is_same_candidate(candidate_solution, self.previous_candidate):
            self.stability_counter += 1
        else:
            self.stability_counter = 1
            self.previous_candidate = candidate_solution

        should_terminate = self.stability_counter >= self.stability_horizon
        return candidate_solution, should_terminate

    def _count_votes(
        self, solutions: List[Solution]
    ) -> Tuple[Dict[str, int], Dict[int, str]]:
        """
        Count votes after applying answer normalization.

        Returns:
            - vote_counts: {normalized_answer: count}
            - normalized_map: {id(solution): normalized_answer}
              (kept so _pick_best_solution_for_answer can find matches)
        """
        normalized_map: Dict[int, str] = {}
        for s in solutions:
            normalized = self._normalize(s.answer)
            normalized_map[id(s)] = normalized
        vote_counts = dict(Counter(normalized_map.values()))
        return vote_counts, normalized_map

    def _normalize(self, answer: str) -> str:
        if self.answer_normalizer is None:
            return answer
        return self.answer_normalizer.normalize(answer, self.normalization_context)

    def _pick_best_solution_for_answer(
        self,
        solutions: List[Solution],
        candidate_answer: str,
        normalized_map: Optional[Dict[int, str]] = None,
    ) -> Solution:
        if normalized_map is not None:
            matches = [s for s in solutions if normalized_map.get(id(s)) == candidate_answer]
        else:
            matches = [s for s in solutions if self._normalize(s.answer) == candidate_answer]
        return max(matches, key=lambda s: (s.confidence, 1 if s.proposal else 0))

    def _is_same_candidate(
        self,
        current: Optional[Solution],
        previous: Optional[Solution]
    ) -> bool:
        if current is None or previous is None:
            return False
        return self._normalize(current.answer) == self._normalize(previous.answer)

    def reset(self) -> None:
        self.stability_counter = 0
        self.previous_candidate = None

    def get_state(self) -> Dict:
        return {
            "stability_counter": self.stability_counter,
            "previous_candidate": (
                self.previous_candidate.answer
                if self.previous_candidate else None
            ),
            "quorum_size": self.quorum_size,
            "stability_horizon": self.stability_horizon,
            "normalizer": (
                self.answer_normalizer.__class__.__name__
                if self.answer_normalizer else None
            ),
        }


class CustomDecisionEngine(DecisionEngine):
    def __init__(self, quorum_size: int, stability_horizon: int):
        self.quorum_size = quorum_size
        self.stability_horizon = stability_horizon

    def evaluate(
        self,
        solutions: List[Solution],
        round_num: int,
        previous_candidate: Optional[Solution] = None
    ) -> Tuple[Optional[Solution], bool]:
        raise NotImplementedError("Implement your custom logic")


class WeightedDecisionEngine(DecisionEngine):
    """
    Weighted decision engine for handling agent capability heterogeneity.
    """

    def __init__(
        self,
        quorum_threshold: float = 0.5,
        stability_horizon: int = 2,
        agent_registry=None,
        answer_normalizer: Optional[AnswerNormalizer] = None,
        normalization_context: Optional[Dict] = None,
    ):
        self.quorum_threshold = quorum_threshold
        self.stability_horizon = stability_horizon
        self.agent_registry = agent_registry
        self.answer_normalizer = answer_normalizer
        self.normalization_context = normalization_context or {}
        self.stability_counter = 0
        self.previous_candidate: Optional[Solution] = None
        self.agent_history: Dict[str, Dict] = {}

        # Health check: warn if any single agent dominates voting.
        # The paper's Refinement Validity assumes equal weights. With weighted
        # voting, validity still holds iff max(w_i) / sum(w_j) < 0.5.
        # Otherwise a single "expert" agent could override all others.
        self._check_weight_distribution()

    def _check_weight_distribution(self) -> None:
        if self.agent_registry is None:
            return
        agents = self.agent_registry.get_all_agents()
        weights = [getattr(a, "capability_weight", 1.0) for a in agents]
        if not weights:
            return
        total = sum(weights)
        if total <= 0:
            return
        max_share = max(weights) / total
        if max_share > 0.5:
            logger.warning(
                "WeightedDecisionEngine: single agent has %.1f%% of total weight "
                "(>50%%). The paper's Refinement Validity guarantee no longer "
                "holds; this agent can override majority. "
                "Consider rebalancing capability_weight values.",
                max_share * 100,
            )

    def evaluate(
        self,
        solutions: List[Solution],
        round_num: int,
        previous_candidate: Optional[Solution] = None
    ) -> Tuple[Optional[Solution], bool]:
        if not solutions:
            return None, False

        weighted_votes, total_weight, normalized_map = self._calculate_weighted_votes(solutions)
        if not weighted_votes or total_weight <= 0:
            self.stability_counter = 0
            self.previous_candidate = None
            return None, False

        candidate_answer, candidate_weight = max(weighted_votes.items(), key=lambda x: x[1])
        vote_ratio = candidate_weight / total_weight if total_weight > 0 else 0.0

        if vote_ratio < self.quorum_threshold:
            self.stability_counter = 0
            self.previous_candidate = None
            return None, False

        candidate_solution = self._pick_best_solution_for_answer(
            solutions, candidate_answer, normalized_map
        )

        if self._is_same_candidate(candidate_solution, self.previous_candidate):
            self.stability_counter += 1
        else:
            self.stability_counter = 1
            self.previous_candidate = candidate_solution

        should_terminate = self.stability_counter >= self.stability_horizon
        return candidate_solution, should_terminate

    def _calculate_weighted_votes(
        self,
        solutions: List[Solution]
    ) -> Tuple[Dict[str, float], float, Dict[int, str]]:
        weighted_votes: Dict[str, float] = {}
        total_weight = 0.0
        normalized_map: Dict[int, str] = {}

        for solution in solutions:
            agent_weight = 1.0
            if self.agent_registry:
                agent = self.agent_registry.get_agent(solution.agent_id)
                if agent:
                    agent_weight = getattr(agent, "capability_weight", 1.0)

            confidence = solution.confidence if solution.confidence is not None else 1.0
            vote_weight = max(agent_weight * confidence, 0.0)

            normalized = self._normalize(solution.answer)
            normalized_map[id(solution)] = normalized

            weighted_votes[normalized] = weighted_votes.get(normalized, 0.0) + vote_weight
            total_weight += vote_weight

        return weighted_votes, total_weight, normalized_map

    def _normalize(self, answer: str) -> str:
        if self.answer_normalizer is None:
            return answer
        return self.answer_normalizer.normalize(answer, self.normalization_context)

    def _pick_best_solution_for_answer(
        self,
        solutions: List[Solution],
        candidate_answer: str,
        normalized_map: Optional[Dict[int, str]] = None,
    ) -> Solution:
        if normalized_map is not None:
            matches = [s for s in solutions if normalized_map.get(id(s)) == candidate_answer]
        else:
            matches = [s for s in solutions if self._normalize(s.answer) == candidate_answer]
        return max(matches, key=lambda s: (s.confidence, 1 if s.proposal else 0))

    def _is_same_candidate(
        self,
        current: Optional[Solution],
        previous: Optional[Solution]
    ) -> bool:
        if current is None or previous is None:
            return False
        return self._normalize(current.answer) == self._normalize(previous.answer)

"""
Unit tests for AnswerNormalizer.

Validates the dictionary-based semantic normalization (Plan A) introduced
to fix the α exact-match deviation from paper §5.2.
"""

import pytest

from aegean.core.answer_normalizer import (
    IdentityNormalizer,
    MatchOutcomeNormalizer,
    TournamentWinnerNormalizer,
    InvestmentActionNormalizer,
    RiskDecisionNormalizer,
    get_normalizer,
)


class TestIdentityNormalizer:
    def test_preserves_input(self):
        n = IdentityNormalizer()
        assert n.normalize("foo") == "foo"
        assert n.normalize("BAR") == "BAR"
        assert n.normalize("  whitespace  ") == "  whitespace  "


class TestMatchOutcomeNormalizer:
    @pytest.fixture
    def n(self):
        return MatchOutcomeNormalizer()

    def test_english_labels(self, n):
        assert n.normalize("home_win") == "home_win"
        assert n.normalize("HOME WIN") == "home_win"
        assert n.normalize("Away wins") == "away_win"
        assert n.normalize("draw") == "draw"
        assert n.normalize("Tie") == "draw"

    def test_chinese_labels(self, n):
        assert n.normalize("主胜") == "home_win"
        assert n.normalize("客胜") == "away_win"
        assert n.normalize("平局") == "draw"

    def test_team_name_context_english(self, n):
        ctx = {"home_team": "Brazil", "away_team": "Germany"}
        assert n.normalize("Brazil wins", ctx) == "home_win"
        assert n.normalize("Germany", ctx) == "away_win"

    def test_team_name_context_bilingual(self, n):
        """When context says 'Brazil' (English) but answer is 巴西 (Chinese)."""
        ctx = {"home_team": "Brazil", "away_team": "Germany"}
        assert n.normalize("巴西胜", ctx) == "home_win"
        assert n.normalize("德国赢", ctx) == "away_win"

    def test_unparseable_falls_back(self, n):
        # No keywords, no context — return cleaned string
        assert n.normalize("xyz") == "xyz"


class TestTournamentWinnerNormalizer:
    @pytest.fixture
    def n(self):
        return TournamentWinnerNormalizer()

    def test_fifa_code(self, n):
        assert n.normalize("BRA") == "BRA"
        assert n.normalize("bra") == "BRA"

    def test_english_names(self, n):
        assert n.normalize("Brazil") == "BRA"
        assert n.normalize("Argentina") == "ARG"
        assert n.normalize("France") == "FRA"

    def test_chinese_names(self, n):
        assert n.normalize("巴西") == "BRA"
        assert n.normalize("阿根廷") == "ARG"
        assert n.normalize("德国") == "GER"

    def test_extended_phrases(self, n):
        assert n.normalize("Brazil National Team") == "BRA"
        assert n.normalize("Three Lions") == "ENG"
        assert n.normalize("Les Bleus") == "FRA"


class TestInvestmentActionNormalizer:
    @pytest.fixture
    def n(self):
        return InvestmentActionNormalizer()

    def test_buy_variants(self, n):
        assert n.normalize("buy") == "buy"
        assert n.normalize("BUY") == "buy"
        assert n.normalize("Long AAPL") == "buy"
        assert n.normalize("做多") == "buy"
        assert n.normalize("买入") == "buy"
        assert n.normalize("看涨") == "buy"

    def test_sell_variants(self, n):
        assert n.normalize("sell") == "sell"
        assert n.normalize("Short TSLA") == "sell"
        assert n.normalize("卖出") == "sell"
        assert n.normalize("减持") == "sell"

    def test_hold_variants(self, n):
        assert n.normalize("hold") == "hold"
        assert n.normalize("Neutral") == "hold"
        assert n.normalize("持有") == "hold"

    def test_watch_variants(self, n):
        assert n.normalize("watch") == "watch"
        assert n.normalize("观望") == "watch"


class TestRiskDecisionNormalizer:
    @pytest.fixture
    def n(self):
        return RiskDecisionNormalizer()

    def test_all_decisions(self, n):
        assert n.normalize("APPROVE") == "approve"
        assert n.normalize("批准") == "approve"
        assert n.normalize("rejected") == "reject"
        assert n.normalize("拒绝") == "reject"
        assert n.normalize("Challenge") == "challenge"
        assert n.normalize("二次验证") == "challenge"
        assert n.normalize("Manual Review") == "review"


class TestRegistry:
    def test_get_normalizer(self):
        assert isinstance(get_normalizer("identity"), IdentityNormalizer)
        assert isinstance(get_normalizer("match_outcome"), MatchOutcomeNormalizer)
        assert isinstance(get_normalizer("tournament_winner"), TournamentWinnerNormalizer)
        assert isinstance(get_normalizer("investment_action"), InvestmentActionNormalizer)
        assert isinstance(get_normalizer("risk_decision"), RiskDecisionNormalizer)

    def test_unknown_normalizer_raises(self):
        with pytest.raises(KeyError):
            get_normalizer("nonexistent")


class TestDecisionEngineIntegration:
    """
    Verify the regression scenario from the paper:
    Without normalizer, '"buy" / "BUY" / "买入"' should be 3 distinct answers
    and never reach quorum.
    With investment_action normalizer they should all collapse to 'buy'.
    """

    def test_paper_regression_scenario(self):
        from aegean.core.decision_engine import DefaultDecisionEngine
        from aegean.core.models import Solution

        solutions = [
            Solution(agent_id="a0", answer="buy"),
            Solution(agent_id="a1", answer="BUY"),
            Solution(agent_id="a2", answer="买入"),
        ]

        # Without normalizer: 3 distinct answers, quorum_size=2 fails
        engine_no_norm = DefaultDecisionEngine(quorum_size=2, stability_horizon=1)
        candidate, _ = engine_no_norm.evaluate(solutions, round_num=1)
        assert candidate is None, "without normalizer should fail to reach quorum"

        # With normalizer: all collapse to "buy", quorum reached
        engine_with_norm = DefaultDecisionEngine(
            quorum_size=2,
            stability_horizon=1,
            answer_normalizer=get_normalizer("investment_action"),
        )
        candidate, terminate = engine_with_norm.evaluate(solutions, round_num=1)
        assert candidate is not None
        assert terminate is True
        # The chosen solution's answer can be any variant; normalization is for voting only
        assert candidate.answer in ("buy", "BUY", "买入")

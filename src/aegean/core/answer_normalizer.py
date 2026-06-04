"""
Answer normalizer for the Aegean consensus protocol.

Implements the α (similarity threshold) semantic equivalence requirement
from the Aegean paper §5.2.

Sprint version: dictionary-based normalization (Plan A).
8月 upgrade: embedding-based semantic similarity (Plan B).

Why this exists:
    The paper requires α agents to give "semantically equivalent" answers,
    but the original DecisionEngine used Counter() for exact string match.
    "buy" / "BUY" / "买入" would be counted as 3 distinct answers and
    quorum would never be reached.

    This module provides pluggable normalizers that map free-form LLM
    output to standard labels before voting.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class AnswerNormalizer(ABC):
    """
    Pluggable answer normalizer.

    Maps free-form LLM output to a canonical label for vote counting.
    Different domains (sports/investment/risk) use different subclasses.
    """

    @abstractmethod
    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        """
        Normalize an answer string to a canonical label.

        Args:
            answer: Raw answer string from agent
            context: Optional context (e.g., {"home_team": "Brazil"} for sports)

        Returns:
            Canonical label string. Returns lowercased input as fallback.
        """

    @staticmethod
    def _clean(s: str) -> str:
        """Common cleanup: lowercase, strip, collapse whitespace."""
        return " ".join(s.lower().strip().split())


class IdentityNormalizer(AnswerNormalizer):
    """No-op normalizer. Equivalent to original Counter() behavior."""

    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        return answer


class MatchOutcomeNormalizer(AnswerNormalizer):
    """
    For sports match prediction: home_win / draw / away_win.

    Use this when consensus task is "predict the outcome of a single match".
    For tournament-level (who wins the cup) use TournamentWinnerNormalizer.
    """

    HOME_WIN_KEYWORDS = (
        "home_win", "home win", "home wins", "home victory",
        "主胜", "主队胜", "主队赢", "主场胜",
    )
    AWAY_WIN_KEYWORDS = (
        "away_win", "away win", "away wins", "away victory",
        "客胜", "客队胜", "客队赢", "客场胜",
    )
    DRAW_KEYWORDS = (
        "draw", "tie", "drawn", "stalemate",
        "平", "平局", "和局",
    )

    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        s = self._clean(answer)

        # First try direct keyword match (works regardless of context)
        if any(k in s for k in self.HOME_WIN_KEYWORDS):
            return "home_win"
        if any(k in s for k in self.AWAY_WIN_KEYWORDS):
            return "away_win"
        if any(k in s for k in self.DRAW_KEYWORDS):
            return "draw"

        # If context provides team names, try to match by team (bilingual)
        if context:
            home_variants = self._expand_team_variants(context.get("home_team"))
            away_variants = self._expand_team_variants(context.get("away_team"))
            home_match = any(v in s for v in home_variants)
            away_match = any(v in s for v in away_variants)
            if home_match and not away_match:
                return "home_win"
            if away_match and not home_match:
                return "away_win"

        # Fallback: return cleaned string (will fail to reach quorum,
        # which is the correct behavior for unparseable answers)
        return s

    @staticmethod
    def _expand_team_variants(team) -> List[str]:
        """
        Expand a team identifier into all known name variants.

        Looks up TournamentWinnerNormalizer.TEAM_VARIANTS for cross-language
        alias matching (e.g., context says "Brazil" but answer says "巴西").
        Accepts either a string ("Brazil"/"BRA"/"巴西") or a list of aliases.
        """
        if team is None:
            return []
        if isinstance(team, (list, tuple)):
            return [str(t).lower().strip() for t in team if t]

        s = str(team).lower().strip()
        if not s:
            return []
        # Try to find this team in the FIFA code registry
        for code, variants in TournamentWinnerNormalizer.TEAM_VARIANTS.items():
            if s == code.lower() or s in variants:
                return [code.lower(), *variants]
        return [s]


class TournamentWinnerNormalizer(AnswerNormalizer):
    """
    For "who wins the tournament" questions: returns FIFA 3-letter code.

    Covers all 32 World Cup 2026 qualified teams (as of 2026-06).
    Edit TEAM_VARIANTS when team list changes.
    """

    TEAM_VARIANTS: Dict[str, Tuple[str, ...]] = {
        "ARG": ("argentina", "阿根廷", "argentine"),
        "BRA": ("brazil", "巴西", "brazilian"),
        "FRA": ("france", "法国", "french", "les bleus"),
        "GER": ("germany", "德国", "german"),
        "ESP": ("spain", "西班牙", "spanish"),
        "ENG": ("england", "英格兰", "english", "three lions"),
        "POR": ("portugal", "葡萄牙", "portuguese"),
        "NED": ("netherlands", "荷兰", "dutch", "holland"),
        "BEL": ("belgium", "比利时", "belgian"),
        "ITA": ("italy", "意大利", "italian", "azzurri"),
        "CRO": ("croatia", "克罗地亚", "croatian"),
        "URU": ("uruguay", "乌拉圭"),
        "MEX": ("mexico", "墨西哥"),
        "USA": ("united states", "美国", "usmnt"),
        "JPN": ("japan", "日本"),
        "KOR": ("south korea", "korea", "韩国"),
        "AUS": ("australia", "澳大利亚", "socceroos"),
        "MAR": ("morocco", "摩洛哥"),
        "SEN": ("senegal", "塞内加尔"),
        "SUI": ("switzerland", "瑞士"),
        "DEN": ("denmark", "丹麦"),
        "POL": ("poland", "波兰"),
        "SRB": ("serbia", "塞尔维亚"),
        "CAN": ("canada", "加拿大"),
        "ECU": ("ecuador", "厄瓜多尔"),
        "IRN": ("iran", "伊朗"),
        "QAT": ("qatar", "卡塔尔"),
        "KSA": ("saudi arabia", "沙特", "saudi"),
        "TUN": ("tunisia", "突尼斯"),
        "CRC": ("costa rica", "哥斯达黎加"),
        "GHA": ("ghana", "加纳"),
        "CMR": ("cameroon", "喀麦隆"),
    }

    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        s = self._clean(answer)
        s_upper = answer.strip().upper()

        # Direct FIFA code match
        if s_upper in self.TEAM_VARIANTS:
            return s_upper

        # Fuzzy match by team name variants
        for code, variants in self.TEAM_VARIANTS.items():
            if any(v in s for v in variants):
                return code

        # Unrecognized — return cleaned string
        return s


class InvestmentActionNormalizer(AnswerNormalizer):
    """
    For investment decisions: buy / sell / hold / watch.

    Handles common LLM output variations (中英文 + 同义词).
    """

    BUY_KEYWORDS = (
        "buy", "long", "purchase", "accumulate", "overweight",
        "买入", "买", "做多", "看涨", "增持", "加仓",
    )
    SELL_KEYWORDS = (
        "sell", "short", "exit", "reduce", "underweight",
        "卖出", "卖", "做空", "看跌", "减持", "清仓",
    )
    HOLD_KEYWORDS = (
        "hold", "neutral", "maintain",
        "持有", "保持", "不动",
    )
    WATCH_KEYWORDS = (
        "watch", "observe", "monitor", "wait",
        "观望", "观察", "等待",
    )

    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        s = self._clean(answer)
        # Order matters: check sell/buy before hold/watch
        # because "buy" might appear inside longer phrases
        if any(k in s for k in self.SELL_KEYWORDS):
            return "sell"
        if any(k in s for k in self.BUY_KEYWORDS):
            return "buy"
        if any(k in s for k in self.WATCH_KEYWORDS):
            return "watch"
        if any(k in s for k in self.HOLD_KEYWORDS):
            return "hold"
        return s


class RiskDecisionNormalizer(AnswerNormalizer):
    """
    For risk gate decisions: approve / reject / challenge / review.

    Aligned with existing ExpectedDecision enum in the codebase.
    """

    APPROVE_KEYWORDS = (
        "approve", "approved", "pass", "allow", "permit",
        "通过", "批准", "允许",
    )
    REJECT_KEYWORDS = (
        "reject", "rejected", "deny", "block", "refuse",
        "拒绝", "驳回", "禁止",
    )
    CHALLENGE_KEYWORDS = (
        "challenge", "challenged", "verify", "second factor",
        "质询", "二次验证", "挑战",
    )
    REVIEW_KEYWORDS = (
        "review", "manual review", "escalate",
        "审查", "人工审核", "升级",
    )

    def normalize(self, answer: str, context: Optional[Dict] = None) -> str:
        s = self._clean(answer)
        if any(k in s for k in self.REJECT_KEYWORDS):
            return "reject"
        if any(k in s for k in self.APPROVE_KEYWORDS):
            return "approve"
        if any(k in s for k in self.CHALLENGE_KEYWORDS):
            return "challenge"
        if any(k in s for k in self.REVIEW_KEYWORDS):
            return "review"
        return s


# Convenience factory for the common domains
_NORMALIZER_REGISTRY: Dict[str, AnswerNormalizer] = {
    "identity": IdentityNormalizer(),
    "match_outcome": MatchOutcomeNormalizer(),
    "tournament_winner": TournamentWinnerNormalizer(),
    "investment_action": InvestmentActionNormalizer(),
    "risk_decision": RiskDecisionNormalizer(),
}


def get_normalizer(name: str) -> AnswerNormalizer:
    """
    Get a normalizer by name.

    Args:
        name: One of: identity, match_outcome, tournament_winner,
              investment_action, risk_decision

    Returns:
        AnswerNormalizer instance

    Raises:
        KeyError: if name is not registered
    """
    if name not in _NORMALIZER_REGISTRY:
        raise KeyError(
            f"Unknown normalizer '{name}'. "
            f"Available: {list(_NORMALIZER_REGISTRY.keys())}"
        )
    return _NORMALIZER_REGISTRY[name]

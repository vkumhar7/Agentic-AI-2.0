from __future__ import annotations

from dataclasses import dataclass, field

from .agents import CommentaryAgent, MarketRiskAgent, PortfolioAggregatorAgent
from .models import AnalysisResponse, PortfolioInput


@dataclass
class RiskAnalysisOrchestrator:
    """Simple agentic pipeline that routes work across specialized agents."""

    market_risk_agent: MarketRiskAgent = field(default_factory=MarketRiskAgent)
    aggregator_agent: PortfolioAggregatorAgent = field(default_factory=PortfolioAggregatorAgent)
    commentary_agent: CommentaryAgent = field(default_factory=CommentaryAgent)

    def run(self, portfolio: PortfolioInput) -> AnalysisResponse:
        evaluated = [self.market_risk_agent.evaluate_position(position) for position in portfolio.positions]
        summary = self.aggregator_agent.summarize(evaluated)
        commentary = self.commentary_agent.generate(portfolio, summary)

        return AnalysisResponse(
            portfolio_name=portfolio.portfolio_name,
            summary=summary,
            position_breakdown=evaluated,
            commentary=commentary,
        )

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import CommentaryBlock, ExposureResult, PortfolioInput, Position, RiskBand, RiskSummary


class Agent(Protocol):
    name: str


@dataclass
class MarketRiskAgent:
    name: str = "market-risk-agent"

    def evaluate_position(self, position: Position) -> ExposureResult:
        var_95 = 1.65 * position.notional_usd * position.volatility
        ecl = position.notional_usd * position.probability_of_default * position.loss_given_default
        liquidity_penalty = position.notional_usd * min(position.liquidity_horizon_days / 30, 2) * 0.002
        risk_points = (var_95 + ecl + liquidity_penalty) / 1000
        return ExposureResult(
            symbol=position.symbol,
            exposure_type=position.exposure_type,
            var_95=round(var_95, 2),
            expected_credit_loss=round(ecl, 2),
            liquidity_penalty=round(liquidity_penalty, 2),
            risk_points=round(risk_points, 2),
        )


@dataclass
class PortfolioAggregatorAgent:
    name: str = "portfolio-aggregator-agent"

    def summarize(self, positions: list[ExposureResult]) -> RiskSummary:
        total_var = round(sum(p.var_95 for p in positions), 2)
        total_ecl = round(sum(p.expected_credit_loss for p in positions), 2)
        total_liq = round(sum(p.liquidity_penalty for p in positions), 2)
        points = round(sum(p.risk_points for p in positions), 2)

        if points < 100:
            band = RiskBand.LOW
        elif points < 300:
            band = RiskBand.MODERATE
        elif points < 700:
            band = RiskBand.HIGH
        else:
            band = RiskBand.CRITICAL

        return RiskSummary(
            total_var_95=total_var,
            total_expected_credit_loss=total_ecl,
            total_liquidity_penalty=total_liq,
            aggregate_risk_points=points,
            risk_band=band,
        )


@dataclass
class CommentaryAgent:
    name: str = "commentary-agent"

    def generate(self, portfolio: PortfolioInput, summary: RiskSummary) -> list[CommentaryBlock]:
        primary = CommentaryBlock(
            title="Portfolio posture",
            detail=(
                f"{portfolio.portfolio_name} is currently in the {summary.risk_band.value.upper()} risk band "
                f"with aggregate risk points of {summary.aggregate_risk_points}."
            ),
        )
        drivers = CommentaryBlock(
            title="Primary risk drivers",
            detail=(
                f"Estimated VaR(95) is ${summary.total_var_95:,.2f}, expected credit loss is "
                f"${summary.total_expected_credit_loss:,.2f}, and liquidity penalties contribute "
                f"${summary.total_liquidity_penalty:,.2f}."
            ),
        )
        action = CommentaryBlock(
            title="Suggested action",
            detail=self._recommendation(summary.risk_band),
        )
        return [primary, drivers, action]

    @staticmethod
    def _recommendation(band: RiskBand) -> str:
        if band in {RiskBand.HIGH, RiskBand.CRITICAL}:
            return "Prioritize de-risking, tighten limits, and run intraday stress scenarios."
        if band == RiskBand.MODERATE:
            return "Monitor concentrations and schedule additional weekly stress testing."
        return "Maintain current controls and continue routine monitoring cadence."

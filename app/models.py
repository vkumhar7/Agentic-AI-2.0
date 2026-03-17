from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class ExposureType(str, Enum):
    MARKET = "market"
    CREDIT = "credit"
    LIQUIDITY = "liquidity"
    OPERATIONAL = "operational"


class Position(BaseModel):
    symbol: str = Field(..., description="Instrument ticker or identifier")
    exposure_type: ExposureType
    notional_usd: float = Field(..., ge=0)
    volatility: float = Field(..., ge=0, le=1, description="Expected annualized volatility")
    probability_of_default: float = Field(0, ge=0, le=1)
    loss_given_default: float = Field(0, ge=0, le=1)
    liquidity_horizon_days: int = Field(1, ge=1)


class PortfolioInput(BaseModel):
    portfolio_name: str
    positions: List[Position] = Field(default_factory=list)


class ExposureResult(BaseModel):
    symbol: str
    exposure_type: ExposureType
    var_95: float
    expected_credit_loss: float
    liquidity_penalty: float
    risk_points: float


class RiskBand(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RiskSummary(BaseModel):
    total_var_95: float
    total_expected_credit_loss: float
    total_liquidity_penalty: float
    aggregate_risk_points: float
    risk_band: RiskBand


class CommentaryBlock(BaseModel):
    title: str
    detail: str


class AnalysisResponse(BaseModel):
    portfolio_name: str
    summary: RiskSummary
    position_breakdown: List[ExposureResult]
    commentary: List[CommentaryBlock]

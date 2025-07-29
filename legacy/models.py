from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TradeData:
    title: str
    slug: str
    event_slug: str
    usd_size: float
    timestamp: int
    side: str
    outcome: str


@dataclass 
class MarketSummary:
    question: str
    slug: str
    volume: float
    trade_count: int


@dataclass
class PortfolioSummary:
    trader_address: str
    total_volume: float
    category_volumes: Dict[str, float]
    category_percentages: Dict[str, float]
    trade_count: int
    categories_traded: int
    top_markets: Optional[List[MarketSummary]] = None
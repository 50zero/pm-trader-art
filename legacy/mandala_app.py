from typing import Tuple

from models import PortfolioSummary
from data_fetcher import PolymarketDataFetcher
from svg_generator import AbstractSVGGenerator


class PolymarketMandalaApp:
    def __init__(self):
        self.data_fetcher = PolymarketDataFetcher()
        self.svg_generator = AbstractSVGGenerator()
    
    async def generate_mandala_for_address(self, trader_address: str) -> Tuple[str, PortfolioSummary]:
        """Generate mandala SVG and portfolio summary for a trader address"""
        portfolio = await self.data_fetcher.analyze_trader_portfolio(trader_address)
        svg = self.svg_generator.generate_abstract_svg(portfolio)
        return svg, portfolio
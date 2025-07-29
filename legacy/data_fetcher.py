import asyncio
import httpx
from typing import Dict, List
from collections import defaultdict

from models import PortfolioSummary, MarketSummary


class PolymarketDataFetcher:
    def __init__(self):
        self.data_api_url = "https://data-api.polymarket.com"
        
        # Enhanced category mapping using keywords that appear in market titles/slugs
        self.category_mapping = {
            "politics": [
                "election", "president", "presidential", "vote", "campaign", "senate", 
                "congress", "democrat", "republican", "biden", "trump", "harris", 
                "political", "governor", "mayor", "legislation", "impeach", "war", "israel", 
                "gaza"
            ],
            "crypto": [
                "bitcoin", "ethereum", "crypto", "defi", "nft", "btc", "eth", 
                "blockchain", "dogecoin", "solana", "polygon", "ada", "xrp",
                "coinbase", "binance", "price", "market-cap", "airdrop"
            ],
            "sports": [
                "nfl", "nba", "wnba", "mlb", "nhl", "soccer", "football", "basketball",
                "baseball", "hockey", "olympics", "super-bowl", "world-cup",
                "championship", "playoffs", "wins", "mvp", "team", "us-open" 
            ],
            "entertainment": [
                "movie", "tv", "television", "celebrity", "music", "awards", "oscar",
                "netflix", "disney", "streaming", "box-office", "album", "concert",
                "grammy", "emmy", "actor", "actress", "artist", "artists", "rotten-tomatoes"
            ],
            "technology": [
                "ai", "artificial-intelligence", "tech", "software", "hardware", 
                "innovation", "chatgpt", "openai", "robot", "automation",
                "iphone", "android", "app", "platform", "stock", "ipo", "merger", "earnings", "company", "ceo", "revenue",
                "apple", "google", "microsoft", "tesla", "amazon", "meta",
                "quarterly", "billion", "market-value"
            ],
            "economics": [
                "inflation", "gdp", "recession", "interest", "fed", "federal-reserve",
                "rate", "economy", "unemployment", "jobs", "housing", "market",
                "dow", "s&p", "nasdaq"
            ],
            "other": []
        }
    
    async def fetch_user_activity(self, user_address: str, limit: int = 1000) -> List[Dict]:
        """Fetch user trading activity from Data API"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.data_api_url}/activity",
                    params={
                        "user": user_address,
                        "limit": limit,
                        "sortDirection": "DESC",
                        "type": "TRADE"  # Only get trades, not deposits/withdrawals
                    }
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Error fetching user activity: {response.status_code}")
                    return []
            except Exception as e:
                print(f"Exception fetching user activity: {e}")
                return []
    
    def categorize_market_from_activity(self, trade: Dict) -> str:
        """Categorize a market based on title, slug, and event slug from activity data"""
        text_to_analyze = (
            trade.get('title', '') + ' ' + 
            trade.get('slug', '') + ' ' +
            trade.get('eventSlug', '')
        ).lower()
        
        # Check each category's keywords
        for category, keywords in self.category_mapping.items():
            if category == "other":
                continue
            for keyword in keywords:
                if keyword in text_to_analyze:
                    return category
        
        return "other"
    
    async def analyze_trader_portfolio(self, trader_address: str) -> PortfolioSummary:
        """Analyze a trader's portfolio using the Data API"""
        
        # Fetch user's trading activity
        activities = await self.fetch_user_activity(trader_address)
        
        if not activities:
            return PortfolioSummary(
                trader_address=trader_address,
                total_volume=0,
                category_volumes={},
                category_percentages={},
                trade_count=0,
                categories_traded=0,
                top_markets=[]
            )
        
        # Process trades and aggregate by category and market
        category_volumes = defaultdict(float)
        market_volumes = defaultdict(float)
        market_trade_counts = defaultdict(int)
        market_questions = {}
        total_volume = 0
        
        for activity in activities:
            if activity.get('type') == 'TRADE':
                usd_size = activity.get('usdcSize', 0)
                category = self.categorize_market_from_activity(activity)
                
                # Get market info
                market_id = activity.get('marketId', '')
                market_question = activity.get('marketTitle', activity.get('marketSlug', 'Unknown Market'))
                
                category_volumes[category] += usd_size
                market_volumes[market_id] += usd_size
                market_trade_counts[market_id] += 1
                market_questions[market_id] = market_question
                total_volume += usd_size
        
        # Calculate percentages
        category_percentages = {}
        if total_volume > 0:
            for category, volume in category_volumes.items():
                category_percentages[category] = (volume / total_volume) * 100
        
        # Create top markets list
        top_markets = []
        sorted_markets = sorted(market_volumes.items(), key=lambda x: x[1], reverse=True)
        for market_id, volume in sorted_markets[:10]:  # Top 10 markets
            if volume > 0:
                top_markets.append(MarketSummary(
                    question=market_questions.get(market_id, 'Unknown Market'),
                    slug=market_id,
                    volume=volume,
                    trade_count=market_trade_counts[market_id]
                ))
        
        return PortfolioSummary(
            trader_address=trader_address,
            total_volume=total_volume,
            category_volumes=dict(category_volumes),
            category_percentages=category_percentages,
            trade_count=len([a for a in activities if a.get('type') == 'TRADE']),
            categories_traded=len(category_volumes),
            top_markets=top_markets
        )
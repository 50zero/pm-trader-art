"""
NFT metadata generation for Portfolio Mandala NFTs
"""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from models import PortfolioSummary
from .config import get_metadata_config

class NFTMetadataGenerator:
    def __init__(self):
        self.config = get_metadata_config()
    
    def generate_metadata(self, token_id: int, portfolio: PortfolioSummary, trader_address: str) -> Dict[str, Any]:
        """Generate OpenSea-compatible metadata for a Portfolio Mandala NFT"""
        
        # Basic metadata
        metadata = {
            "name": f"Portfolio Mandala #{token_id}",
            "description": self.config['description_template'].format(trader_address=trader_address),
            "image": f"{self.config['image_base_uri']}{trader_address}.svg",
            "external_url": f"{self.config['external_url_base']}{trader_address}",
            "attributes": []
        }
        
        # Add portfolio-based attributes
        attributes = self._generate_attributes(portfolio)
        metadata["attributes"] = attributes
        
        # Add collection and creator info
        metadata.update({
            "collection": {
                "name": "Portfolio Mandala",
                "description": "Unique visual representations of Polymarket trading patterns",
                "image": f"{self.config['base_uri']}collection.png",
                "external_link": self.config['external_url_base']
            },
            "creator": {
                "name": "Portfolio Mandala Generator",
                "description": "AI-generated portfolio visualizations"
            }
        })
        
        # Add technical metadata
        metadata.update({
            "animation_url": f"{self.config['image_base_uri']}{trader_address}.svg",
            "background_color": "000000",
            "image_data": None,  # We use image URL instead
            "created_date": datetime.utcnow().isoformat(),
            "token_id": token_id,
            "trader_address": trader_address
        })
        
        return metadata
    
    def _generate_attributes(self, portfolio: PortfolioSummary) -> List[Dict[str, Any]]:
        """Generate NFT attributes based on portfolio data"""
        attributes = []
        
        # Financial attributes
        attributes.append({
            "trait_type": "Total Volume",
            "value": f"${portfolio.total_volume:,.0f}",
            "display_type": "number"
        })
        
        attributes.append({
            "trait_type": "Trade Count",
            "value": portfolio.trade_count,
            "display_type": "number"
        })
        
        attributes.append({
            "trait_type": "Categories Traded",
            "value": portfolio.categories_traded,
            "display_type": "number"
        })
        
        # Volume tiers
        volume_tier = self._get_volume_tier(portfolio.total_volume)
        attributes.append({
            "trait_type": "Volume Tier",
            "value": volume_tier
        })
        
        # Trading activity level
        activity_level = self._get_activity_level(portfolio.trade_count)
        attributes.append({
            "trait_type": "Activity Level",
            "value": activity_level
        })
        
        # Dominant category
        if portfolio.category_percentages:
            dominant_category = max(portfolio.category_percentages.items(), key=lambda x: x[1])
            attributes.append({
                "trait_type": "Dominant Category",
                "value": dominant_category[0].title()
            })
            
            attributes.append({
                "trait_type": "Dominant Category Percentage",
                "value": f"{dominant_category[1]:.1f}%",
                "display_type": "number"
            })
        
        # Portfolio diversity
        diversity_score = self._calculate_diversity_score(portfolio.category_percentages)
        attributes.append({
            "trait_type": "Portfolio Diversity",
            "value": diversity_score
        })
        
        # Pattern type based on number of categories
        pattern_type = self._get_pattern_type(len(portfolio.category_percentages))
        attributes.append({
            "trait_type": "Pattern Type",
            "value": pattern_type
        })
        
        # Add individual category percentages as traits
        for category, percentage in portfolio.category_percentages.items():
            if percentage > 5:  # Only include categories with >5% allocation
                attributes.append({
                    "trait_type": f"{category.title()} %",
                    "value": f"{percentage:.1f}%",
                    "display_type": "number"
                })
        
        # Rarity score (based on trading volume and diversity)
        rarity_score = self._calculate_rarity_score(portfolio)
        attributes.append({
            "trait_type": "Rarity Score",
            "value": rarity_score,
            "display_type": "number"
        })
        
        return attributes
    
    def _get_volume_tier(self, volume: float) -> str:
        """Categorize trading volume into tiers"""
        if volume >= 1000000:
            return "Whale"
        elif volume >= 100000:
            return "High Roller"
        elif volume >= 10000:
            return "Active Trader"
        elif volume >= 1000:
            return "Regular Trader"
        elif volume >= 100:
            return "Casual Trader"
        else:
            return "Beginner"
    
    def _get_activity_level(self, trade_count: int) -> str:
        """Categorize trading activity level"""
        if trade_count >= 1000:
            return "Hyperactive"
        elif trade_count >= 500:
            return "Very Active"
        elif trade_count >= 100:
            return "Active"
        elif trade_count >= 50:
            return "Moderate"
        elif trade_count >= 10:
            return "Light"
        else:
            return "Minimal"
    
    def _calculate_diversity_score(self, category_percentages: Dict[str, float]) -> str:
        """Calculate portfolio diversity score"""
        if not category_percentages:
            return "None"
        
        # Calculate Herfindahl-Hirschman Index (HHI) for diversity
        hhi = sum((percentage / 100) ** 2 for percentage in category_percentages.values())
        
        # Convert to diversity score (lower HHI = higher diversity)
        if hhi >= 0.8:
            return "Focused"
        elif hhi >= 0.5:
            return "Moderate"
        elif hhi >= 0.3:
            return "Diversified"
        else:
            return "Highly Diversified"
    
    def _get_pattern_type(self, category_count: int) -> str:
        """Get the visual pattern type based on category count"""
        if category_count == 1:
            return "Spiral Flow"
        elif category_count == 2:
            return "Dual Flow"
        elif category_count == 3:
            return "Trinity Flow"
        else:
            return "Network Flow"
    
    def _calculate_rarity_score(self, portfolio: PortfolioSummary) -> int:
        """Calculate a rarity score from 1-100 based on various factors"""
        score = 0
        
        # Volume contribution (0-30 points)
        volume_score = min(30, int(portfolio.total_volume / 10000))
        score += volume_score
        
        # Activity contribution (0-25 points)
        activity_score = min(25, int(portfolio.trade_count / 20))
        score += activity_score
        
        # Diversity contribution (0-20 points)
        if portfolio.category_percentages:
            diversity_score = min(20, len(portfolio.category_percentages) * 4)
            score += diversity_score
        
        # Balance contribution (0-25 points)
        if portfolio.category_percentages:
            # Reward balanced portfolios
            percentages = list(portfolio.category_percentages.values())
            balance_variance = sum((p - (100/len(percentages)))**2 for p in percentages)
            balance_score = max(0, 25 - int(balance_variance / 100))
            score += balance_score
        
        return min(100, score)
    
    def generate_contract_metadata(self) -> Dict[str, Any]:
        """Generate contract-level metadata for OpenSea"""
        return {
            "name": "Portfolio Mandala",
            "description": "A collection of unique NFTs representing Polymarket trading portfolios as beautiful, animated mandala patterns. Each NFT is a personalized visualization of a trader's market activity, showing their category preferences and trading patterns through flowing, artistic designs.",
            "image": f"{self.config['base_uri']}collection.png",
            "external_link": self.config['external_url_base'],
            "seller_fee_basis_points": 250,  # 2.5% royalty
            "fee_recipient": "0x0000000000000000000000000000000000000000"  # Update with actual address
        }
import asyncio

from mandala_app import PolymarketMandalaApp


async def main():
    app = PolymarketMandalaApp()
    
    # Test with the address from the API documentation example
    test_address = "0x6af75d4e4aaf700450efbac3708cce1665810ff1"
    
    test_address = "0x1f2dd6d473f3e824cd2f8a89d9c69fb96f6ad0cf"
    
    #test_address = "0x8b5a7da2fdf239b51b9c68a2a1a35bb156d200f2" #3 markets

    print(f"Generating mandala for trader: {test_address}")
    svg, portfolio = await app.generate_mandala_for_address(test_address)
    
    print("\n" + "="*50)
    print("PORTFOLIO SUMMARY")
    print("="*50)
    print(f"Trader: {portfolio.trader_address}")
    print(f"Total Volume: ${portfolio.total_volume:,.2f}")
    print(f"Total Trades: {portfolio.trade_count}")
    print(f"Categories Traded: {portfolio.categories_traded}")
    
    print(f"\nCategory Breakdown:")
    for category, percentage in sorted(portfolio.category_percentages.items(), key=lambda x: x[1], reverse=True):
        volume = portfolio.category_volumes.get(category, 0)
        print(f"  {category.title():15}: {percentage:5.1f}% (${volume:8,.0f})")
    
    # Save SVG to file
    filename = f"mandala_{test_address[:8]}.svg"
    with open(filename, "w") as f:
        f.write(svg)
    
    print(f"\nMandala SVG saved to {filename}")

if __name__ == "__main__":
    asyncio.run(main())
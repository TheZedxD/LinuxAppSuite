#!/usr/bin/env python3
"""
Tool definitions and implementations for Ollama Chat
"""

import json
import requests
from typing import Dict, List, Any


class ToolRegistry:
    """Registry for available tools"""

    def __init__(self):
        self.tools = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools"""
        self.register_tool(
            name="get_top_cryptocurrencies",
            description="Get the top 10 cryptocurrencies by market cap with current prices and 24h change",
            function=get_top_cryptocurrencies,
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )

    def register_tool(self, name: str, description: str, function: callable,
                     parameters: Dict[str, Any]):
        """Register a new tool"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }

    def get_tool_definitions(self) -> List[Dict]:
        """Get tool definitions for Ollama API"""
        definitions = []
        for tool_name, tool_info in self.tools.items():
            definitions.append({
                "type": "function",
                "function": {
                    "name": tool_info["name"],
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            })
        return definitions

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name with given arguments"""
        if tool_name not in self.tools:
            return json.dumps({"error": f"Tool '{tool_name}' not found"})

        try:
            tool_function = self.tools[tool_name]["function"]
            result = tool_function(**arguments)
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error executing tool: {str(e)}"})


def get_top_cryptocurrencies() -> Dict:
    """
    Fetch top 10 cryptocurrencies from CoinGecko API

    Returns:
        Dict containing cryptocurrency data or error message
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "24h"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Format the data nicely
        cryptocurrencies = []
        for i, coin in enumerate(data, 1):
            crypto_info = {
                "rank": i,
                "name": coin.get("name", "N/A"),
                "symbol": coin.get("symbol", "N/A").upper(),
                "current_price": f"${coin.get('current_price', 0):,.2f}",
                "market_cap": f"${coin.get('market_cap', 0):,.0f}",
                "24h_change": f"{coin.get('price_change_percentage_24h', 0):.2f}%",
                "24h_volume": f"${coin.get('total_volume', 0):,.0f}"
            }
            cryptocurrencies.append(crypto_info)

        return {
            "success": True,
            "data": cryptocurrencies,
            "timestamp": "now"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Failed to fetch cryptocurrency data: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def format_crypto_display(crypto_data: Dict) -> str:
    """Format cryptocurrency data for display"""
    if not crypto_data.get("success"):
        return f"Error: {crypto_data.get('error', 'Unknown error')}"

    lines = ["Top 10 Cryptocurrencies by Market Cap:\n"]
    lines.append("=" * 80)

    for crypto in crypto_data.get("data", []):
        line = (
            f"{crypto['rank']:2d}. {crypto['name']:15s} ({crypto['symbol']:6s}) "
            f"| Price: {crypto['current_price']:>12s} "
            f"| 24h: {crypto['24h_change']:>8s} "
            f"| MCap: {crypto['market_cap']}"
        )
        lines.append(line)

    lines.append("=" * 80)
    return "\n".join(lines)


if __name__ == '__main__':
    # Test the tool
    print("Testing CoinGecko tool...")
    result = get_top_cryptocurrencies()

    if result.get("success"):
        print(format_crypto_display(result))
    else:
        print(f"Error: {result.get('error')}")

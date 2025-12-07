"""
Web search tool using DuckDuckGo.
"""
from typing import Optional
from agentblueprint_core import Tool

try:
    from duckduckgo_search import DDGS
    HAS_DDG = True
except ImportError:
    HAS_DDG = False

class WebSearchTool(Tool):
    """
    A tool for searching the web using DuckDuckGo.
    Requires 'duckduckgo-search' package (pip install agentblueprint-tools[search]).
    """
    name = "web_search"
    description = "Searches the web for the given query. Returns top results."
    
    def run(self, query: str, max_results: int = 3) -> str:
        """
        Execute a web search.
        
        Args:
            query: Search query.
            max_results: Number of results to return.
            
        Returns:
            Formatted search results.
        """
        if not HAS_DDG:
            return "Error: 'duckduckgo-search' is not installed. Please install it to use this tool."
            
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
            if not results:
                return "No results found."
                
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(f"{i}. {r['title']}\n   {r['href']}\n   {r['body']}")
                
            return "\n\n".join(formatted)
            
        except Exception as e:
            return f"Error performing search: {str(e)}"

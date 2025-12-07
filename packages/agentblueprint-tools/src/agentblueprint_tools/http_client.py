"""
HTTP Client tool for making web requests.
"""
import httpx
from typing import Optional, Dict, Any
from agentblueprint_core import Tool

class HTTPClientTool(Tool):
    """
    A tool for making HTTP requests (GET, POST, etc.).
    """
    name = "http_client"
    description = "Makes HTTP requests. useful for getting data from APIs or webpages. Inputs: url, method (GET/POST), json_data (optional dict)."
    
    def run(self, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, json_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute an HTTP request.
        
        Args:
            url: The URL to request.
            method: The HTTP method (GET, POST, PUT, DELETE).
            headers: Optional headers.
            json_data: Optional JSON body for POST/PUT.
            
        Returns:
            The response text or error message.
        """
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_data
                )
                # Return status and text, maybe truncated if too long
                return f"Status: {response.status_code}\nContent: {response.text[:2000]}"
                
        except Exception as e:
            return f"Error making request: {str(e)}"

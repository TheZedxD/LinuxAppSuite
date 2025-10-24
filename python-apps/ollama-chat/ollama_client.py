#!/usr/bin/env python3
"""
Ollama API Client
Handles communication with local Ollama server
"""

import json
import requests
from typing import Iterator, List, Dict, Optional, Callable


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def list_models(self) -> List[Dict]:
        """Get list of available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get('models', [])
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def chat_stream(self,
                   model: str,
                   messages: List[Dict[str, str]],
                   tools: Optional[List[Dict]] = None) -> Iterator[Dict]:
        """
        Stream chat responses from Ollama

        Args:
            model: Model name
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions

        Yields:
            Response chunks from the API
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        if tools:
            payload["tools"] = tools

        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        yield chunk
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        continue
        except requests.exceptions.RequestException as e:
            yield {
                "error": True,
                "message": f"Error communicating with Ollama: {str(e)}"
            }

    def chat(self,
            model: str,
            messages: List[Dict[str, str]],
            tools: Optional[List[Dict]] = None) -> Dict:
        """
        Non-streaming chat request

        Args:
            model: Model name
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions

        Returns:
            Complete response dict
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }

        if tools:
            payload["tools"] = tools

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": f"Error communicating with Ollama: {str(e)}"
            }

    def is_available(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False


if __name__ == '__main__':
    # Test the client
    client = OllamaClient()

    if client.is_available():
        print("Ollama server is available")
        models = client.list_models()
        print(f"Available models: {len(models)}")
        for model in models:
            print(f"  - {model.get('name', 'unknown')}")
    else:
        print("Ollama server is not available")

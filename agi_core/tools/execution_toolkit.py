from __future__ import annotations

import json
from typing import Any, Dict, Iterable, List, Optional


class ToolCall:
    def __init__(self, name: str, arguments: Optional[Dict[str, Any]] = None):
        self.name = name
        self.arguments = arguments or {}

    def to_dict(self):
        return {"name": self.name, "arguments": self.arguments}


class ExecutionToolkit:
    """Ferramentas mínimas de execução e integração com APIs e shell."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def execute_python_snippet(self, snippet: str):
        # Execução segura apenas em ambiente controlado; sem runtime real em produção.
        ns: Dict[str, Any] = {"__builtins__": __builtins__}
        result = eval(snippet, ns, ns)
        self.history.append({"tool": "execute_python_snippet", "result": result})
        return result

    def call_http_get(self, url: str, timeout: int = 10):
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=timeout) as response:
                payload = response.read().decode("utf-8", errors="replace")
                self.history.append({"tool": "call_http_get", "url": url, "status": "ok", "payload": payload})
                return payload
        except Exception as exc:  # pragma: no cover
            self.history.append({"tool": "call_http_get", "url": url, "status": "error", "exception": str(exc)})
            return {"error": str(exc)}

    def call_json_tool(self, tool_name: str, payload: Dict[str, Any]):
        self.history.append({"tool": tool_name, "payload": payload})
        return {"tool": tool_name, "payload": payload}

    def summarize_history(self):
        return json.dumps(self.history, default=str)

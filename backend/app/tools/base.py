"""
Base tool interface and registry for agent tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from app.utils.logger import get_logger

logger = get_logger(__name__)


class AgentTool(ABC):
    """
    Base class for all agent tools.
    Tools are deterministic, fast operations the agent can call.
    """

    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs: Any) -> dict[str, Any]:
        """
        Execute the tool with given parameters.

        Returns:
            Dictionary with results and status
        """
        pass

    @staticmethod
    def _format_result(success: bool, data: Any, error: Optional[str] = None) -> dict[str, Any]:
        """Standardize tool result format."""
        return {
            "success": success,
            "data": data,
            "error": error,
        }


class ToolRegistry:
    """
    Central registry for agent tools.
    Manages tool registration, lookup, and execution.
    """

    def __init__(self):
        self._tools: dict[str, AgentTool] = {}

    def register(self, tool: AgentTool) -> None:
        """Register a tool in the registry."""
        if tool.name in self._tools:
            logger.warning("Overwriting existing tool: %s", tool.name)
        self._tools[tool.name] = tool
        logger.debug("Registered tool: %s", tool.name)

    def get(self, tool_name: str) -> Optional[AgentTool]:
        """Get a tool by name."""
        return self._tools.get(tool_name)

    async def execute(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:
        """
        Execute a tool by name.

        Returns:
            Result from tool execution
        """
        tool = self.get(tool_name)
        if not tool:
            logger.error("Tool not found: %s", tool_name)
            return AgentTool._format_result(False, None, f"Tool not found: {tool_name}")

        try:
            logger.debug("Executing tool: %s with params: %s", tool_name, kwargs)
            result = await tool.execute(**kwargs)
            return result
        except Exception as exc:
            logger.error("Tool execution failed: %s: %s", tool_name, exc, exc_info=True)
            return AgentTool._format_result(False, None, str(exc))

    def list_tools(self) -> list[dict[str, str]]:
        """List all registered tools with descriptions."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self._tools.values()
        ]

    def __len__(self) -> int:
        return len(self._tools)


# Global registry instance
_global_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create global tool registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = ToolRegistry()
    return _global_registry

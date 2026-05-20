"""
Tool registry initialization and management.
"""

from app.tools.base import get_tool_registry
from app.tools.knowledge_tools import SearchKnowledgeBaseTool
from app.tools.crm_tools import GetThreadHistoryTool, GetContactProfileTool, CheckAccountStatusTool
from app.tools.drafting_tools import DraftReplyTool
from app.tools.escalation_tools import EscalateToHumanTool, FlagForLegalTool, CreateInternalTicketTool
from app.tools.communication_tools import SendAutoReplyTool
from app.utils.logger import get_logger

logger = get_logger(__name__)


def initialize_tools() -> None:
    """Initialize and register all agent tools."""
    registry = get_tool_registry()

    # Knowledge tools
    registry.register(SearchKnowledgeBaseTool())

    # CRM tools
    registry.register(GetThreadHistoryTool())
    registry.register(GetContactProfileTool())
    registry.register(CheckAccountStatusTool())

    # Drafting tools
    registry.register(DraftReplyTool())

    # Escalation tools
    registry.register(EscalateToHumanTool())
    registry.register(FlagForLegalTool())
    registry.register(CreateInternalTicketTool())

    # Communication tools
    registry.register(SendAutoReplyTool())

    logger.info("✓ Initialized %d agent tools", len(registry))


# Initialize on import
initialize_tools()

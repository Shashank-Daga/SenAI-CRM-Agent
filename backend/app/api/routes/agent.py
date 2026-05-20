from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.agents.agent_executor import AgentExecutor
from app.schemas.email import StandardResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/dry-run/{email_id}", response_model=StandardResponse)
async def dry_run_agent(email_id: str, session: AsyncSession = Depends(get_db_session)) -> StandardResponse:
    """Run agent reasoning in dry-run mode without committing side effects."""
    logger.info("Dry-run agent requested for email %s", email_id)

    try:
        executor = AgentExecutor()
        result = await executor.execute(email_id=email_id, session=session, is_dry_run=True)
        return StandardResponse(
            success=True,
            message="Agent dry-run completed.",
            data=result.model_dump(),
        )
    except ValueError as exc:
        logger.warning("Dry-run agent failed: %s", exc)
        return StandardResponse(success=False, message=str(exc), error_code="email_not_found")
    except Exception as exc:
        logger.error("Dry-run agent exception: %s", exc, exc_info=True)
        return StandardResponse(
            success=False,
            message="Agent dry-run failed.",
            error_code="agent_dry_run_error",
            details={"error": str(exc)},
        )


@router.post("/execute/{email_id}", response_model=StandardResponse)
async def execute_agent(email_id: str, session: AsyncSession = Depends(get_db_session)) -> StandardResponse:
    """Execute agent reasoning and carry out actions for the email."""
    logger.info("Agent execution requested for email %s", email_id)

    try:
        executor = AgentExecutor()
        result = await executor.execute(email_id=email_id, session=session, is_dry_run=False)
        return StandardResponse(
            success=True,
            message="Agent execution completed.",
            data=result.model_dump(),
        )
    except ValueError as exc:
        logger.warning("Agent execution failed: %s", exc)
        return StandardResponse(success=False, message=str(exc), error_code="email_not_found")
    except Exception as exc:
        logger.error("Agent execution exception: %s", exc, exc_info=True)
        return StandardResponse(
            success=False,
            message="Agent execution failed.",
            error_code="agent_execution_error",
            details={"error": str(exc)},
        )

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from utils.auth_utils import get_current_user
from workflows.fundamental_workflow-v1 import fundamental_workflow
from models.fundamental_models import UserQuery, Executive_Summary
from core.logger_config import logger
from core.llm_cost import LLMCost
import time

router = APIRouter(tags=["Fundamentals"])
process_name = "Chat with Fundamentals"

# Endpoint
@router.post("/chat", response_model=Executive_Summary)
async def fundamentals_chat(
    request: UserQuery,
    user: str = Depends(get_current_user)
):
    logger.info(f"👤 Authenticated as: {user}")
    try:
        user_query = request.user_query  #  fixed here to use the correct attribute
        logger.info(f"User Query: {user_query}")

        start_time = time.time()

        # Run the fundamental analysis workflow
        result = fundamental_workflow.kickoff(inputs={"user_query": user_query})

        elapsed = time.time() - start_time
        logger.info(f"⏱️ Fundamental workflow executed in {elapsed:.2f} seconds")

        # Track token usage
        token_count = (
            fundamental_workflow.usage_metrics.prompt_tokens +
            fundamental_workflow.usage_metrics.completion_tokens
        )
        LLMCost.update_cost(process_name, token_count)
        logger.info(f"Token cost tracked for {token_count} tokens")

        return result.to_dict()

    except Exception as e:
        logger.error("Error in Chat with Fundamentals", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

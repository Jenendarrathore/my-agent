from fastapi import APIRouter

from .users import router as users_router
from .categories import router as categories_router
from .connected_accounts import router as connected_accounts_router
from .transactions import router as transactions_router
from .emails import router as emails_router
from .email_extractions import router as email_extractions_router
from .jobs import router as jobs_router
from .llm_transactions import router as llm_transactions_router
from .google_auth import router as google_auth_router
from .roles import router as roles_router

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(categories_router)
router.include_router(connected_accounts_router)
router.include_router(transactions_router)
router.include_router(emails_router)
router.include_router(email_extractions_router)
router.include_router(jobs_router)
router.include_router(llm_transactions_router)
router.include_router(google_auth_router)
router.include_router(roles_router)
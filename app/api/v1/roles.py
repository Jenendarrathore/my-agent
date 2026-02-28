from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse
from app.services.role_service import RoleService
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_in: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new role.
    """
    service = RoleService(db)
    try:
        return await service.create_role(role_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RoleResponse])
async def read_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all roles.
    """
    service = RoleService(db)
    return await service.list_roles(skip=skip, limit=limit)


@router.get("/{role_id}", response_model=RoleResponse)
async def read_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific role by ID.
    """
    service = RoleService(db)
    role = await service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.patch("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a role.
    """
    service = RoleService(db)
    try:
        return await service.update_role(role_id, role_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a role.
    """
    service = RoleService(db)
    success = await service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return None

from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.token import AccessTokenResponse, RefreshRequest, TokenResponse
from app.schemas.user import RegisterRequest, LoginRequest, UserResponse
from app.services.auth_service import login_user, refresh_access_token, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest):
    user = await register_user(data)
    return UserResponse(id=str(user.id), email=user.email, is_active=user.is_active)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    return await login_user(data)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(data: RefreshRequest):
    new_access_token = await refresh_access_token(data.refresh_token)
    return AccessTokenResponse(access_token=new_access_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
    )

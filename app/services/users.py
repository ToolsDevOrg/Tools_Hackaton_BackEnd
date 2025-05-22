from datetime import datetime, timedelta, timezone
import string
from app.dependencies.unitofwork import UnitOfWork
from app.dependencies.users import authenticate_user, create_access_token, create_refresh_token, get_password_hash
from app.exceptions.users.exceptions import InvalidTokenExc, TokenExpiredExc, UserAlreadyExistsExc, UserNotFoundExc
from app.models.users import RefreshSession, User
from app.schemas.users import SUserCreate, SUserLogin, UserTokens
from fastapi import Request, Response
from app.config.main import settings

class UsersService:
    
    async def register_user(self, uow: UnitOfWork, user_data: SUserCreate, response: Response) -> User:
        async with uow:
            find_user: User | None = await uow.users.find_one_or_none(email=user_data.email)
            if find_user:
                raise UserAlreadyExistsExc
            
            new_user: User = await uow.users.insert_by_data(user_data.model_dump())
            
            access_token = create_access_token(user_id=new_user.id)
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            refresh_token = create_refresh_token()

            await uow.refresh_session.insert_by_data(
                {
                    "refresh_token": refresh_token,
                    "expires_in": refresh_token_expires.total_seconds(),
                    "user_id": new_user.id,
                }
            )

            response.set_cookie(
                "access_token",
                access_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                samesite=settings.COOKIE_SAMESITE,
                secure=settings.COOKIE_SECURE,
                httponly=True,
            )
            response.set_cookie(
                "refresh_token",
                refresh_token,
                max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
                samesite=settings.COOKIE_SAMESITE,
                secure=settings.COOKIE_SECURE,
                httponly=True,
            )
            hashed_password = get_password_hash(user_data.password)

            await uow.users.update_by_filter(
                {"password": hashed_password}, id=new_user.id
            )
                    
            await uow.commit()
            return new_user
    
        
    async def login(self, uow: UnitOfWork, user_data: SUserLogin, response: Response) -> User:
        async with uow:
            find_user: User | None = await uow.users.find_one_or_none(email=user_data.email)
            if not find_user:
                raise UserNotFoundExc
            
            user = await authenticate_user(uow, user_data.email, user_data.password)
            
            access_token = create_access_token(user_id=user.id)
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            refresh_token = create_refresh_token()
            
            await uow.refresh_session.insert_by_data(
                {
                    "refresh_token": refresh_token,
                    "expires_in": refresh_token_expires.total_seconds(),
                    "user_id": user.id,
                }
            )
            
            response.set_cookie(
                "access_token",
                access_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                samesite=settings.COOKIE_SAMESITE,
                secure=settings.COOKIE_SECURE,
                httponly=True,
            )
            
            response.set_cookie(
                "refresh_token",
                refresh_token,
                max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
                samesite=settings.COOKIE_SAMESITE,
                secure=settings.COOKIE_SECURE,
                httponly=True,
            )
            
            await uow.commit()
            return user

    
    async def refresh_token(self, uow: UnitOfWork, response: Response, request: Request) -> UserTokens:
        """Обновить access_token"""
        try:
            async with uow:
                refresh_session: RefreshSession = await uow.refresh_session.find_one_or_none(
                    refresh_token=request.cookies.get("refresh_token")
                )

                if refresh_session is None:
                    raise InvalidTokenExc
                if datetime.now(timezone.utc) >= refresh_session.created_at + timedelta(
                    seconds=refresh_session.expires_in
                ):
                    await uow.refresh_session.delete_by_filter(id=refresh_session.id)
                    await uow.commit()
                    raise TokenExpiredExc

                user: User = await uow.users.find_one_or_none(id=refresh_session.user_id)
                if not user:
                    raise InvalidTokenExc

                access_token = create_access_token(user.id)
                refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
                refresh_token = create_refresh_token()

                await uow.refresh_session.update_session(
                    refresh_session_id=refresh_session.id,
                    refresh_token=refresh_token,
                    expires_in=refresh_token_expires.total_seconds(),
                )

                response.set_cookie(
                    "access_token",
                    access_token,
                    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    samesite=settings.COOKIE_SAMESITE,
                    secure=settings.COOKIE_SECURE,
                    httponly=True,
                )
                response.set_cookie(
                    "refresh_token",
                    refresh_token,
                    max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
                    samesite=settings.COOKIE_SAMESITE,
                    secure=settings.COOKIE_SECURE,
                    httponly=True,
                )
                await uow.commit()
                return UserTokens(access_token=access_token, refresh_token=refresh_token)

        except InvalidTokenExc:
            raise InvalidTokenExc
        except TokenExpiredExc:
            raise TokenExpiredExc
        
        
    async def logout(self, uow: UnitOfWork, response: Response, request: Request) -> None:
        """Выйти из компании"""
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        async with uow:
            refresh_session: RefreshSession = await uow.refresh_session.find_one_or_none(
                refresh_token=request.cookies.get("refresh_token")
            )
            if refresh_session:
                await uow.refresh_session.delete_by_filter(id=refresh_session.id)
                await uow.commit()
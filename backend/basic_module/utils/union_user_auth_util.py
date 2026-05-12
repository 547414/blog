import os

import toml
from fastapi import Depends, HTTPException, Request
from dependency_injector.wiring import inject, Provide

from basic.api_response.api_response import ApiResponse
from basic.repository.unit_of_work import UnitOfWork
from basic_module import BasicModuleContainer
from basic_module.service.union_user_service import UnionUserService

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.join(PATH, "../")
APP_CONFIG = toml.load(fr"{BASE_PATH}app_config.toml")
ACTIVE = APP_CONFIG.get('settings', {}).get('active', 'development')
CONFIG_NAME = f'app_{ACTIVE}_config.toml'
CONFIG = toml.load(fr"{BASE_PATH}config/{CONFIG_NAME}")


@inject
def optional_validate_token(
        request: Request,
        uow: UnitOfWork = Depends(Provide[BasicModuleContainer.unit_of_work]),
        union_user_service: UnionUserService = Depends(Provide[BasicModuleContainer.union_user_service])
):
    """尝试验证 token，无 token 或 token 无效时返回 None，不抛异常"""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    try:
        token_value = token.split(" ")[1]
        scene = request.headers.get("Scene", "DEFAULT")
        space = request.headers.get("Space", "DEFAULT")
        with uow:
            return union_user_service.validate_token(
                token=token_value,
                url=request.url.path,
                space=space,
                scene=scene,
            )
    except Exception:
        return None


@inject
def validate_token(
        request: Request,
        uow: UnitOfWork = Depends(Provide[BasicModuleContainer.unit_of_work]),
        union_user_service: UnionUserService = Depends(Provide[BasicModuleContainer.union_user_service])
):
    with uow:
        # ignore_auth = union_user_service.check_backend_api_ignore(
        #     url=request.url.path,
        # )
        # if ignore_auth:
        #     return

        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail=ApiResponse(code=40131, message="令牌缺失").to_json())

        token_value = token.split(" ")[1]

        scene = request.headers.get("Scene", "DEFAULT")
        space = request.headers.get("Space", "DEFAULT")

        return union_user_service.validate_token(
            token=token_value,
            url=request.url.path,
            space=space,
            scene=scene,
        )

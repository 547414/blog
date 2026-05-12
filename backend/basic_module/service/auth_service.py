import logging
import os
import toml

from basic.error.base_error import BusinessError
from basic.redis_client.redis_client import RedisClient
from basic_module.model.auth_model import EnumSpace
from basic_module.model.role_model import EnumRoleCode
from basic_module.model.union_user_user_model import EnumUnionUserCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.service.storage_service import StorageService
from basic_module.service.union_user_service import UnionUserService

logger = logging.getLogger('auth_service')


class AuthService:
    def __init__(
            self,
            redis_client: RedisClient,
            union_user_service: UnionUserService,
            storage_service: StorageService,
    ):
        self.__redis_client = redis_client
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__union_user_service = union_user_service
        self.__storage_service = storage_service
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")
        if not os.path.exists(f"{self.__base_path}/temp"):
            os.makedirs(f"{self.__base_path}/temp")

    @staticmethod
    def check_is_super_admin(
            space: str = 'WEB',
            current_user_info: ValidateTokenResModel = None
    ):
        passed = False
        if space == EnumSpace.WEB.value:
            for user in current_user_info.union_user_info.user_list:
                if user.union_user_user_category == EnumUnionUserCategory.WEB_USER.value:
                    if user.current_role_code == EnumRoleCode.SUPER_ADMIN.value:
                        passed = True
        if not passed:
            raise BusinessError('禁止此操作, 仅超级管理员可以操作')

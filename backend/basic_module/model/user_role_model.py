from enum import Enum

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class EnumUserRoleCategory(Enum):
    WEB_USER = "WEB_USER"

    def __str__(self):
        labels = {
            EnumUserRoleCategory.WEB_USER: "用户",
        }
        return labels[self]


class UserRoleModel(BasicVersionModel):
    user_id: str = Field(..., description="用户id")
    user_category: EnumUserRoleCategory = Field(..., description="用户类型，企微用户、用户")
    role_id: str = Field(..., description="角色id")


class UserRoleViewModel(BasicVersionModel):
    user_id: str = Field(..., description="用户id")
    user_category: EnumUserRoleCategory = Field(..., description="用户类型，企微用户、用户")
    role_id: str = Field(..., description="角色id")
    role_code: str = Field(..., description="角色编码")

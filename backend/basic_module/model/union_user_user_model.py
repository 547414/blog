from enum import Enum

from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class EnumUnionUserCategory(Enum):
    WEB_USER = "WEB_USER"

    def __str__(self):
        labels = {
            EnumUnionUserCategory.WEB_USER: "web用户",
        }
        return labels[self]


class UnionUserUserModel(BasicVersionModel):
    union_user_id: str = Field(..., description="联合用户ID")
    union_user_user_category: str = Field(..., description="联合用户类别")
    union_user_user_id: str = Field(..., description="联合用户用户ID")

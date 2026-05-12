from enum import Enum
from typing import Optional

from pydantic import Field

from basic.model.basic_model import BasisModel
from basic_module.model.union_user_model import UnionUserInfoModel


class EnumUserCategory(Enum):
    WEB_USER = "WEB_USER"
    UNION_USER = "UNION_USER"

    def __str__(self):
        labels = {
            EnumUserCategory.WEB_USER: "web用户",
            EnumUserCategory.UNION_USER: "联合用户"
        }
        return labels[self]


class JwtPayloadInfo(BasisModel):
    exp: Optional[int] = Field(None, description="过期时间")
    union_user_info: Optional[UnionUserInfoModel] = Field(None, description="联合用户信息")


class EnumSpace(Enum):
    WEB = "WEB"

    def __str__(self):
        labels = {
            EnumSpace.WEB: "Web",
        }
        return labels[self]

    def __covert__(self):
        labels = {
            EnumSpace.WEB: "WEB_USER",
        }
        return labels[self]

import secrets
import string


class ToolsService:
    def __init__(
            self,
    ):
        self.__charset = string.ascii_letters + string.digits

    # 生成一个指定长度的密钥，确保包含大写字母、小写字母和数字
    def generate_secure_key(self, length=32):
        while True:
            key = ''.join(secrets.choice(self.__charset) for _ in range(length))
            if (any(c.islower() for c in key) and
                    any(c.isupper() for c in key) and
                    any(c.isdigit() for c in key)):
                return key

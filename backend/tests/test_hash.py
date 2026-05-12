import hashlib
import secrets


def test_generate_hash_with_salt():
    input_string = "wiwj1314"
    # 随机生成 16 字节的 salt
    salt = secrets.token_hex(16)
    # 创建 SHA-256 哈希对象
    sha256_hash = hashlib.sha256()
    # 将输入字符串和 salt 组合并编码，然后更新哈希对象
    sha256_hash.update((input_string + salt).encode('utf-8'))
    # 生成哈希值的十六进制表示
    hash_value = sha256_hash.hexdigest()
    print(f"Salt: {salt}")
    print(f"SHA-256 Hash with salt: {hash_value}")

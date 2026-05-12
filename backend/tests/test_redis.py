import redis


def test_redis():
    # 连接到 Redis 服务器，假设服务器在本地，端口为 6379
    # 并且已设置密码 'yourpassword'
    r = redis.Redis(host='localhost', port=6378, password='g9kw3ndguim63dfaslgmqp86m3')

    # 测试连接是否成功
    try:
        # 设置一个键值对
        r.set('name', 'OpenAI')

        # 获取这个键的值
        value = r.get('name')
        print(f"The value of 'name' is: {value.decode('utf-8')}")  # 将 bytes 转换为字符串

        # 验证连接是否成功
        if r.ping():
            print("Successfully connected to Redis!")
    except redis.AuthenticationError:
        print("Authentication failed: Incorrect Redis password.")
    except redis.ConnectionError:
        print("Failed to connect to Redis.")

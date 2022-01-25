###SMS####
TENCENT_SMS_APP_ID = 1400623982
TENCENT_SMS_APP_KEY = 'c5c748ffb74a8d3f9a7f1c16b0c0bb38'
TENCENT_SMS_APP_SIGN = '是一个好人公众号'
TENCENT_SMS_TEMPLATE = {
    'register': 1284580,
    'login': 1284581,
    'rest': 1284582,
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://42.193.150.217:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "Root123+" # redis密码
        }
    }
}



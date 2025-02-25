import redis

# Redis连接配置
r = redis.Redis(
    host='redis-10243.c9.us-east-1-2.ec2.redns.redis-cloud.com',
    port=10243,
    decode_responses=True,
    username="default",
    password="x1JA7OdNnZtnbj5K1eTFzb85ls09Vh6E"
)

# 测试连接
try:
    success = r.set('foo', 'bar')
    print("写入成功:", success)
    
    result = r.get('foo')
    print("读取结果:", result)
except Exception as e:
    print("连接失败:", e)
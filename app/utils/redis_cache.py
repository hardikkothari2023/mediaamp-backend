import redis
import json
import os
from datetime import timedelta
 
redis_client = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=int(os.environ.get("REDIS_DB", 0)),
    decode_responses=True   
)
 
def cache_tasks_for_date(date_str, tasks):
    key = f"tasks:{date_str}"
    redis_client.setex(key, timedelta(hours=1), json.dumps(tasks))  
 
def get_cached_tasks(date_str):
    key = f"tasks:{date_str}"
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None

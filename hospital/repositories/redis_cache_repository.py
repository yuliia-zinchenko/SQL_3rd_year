import redis
import json
import time
from datetime import date

class RedisCacheRepository:
    def __init__(self, sql_retriever_func):

        self.redis_client = redis.Redis(decode_responses=True)
        self.sql_retriever_func = sql_retriever_func

    def get_doctor_schedule(self, doctor_id):

        today = date.today().isoformat()
        cache_key = f"doctor:{doctor_id}:schedule:{today}"

        cached_schedule = self.redis_client.get(cache_key)
        
        if cached_schedule:
            print(f"Redis: Schedule for doctor {doctor_id} FOUND IN CACHE!")
            return json.loads(cached_schedule)
        else:
            print(f"Redis: Schedule for doctor {doctor_id} NOT in cache.")
            schedule = self.sql_retriever_func(doctor_id)

            self.redis_client.set(cache_key, json.dumps(schedule), ex=3600)
            
            return schedule

def get_doctor_schedule_from_sql_db(doctor_id):
    print(f"PostgreSQL: Fetching schedule for doctor {doctor_id} from DB (SLOW)...")
    time.sleep(0.5) 
    return [
        {"time": "10:00", "patient": "John Doe", "status": "scheduled"},
        {"time": "10:30", "patient": "Jane Smith", "status": "scheduled"}
    ]
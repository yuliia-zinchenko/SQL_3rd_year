import time
import random
from tqdm import tqdm 


from hospital.repositories.mongo_observation_repository import ObservationRepository
from hospital.repositories.sql_observation_repository import SqlObservationRepository

from hospital.database.connection import get_db_connection

def populate_data(count=10000):
    print(f"--- Populating {count} records for performance test ---")
    mongo_repo = ObservationRepository(use_local=True)
    
    sql_conn = get_db_connection()
    sql_repo = SqlObservationRepository(sql_conn)

    for i in tqdm(range(1, count+1)):
        test_results = { "param_" + str(j): random.random() for j in range(10) }
        

        mongo_repo.add_observation(i, "perf_test", test_results)
        
        sql_repo.add_observation(i, test_results)
    
    sql_conn.commit()
    sql_conn.close()
    print("--- Data population complete ---")

def run_read_performance_test(reads=1000, max_id=10000):
    print(f"\n--- Running READ performance test ({reads} reads) ---")

    mongo_repo = ObservationRepository(use_local=True) 
    sql_conn = get_db_connection()
    sql_repo = SqlObservationRepository(sql_conn)

    mongo_times = []
    print("Testing MongoDB reads...")
    for _ in tqdm(range(reads)):
        record_id = random.randint(1, max_id)
        start_time = time.perf_counter()
        mongo_repo.get_observations_by_record_id(record_id)
        end_time = time.perf_counter()
        mongo_times.append(end_time - start_time)
    
    postgres_times = []
    print("Testing PostgreSQL reads...")
    for _ in tqdm(range(reads)):
        record_id = random.randint(1, max_id)
        start_time = time.perf_counter()
        sql_repo.get_observations_by_record_id(record_id)
        end_time = time.perf_counter()
        postgres_times.append(end_time - start_time)
    
    sql_conn.close()


    avg_mongo_ms = (sum(mongo_times) / len(mongo_times)) * 1000
    avg_postgres_ms = (sum(postgres_times) / len(postgres_times)) * 1000
    
    print("\n--- READ Test Results ---")
    print(f"MongoDB (Local) average read time:      {avg_mongo_ms:.4f} ms")
    print(f"PostgreSQL (Local) average read time: {avg_postgres_ms:.4f} ms")
    
    if avg_mongo_ms < avg_postgres_ms:
        print(f"--> MongoDB was {avg_postgres_ms / avg_mongo_ms:.2f} times faster for reads.")
    else:
        print(f"--> PostgreSQL was {avg_mongo_ms / avg_postgres_ms:.2f} times faster for reads.")

def run_write_performance_test(writes=1000, max_id=10000):
    print(f"\n--- Running WRITE performance test ({writes} writes) ---")

    mongo_repo = ObservationRepository(use_local=True)
    sql_conn = get_db_connection()
    sql_repo = SqlObservationRepository(sql_conn)

    mongo_times = []
    print("Testing MongoDB writes (updates)...")
    for _ in tqdm(range(writes)):
        record_id = random.randint(1, max_id)
        test_data = {"updated_param": random.random()}
        start_time = time.perf_counter()

        mongo_repo.collection.update_one({'record_id': record_id}, {'$set': {'results': test_data}})
        end_time = time.perf_counter()
        mongo_times.append(end_time - start_time)
    
    postgres_times = []
    print("Testing PostgreSQL writes (updates)...")
    for _ in tqdm(range(writes)):
        record_id = random.randint(1, max_id)
        test_data = {"updated_param": random.random()}
        start_time = time.perf_counter()
        sql_repo.add_observation(record_id, test_data)
        end_time = time.perf_counter()
        postgres_times.append(end_time - start_time)
        
    sql_conn.commit() 
    sql_conn.close()

    avg_mongo_ms = (sum(mongo_times) / len(mongo_times)) * 1000
    avg_postgres_ms = (sum(postgres_times) / len(postgres_times)) * 1000

    print("\n--- WRITE Test Results ---")
    print(f"MongoDB (Local) average write time:      {avg_mongo_ms:.4f} ms")
    print(f"PostgreSQL (Local) average write time: {avg_postgres_ms:.4f} ms")

    if avg_mongo_ms < avg_postgres_ms:
        print(f"--> MongoDB was {avg_postgres_ms / avg_mongo_ms:.2f} times faster for writes.")
    else:
        print(f"--> PostgreSQL was {avg_mongo_ms / avg_postgres_ms:.2f} times faster for writes.")



if __name__ == '__main__':

    
    #populate_data()

    #run_read_performance_test()
    run_write_performance_test()
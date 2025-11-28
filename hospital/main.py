import time
from hospital.repositories.mongo_observation_repository import ObservationRepository
from hospital.repositories.redis_cache_repository import RedisCacheRepository, get_doctor_schedule_from_sql_db
from hospital.unit_of_work.unit_of_work import UnitOfWork
from datetime import date, datetime

def demonstrate_mongodb_usage():

    print("\n--- Testing MongoDB Integration ---")
    mongo_repo = ObservationRepository()
    

    blood_test_results = {
        "hemoglobin": {"value": 145, "unit": "g/L"},
        "leukocytes": {"value": 7.2, "unit": "10^9/L"}
    }
    

    record_id_from_sql = 1
    mongo_repo.add_observation(
        record_id=record_id_from_sql,
        observation_type="blood_analysis",
        results=blood_test_results,
        notes="Patient condition is stable."
    )
    
    observations = mongo_repo.get_observations_by_record_id(record_id_from_sql)
    print("\nFetched observations from MongoDB:")
    for obs in observations:

        obs.pop('_id', None) 
        print(obs)

def demonstrate_redis_cache():

    print("\n--- Testing Redis Cache Integration ---")

    cache_repo = RedisCacheRepository(sql_retriever_func=get_doctor_schedule_from_sql_db)
    
    doctor_id = 1
    
    print("\n[First Request] Getting schedule for doctor...")
    start_time = time.time()
    schedule1 = cache_repo.get_doctor_schedule(doctor_id)
    print(f"Schedule: {schedule1}")
    print(f"Time taken: {time.time() - start_time:.4f} seconds.")
    
    print("\n[Second Request] Getting same schedule again...")
    start_time = time.time()
    schedule2 = cache_repo.get_doctor_schedule(doctor_id)
    print(f"Schedule: {schedule2}")
    print(f"Time taken: {time.time() - start_time:.4f} seconds.")
    print("Notice the second request was much faster and didn't query the SQL DB.")

def register_patient_and_schedule_appointment():
    try:
        with UnitOfWork() as uow:
            print("Creating a new patient...")
            current_user_id = 1
            
            new_patient_id = uow.patients.add(
                first_name='John',
                last_name='Doe',
                date_of_birth=date(1990, 5, 15),
                user_id=current_user_id
            )
            print(f"Patient created with ID: {new_patient_id}")

            appointment_id = uow.appointments.add(
                patient_id=new_patient_id,
                doctor_id=1,
                appointment_date=datetime(2025, 11, 10, 10, 30),
                user_id=current_user_id
            )
            print(f"Appointment scheduled with ID: {appointment_id}")

            print("\nTransaction completed successfully!")

    except Exception as e:
        print(f"\nAn error occurred. Transaction rolled back. Error: {e}")

def view_active_appointments():
    with UnitOfWork() as uow:
        print("\n--- Active Appointments (from View) ---")
        appointments = uow.appointments.get_active_appointments()
        if not appointments:
            print("No active appointments found.")
            return
            
        for app in appointments:
            print(
                f"ID: {app['appointment_id']}, "
                f"Date: {app['appointment_date']}, "
                f"Patient: {app['patient_first_name']} {app['patient_last_name']}, "
                f"Doctor: {app['doctor_first_name']} {app['doctor_last_name']} "
                f"({app['specialization']})"
            )

if __name__ == "__main__":
    while True:
        print("\n--- Hospital System Main Menu ---")
        print("1. [SQL] Register Patient and Schedule Appointment")
        print("2. [SQL] View Active Appointments")
        print("3. [NoSQL] Demonstrate MongoDB Usage")
        print("4. [NoSQL] Demonstrate Redis Cache")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            register_patient_and_schedule_appointment()
        elif choice == '2':
            view_active_appointments()
        elif choice == '3':
            demonstrate_mongodb_usage()
        elif choice == '4':
            demonstrate_redis_cache()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
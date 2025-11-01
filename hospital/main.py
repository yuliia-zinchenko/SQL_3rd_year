from hospital.unit_of_work.unit_of_work import UnitOfWork
from datetime import date, datetime

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
        print("\n--- Hospital Management System ---")
        print("1. Register a new patient and schedule an appointment")
        print("2. View all active appointments")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            register_patient_and_schedule_appointment()
        elif choice == '2':
            view_active_appointments()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
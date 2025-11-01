from hospital.database.connection import get_db_connection
from hospital.repositories.patient_repository import PatientRepository
from hospital.repositories.appointment_repository import AppointmentRepository

class UnitOfWork:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = get_db_connection()
        self.connection.autocommit = False 
        self.patients = PatientRepository(self.connection)
        self.appointments = AppointmentRepository(self.connection)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
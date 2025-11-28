from hospital.repositories.base_repository import BaseRepository
import psycopg2.extras

class AppointmentRepository(BaseRepository):
    def add(self, patient_id, doctor_id, appointment_date, user_id):
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO Appointments (patient_id, doctor_id, appointment_date, status, updated_by)
                VALUES (%s, %s, %s, 'scheduled', %s) RETURNING appointment_id;
            """
            cursor.execute(sql, (patient_id, doctor_id, appointment_date, user_id))
            appointment_id = cursor.fetchone()[0]
            return appointment_id

    def get_active_appointments(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT * FROM v_active_appointments;")
            return cursor.fetchall()
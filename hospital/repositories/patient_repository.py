import psycopg2
from hospital.repositories.base_repository import BaseRepository

class PatientRepository(BaseRepository):
    def add(self, first_name, last_name, date_of_birth, user_id):
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO Patients (first_name, last_name, date_of_birth, updated_by)
                VALUES (%s, %s, %s, %s) RETURNING patient_id;
            """
            cursor.execute(sql, (first_name, last_name, date_of_birth, user_id))
            patient_id = cursor.fetchone()[0]
            return patient_id

    def get_by_id(self, patient_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql = "SELECT * FROM Patients WHERE patient_id = %s AND is_deleted = false;"
            cursor.execute(sql, (patient_id,))
            return cursor.fetchone()

    def soft_delete(self, patient_id, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("CALL sp_soft_delete_patient(%s, %s);", (patient_id, user_id))
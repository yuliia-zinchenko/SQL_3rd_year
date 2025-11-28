import json
import psycopg2.extras
from .base_repository import BaseRepository

class SqlObservationRepository(BaseRepository):
    def add_observation(self, record_id, observation_data):

        with self.connection.cursor() as cursor:

            sql = """
                UPDATE Medical_Records
                SET observations = %s
                WHERE record_id = %s;
            """
            cursor.execute(sql, (json.dumps(observation_data), record_id))
            print(f"PostgreSQL: Observation for record_id {record_id} updated.")

    def get_observations_by_record_id(self, record_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            sql = "SELECT observations FROM Medical_Records WHERE record_id = %s;"
            cursor.execute(sql, (record_id,))
            result = cursor.fetchone()
            print(f"PostgreSQL: Fetching observations for record_id {record_id}.")
            return result['observations'] if result and result['observations'] else None
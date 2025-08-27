# db.py
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv

# ---------------- Database Connection ----------------
class Database:
    """
    Handles connections to the PostgreSQL database using environment variables.

    Environment variables (from .env):
        DATABASE_NAME      - Database name (default: photosift)
        DATABASE_USERNAME  - Database username (default: postgres)
        DATABASE_PASSWORD  - Database password (default: postgres)
        DATABASE_HOST      - Host (default: localhost)
        DATABASE_PORT      - Port (default: 5432)

    Example:
        db = Database()
        results = db.execute_query("SELECT * FROM users WHERE user_id = %s;", (1,))
        print(results)
    """

    def __init__(self):
        load_dotenv(find_dotenv())
        
        self.dbname = os.getenv("DATABASE_NAME", "photosift")
        self.user = os.getenv("DATABASE_USERNAME", "postgres")
        self.password = os.getenv("DATABASE_PASSWORD", "postgres")
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = os.getenv("DATABASE_PORT", "5432")

    def get_connection(self):
        """Get a new psycopg2 database connection."""
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def execute_query(self, query, params=None):
        """
        Execute a query and return all results as a list of dictionaries.

        Args:
            query (str): SQL query to execute.
            params (tuple, optional): Parameters for the SQL query.

        Returns:
            list[dict] | None: Results of the query or None if no results.

        Example:
            db = Database()
            users = db.execute_query("SELECT * FROM users;")
            print(users)
        """
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)

        rows = cur.fetchall() if cur.description else None

        conn.commit()
        cur.close()
        conn.close()
        return rows
    
    def execute_sql_script(self, script_path):
        """
        Execute a SQL script from a file.

        Args:
            script_path (str): Path to the SQL file.

        Returns:
            Query results (if any).
        
        Example:
            db = Database()
            db.execute_sql_script("sql/create_tables.sql")
        """
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"SQL script not found: {script_path}")
        
        with open(script_path, 'r') as file:
            sql_script = file.read()
        
        return self.execute_query(sql_script)

    def init_db(self):
        """
        Initialize the database by creating necessary tables
        and inserting a test user.
        """
        self.execute_sql_script('sql/create_tables.sql')
        self.execute_sql_script('sql/populate_test_user.sql')
        """
        Create a new score record for a photo.

        Args:
            photo_id (int): The ID of the photo.
            metric_name (str): The name of the metric (e.g., 'sharpness', 'exposure').
            value (float): The value of the metric.

        Returns:
            dict: The created score record.
        """
        query = """
            INSERT INTO scores (photo_id, metric_name, value)
            VALUES (%s, %s, %s)
            RETURNING *;
            """
        params = (photo_id, metric_name, value)
        result = self.execute_query(query, params)
        return result[0] if result else None

        """
        Create a full collection with associated photos and their scores.

        Args:
            user_ids (list[int]): List of user IDs to associate with the collection.
            collection_name (str): The name of the collection.
            collection_description (str): A description of the collection.
            photos_data (list[dict]): List of photo data dictionaries, each containing:
                - original_path (str): Path to the original photo.
                - thumbnail_path (str): Path to the thumbnail image.
                - scores (dict): Dictionary of metric names to values.

        Returns:
            dict: The created collection record with associated photos and scores.
        """
        # Create the collection for each user
        collections = []
        for user_id in user_ids:
            collection = self.create_collection_record(user_id, collection_name, collection_description)
            if collection:
                collections.append(collection)

                # Create photos and their scores
                for photo in photos_data:
                    photo_record = self.create_photo_record(
                        collection['collection_id'],
                        photo['original_path'],
                        photo['thumbnail_path']
                    )
                    if photo_record and 'scores' in photo:
                        for metric_name, value in photo['scores'].items():
                            self.create_score_record(photo_record['photo_id'], metric_name, value)

        return collections

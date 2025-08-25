# db.py
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv


# ---------------- Database Connection ----------------
class Database:
    def __init__(self):
        load_dotenv()
        
        self.dbname = os.getenv("DATABASE_NAME", "photosift")
        self.user = os.getenv("DATABASE_USERNAME", "postgres")
        self.password = os.getenv("DATABASE_PASSWORD", "postgres")
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = os.getenv("DATABASE_PORT", "5432")

    def get_connection(self):
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
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to pass to the SQL query.
        Returns:
            list: A list of dictionaries representing the query results.
        """
        ## Get a connection from this database instance
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        ## Execute the query with parameters if provided
        if params is None:
            cur.execute(query)
        else:
            cur.execute(query, params)

        if cur.description:  # Only fetch if there are results
            rows = cur.fetchall()
        else:
            rows = None

        ## Clean up
        conn.commit()
        cur.close()
        conn.close()

        ## Return the fetched rows
        return rows
    
    def execute_sql_script(self, script_path):
        """
        Execute a SQL script from a file.
        Args:
            script_path (str): The path to the SQL script file.

        Returns:
            Returns the result of the executed script.
        """
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"SQL script not found: {script_path}")
        
        with open(script_path, 'r') as file:
            sql_script = file.read()
        
        return self.execute_query(sql_script)

    def init_db(self):
        ## Initialize the database by creating necessary tables from 'sql/create_tables.sql'
        self.execute_sql_script('sql/create_tables.sql')
        self.execute_sql_script('sql/populate_test_user.sql')


# ---------------- Generic Base Model ----------------
class BaseModel:

    """
    Base model class for database operations.
    """
    def __init__(self, db: Database, table_name: str, pk: str):
        self.db = db
        self.table_name = table_name
        self.pk = pk

    def create(self, **kwargs):
        keys = ", ".join(kwargs.keys())
        values_placeholders = ", ".join(["%s"] * len(kwargs))
        values = tuple(kwargs.values())
        query = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values_placeholders}) RETURNING *;"
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, values)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result

    def get(self, id_value):
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.pk}=%s;", (id_value,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def update(self, id_value, **kwargs):
        set_clause = ", ".join([f"{k}=%s" for k in kwargs])
        values = tuple(kwargs.values()) + (id_value,)
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk}=%s RETURNING *;"
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, values)
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return result

    def delete(self, id_value):
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE {self.pk}=%s;", (id_value,))
        conn.commit()
        cur.close()
        conn.close()
        return True

    def list_all(self):
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {self.table_name};")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    


# ---------------- Table Classes ----------------
class User(BaseModel):
    def __init__(self, db):
        super().__init__(db, "users", "user_id")

class Collection(BaseModel):
    def __init__(self, db):
        super().__init__(db, "collections", "collection_id")

class Photo(BaseModel):
    def __init__(self, db):
        super().__init__(db, "photos", "photo_id")

class Thumbnail(BaseModel):
    def __init__(self, db):
        super().__init__(db, "thumbnails", "thumbnail_id")

class ExifData(BaseModel):
    def __init__(self, db):
        super().__init__(db, "exif_data", "photo_id")  # photo_id is PK here

class Score(BaseModel):
    def __init__(self, db):
        super().__init__(db, "scores", "score_id")

class Face(BaseModel):
    def __init__(self, db):
        super().__init__(db, "faces", "face_id")

class ImageComment(BaseModel):
    def __init__(self, db):
        super().__init__(db, "image_comments", "image_comment_id")

class CollectionComment(BaseModel):
    def __init__(self, db):
        super().__init__(db, "collection_comments", "collection_comment_id")

class NearDuplicateGroup(BaseModel):
    def __init__(self, db):
        super().__init__(db, "near_duplicate_groups", "group_id")

class NearDuplicatePhoto(BaseModel):
    def __init__(self, db):
        super().__init__(db, "near_duplicate_photos", "photo_id")  # composite PK, handle carefully

class Camera(BaseModel):
    def __init__(self, db):
        super().__init__(db, "cameras", "camera_id")



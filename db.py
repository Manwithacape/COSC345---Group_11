# db.py
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv


# ---------------- Database Connection ----------------
class Database:
    """
    Handles connections to the PostgreSQL database using environment variables.

    SEE `DB Connection instructions.md` for setup details.

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


# ---------------- Generic Base Model ----------------
class BaseModel:
    """
    Generic base model class that provides CRUD operations
    for a given table.

    Args:
        db (Database): Instance of Database.
        table_name (str): Table name in the database.
        pk (str): Primary key column name.

    Example:
        db = Database()
        users = User(db)
        new_user = users.create(name="Alice")
        print(new_user)
    """

    def __init__(self, db: Database, table_name: str, pk: str):
        self.db = db
        self.table_name = table_name
        self.pk = pk

    def create(self, **kwargs):
        """Insert a new record and return it."""
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
        """Retrieve a record by primary key."""
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.pk}=%s;", (id_value,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def update(self, id_value, **kwargs):
        """
        **kwargs - Key Word Arguments - for dynamic col setting
        Update a record and return the updated row."""
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
        """Delete a record by primary key."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {self.table_name} WHERE {self.pk}=%s;", (id_value,))
        conn.commit()
        cur.close()
        conn.close()
        return True

    def list_all(self):
        """Return all rows in the table."""
        conn = self.db.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {self.table_name};")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    

# ---------------- Table Classes ----------------
class User(BaseModel):
    """Table model for `users` table (PK: user_id)."""
    def __init__(self, db):
        super().__init__(db, "users", "user_id")

    # Example usage:
    # db = Database()
    # users = User(db)
    # new_user = users.create(name="Alice", preferences={"theme":"dark"})
    # fetched_user = users.get(new_user["user_id"])


class Collection(BaseModel):
    """Table model for `collections` table (PK: collection_id)."""
    def __init__(self, db):
        super().__init__(db, "collections", "collection_id")

    # Example:
    # collections = Collection(db)
    # collections.create(user_id=1, name="Holiday Trip")


class Photo(BaseModel):
    """Table model for `photos` table (PK: photo_id)."""
    def __init__(self, db):
        super().__init__(db, "photos", "photo_id")

    # Example:
    # photos = Photo(db)
    # photos.create(collection_id=1, path="/images/pic1.jpg")


class Thumbnail(BaseModel):
    """Table model for `thumbnails` table (PK: thumbnail_id)."""
    def __init__(self, db):
        super().__init__(db, "thumbnails", "thumbnail_id")


class ExifData(BaseModel):
    """Table model for `exif_data` table (PK: photo_id)."""
    def __init__(self, db):
        super().__init__(db, "exif_data", "photo_id")

    # Example:
    # exif = ExifData(db)
    # exif.create(photo_id=1, camera_model="Canon", iso=100)


class Score(BaseModel):
    """Table model for `scores` table (PK: score_id)."""
    def __init__(self, db):
        super().__init__(db, "scores", "score_id")


class Face(BaseModel):
    """Table model for `faces` table (PK: face_id)."""
    def __init__(self, db):
        super().__init__(db, "faces", "face_id")


class ImageComment(BaseModel):
    """Table model for `image_comments` table (PK: image_comment_id)."""
    def __init__(self, db):
        super().__init__(db, "image_comments", "image_comment_id")


class CollectionComment(BaseModel):
    """Table model for `collection_comments` table (PK: collection_comment_id)."""
    def __init__(self, db):
        super().__init__(db, "collection_comments", "collection_comment_id")


class NearDuplicateGroup(BaseModel):
    """Table model for `near_duplicate_groups` table (PK: group_id)."""
    def __init__(self, db):
        super().__init__(db, "near_duplicate_groups", "group_id")


class NearDuplicatePhoto(BaseModel):
    """
    Table model for `near_duplicate_photos` table (PK: photo_id).
    NOTE: This table may use a composite primary key, so you might
    need to extend this class for custom handling.
    """
    def __init__(self, db):
        super().__init__(db, "near_duplicate_photos", "photo_id")


class Camera(BaseModel):
    """Table model for `cameras` table (PK: camera_id)."""
    def __init__(self, db):
        super().__init__(db, "cameras", "camera_id")


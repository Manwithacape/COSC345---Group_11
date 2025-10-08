import os
import sys
import psycopg2
from psycopg2 import sql, OperationalError
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()  # loads DB credentials from .env


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)


class Database:
    def __init__(self):
        dbname = os.getenv("DB_NAME", "autocull_db")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASS", "admin")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
        except OperationalError as e:
            if f'database "{dbname}" does not exist' in str(e):
                # Connect to default database and create the target database
                conn = psycopg2.connect(
                    dbname="postgres",
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                )
                conn.autocommit = True
                with conn.cursor() as cur:
                    cur.execute(
                        sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname))
                    )
                conn.close()
                # Try connecting again
                self.conn = psycopg2.connect(
                    dbname=dbname, user=user, password=password, host=host, port=port
                )
            else:
                raise
        self.conn.autocommit = True

    # ----------------- Helper Methods -----------------
    def fetch(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

    def execute(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query, params or ())
            return True

    # ----------------- Schema -----------------
    def create_schema(self, schema_file="schema.sql"):
        """Run schema.sql to create tables."""
        schema_path = resource_path(schema_file)
        with open(schema_path, "r") as f:
            sql_code = f.read()
        self.execute(sql_code)
        print("Database schema created.")

    # ----------------- Collections -----------------
    def add_collection(self, name: str):
        query = "INSERT INTO collections (name) VALUES (%s) RETURNING id"
        return self.fetch(query, (name,))[0]["id"]

    def get_collections(self):
        return self.fetch("SELECT * FROM collections ORDER BY created_at DESC")

    def get_collection(self, collection_id):
        query = """
            SELECT * 
            FROM collections
            WHERE collection_id='%s'"""
        return self

    # ----------------- Photos -----------------
    def add_photo(
        self, collection_id: int, file_path: str, file_name: str, status="undecided"
    ):
        query = """
        INSERT INTO photos (collection_id, file_path, file_name, status)
        VALUES (%s,%s,%s,%s) RETURNING id
        """
        return self.fetch(query, (collection_id, file_path, file_name, status))[0]["id"]

    def delete_photo(self, photo_id: int):
        """Delete a photo; ON DELETE CASCADE in schema removes related rows."""
        self.execute("DELETE FROM photos WHERE id=%s", (photo_id,))

    def delete_collection(self, collection_id: int):
        """Delete a collection; photos and related rows cascade via FK."""
        self.execute("DELETE FROM collections WHERE id=%s", (collection_id,))

    def create_face(self, photo_id: int, bbox):
        query = """
        INSERT INTO faces (photo_id, x1, y1, x2, y2)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        return self.fetch(query, (photo_id, bbox[0], bbox[1], bbox[2], bbox[3]))[0][
            "id"
        ]

    def get_faces(self, photo_id: int):
        """
        Retrieve all faces associated with a given photo, including the photo's file path.
        """
        query = """
            SELECT f.*, p.file_path
            FROM faces f
            JOIN photos p ON f.photo_id = p.id
            WHERE f.photo_id=%s
        """
        return self.fetch(query, (photo_id,))

    def get_photos(self, collection_id=None):
        query = "SELECT * FROM photos"
        if collection_id:
            query += " WHERE collection_id=%s"
            return self.fetch(query, (collection_id,))
        return self.fetch(query)

    def get_all_photos(self):
        return self.fetch("SELECT * FROM photos")

    def update_photo_file_path(self, photo_id, new_path):
        """Update the file path of a photo."""
        query = "UPDATE photos SET file_path=%s WHERE id=%s"
        self.execute(query, (new_path, photo_id))

    # ----------------- EXIF -----------------
    def add_exif(self, photo_id, tag_name, tag_value):
        query = """
        INSERT INTO exif_data (photo_id, tag_name, tag_value)
        VALUES (%s, %s, %s)
        """
        self.execute(query, (photo_id, tag_name, str(tag_value)))

    def get_exif(self, photo_id):
        query = "SELECT tag_name, tag_value FROM exif_data WHERE photo_id=%s"
        results = self.fetch(query, (photo_id,))
        return {row["tag_name"]: row["tag_value"] for row in results} if results else {}

    # ----------------- Embeddings -----------------
    def add_embedding(self, photo_id, embedding):
        """Store a CLIP embedding vector for a photo."""
        query = "INSERT INTO embeddings (photo_id, embedding) VALUES (%s, %s)"
        self.execute(query, (photo_id, embedding))

    def get_embedding(self, photo_id):
        return self.fetch(
            "SELECT embedding FROM embeddings WHERE photo_id=%s", (photo_id,)
        )

    # ----------------- Scores -----------------
    def add_score(self, photo_id, score_type, value, scaled_value):
        query = "INSERT INTO scores (photo_id, type, value, scaled_value) VALUES (%s,%s,%s,%s)"
        self.execute(query, (photo_id, score_type, value, scaled_value))

    def get_scores(self, photo_id):
        return self.fetch("SELECT * FROM scores WHERE photo_id=%s", (photo_id,))

    def get_scaled_scores(self, photo_id):
        return self.fetch("SELECT * FROM scores WHERE photo_id=%s", (photo_id,))

    def add_quality_score(self, photo_id, quality_score):
        query = "INSERT INTO photo_quality (photo_id, quality_score) VALUES (%s,%s)"
        self.execute(query, (photo_id, quality_score))

    def get_quality_score(self, photo_id):
        row = self.fetch(
            "SELECT quality_score FROM photo_quality WHERE photo_id=%s", (photo_id,)
        )
        if row:
            return row[0]["quality_score"]
        return None

    # ----------------- Styles -----------------
    def add_style(self, name, description=None):
        query = "INSERT INTO styles (name, description) VALUES (%s,%s) ON CONFLICT (name) DO NOTHING RETURNING id"
        result = self.fetch(query, (name, description))
        return result[0]["id"] if result else None

    def assign_style(self, photo_id, style_id):
        query = "INSERT INTO photo_styles (photo_id, style_id) VALUES (%s,%s) ON CONFLICT DO NOTHING"
        self.execute(query, (photo_id, style_id))

    def get_styles_for_photo(self, photo_id):
        return self.fetch(
            """
            SELECT s.* FROM styles s
            JOIN photo_styles ps ON s.id = ps.style_id
            WHERE ps.photo_id=%s
        """,
            (photo_id,),
        )

    # ----------------- Near Duplicates -----------------
    def add_near_duplicate_group(self, method=None):
        """
        Create a new near-duplicate group and return its ID.
        :param method: method used to detect duplicates (e.g., 'phash')
        """
        query = "INSERT INTO near_duplicate_groups (method) VALUES (%s) RETURNING id"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (method,))
            group_id = cursor.fetchone()[0]
            print(
                f"[DEBUG] Created near-duplicate group_id={group_id}, method={method}"
            )
            return group_id
        except Exception as e:
            print(
                f"[ERROR] Failed to create near-duplicate group (method={method}): {e}"
            )
            return None
        finally:
            cursor.close()

    def assign_photo_to_near_duplicate_group(self, group_id, photo_id):
        """
        Assign a photo to an existing near-duplicate group.
        :param group_id: ID of the near-duplicate group
        :param photo_id: ID of the photo
        """
        query = """
            INSERT INTO near_duplicate_photos (group_id, photo_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (group_id, photo_id))
            print(f"[DEBUG] Assigned photo_id={photo_id} to group_id={group_id}")
        except Exception as e:
            print(
                f"[ERROR] Failed to assign photo_id={photo_id} to group_id={group_id}: {e}"
            )
        finally:
            cursor.close()

    def get_near_duplicate_groups(self):
        """
        Retrieve all near-duplicate groups with their associated photos.
        :return: List of groups with photo IDs
        """
        query = "SELECT * FROM near_duplicate_groups"
        groups = self.fetch(query)
        for group in groups:
            photos = self.fetch(
                """
                SELECT p.* FROM photos p
                JOIN near_duplicate_photos ndp ON p.id = ndp.photo_id
                WHERE ndp.group_id=%s
            """,
                (group["id"],),
            )
            group["photos"] = photos
        return groups

    def get_photos_in_near_duplicate_group(self, group_id):
        """
        Retrieve all photos in a specific near-duplicate group.
        :param group_id: ID of the near-duplicate group
        :return: List of photos in the group
        """
        query = """
            SELECT p.* FROM photos p
            JOIN near_duplicate_photos ndp ON p.id = ndp.photo_id
            WHERE ndp.group_id=%s
        """
        return self.fetch(query, (group_id,))

    def get_near_duplicate_groups_for_photo(self, photo_id):
        """
        Retrieve the near-duplicate group for a specific photo.
        :param photo_id: ID of the photo
        :return: Group details or None if not found
        """
        query = """
            SELECT g.* FROM near_duplicate_groups g
            JOIN near_duplicate_photos ndp ON g.id = ndp.group_id
            WHERE ndp.photo_id=%s
        """
        groups = self.fetch(query, (photo_id,))
        return groups[0] if groups else None

    def get_groups_for_photo(self, photo_id):
        """
        Get all group IDs that a given photo belongs to.
        """
        query = "SELECT group_id FROM near_duplicate_photos WHERE photo_id=%s"
        return self.fetch(query, (photo_id,))

    def get_photos_in_group(self, group_id):
        """
        Get all photos (id, file_name) in a near-duplicate group.
        """
        query = """
            SELECT p.id AS photo_id, p.file_name
            FROM photos p
            JOIN near_duplicate_photos ndp ON p.id = ndp.photo_id
            WHERE ndp.group_id=%s
        """
        return self.fetch(query, (group_id,))

    def clear_duplicates(self):
        """Development method: clear all near-duplicate groups and assignments."""
        self.execute("DELETE FROM near_duplicate_photos")
        self.execute("DELETE FROM near_duplicate_groups")
        print("Cleared all near-duplicate groups and assignments.")

    # ----------------- Queries -----------------
    def get_first_photo_for_collection(self, collection_id):
        query = "SELECT * FROM photos WHERE collection_id=%s ORDER BY id LIMIT 1"
        results = self.fetch(query, (collection_id,))
        return results[0] if results else None

    # -----------------Suggestions -----------------
    def update_photo_suggestion(self, photo_id, suggestion):
        """Set or update the suggestioin for a photo ('keep', or 'delete')."""
        query = "UPDATE photos SET suggestion=%s WHERE id=%s"
        self.execute(query, (suggestion, photo_id))

    def get_photo_suggestion(self, photo_id):
        """Retrieve the suggestion for a photo."""
        rows = self.fetch("SELECT suggestion FROM photos WHERE id=%s", (photo_id,))
        return rows[0]["suggestion"] if rows and "suggestion" in rows[0] else None

    def get_photos_with_suggestions(self, group_id):
        """Retrieve all photos in a group along with their suggestions."""
        query = """
            SELECT p.id AS photo_id, p.file_name, p.suggestion
            FROM photos p
            JOIN near_duplicate_photos ndp ON p.id = ndp.photo_id
            WHERE ndp.group_id=%s"""
        return self.fetch(query, (group_id,))

    def get_photos_by_suggestion(self, suggestion):
        """
        Retrieve all photos with a specific suggestion ('keep' or 'delete').
        Returns list of dicts with id and filepath
        """
        query = "SELECT id, file_path FROM photos WHERE suggestion=%s"
        return self.fetch(query, (suggestion,))

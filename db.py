# db.py
import psycopg2
from psycopg2.extras import RealDictCursor

# ---------------- Database Connection ----------------
class Database:
    def __init__(self, dbname="postgres", user="postgres", password="admin", host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_connection(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def init_db(self):
        conn = self.get_connection()
        cur = conn.cursor()

        # ---------- Users ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                preferences JSONB DEFAULT '{}'::jsonb,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)

        # ---------- Collections ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                collection_id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                date_created TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)

        # ---------- Photos ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                photo_id BIGSERIAL PRIMARY KEY,
                collection_id BIGINT REFERENCES collections(collection_id) ON DELETE SET NULL,
                file_path TEXT NOT NULL UNIQUE,
                date_added TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)

        # ---------- Thumbnails ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS thumbnails (
                thumbnail_id BIGSERIAL PRIMARY KEY,
                photo_id BIGINT NOT NULL UNIQUE REFERENCES photos(photo_id) ON DELETE CASCADE,
                image_path TEXT NOT NULL UNIQUE
            );
        """)

        # ---------- Exif Data ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS exif_data (
                exif_id BIGSERIAL UNIQUE,
                photo_id BIGINT PRIMARY KEY REFERENCES photos(photo_id) ON DELETE CASCADE,
                thumbnail_id BIGINT UNIQUE REFERENCES thumbnails(thumbnail_id) ON DELETE SET NULL,
                make TEXT,
                model TEXT,
                lens_model TEXT,
                focal_length_mm NUMERIC(6,2),
                exposure_time TEXT,
                f_number NUMERIC(4,2),
                iso_speed INTEGER,
                datetime_original TIMESTAMPTZ,
                gps_latitude DOUBLE PRECISION,
                gps_longitude DOUBLE PRECISION
            );
        """)

        # ---------- Scores ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                score_id BIGSERIAL PRIMARY KEY,
                photo_id BIGINT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
                metric_name TEXT NOT NULL,
                value DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                CONSTRAINT uq_scores_photo_metric UNIQUE (photo_id, metric_name)
            );
        """)

        # ---------- Faces ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                face_id BIGSERIAL PRIMARY KEY,
                photo_id BIGINT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
                bounding_box JSONB NOT NULL,
                attributes JSONB DEFAULT '{}'::jsonb
            );
        """)

        # ---------- Image Comments ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS image_comments (
                image_comment_id BIGSERIAL PRIMARY KEY,
                photo_id BIGINT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                created_by BIGINT REFERENCES users(user_id) ON DELETE SET NULL
            );
        """)

        # ---------- Collection Comments ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS collection_comments (
                collection_comment_id BIGSERIAL PRIMARY KEY,
                collection_id BIGINT NOT NULL REFERENCES collections(collection_id) ON DELETE CASCADE,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                created_by BIGINT REFERENCES users(user_id) ON DELETE SET NULL
            );
        """)

        # ---------- Near Duplicate Groups ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS near_duplicate_groups (
                group_id BIGSERIAL PRIMARY KEY,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """)

        # ---------- Near Duplicate Photos ----------
        cur.execute("""
            CREATE TABLE IF NOT EXISTS near_duplicate_photos (
                group_id BIGINT NOT NULL REFERENCES near_duplicate_groups(group_id) ON DELETE CASCADE,
                photo_id BIGINT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
                similarity_score DOUBLE PRECISION,
                PRIMARY KEY (group_id, photo_id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()


# ---------------- Generic Base Model ----------------
class BaseModel:
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

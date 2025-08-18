# db.py
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_connection()
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


# ---------------- CRUD METHODS ----------------

# ---- Users ----
def create_user(name, preferences={}):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO users (name, preferences) VALUES (%s, %s) RETURNING *;", (name, preferences))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return user

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE user_id=%s;", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def update_user(user_id, name=None, preferences=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if name:
        cur.execute("UPDATE users SET name=%s WHERE user_id=%s;", (name, user_id))
    if preferences is not None:
        cur.execute("UPDATE users SET preferences=%s WHERE user_id=%s;", (preferences, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return get_user(user_id)

def delete_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id=%s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()


# ---- Collections ----
def create_collection(user_id, name):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO collections (user_id, name) VALUES (%s, %s) RETURNING *;", (user_id, name))
    collection = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return collection

def get_collection(collection_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM collections WHERE collection_id=%s;", (collection_id,))
    collection = cur.fetchone()
    cur.close()
    conn.close()
    return collection

def update_collection(collection_id, name=None, user_id=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if name:
        cur.execute("UPDATE collections SET name=%s WHERE collection_id=%s;", (name, collection_id))
    if user_id:
        cur.execute("UPDATE collections SET user_id=%s WHERE collection_id=%s;", (user_id, collection_id))
    conn.commit()
    cur.close()
    conn.close()
    return get_collection(collection_id)

def delete_collection(collection_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM collections WHERE collection_id=%s;", (collection_id,))
    conn.commit()
    cur.close()
    conn.close()


# ---- Photos ----
def create_photo(collection_id, file_path):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO photos (collection_id, file_path) VALUES (%s, %s) RETURNING *;", (collection_id, file_path))
    photo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return photo

def get_photo(photo_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM photos WHERE photo_id=%s;", (photo_id,))
    photo = cur.fetchone()
    cur.close()
    conn.close()
    return photo

def update_photo(photo_id, collection_id=None, file_path=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if collection_id:
        cur.execute("UPDATE photos SET collection_id=%s WHERE photo_id=%s;", (collection_id, photo_id))
    if file_path:
        cur.execute("UPDATE photos SET file_path=%s WHERE photo_id=%s;", (file_path, photo_id))
    conn.commit()
    cur.close()
    conn.close()
    return get_photo(photo_id)

def delete_photo(photo_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM photos WHERE photo_id=%s;", (photo_id,))
    conn.commit()
    cur.close()
    conn.close()


# ---- Thumbnails ----
def create_thumbnail(photo_id, image_path):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO thumbnails (photo_id, image_path) VALUES (%s, %s) RETURNING *;", (photo_id, image_path))
    thumbnail = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return thumbnail

def get_thumbnail(thumbnail_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM thumbnails WHERE thumbnail_id=%s;", (thumbnail_id,))
    thumbnail = cur.fetchone()
    cur.close()
    conn.close()
    return thumbnail

def update_thumbnail(thumbnail_id, photo_id=None, image_path=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if photo_id:
        cur.execute("UPDATE thumbnails SET photo_id=%s WHERE thumbnail_id=%s;", (photo_id, thumbnail_id))
    if image_path:
        cur.execute("UPDATE thumbnails SET image_path=%s WHERE thumbnail_id=%s;", (image_path, thumbnail_id))
    conn.commit()
    cur.close()
    conn.close()
    return get_thumbnail(thumbnail_id)

def delete_thumbnail(thumbnail_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM thumbnails WHERE thumbnail_id=%s;", (thumbnail_id,))
    conn.commit()
    cur.close()
    conn.close()

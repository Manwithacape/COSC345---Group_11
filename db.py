# db.py
import psycopg2

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

    # ---------- Near Duplicate Photos (bridge) ----------
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

# PhotoSift Database Setup Guide

This guide provides high-level instructions for setting up PostgreSQL, connecting with Python, and running test data for the PhotoSift project.

---

## 1. Install PostgreSQL

1. Download and install PostgreSQL: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. During installation, set your password for the default user `postgres` to `admin`.
3. Ensure PostgreSQL service is running.
4. Create the project database:

```sql
CREATE DATABASE photosift;
```

---

## Note (Cam)
Have been using pgAdmin 4 - I suggest it easy to understand UI can help everyone setup if want

## 2. Python Connection

Install the PostgreSQL Python library:

```bash
pip install psycopg2
```
---

## 3. Initialise Database

Run `app.py` to initialise database. 

This should add in all tables etc.



---

## 3. Test Inserts

Run these statements AI generated statements in the database:

```sql
-- Users
INSERT INTO users (name, preferences) VALUES ('Alice', '{"theme":"dark"}');
INSERT INTO users (name, preferences) VALUES ('Bob', '{"theme":"light"}');

-- Collections
INSERT INTO collections (user_id, name) VALUES (1, 'Holiday Trip');
INSERT INTO collections (user_id, name) VALUES (2, 'Work Photos');

-- Photos
INSERT INTO photos (collection_id, file_path) VALUES (1, '/photos/holiday/beach.jpg');
INSERT INTO photos (collection_id, file_path) VALUES (1, '/photos/holiday/mountains.jpg');
INSERT INTO photos (collection_id, file_path) VALUES (2, '/photos/work/conference.jpg');

-- Thumbnails
INSERT INTO thumbnails (photo_id, image_path) VALUES (1, '/thumbnails/beach_thumb.jpg');
INSERT INTO thumbnails (photo_id, image_path) VALUES (2, '/thumbnails/mountains_thumb.jpg');
INSERT INTO thumbnails (photo_id, image_path) VALUES (3, '/thumbnails/conference_thumb.jpg');

-- EXIF Data
INSERT INTO exif_data (photo_id, thumbnail_id, make, model)
VALUES (1, 1, 'Canon', 'EOS 80D');

-- Scores
INSERT INTO scores (photo_id, metric_name, value) VALUES (1, 'sharpness', 0.92);
INSERT INTO scores (photo_id, metric_name, value) VALUES (1, 'exposure', 0.75);
INSERT INTO scores (photo_id, metric_name, value) VALUES (2, 'sharpness', 0.88);

-- Faces
INSERT INTO faces (photo_id, bounding_box) VALUES (1, '{"x":0.12,"y":0.33,"w":0.25,"h":0.30}');

-- Comments
INSERT INTO image_comments (photo_id, content, created_by) VALUES (1, 'Beautiful beach photo!', 2);
INSERT INTO collection_comments (collection_id, content, created_by) VALUES (1, 'Can’t wait to see more holiday pics!', 2);

-- Near-Duplicate Groups
INSERT INTO near_duplicate_groups (created_at) VALUES (NOW());

-- Near-Duplicate Photos
INSERT INTO near_duplicate_photos (group_id, photo_id, similarity_score) VALUES (1, 1, 0.95);
INSERT INTO near_duplicate_photos (group_id, photo_id, similarity_score) VALUES (1, 2, 0.90);
```

---

## 4. Test Queries

```sql
-- List all users
SELECT * FROM users;

-- Collections for a user
SELECT * FROM collections WHERE user_id = 1;

-- Photos with EXIF info
SELECT p.file_path, e.make, e.model
FROM photos p
JOIN exif_data e ON p.photo_id = e.photo_id;

-- Comments on a collection
SELECT u.name, c.content
FROM collection_comments c
JOIN users u ON c.created_by = u.user_id
WHERE collection_id = 1;
```

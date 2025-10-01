# Notes for program architecture (Roles of each component)

This document describes the roles of the main components in the AI photo culling, grading, and educational application. It references the schema previously defined and is intended to ensure consistent understanding of responsibilities within the system. It provides a high-level overview and does not attempt to specify implementation details beyond the chosen stack.

## Desktop GUI (Tkinter)

The user interface is built with Tkinter, following an MVC-inspired approach. The GUI presents the user with a main window that includes navigation to collections, thumbnails, and associated photo data. Interactions are kept responsive by separating UI concerns from backend logic. Sorting, browsing, and management of collections are primary tasks handled at this layer.

The GUI communicates with the backend to retrieve information stored in the database and display it to the user. Results from scoring, duplicate detection, and analysis are presented through this interface.

## Collections

A collection is a logical grouping of photographs. Users can create new collections or add images to existing ones when importing. Collections are stored in the database following the defined schema and act as the primary organizational unit for photo management.

## Thumbnail Generator

When photos are imported, thumbnails are generated to support efficient browsing in the GUI. These thumbnails are stored in the database and remain accessible even if the original files are unavailable. OpenCV is used to generate resized versions of the images.

## Database

The database uses PostgreSQL, with communication handled via psycopg2. The schema defines entities such as User, Collection, Photo, ExifData, Thumbnail, Score, Face, ImageComment, CollectionComment, and near-duplicate groupings.

The database stores both raw information (e.g., EXIF metadata, paths, and thumbnails) and processed information (e.g., scores, duplicate group membership). It forms the core of the system, ensuring persistence and structured access to all photo-related data.

## Scoring Engine

The scoring engine applies computer vision techniques to evaluate photos against a set of quality metrics. OpenCV methods are used to measure aspects such as sharpness, exposure, and face detection. Results are normalized into scores ranging from 0 to 1, where higher values indicate higher quality.

These scores are stored in the database and are later used by other components, including the preference model and duplicate resolution logic. Flexibility in metric definitions is maintained to allow for adjustment and improvement over time.

## Preference Model

The preference model determines how scores are interpreted to select good or bad photos. While the scoring engine generates raw metric values, the preference model applies user-driven or task-specific weighting.

Users may refine preferences through interaction with the application, enabling the system to adapt to individual styles or requirements. This layer is designed to be modular, allowing for different models depending on the type of photography (e.g., portrait, landscape, wildlife).

## Near-Duplicate Detection

Near-duplicate detection identifies sets of photos that are visually similar, such as those captured in bursts. The current implementation uses perceptual hashing (via imagehash) combined with DBSCAN clustering to group similar photos.

Groups of near-duplicates are stored in the database through NearDuplicateGroup and NearDuplicatePhoto. This enables the system to highlight duplicates for user review or automatic culling, ensuring that only the best photo in a set is kept.

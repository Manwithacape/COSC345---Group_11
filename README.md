# AutoCull

## Table of Contents

- [AutoCull](#autocull)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [High-level Description of Modules](#high-level-description-of-modules)
    - [Main Application (`app.py`)](#main-application-apppy)
    - [Base Sidebar Viewer (`base_sidebar_viewer.py`)](#base-sidebar-viewer-base_sidebar_viewerpy)
    - [Base Thumbnail Viewer (`base_viewer.py`)](#base-thumbnail-viewer-base_viewerpy)
    - [Collections Viewer (`collections_viewer.py`)](#collections-viewer-collections_viewerpy)
    - [Database Module (`db.py`)](#database-module-dbpy)
    - [Prototype GUI Test (`gui-test.py`)](#prototype-gui-test-gui-testpy)
    - [Image Analysis Prototypes (`img-anal.py`, `subject_detection.py`)](#image-analysis-prototypes-img-analpy-subject_detectionpy)
    - [PyQt5 Prototype GUI (`Design/Prototypes/Daniel/PrototypeGUI/gui-test.py`)](#pyqt5-prototype-gui-designprototypesdanielprototypeguigui-testpy)
    - [Duplicates Detection and Viewer (`duplicates.py`, `duplicate_viewer.py`)](#duplicates-detection-and-viewer-duplicatespy-duplicate_viewerpy)
    - [EXIF Reader and Viewer (`exif_reader.py`, `exif_viewer.py`)](#exif-reader-and-viewer-exif_readerpy-exif_viewerpy)
    - [Faces Frame and Face Frame Modules (`faces_frame.py`, `face_frame.py`)](#faces-frame-and-face-frame-modules-faces_framepy-face_framepy)
    - [Filmstrip Viewer (`filmstrip_viewer.py`)](#filmstrip-viewer-filmstrip_viewerpy)
    - [Collapsible Sidebar Component (`gui.py`)](#collapsible-sidebar-component-guipy)
    - [LLM Feedback Module (`llm_feedback.py`)](#llm-feedback-module-llm_feedbackpy)
    - [Main Viewer Base Class (`main_viewer.py`)](#main-viewer-base-class-main_viewerpy)
    - [Photo Analyzer (`photo_analyzer.py`)](#photo-analyzer-photo_analyzerpy)
    - [Photo Importer (`photo_importer.py`)](#photo-importer-photo_importerpy)
    - [Photo Scorer (`photo_scorer.py`)](#photo-scorer-photo_scorerpy)
    - [Photo Viewer (`photo_viewer.py`)](#photo-viewer-photo_viewerpy)
    - [Progress Dialog (`progress_dialog.py`)](#progress-dialog-progress_dialogpy)
    - [Score Viewer (`score_viewer.py`)](#score-viewer-score_viewerpy)
    - [Scrollable Frame Component (`scrollable_frame.py`)](#scrollable-frame-component-scrollable_framepy)
    - [Sidebar Buttons Module (`sidebar_buttons.py`)](#sidebar-buttons-module-sidebar_buttonspy)
    - [Single Photo Viewer (`single_photo_viewer.py`)](#single-photo-viewer-single_photo_viewerpy)
  - [Usage Instructions](#usage-instructions)
  - [Dependencies](#dependencies)
  - [Configuration and Setup Notes](#configuration-and-setup-notes)
  - [Best Practices and Important Warnings](#best-practices-and-important-warnings)
  - [License](#license)
  - [Roadmap](#roadmap)
  - [Acknowledgments](#acknowledgments)

## Project Overview

AutoCull is a photo culling and scoring application designed to help photographers manage their photo collections more efficiently. The application features a dark-themed interface, sidebar navigation, EXIF data display, scoring, duplicate detection, and more. Intended to be used post shoot and pre-post-processing. AutoCull should be capable of completing the majority of culling in a fraction of the time the same operation would take a human.

## Features

This project has been developed as part of the COSC345 paper at the University of Otago. Inspired by post processing software already used by photographers, such as Lightroom, and Photoshop.

- Import photos
- Photo collection management
- Photo viewing
- Detect duplicate and near-duplicate photographs
- Computes photo quality metrics
- Provides AI-generated feedback using Google Gemini
- Intelligent culling suggestions powered by AI/ML
- Duplicate & near-duplicate deletion

## High-level Description of Modules

### Main Application (`app.py`)

This file launches the AutoCull GUI with a dark theme using ttkbootstrap. It features:

- Sidebar navigation for photos, collections, EXIF data, scores, duplicates
- Splash screen with window centering
- Database integration with automatic schema creation
- Support for RAW and standard image formats

Key classes/functions include `AutoCullApp`, `resource_path`, `center_window`, and `create_splash`.

### Base Sidebar Viewer (`base_sidebar_viewer.py`)

Defines a base class for creating right-hand sidebar viewers with:

- Collapsible header bar
- Scrollable treeview
- Resizable grip

Key methods include `__init__`, `setup_columns`, `update_content`, and resizing/toggling functionality.

### Base Thumbnail Viewer (`base_viewer.py`)

Provides a base class for displaying photo thumbnails with:

- Image loading (including RAW formats)
- Uniform thumbnail generation
- Selection tracking
- Notification of linked viewers

Key methods include `__init__`, `_open_image`, `create_uniform_thumbnail_pil`, and selection handling.

### Collections Viewer (`collections_viewer.py`)

Displays a scrollable list of photo collections with:

- Thumbnail previews
- Navigation to photo viewer on selection
- Context menu for deleting collections

Key methods include `__init__`, `refresh_collections`, `get_thumbnail`, `_load_thumbnail`, and context menu handling.

### Database Module (`db.py`)

Provides an interface for interacting with a PostgreSQL database. It includes:

- CRUD operations for photos, EXIF data, embeddings, scores, styles, and near-duplicate groups
- Schema management

Key classes/functions include `Database` initialization, schema creation, collection/photo management, face/exif management, embedding management, score management, style management, and near-duplicate management.

### Prototype GUI Test (`gui-test.py`)

A simple prototype GUI using Tkinter that demonstrates:

- File dialog for selecting files
- Confirmation message with selected filename

Key functions include `open_file_dialog` and `main`.

### Image Analysis Prototypes (`img-anal.py`, `subject_detection.py`)

Prototypes for image analysis using OpenCV, including:

- Sharpness, exposure, saturation, contrast detection
- Focus masking
- Grid of images for comparison

Key functions include `focus_mask`, `rezize_image_preserve_aspect_ratio`, and various detection/analysis functions.

### PyQt5 Prototype GUI (`Design/Prototypes/Daniel/PrototypeGUI/gui-test.py`)

A prototype GUI using PyQt5 with:

- Sidebar containing buttons
- Main area displaying collection cards in a grid

Key components include button creation, stylesheet application, and layout management.

### Duplicates Detection and Viewer (`duplicates.py`, `duplicate_viewer.py`)

Detects near-duplicate photos using perceptual hashing and DBSCAN clustering with:

- Batch processing for duplicates
- Display of duplicate groups in a treeview

Key classes/functions include `NearDuplicateDetector` and `DuplicateViewer`.

### EXIF Reader and Viewer (`exif_reader.py`, `exif_viewer.py`)

Extracts and displays EXIF data from image files, including support for RAW formats with:

- Normalization of extracted data
- Display in a sidebar treeview

Key classes/functions include `ExifReader` and `ExifViewer`.

### Faces Frame and Face Frame Modules (`faces_frame.py`, `face_frame.py`)

Displays cropped face images extracted from photos with:

- Toggle functionality for showing/hiding faces
- Cropping and resizing of face images

Key classes include `FacesFrame` and `FaceFrame`.

### Filmstrip Viewer (`filmstrip_viewer.py`)

Provides a horizontal scrolling strip of photo thumbnails with integration to:

- Main PhotoViewer instance
- EXIF, score, duplicates viewers (optional)

Key methods include `__init__`, `refresh_thumbs`, `update_highlight`, and thumbnail interaction handling.

### Collapsible Sidebar Component (`gui.py`)

Defines a collapsible sidebar component that can be positioned on either side of the main window with:

- Resizable grip
- Toggle functionality

Key class/methods include `Sidebar` initialization, toggling, resizing, and layout updates.

### LLM Feedback Module (`llm_feedback.py`)

Generates structured text paragraphs based on given facts using Google's Gemini AI model with:

- API key management
- Fact formatting for AI model input
- Paragraph generation

Key functions include `get_api_key_from_config`, `_build_client`, `_pack_facts`, and `make_paragraph`.

### Main Viewer Base Class (`main_viewer.py`)

Provides a base implementation for scrollable viewers using Canvas and Frame with:

- Dynamic resizing support
- Optional single-item display mode

Key methods include `__init__`, resize handling, and reflow grid placeholder.

### Photo Analyzer (`photo_analyzer.py`)

Analyzes photos using deep learning models (CLIP) to extract semantic embeddings for:

- Clustering/grouping photos
- Searching by similarity
- Duplicate detection

Key classes/functions include `PhotoAnalyzer` initialization, embedding extraction, clustering, and ranking.

### Photo Importer (`photo_importer.py`)

Imports photos into the database with support for:

- Various photo formats (RAW, standard)
- EXIF data extraction
- Near-duplicate detection during import

Key class/methods include `PhotoImporter`, importing files/folders, and internal file import logic.

### Photo Scorer (`photo_scorer.py`)

Computes various metrics from images to assess quality with:

- Sharpness, noise, exposure, contrast, etc.
- Face detection (currently commented out)
- Database storage of computed metrics

Key class/methods include `PhotoScorer`, metric computation, scaling, and database integration.

### Photo Viewer (`photo_viewer.py`)

Displays a scrollable grid of photo thumbnails with:

- Preview functionality
- Context menu for deleting photos
- LLM feedback generation

Key class/methods include `PhotoViewer` initialization, thumbnail management, selection handling, context menu, and LLM integration.

### Progress Dialog (`progress_dialog.py`)

Provides a reusable progress dialog for Tkinter applications with:

- Indeterminate/determinate progress bars
- Customizable messages
- Methods for starting/stopping animation and setting progress

Key class/methods include `ProgressDialog` initialization, progress control, and message updates.

### Score Viewer (`score_viewer.py`)

Displays photo scores in a sidebar interface with:

- Metric-value pairs in treeview format
- Database integration for score retrieval

Key methods include `__init__`, column setup, and content update.

### Scrollable Frame Component (`scrollable_frame.py`)

Provides a vertically scrollable frame for Tkinter applications with:

- Automatic adjustment of scroll region based on content size
- Cross-platform mouse wheel support

Key class/methods include `ScrollableFrame` initialization and event handling.

### Sidebar Buttons Module (`sidebar_buttons.py`)

Manages sidebar button functionality for:

- Importing photos
- Finding duplicates
- Switching views
- Navigation tasks

Key methods include `__init__`, adding buttons, importing files, finding duplicates, switching views, clearing duplicates, and return button functionality.

### Single Photo Viewer (`single_photo_viewer.py`)

Displays a single photo scaled-to-fit with:

- LLM feedback box at the bottom-left
- Image rendering to fit canvas while preserving aspect ratio

Key methods include `__init__`, image loading/rendering, resizing handling, and LLM feedback generation.

## Usage Instructions

See `End User.pdf` for more information

1. Ensure all dependencies are installed (see Dependencies section).
2. Set up your PostgreSQL database with appropriate credentials.
3. Run the `app.py` file to launch the AutoCull application.

## Dependencies

See `requirements.txt`

## Configuration and Setup Notes

1. Set up your PostgreSQL database with the necessary tables.
2. Create a `.env` file to configure database credentials and API keys:

   ``` bash
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

   GEMINI_API_KEY=your_gemini_api_key
   ```

## Best Practices and Important Warnings

- Always ensure database credentials are securely stored.
- Test thoroughly with different photo formats, especially RAW files.
- Regularly back up your database to prevent data loss.
- When using AI models for feedback generation, monitor API usage limits.

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software for any purpose, provided that the original license text and attribution are included with all copies or substantial portions of the software.

The software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. The authors are not liable for any claim, damages, or other liability arising from use of the software.

## Roadmap

- [ ] Add face clustering visualization
- [ ] Improve RAW decoding performance
- [ ] Implement undo/redo for scoring actions
- [ ] Add multi-threaded import pipeline

## Acknowledgments

AutoCull was developed by Group 11 as part of COSC345 coursework at the University of Otago.

Thanks to:

- Sherlock Licorich for his continued patience towards the project
- ttkbootstrap and Pillow for the beautiful GUI
- rawpy and OpenCV for RAW and image analysis
- Google Gemini for AI-assisted feedback

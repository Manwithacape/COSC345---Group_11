# AI-Powered Photo Culling Desktop App (Local-First)

This document describes the architecture and technology stack for a desktop application that helps photographers automatically select the best images from a large photo shoot using machine learning and computer vision.

## Goal

Build a desktop application that:
- Analyses photos for technical quality (e.g., sharpness, facial expression)
- Identifies and removes near-duplicates
- Learns your personal photo preferences over time
- Suggests which photos to keep

---

## System Overview

```
+-----------------------------+
|  Folder of Photos           |
+-----------------------------+
            ↓
+-----------------------------+
|  Preprocessing (OpenCV)     |
|  - Resize, normalise, etc.  |
|  - Detect faces/sharpness   |
+-----------------------------+
            ↓
+-----------------------------+
|  Feature Extraction         |
|  - CLIP Embeddings          |
|  - Aesthetic Score          |
+-----------------------------+
            ↓
+-----------------------------+
|  Preference Model (ML)      |
|  - Trained on your ratings  |
|  - Predicts which to keep   |
+-----------------------------+
            ↓
+-----------------------------+
|  Desktop Interface (UI)     |
|  - Show images and scores   |
|  - Let user confirm/override|
+-----------------------------+
            ↓
+-----------------------------+
|  Save Feedback + Retrain    |
+-----------------------------+
```

---

## Technology Stack

### 1. Python

**What it does**  
Python is the main programming language for the application. It ties together the image analysis, machine learning models, and user interface.

**Why this works**  
Python has strong support for both AI tools and desktop apps, with a large community and extensive documentation.

---

### 2. OpenCV

**What it does**  
OpenCV is used to analyze technical aspects of the photo, including:
- Sharpness (via edge detection)
- Face detection
- Basic image transformations (resize, crop, etc.)

**Why this works**  
OpenCV is optimized for fast, local image processing and runs entirely offline. It provides the core analysis needed before higher-level AI models are applied.

---

### 3. PyTorch

**What it does**  
PyTorch is used for training and running machine learning models. This includes:
- Aesthetic scoring (predicting image appeal)
- Learning your personal preferences from labeled data

**Why this works**  
PyTorch is beginner-friendly, widely used in the industry, and allows you to build and train neural networks without needing cloud servers. It also supports GPU acceleration if needed.

---

### 4. CLIP (Contrastive Language–Image Pretraining)

**What it does**  
CLIP generates a numerical representation (embedding) of each image that captures its content and style. These embeddings can be used to:
- Detect similar/duplicate images
- Cluster or organize photos by content

**Why this works**  
CLIP embeddings are rich and expressive, making them ideal for comparing photos or learning user preferences, even without labels.

---

### 5. scikit-learn

**What it does**  
scikit-learn is used to train a simple model that learns from your image selections. Example models include:
- Logistic Regression
- Support Vector Machines (SVM)

**Why this works**  
These models are quick to train and require little configuration. They are ideal for small datasets, such as personal selections from a few photo shoots.

---

### 6. PyQt (or Tkinter)

**What it does**  
PyQt builds the desktop interface where you can:
- View photos one by one or in batches
- See AI-generated scores and duplicate warnings
- Keep or discard images with one click

**Why this works**  
PyQt creates a polished and responsive native application interface. It integrates well with Python and supports cross-platform deployment.

---

## Preference learning

1. You manually label a small batch of photos as "keep" or "discard".
2. The system extracts features/quantifiable metrics for each image (aesthetic score, sharpness, content vector).
3. A machine learning model is trained using your labels and those features.
4. The model is saved and used to make predictions on future photo shoots.
5. Over time, you can retrain or fine-tune the model as your taste evolves.

---

## Other things

- Duplicate filtering  
  Use CLIP or perceptual hashing to group similar shots and keep only the best one.

- Genre-specific models  
  Train separate models for portraits, landscapes, events, etc.

- Auto-culling in batches  
  Process entire folders and automatically suggest a final selection.


---

## Steps?

To begin, set up a basic pipeline like this:

1. Use OpenCV to scan a folder of images for sharpness and faces.
2. Extract CLIP embeddings and aesthetic scores.
3. Build a simple UI to view images and record "keep/discard" decisions.
4. Train a scikit-learn model on your decisions.
5. Use that model to automatically sort or filter future photo sets.


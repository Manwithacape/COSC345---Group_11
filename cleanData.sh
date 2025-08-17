#!/bin/bash
# chmod +x cleanData.sh
# ./cleanData.sh
# Set the target directory
TARGET_DIR="C:\Users\paxto\PhotoSIFT" # CAUTION!!!!!

# Remove all files in the directory
rm -rf "$TARGET_DIR"/*

echo "Cleaned $TARGET_DIR"
#!/bin/bash
# -------------------------------------------------------------------------
# Script: auto_doc_ollama.sh
# Purpose: Automatically generate technical documentation for all Python
#          (.py) files using Ollama (devstral), without changing code.
#          Automatically uses all available CPU threads.
# -------------------------------------------------------------------------

set -e  # Exit on error
set -u  # Exit on unset variables

# ----------------------------
# Auto-detect number of CPU threads
# ----------------------------
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash / Cygwin)
    NUM_THREADS=$(powershell -Command "[Environment]::ProcessorCount" | tr -d '\r')
else
    # Linux / macOS
    NUM_THREADS=$(nproc)
fi

# Fallback if detection fails
if [[ -z "$NUM_THREADS" ]]; then
    NUM_THREADS=4
    echo "Could not detect CPU threads, defaulting to $NUM_THREADS"
fi

export OLLAMA_NUM_THREADS="$NUM_THREADS"
echo "🔹 Using $NUM_THREADS CPU threads for Ollama"


# ----------------------------
# Target directory (default current)
# ----------------------------
TARGET_DIR="${1:-.}"

# ----------------------------
# Check Ollama installed
# ----------------------------
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Install first: https://ollama.com/download"
    exit 1
fi

# ----------------------------
# Check devstral model
# ----------------------------
if ! ollama list | grep -q "devstral"; then
    echo "'devstral' model not found. Run: ollama pull devstral"
    exit 1
fi

echo "------------------------------------------------------------"
echo "Auto-documenting Python files in: $TARGET_DIR"
echo "------------------------------------------------------------"

# ----------------------------
# Loop through all .py files
# ----------------------------
find "$TARGET_DIR" -type f -name "*.py" | while read -r FILE; do
    echo "$(date '+%H:%M:%S') - Processing: $FILE"

    # Read original content
    ORIGINAL_CONTENT=$(cat "$FILE")

    # Run Ollama to generate docstrings/comments
    UPDATED_CONTENT=$(ollama run devstral <<EOF
You are a documentation assistant. Add clear, concise docstrings and inline comments
to this Python code. DO NOT change any functionality or logic. Maintain formatting.

Original code:
$ORIGINAL_CONTENT
EOF
)

    # Backup original
    cp "$FILE" "$FILE.bak"

    # Overwrite with updated version
    echo "$UPDATED_CONTENT" > "$FILE"

    echo "$(date '+%H:%M:%S') - Finished: $FILE (backup saved as $FILE.bak)"
done

echo "------------------------------------------------------------"
echo "Documentation complete for all Python files in $TARGET_DIR"
echo "------------------------------------------------------------"

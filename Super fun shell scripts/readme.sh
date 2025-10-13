#!/bin/bash
# -------------------------------------------------------------------------
# Script: generate_readme_ollama.sh
# Purpose: Automatically generate a README.md for a Python project using
#          Ollama (devstral), summarizing all .py files and project structure.
# -------------------------------------------------------------------------

set -e  # Exit on error
set -u  # Exit on unset variables

# ----------------------------
# Auto-detect number of CPU threads
# ----------------------------
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    NUM_THREADS=$(powershell -Command "[Environment]::ProcessorCount" | tr -d '\r')
else
    NUM_THREADS=$(nproc)
fi

if [[ -z "$NUM_THREADS" ]]; then
    NUM_THREADS=4
    echo "Could not detect CPU threads, defaulting to $NUM_THREADS"
fi

export OLLAMA_NUM_THREADS="$NUM_THREADS"
echo "Using $NUM_THREADS CPU threads for Ollama"

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
echo "Generating README.md for Python project in: $TARGET_DIR"
echo "------------------------------------------------------------"

# ----------------------------
# Aggregate all Python code into one input
# ----------------------------
AGGREGATED_CODE=""
while IFS= read -r FILE; do
    AGGREGATED_CODE+="
# File: ${FILE}
"
    AGGREGATED_CODE+="$(cat "$FILE")"$'\n\n'
done < <(find "$TARGET_DIR" -type f -name "*.py")

# ----------------------------
# Generate README using Ollama
# ----------------------------
README_CONTENT=$(ollama run devstral <<EOF
You are a documentation assistant. Create a professional README.md
for a Python project based on the following source code. Include:

- Project purpose and description
- High-level module/file overview
- Usage instructions
- Dependencies
- Notes on configuration if relevant

Do NOT modify any code. Write in Markdown format.

Project source code:
$AGGREGATED_CODE
EOF
)

# Save README.md
echo "$README_CONTENT" > "$TARGET_DIR/README.md"

echo "------------------------------------------------------------"
echo "README.md generated at $TARGET_DIR/README.md"
echo "------------------------------------------------------------"

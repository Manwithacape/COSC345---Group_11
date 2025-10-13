#!/bin/bash
# -------------------------------------------------------------------------
# Script: generate_readme_ollama_iterative.sh
# Purpose: Automatically generate a professional README.md for a Python
#          project using Ollama (devstral). Handles large projects by
#          summarizing files iteratively and building a table of contents.
# -------------------------------------------------------------------------

set -e
set -u

# ----------------------------
# Auto-detect CPU threads
# ----------------------------
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    NUM_THREADS=$(powershell -Command "[Environment]::ProcessorCount" | tr -d '\r')
else
    NUM_THREADS=$(nproc)
fi

NUM_THREADS=${NUM_THREADS:-4}
export OLLAMA_NUM_THREADS="$NUM_THREADS"
echo "🔹 Using $NUM_THREADS CPU threads for Ollama"

# ----------------------------
# Target directory
# ----------------------------
TARGET_DIR="${1:-.}"

# ----------------------------
# Check Ollama and model
# ----------------------------
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Install: https://ollama.com/download"
    exit 1
fi

if ! ollama list | grep -q "devstral"; then
    echo "'devstral' model not found. Run: ollama pull devstral"
    exit 1
fi

echo "------------------------------------------------------------"
echo "Generating README.md iteratively for project in: $TARGET_DIR"
echo "------------------------------------------------------------"

# ----------------------------
# Temporary storage for per-module summaries
# ----------------------------
TMP_SUMMARY=$(mktemp)
> "$TMP_SUMMARY"

# ----------------------------
# Process each .py file individually
# ----------------------------
while IFS= read -r FILE; do
    echo "$(date '+%H:%M:%S') - Summarizing: $FILE"

    CODE_CONTENT=$(cat "$FILE")

    SUMMARY=$(ollama run devstral <<EOF
You are a documentation assistant. Summarize this Python file for a README.md.
Include:

- Purpose of the file/module
- Key classes/functions and their responsibilities
- Any usage notes or important details

Do NOT modify the code. Write in Markdown format, suitable for inclusion in a README.

File path: $FILE
File content:
$CODE_CONTENT
EOF
)

    # Append to temp summary
    echo -e "### ${FILE}\n$SUMMARY\n" >> "$TMP_SUMMARY"
done < <(find "$TARGET_DIR" -type f -name "*.py")

# ----------------------------
# Generate final README using aggregated summaries
# ----------------------------
README_CONTENT=$(ollama run devstral <<EOF
You are a professional documentation writer. Using the following module-level
summaries, create a complete README.md for the project. Include:

- Project name and purpose
- High-level description of modules/files (from summaries below)
- Table of contents
- Usage instructions
- Dependencies
- Configuration or setup notes if relevant
- Any best practices or important warnings

Do NOT modify any code. Output should be valid Markdown.

Module summaries:
$(cat "$TMP_SUMMARY")
EOF
)

# Save final README
echo "$README_CONTENT" > "$TARGET_DIR/README.md"

# Cleanup
rm "$TMP_SUMMARY"

echo "------------------------------------------------------------"
echo "Iterative README.md generated at $TARGET_DIR/README.md"
echo "------------------------------------------------------------"

#!/bin/bash
# MDAA - PDF Download Helper Script
# Downloads PDFs with appropriate headers to avoid basic bot blocking

set -e

# Default values
OUTPUT_DIR="${MDAA_TEMP_DIR:-temp}"
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REFERRER="https://www.google.com"

# Usage
usage() {
    echo "Usage: $0 <url> [output_filename]"
    echo ""
    echo "Downloads a PDF with browser-like headers."
    echo ""
    echo "Arguments:"
    echo "  url              The URL of the PDF to download"
    echo "  output_filename  Optional. Output filename (default: derived from URL)"
    echo ""
    echo "Environment variables:"
    echo "  MDAA_TEMP_DIR    Output directory (default: temp)"
    echo ""
    echo "Example:"
    echo "  $0 'https://sec.gov/document.pdf'"
    echo "  $0 'https://sec.gov/document.pdf' 'AAPL_10K_2024.pdf'"
    exit 1
}

# Check arguments
if [ -z "$1" ]; then
    usage
fi

URL="$1"
FILENAME="${2:-$(basename "$URL" | sed 's/\?.*//')}"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

OUTPUT_PATH="$OUTPUT_DIR/$FILENAME"

echo "Downloading: $URL"
echo "Output: $OUTPUT_PATH"

# Download with curl
curl -L \
    -A "$USER_AGENT" \
    -H "Referer: $REFERRER" \
    -H "Accept: application/pdf,*/*" \
    -H "Accept-Language: en-US,en;q=0.9" \
    --connect-timeout 30 \
    --max-time 120 \
    -o "$OUTPUT_PATH" \
    "$URL"

# Verify download
if [ -f "$OUTPUT_PATH" ]; then
    SIZE=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || stat -c%s "$OUTPUT_PATH" 2>/dev/null)
    echo "Downloaded: $OUTPUT_PATH ($SIZE bytes)"

    # Basic PDF validation
    if head -c 4 "$OUTPUT_PATH" | grep -q "%PDF"; then
        echo "Validation: Valid PDF header detected"
    else
        echo "Error: Downloaded file is not a valid PDF (may be HTML error page)"
        echo "First 100 bytes: $(head -c 100 "$OUTPUT_PATH" | tr '\n' ' ')"
        rm -f "$OUTPUT_PATH"
        exit 1
    fi
else
    echo "Error: Download failed"
    exit 1
fi

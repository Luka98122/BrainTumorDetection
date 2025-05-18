#!/bin/bash

# Directory to scan; default is current dir if not provided
DIR="${1:-.}"

# Use find to get PNG files and extract dimensions using `file`
find "$DIR" -type f -iname "*.png" -print0 |
while IFS= read -r -d '' file; do
    # Use `file` to get image info
    info=$(file "$file")
    
    # Extract dimensions (e.g., 512 x 512)
    if [[ $info =~ ([0-9]+)\ x\ ([0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}x${BASH_REMATCH[2]}"
    fi
done | sort | uniq -c | awk '{print $2 " - " $1}'

#!/bin/bash

# Directory to scan; default is current dir if not provided
DIR="${1:-.}"

# Use find to get PNG files and extract dimensions using `file`
find "$DIR" -type f -iname "*.png" -print0 |
while IFS= read -r -d '' file; do
    # Use `file` to get image info
    info=$(file "$file")
    
    # Extract dimensions (e.g., 256 x 256)
    if [[ $info =~ ([0-9]+)\ x\ ([0-9]+) ]]; then
        width=${BASH_REMATCH[1]}
        height=${BASH_REMATCH[2]}
        dimension="${width}x${height}"
        echo "$dimension"
        
        # Delete if dimensions are 256x256
        if [[ "$dimension" == "256x256" ]]; then
            echo "Deleting $file"
            rm "$file"
        fi
    fi
done | sort | uniq -c | awk '{print $2 " - " $1}'

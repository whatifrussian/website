#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "usage: $0 OLD_OUTPUT NEW_OUTPUT REPORT_DIR" >&2
    exit 2
fi

old_output=$(realpath "$1")
new_output=$(realpath "$2")
report=$(realpath -m "$3")
staging=$(mktemp -d)
trap 'rm -rf "$staging"' EXIT

mkdir -p "$report" "$staging/old" "$staging/new"

stage_output() {
    local source=$1 destination=$2

    # HTML is the review target. Feeds, gzip output and build_info.txt are
    # intentionally absent, as their generated representation is not stable.
    while IFS= read -r -d '' path; do
        relative=${path#"$source"/}
        mkdir -p "$destination/$(dirname "$relative")"
        cp "$path" "$destination/$relative"
    done < <(find "$source" -type f -name '*.html' -print0)

    # Binary files do not belong in a textual diff, but their checksums catch
    # missing or changed uploads (the failure mode that prompted this check).
    if [[ -d "$source/uploads" ]]; then
        (
            cd "$source/uploads"
            find . -type f -print0 | sort -z | xargs -0 sha256sum
        ) > "$destination/uploads.sha256"
    fi
}

stage_output "$old_output" "$staging/old"
stage_output "$new_output" "$staging/new"

set +e
diff -ruN -U 5 "$staging/old" "$staging/new" > "$report/site.diff"
diff_status=$?
set -e
if [[ $diff_status -gt 1 ]]; then
    echo "diff failed with status $diff_status" >&2
    exit "$diff_status"
fi

old_html=$(find "$staging/old" -type f -name '*.html' | wc -l)
new_html=$(find "$staging/new" -type f -name '*.html' | wc -l)
changed=$(diff -qr "$staging/old" "$staging/new" 2>/dev/null | wc -l || true)
cat > "$report/summary.md" <<EOF
# Base/branch generated-site comparison

- Base HTML files: $old_html
- Branch HTML files: $new_html
- Changed or missing files (including the upload manifest): $changed
- Excluded by design: feeds, compressed files, and build_info.txt

Open \`site-diff.html\` for the side-by-side report or \`site.diff\` for the
underlying unified diff.
EOF

if [[ -s "$report/site.diff" ]]; then
    diff2html -i file -s side -d word --lm lines --su open \
        -F "$report/site-diff.html" -- "$report/site.diff"
else
    cat > "$report/site-diff.html" <<'EOF'
<!doctype html><meta charset="utf-8"><title>No renderer differences</title>
<h1>No renderer differences</h1>
<p>The staged HTML and upload checksum manifests are identical.</p>
EOF
fi

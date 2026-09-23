#!/usr/bin/env bash
# Refresh the committed Substack feed snapshot and trigger a deploy.
# Run this after publishing a new post on Substack.
set -euo pipefail
cd "$(dirname "$0")/.."
curl -fsSL --retry 3 -o assets/substack-feed.xml https://zalakb.substack.com/feed
if git diff --quiet assets/substack-feed.xml; then
  echo "Feed unchanged - nothing to do."
  exit 0
fi
git add assets/substack-feed.xml
git commit -m "Refresh Substack feed snapshot"
git push origin main
echo "Deploy triggered - new posts will appear on /blogs shortly."

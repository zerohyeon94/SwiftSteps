#!/bin/bash
# Daily 피드백은 생성하지 않고, Daily와 연결된 생성 자료만 커밋한다.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/../Scripts/daily_review.py"

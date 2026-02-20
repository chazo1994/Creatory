#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-chazo1994/Creatory}"
BRANCH="${2:-main}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required. Install it first: https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Please login first: gh auth login"
  exit 1
fi

echo "Enabling auto-merge on ${REPO} ..."
gh repo edit "${REPO}" --enable-auto-merge >/dev/null

tmp_json="$(mktemp)"
trap 'rm -f "${tmp_json}"' EXIT

cat >"${tmp_json}" <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["lint-test", "frontend-check"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": true
}
JSON

echo "Applying branch protection for ${REPO}:${BRANCH} ..."
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${REPO}/branches/${BRANCH}/protection" \
  --input "${tmp_json}" >/dev/null

echo "Done."
echo "Protected branch: ${REPO}:${BRANCH}"
echo "Required checks: lint-test, frontend-check"

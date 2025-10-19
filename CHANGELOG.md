# Changelog

All notable changes to this project will be documented in this file.
This project adheres to "Keep a Changelog" and uses Semantic Versioning where appropriate.

The format is:
- `Unreleased` section for changes not yet released
- dated release entries for released versions

## [Unreleased]

### Added
- Initial changelog file to track repository changes and releases.

### Changed
- Documentation reorganization: legacy top-level markdown files moved into `docs/legacy-md/`.
- CI workflows migrated to use `uv` for faster, reproducible installation in GitHub Actions.
- Code-quality enhancements in CI: aggregated reports for Black, isort, flake8, pylint, mypy, bandit and safety were added to improve PR feedback.

### Removed
- Docker build steps and Slack notification steps removed from CI workflows (CI no longer depends on Docker Hub or Slack secrets). This repo still contains a `Dockerfile` if needed; remove it separately if desired.

## 2025-10-19 - Project snapshot

### Added
- `docs/legacy-md/` created and populated with migrated markdown (CI/CD, mkdocs migration notes, UV cheat sheet, research notes).
- Project build/docs instructions clarified in `mkdocs.yml` (site URL and Material theme configuration).

### Fixed
- Ran import cleanup, formatting and linting across repository (Black, isort, autoflake were used during cleanup efforts).

---

## How to use this file
- For ongoing development, add a short bullet under the `Unreleased` section for any pull request that introduces a user-facing or repo-level change.
- When you make a release, replace `Unreleased` with a dated release header and add a semantic version if appropriate:

```
## [1.0.0] - 2025-10-30
### Added
- Example release note
```

- Follow the guidance at https://keepachangelog.com for best practices.

---

(Generated/updated on 2025-10-19)

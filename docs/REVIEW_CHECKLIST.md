# Pull request review checklist

Use this checklist before asking for review:

- Keep the pull request focused on one outcome.
- Explain user-visible behavior and important non-goals.
- Add tests for changed behavior and failure modes.
- Update operator documentation when configuration or recovery changes.
- Keep credentials, personal data, and generated build output out of the diff.

A reviewer may ask for evidence that is not useful to keep in the repository,
such as a local benchmark or a redacted deployment log. Summarize that evidence
in the pull request without committing sensitive output.

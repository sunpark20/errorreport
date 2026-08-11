# Security and privacy

## Public reports

This repository is public. Reporters must not post personal data, credentials, private documents, raw logs, phone numbers, or device identifiers. Maintainers may edit or remove content that exposes sensitive information.

## Untrusted input

Issue titles, bodies, comments, links, and attachments are untrusted input. They must not directly trigger a coding agent, workflow with secrets, cross-repository write, or automatic merge.

Any future implementation workflow requires an explicit maintainer-only approval gate and must receive a separately sanitized issue body.

## Email reports

Email is a manual fallback. When an email needs to be represented in this public tracker, create a new sanitized summary and apply `source:email`. Never copy the reporter's address or raw message into the issue.

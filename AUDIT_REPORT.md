# Source Audit — Hand-Gesture-Mouse

Reviewed 4 November 2026 against source commit `8991f24ce0428567149e2f7f3d0ebb75c585112d`. This is a focused code/documentation review and selected local validation, not a penetration test or an exhaustive vulnerability scan. Application files and credentials were not changed. Secret values are intentionally omitted.

## Severity summary

| Critical | High | Medium | Low |
|---:|---:|---:|---:|
| 0 | 1 | 3 | 1 |

Critical: direct resource/identity boundary failure. High: serious exposure or a core reproducibility blocker. Medium: correctness, validation, or deployment issue. Low: maintenance or coverage gap. Static findings describe potential impact; only explicitly listed runtime checks were executed.

## Findings

### 1. High — Start/stop routes have no authentication or CSRF protection and control a host automation process

- **Affected file:** [server.py](<server.py>)
- **Evidence:** Start/stop routes have no authentication or CSRF protection and control a host automation process.
- **Potential impact:** If exposed beyond the local machine, callers can trigger desktop automation.
- **Recommended correction:** Restrict to trusted local use; design authenticated controls before remote deployment.

### 2. Medium — signup

- **Affected file:** [server.py](<server.py>)
- **Evidence:** signup.html and about.html are requested but absent.
- **Potential impact:** GET /signup and /about return HTTP 500; confirmed using Flask test client.
- **Recommended correction:** Add templates or remove these routes in a separate application change.

### 3. Medium — Click and screenshot actions execute on every matching frame with no cooldown

- **Affected file:** [gesture_control.py](<gesture_control.py>)
- **Evidence:** Click and screenshot actions execute on every matching frame with no cooldown.
- **Potential impact:** A held gesture can produce repeated clicks or many screenshots.
- **Recommended correction:** Add debouncing and state transitions.

### 4. Medium — The stored subprocess is not polled for exit before reporting it as running

- **Affected file:** [server.py](<server.py>)
- **Evidence:** The stored subprocess is not polled for exit before reporting it as running.
- **Potential impact:** A failed camera/process can leave stale start/stop state.
- **Recommended correction:** Check poll(), handle process exit, and clean up on shutdown.

### 5. Low — No dependency lockfile or hardware test suite is supplied

- **Affected file:** [gesture_control.py](<gesture_control.py>)
- **Evidence:** No dependency lockfile or hardware test suite is supplied.
- **Potential impact:** MediaPipe API changes and desktop permissions can break startup.
- **Recommended correction:** Pin a tested Python/MediaPipe combination and document a manual hardware checklist.

## Validation evidence

Flask test client: `/` and `/login` returned HTTP 200; `/signup` and `/about` returned HTTP 500 because templates are missing. No webcam, click, or screenshot actions were executed.

## Review scope and limits

Reviewed tracked application source, entry points, manifests/configuration, routes and data models where present, existing documentation, and available test definitions. Generated dependencies and binary artifacts were inventoried rather than treated as authored application logic. Provider calls, cloud deployment, and external data/model claims remain unverified unless explicitly listed above. No secret was rotated and no migration was run against a user database.

## Priorities

Address Critical and High findings before public deployment. Then add regression tests for the affected boundary or workflow, fix Medium issues, and resolve Low maintenance findings. All application corrections require a separate reviewed coding change.

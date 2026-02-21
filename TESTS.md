# YomaAI — Test Documentation

Automated end-to-end tests for YomaAI using **pytest** + **Selenium** (Chrome headless).

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | |
| Google Chrome | latest | Headless mode is used |
| ChromeDriver | matching Chrome version | Must be in `PATH` |
| uv *(recommended)* | latest | Python package runner |
| Running app | — | `npm run dev:full` must be active |

## Installation

### With uv (recommended)

No separate install step is needed — `uv run` handles everything automatically:

```bash
uv run --with pytest --with selenium pytest tests/ -v
```

### With pip

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

## Running the Tests

### Step 1 — Start the application

In a separate terminal:

```bash
npm run dev:full
```

Wait until both the frontend (`http://localhost:5173`) and backend (`http://localhost:3001`) are up.

### Step 2 — Run the tests

```bash
# With uv (zero setup)
uv run --with pytest --with selenium pytest tests/ -v

# With pip (after installing dependencies)
pytest tests/ -v
```

### Useful pytest flags

| Flag | Description |
|------|-------------|
| `-v` | Verbose output — shows each test name and result |
| `-s` | Show `print()` output (useful for debugging) |
| `-x` | Stop on first failure |
| `-k "test_name"` | Run only tests matching the name |
| `--tb=short` | Shorter traceback on failure |

### Examples

```bash
# Run only site-loading tests
uv run --with pytest --with selenium pytest tests/ -v -k "TestSiteLoads"

# Run only the AI generation test
uv run --with pytest --with selenium pytest tests/ -v -k "test_create_story"

# Run only responsiveness tests
uv run --with pytest --with selenium pytest tests/ -v -k "TestResponsiveness"

# Run only dialog tests
uv run --with pytest --with selenium pytest tests/ -v -k "TestYomaDialog"

# Run only error handling tests
uv run --with pytest --with selenium pytest tests/ -v -k "TestErrorHandling"

# Run all extended tests (file 2)
uv run --with pytest --with selenium pytest tests/test_yomaai_extended.py -v

# Stop on first failure with short traceback
uv run --with pytest --with selenium pytest tests/ -v -x --tb=short
```

## Test Structure

```
tests/
├── conftest.py               # Shared fixtures (drivers, base_url)
├── test_yomaai.py            # Core tests (site load, settings, AI generation)
├── test_yomaai_extended.py   # Extended tests (responsiveness, localStorage, errors, dialog)
└── requirements.txt          # Python dependencies (pytest, selenium)
```

### conftest.py — Fixtures

| Fixture | Scope | Viewport | Description |
|---------|-------|----------|-------------|
| `base_url` | session | — | Returns `http://localhost:5173` |
| `driver` | function | 1920×1080 | Desktop Chrome headless, fresh per test |
| `mobile_driver` | function | 375×812 | Mobile Chrome headless (iPhone-like) |
| `tablet_driver` | function | 768×1024 | Tablet Chrome headless (iPad-like) |

All WebDrivers are configured with:
- `--headless=new` — no GUI window
- `--no-sandbox` — required for CI/containers
- `--disable-dev-shm-usage` — prevents shared memory issues

## Test Cases

### test_yomaai.py — Core Tests

#### 1. TestSiteLoads — Does the site load?

| Test | What it checks |
|------|----------------|
| `test_main_page_opens` | Main page (`/`) opens, `<h1>` contains expected text |
| `test_main_page_has_cta_button` | CTA button "Create Idea with Yoma" is visible |
| `test_navigation_links_exist` | Header nav has "Main", "Create new Idea", "Settings" buttons |

**No backend/AI required** — these tests only check the frontend.

#### 2. TestSettingsSkipDialog — Do settings work?

| Test | What it checks |
|------|----------------|
| `test_dialog_shown_by_default` | On `/create`, the Yoma intro dialog ("Yoma:") appears by default |
| `test_skip_dialog_setting_works` | After enabling "Skip dialog" in Settings, navigating to `/create` shows "Craft Your Idea" with no dialog |
| `test_reset_skip_dialog` | After disabling the toggle back, the dialog reappears on `/create` |

**How it works:**
1. The bot navigates to `/settings` and clicks the toggle switch.
2. Then it navigates to `/create` and checks whether the dialog phase or settings phase is displayed.
3. The setting is stored in `localStorage` as `yoma-skip-dialog`.

**No backend/AI required.**

#### 3. TestAIGeneration — Does AI generation work?

| Test | What it checks |
|------|----------------|
| `test_create_story` | Skips dialog, clicks "Create!", waits for loading phase, then waits up to **120 seconds** for AI to return a result. Verifies result text >50 characters and action buttons appear. |

**How it works:**
1. Sets `localStorage['yoma-skip-dialog'] = 'true'` to skip the dialog.
2. Navigates to `/create` — the settings form appears immediately.
3. Clicks the "Create!" rainbow button.
4. Verifies the loading phase ("Yoma is crafting your idea...").
5. Waits up to 120 seconds for the result phase ("Yoma's Idea").
6. Checks text length and button visibility.

**Backend + valid API key required** — makes a real API call.

---

### test_yomaai_extended.py — Extended Tests

#### 4. TestResponsiveness — Adaptive layout

| Test | Viewport | What it checks |
|------|----------|----------------|
| `test_mobile_main_page_no_overflow` | 375×812 | No horizontal scroll on main page |
| `test_mobile_heading_font_size` | 375×812 | `<h1>` font-size is ~36px (`text-4xl`), not ~48px (`md:text-5xl`) |
| `test_mobile_create_page_no_overflow` | 375×812 | No horizontal scroll on `/create` |
| `test_tablet_main_page_no_overflow` | 768×1024 | No horizontal scroll on main page |
| `test_tablet_heading_font_size` | 768×1024 | `<h1>` font-size is ~48px (`md:text-5xl`) since 768px ≥ md breakpoint |
| `test_tablet_create_page_no_overflow` | 768×1024 | No horizontal scroll on `/create` |

**How it works:**
- Compares `document.body.scrollWidth` with `window.innerWidth` to detect horizontal overflow.
- Uses `window.getComputedStyle()` to read the actual rendered font-size and verify Tailwind responsive classes apply correctly.

**No backend/AI required.**

#### 5. TestLocalStorage — Persistence and cleanup

| Test | What it checks |
|------|----------------|
| `test_skip_dialog_persists_after_reload` | Enable skip dialog → reload page → value still `'true'` in localStorage → dialog is skipped on `/create` |
| `test_clearing_localstorage_restores_default` | Set skip dialog → remove key → navigate to `/create` → dialog reappears |

**How it works:**
- Uses `driver.execute_script()` to read/write/remove `localStorage` items.
- Verifies both the raw value in storage and the actual UI behavior.

**No backend/AI required.**

#### 6. TestErrorHandling — Error display

| Test | What it checks |
|------|----------------|
| `test_api_error_shows_red_message` | When backend returns 500 (no API key), a red error `div` with `border-red-300` appears containing "API key" text |
| `test_network_error_shows_failed_message` | When backend is unreachable (fetch throws), error message "Failed to connect to the server" appears |

**How it works:**
- Uses JavaScript to **override `window.fetch`** in the browser:
  - `_mock_fetch_api_error()` — makes `/api/generate` return `{ status: 500, error: "API key for Claude is not configured" }`
  - `_mock_fetch_network_error()` — makes `/api/generate` throw `TypeError('Failed to fetch')`
- This avoids needing to stop the real backend or change `.env` during tests.

**No real backend required** — fetch is mocked in-browser.

#### 7. TestResultButtons — Post-generation actions

| Test | What it checks |
|------|----------------|
| `test_create_another_idea_resets_to_settings` | Clicking "Create Another Idea" returns to settings with all `<select>` values reset to `""` and textarea empty |
| `test_regenerate_produces_new_result` | Clicking "Regenerate" shows loading phase again, then renders a new result |

**How it works:**
- Uses `_mock_fetch_success()` to get instant fake AI responses (no 120s wait).
- `_generate_with_mock()` helper runs the full cycle: skip dialog → mock fetch → click Create! → wait for result.
- After "Create Another Idea": checks every `select.sketchy-select` value is `""` and `#additional-details` textarea is empty.
- After "Regenerate": verifies the loading phase reappears before the new result.

**No real backend required** — fetch is mocked.

#### 8. TestYomaDialog — Typewriter dialog flow

| Test | What it checks |
|------|----------------|
| `test_next_button_appears_after_first_line` | After the typewriter finishes line 1, a "Next" button appears |
| `test_next_shows_second_line` | Clicking "Next" advances to line 2 (contains "help you create" / "ready") |
| `test_lets_go_button_on_last_line` | On the last line, "Let's go!" replaces "Next" |
| `test_lets_go_transitions_to_settings` | Clicking "Let's go!" transitions to the settings phase ("Craft Your Idea") |
| `test_skip_dialog_button` | Clicking "Skip dialog" at any point skips directly to settings |

**How it works:**
- Opens `/create` with clean `localStorage` (no skip-dialog) so the dialog appears.
- Waits ~1 second for the typewriter effect to complete (3ms per char × ~80 chars ≈ 240ms + buffer).
- Verifies button text changes from "Next" to "Let's go!" on the final line.
- Confirms "Skip dialog" works even before the typewriter finishes.

**No backend/AI required.**

## Fetch Mocking

Several extended tests override `window.fetch` in the browser to avoid real API calls. This provides:

- **Speed** — no 120-second waits for AI responses
- **Isolation** — tests don't depend on a running backend or valid API keys
- **Reliability** — no flaky failures from network timeouts or rate limits

| Helper function | What it does |
|----------------|--------------|
| `_mock_fetch_success(driver)` | `/api/generate` returns instant mock markdown response |
| `_mock_fetch_api_error(driver)` | `/api/generate` returns `500` with error JSON |
| `_mock_fetch_network_error(driver)` | `/api/generate` throws `TypeError` (connection refused) |

The original `window.fetch` is preserved as `window.__originalFetch`, and non-API requests pass through normally.

## Timeouts

| Context | Timeout | Reason |
|---------|---------|--------|
| General element waits | 10 s | Standard UI rendering time |
| Implicit wait | 5 s | Configured in WebDriver fixtures |
| AI generation result | 120 s | LLM APIs can be slow (only in `test_create_story`) |
| Typewriter wait | 1 s | 3ms/char × ~80 chars + buffer |

## Summary Table

| # | Class | File | Tests | Backend needed? |
|---|-------|------|-------|-----------------|
| 1 | `TestSiteLoads` | `test_yomaai.py` | 3 | No |
| 2 | `TestSettingsSkipDialog` | `test_yomaai.py` | 3 | No |
| 3 | `TestAIGeneration` | `test_yomaai.py` | 1 | **Yes** (real API) |
| 4 | `TestResponsiveness` | `test_yomaai_extended.py` | 6 | No |
| 5 | `TestLocalStorage` | `test_yomaai_extended.py` | 2 | No |
| 6 | `TestErrorHandling` | `test_yomaai_extended.py` | 2 | No (mocked) |
| 7 | `TestResultButtons` | `test_yomaai_extended.py` | 2 | No (mocked) |
| 8 | `TestYomaDialog` | `test_yomaai_extended.py` | 5 | No |
| | | **Total** | **24** | |

## Troubleshooting

### `WebDriverException: chrome not reachable`

Chrome or ChromeDriver is not installed or not in `PATH`.

```bash
# Check Chrome
google-chrome --version

# Check ChromeDriver
chromedriver --version
```

### `ConnectionRefusedError` or elements not found

The app is not running. Start it first:

```bash
npm run dev:full
```

### AI test fails with "Failed to connect to the server"

The backend (`http://localhost:3001`) is not running or the API key is not configured in `.env`.

### AI test times out after 120 seconds

The AI provider is taking too long or the API key is invalid. Check the backend terminal for error messages.

### Dialog tests fail (typewriter timing)

The `_wait_for_typewriter()` helper sleeps for 1 second. If your machine is very slow, increase the sleep time in the helper or run fewer parallel processes.

### Responsiveness tests fail (font size)

Tailwind CSS breakpoints depend on the actual viewport width. Verify that the `mobile_driver` fixture has `--window-size=375,812` and `tablet_driver` has `--window-size=768,1024`. Some Chrome versions may report slightly different inner widths.

## CI / Docker

For CI environments, ensure:

1. Chrome is installed (`apt install google-chrome-stable` or use a Chrome-based Docker image)
2. ChromeDriver version matches Chrome
3. The app is started before tests (e.g., using `concurrently` or a `wait-on` script)
4. Environment variable `CI=true` may be useful for additional headless flags

Example CI step:

```bash
npm run dev:full &
sleep 10
uv run --with pytest --with selenium pytest tests/ -v
```

To skip the real AI test in CI (no API key available):

```bash
uv run --with pytest --with selenium pytest tests/ -v -k "not test_create_story"
```

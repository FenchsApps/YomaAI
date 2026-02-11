# YomaAI — Documentation

## What is YomaAI?

**YomaAI** is a web application that uses artificial intelligence to generate original, non-cliché ideas for creative projects. It is designed for writers, mangakas, screenwriters, game designers, and anyone who needs a spark of inspiration.

YomaAI is **not** a chatbot. It is a specialized idea generator with a curated set of 20 configurable parameters that shape the AI's output. The core philosophy: **every idea must feel fresh** — no overused tropes, no rehashed plots.

---

## How It Works

### Architecture

YomaAI consists of two parts:

- **Frontend** — React SPA (Single Page Application) built with Vite, TypeScript, and Tailwind CSS. Serves the user interface.
- **Backend** — Express.js server that acts as a secure proxy between the frontend and AI APIs (Claude / OpenRouter). API keys are stored server-side in `.env` and never exposed to the client.

### Flow

```
User → selects 20 settings → clicks "Create!"
  ↓
Frontend builds a structured prompt from selections
  ↓
POST /api/generate { prompt: "..." }
  ↓
Backend injects the system prompt + user prompt → sends to AI API
  ↓
AI generates an original idea → returns to frontend
  ↓
Result rendered with Markdown formatting
```

---

## Pages

### `/` — Main Page

Landing page with a call-to-action. Displays the message "Can't come up with an idea for your work?" and a button leading to the idea creation page.

### `/create` — Create Idea

The core feature. This page has three phases:

1. **Dialog Phase** — A typewriter-animated intro dialog from Yoma (the AI character). Two lines of text appear character by character (3ms per character). The user can skip the dialog or disable it permanently in Settings.

2. **Settings Phase** — A grid of 20 dropdown menus where the user configures their desired idea. All settings are optional — the more you fill in, the more tailored the result. Settings include:

   | # | Setting | Description |
   |---|---------|-------------|
   | 1 | Genre | Fantasy, Sci-Fi, Horror, Romance, etc. (22 options) |
   | 2 | Medium / Format | Manga, Anime, Book, Webtoon, Visual Novel, etc. (22 options) |
   | 3 | Setting Country | Where the story takes place — AI adapts to the culture (22 options) |
   | 4 | Character Names Origin | What culture the character names come from (16 options) |
   | 5 | Target Audience | Children, Teens, Adults, All Ages, etc. (7 options) |
   | 6 | Tone / Mood | Light & Fun, Dark & Gritty, Philosophical, etc. (14 options) |
   | 7 | Setting Era | Ancient, Medieval, Modern, Far Future, etc. (12 options) |
   | 8 | Number of Main Characters | Solo, Duo, Small Group, Ensemble (6 options) |
   | 9 | Protagonist Type | Classic Hero, Anti-Hero, Villain, Trickster, etc. (12 options) |
   | 10 | Main Conflict | Person vs Person, vs Society, vs Self, etc. (10 options) |
   | 11 | Story Length | One-shot, Medium, Long, Epic, Trilogy (8 options) |
   | 12 | Romance Level | None, Subtle, Central Theme, Slow Burn (8 options) |
   | 13 | Action / Combat Level | None to Extreme, Martial Arts Focus (7 options) |
   | 14 | World Building Depth | Minimal to Extremely Intricate (6 options) |
   | 15 | Magic / Power System | None, Soft/Hard Magic, Cultivation, Tech (10 options) |
   | 16 | Plot Complexity | Simple to Multiple Interweaving Storylines (7 options) |
   | 17 | Ending Preference | Happy, Tragic, Twist, Open-ended, etc. (8 options) |
   | 18 | Core Themes | Friendship, Revenge, Identity, Sacrifice, etc. (16 options) |
   | 19 | Narrative Style | First Person, Multiple POVs, Unreliable Narrator, etc. (10 options) |
   | 20 | Unique Twist / Element | Time Loop, Parallel Universes, Body Swap, etc. (15 options) |

   After configuring, the user clicks the rainbow-animated **"Create!"** button.

3. **Result Phase** — The AI's response is displayed with full Markdown rendering (headings, bold, lists, etc.). The user can regenerate or start over.

### `/settings` — Settings

Application settings stored in `localStorage`:

- **Skip Yoma's intro dialog** — Toggle to bypass the typewriter dialog on the Create page.

---

## Environment Variables

All configuration is done via the `.env` file in the project root. A template is provided in `.env.example`.

| Variable | Description | Example |
|----------|-------------|---------|
| `WhatAIYomaWillUse` | Which AI provider to use | `Claude` or `Openrouter` |
| `ClaudeAPI` | Anthropic API key | `sk-ant-...` |
| `ClaudeModel` | Claude model identifier | `claude-sonnet-4-20250514` |
| `OpenrouterAPI` | OpenRouter API key | `sk-or-v1-...` |
| `OpenrouterModel` | OpenRouter model identifier | `openai/gpt-4o` |
| `PORT` | Backend server port (optional) | `3001` (default) |

The `WhatAIYomaWillUse` variable is **case-insensitive** — `Claude`, `claude`, `CLAUDE` all work.

If set to `Claude`, the server uses `ClaudeAPI` + `ClaudeModel`.
If set to `Openrouter`, the server uses `OpenrouterAPI` + `OpenrouterModel`.

---

## API

### `POST /api/generate`

Generates a creative idea.

**Request body:**

```json
{
  "prompt": "Create an original creative idea based on these preferences:\n\nGenre: Dark Fantasy\nMedium / Format: Manga\n..."
}
```

**Success response (200):**

```json
{
  "result": "## Title: ...\n\n**Logline:** ...\n\n### Synopsis\n..."
}
```

**Error responses:**

- `400` — Missing prompt
- `500` — API key not configured or AI API failure

---

## Anti-Cliché System

YomaAI uses a carefully crafted system prompt that instructs the AI to:

1. **Never** suggest overused tropes without a fresh twist
2. Make every idea contain at least one element that feels new
3. Blend unexpected genres, cultures, and concepts
4. Create characters with real contradictions, not archetypes
5. Build worlds with unique rules that affect the entire story
6. Deeply integrate chosen cultures (mythology, norms, history, art) — not surface-level stereotypes
7. Adapt pacing and structure to the chosen medium

The AI's output is structured into: **Title**, **Logline**, **Synopsis**, **Main Characters**, **The Hook**, **Key Themes**, and **Opening Scene**.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend framework | React 19 |
| Language | TypeScript |
| Bundler | Vite 7 |
| Styling | Tailwind CSS 4 |
| Routing | React Router DOM 7 |
| Markdown | react-markdown |
| Backend | Express 5 (Node.js) |
| AI APIs | Anthropic Claude API, OpenRouter API |
| Fonts | Walter Turncoat (header), Chilanka (body) |

---

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start Vite dev server (frontend only) |
| `npm run server` | Start Express API server (backend only) |
| `npm run dev:full` | Start both frontend and backend concurrently |
| `npm run build` | TypeScript check + production build |
| `npm run lint` | Run ESLint |
| `npm run preview` | Preview production build |

---

## License

**AGPL-3.0** — GNU Affero General Public License v3.0

Author: **FenchsApps** — [https://github.com/FenchsApps](https://github.com/FenchsApps)

Repository: [https://github.com/FenchsApps/YomaAI](https://github.com/FenchsApps/YomaAI)

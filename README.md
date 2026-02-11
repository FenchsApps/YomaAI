# YomaAI — Creative Idea Generator

**YomaAI** is an AI-powered creative assistant that helps you brainstorm original, non-cliché ideas for your creative projects — manga, books, anime, comics, visual novels, games, and more.

Built with a unique **hand-drawn paper notebook** aesthetic.

## Features

- **20 Flexible Settings** — Fine-tune your idea: genre, country, medium, character names, tone, era, conflict type, power system, and more
- **AI-Powered Generation** — Supports Claude (Anthropic) and OpenRouter APIs
- **Anti-Cliché System** — Crafted prompts ensure genuinely original ideas, not rehashed tropes
- **Markdown Rendering** — AI responses are beautifully formatted with headings, lists, bold, and more
- **Yoma Dialog** — A charming typewriter intro dialog (can be skipped or disabled in settings)
- **Rainbow Create Button** — Nyancat-style animated gradient
- **Paper Aesthetic** — Hand-drawn style with sketchy buttons and crumpled paper background

## Tech Stack

| Layer    | Technology                     |
|----------|--------------------------------|
| Frontend | React, TypeScript, Tailwind CSS |
| Bundler  | Vite                           |
| Backend  | Express.js (Node.js)           |
| AI       | Claude API / OpenRouter API    |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/FenchsApps/YomaAI.git
cd YomaAI
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

Copy the example and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Which AI provider to use: "Claude" or "Openrouter"
WhatAIYomaWillUse=Claude

# OpenRouter settings
OpenrouterAPI=your_openrouter_key_here
OpenrouterModel=openai/gpt-4o

# Claude (Anthropic) settings
ClaudeAPI=your_claude_key_here
ClaudeModel=claude-sonnet-4-20250514
```

### 4. Run the project

Start both frontend and backend:

```bash
npm run dev:full
```

Or run them separately:

```bash
# Frontend (Vite dev server)
npm run dev

# Backend (Express API server)
npm run server
```

The frontend runs on `http://localhost:5173` and the backend on `http://localhost:3001`.

## Project Structure

```
YomaAI/
├── server/
│   └── index.ts               # Express API server with anti-cliché system prompt
├── src/
│   ├── components/
│   │   ├── Header.tsx          # Navigation header (Walter Turncoat font)
│   │   ├── Footer.tsx          # Footer with license & credits
│   │   └── TypewriterDialog.tsx # Yoma intro dialog with typewriter effect
│   ├── data/
│   │   └── ideaOptions.ts     # 20 configurable idea settings
│   ├── pages/
│   │   ├── MainPage.tsx        # Landing page
│   │   ├── CreateIdeaPage.tsx  # AI idea generator (dialog → settings → result)
│   │   └── SettingsPage.tsx    # App settings (skip dialog toggle)
│   ├── App.tsx                 # App routes
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles, paper theme, rainbow button
├── .env.example                # Environment variables template
├── index.html                  # HTML entry
├── vite.config.ts              # Vite config with Tailwind & proxy
├── package.json
├── LICENSE                     # AGPL-3.0
└── README.md
```

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See [LICENSE](./LICENSE) for details.

## Author

**FenchsApps** — [https://github.com/FenchsApps](https://github.com/FenchsApps)

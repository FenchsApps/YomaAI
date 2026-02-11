import path from 'path'
import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

dotenv.config({ path: path.resolve(import.meta.dirname, '..', '.env') })

const app = express()
app.use(cors())
app.use(express.json())

const PORT = process.env.PORT || 3001

const AI_PROVIDER = (process.env.WhatAIYomaWillUse || 'Claude').toLowerCase()

function getAIConfig() {
  if (AI_PROVIDER === 'claude') {
    return {
      provider: 'Claude' as const,
      apiKey: process.env.ClaudeAPI || '',
      model: process.env.ClaudeModel || 'claude-sonnet-4-20250514',
    }
  }
  return {
    provider: 'Openrouter' as const,
    apiKey: process.env.OpenrouterAPI || '',
    model: process.env.OpenrouterModel || 'openai/gpt-4o',
  }
}

const SYSTEM_PROMPT = `You are YomaAI — a uniquely creative idea generator for storytelling projects. Your entire purpose is to craft ORIGINAL, NON-CLICHÉ ideas that surprise and inspire creators.

CORE RULES:
1. NEVER suggest overused tropes without a fresh twist. Avoid: "chosen one saves the world", "boy meets girl at school", "hero gets isekai'd and becomes overpowered", "secret prince/princess", or any idea that sounds like it's been done 1000 times.
2. Every idea MUST have at least one element that makes someone think "I've never seen that before."
3. Blend unexpected genres, cultures, and concepts. Combine things that shouldn't work together but do.
4. Characters must feel like REAL people with contradictions, not archetypes. Give them unusual motivations, quirks, or backstories.
5. The world/setting should have at least one unique rule or feature that affects the entire story.

WHEN THE USER PROVIDES PREFERENCES:
- Respect their chosen genre, medium, country, tone, and all other settings.
- If a country/region is specified, deeply integrate that culture's mythology, social norms, history, art, food, architecture, and philosophy — not surface-level stereotypes.
- If character name origins are specified, use authentic names from that culture with correct conventions.
- Adapt the idea's structure and pacing to match the chosen medium (manga pacing differs from novel pacing, etc.).

YOUR OUTPUT FORMAT:
Structure your response clearly with these sections:
- **Title** — A compelling, memorable title
- **Logline** — One powerful sentence that captures the essence
- **Synopsis** — 2-3 paragraphs describing the core story concept
- **Main Characters** — 2-4 key characters with names, brief descriptions, and what makes them unique
- **The Hook** — What makes this idea stand out from everything else
- **Key Themes** — The deeper meanings woven into the story
- **Opening Scene** — A vivid description of how the story could begin

STYLE:
- Write with enthusiasm and passion, as if you're pitching this idea to a producer.
- Be specific — vague ideas are boring. Give concrete details.
- Respond in the same language the user writes in.
- If the user writes in English, respond in English. If in Russian, respond in Russian. And so on.

Remember: Your reputation depends on generating ideas that are genuinely fresh. Every idea should feel like it could be the next hit that redefines its genre.`

app.post('/api/generate', async (req, res) => {
  const { prompt } = req.body

  if (!prompt) {
    res.status(400).json({ error: 'Prompt is required' })
    return
  }

  const config = getAIConfig()

  if (!config.apiKey) {
    res.status(500).json({ error: `API key for ${config.provider} is not configured` })
    return
  }

  try {
    if (config.provider === 'Claude') {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': config.apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: config.model,
          max_tokens: 4096,
          system: SYSTEM_PROMPT,
          messages: [{ role: 'user', content: prompt }],
        }),
      })

      if (!response.ok) {
        const err = await response.text()
        res.status(response.status).json({ error: err })
        return
      }

      const data = await response.json()
      const text = data.content?.[0]?.text || ''
      res.json({ result: text })
    } else {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${config.apiKey}`,
        },
        body: JSON.stringify({
          model: config.model,
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            { role: 'user', content: prompt },
          ],
          max_tokens: 4096,
        }),
      })

      if (!response.ok) {
        const err = await response.text()
        res.status(response.status).json({ error: err })
        return
      }

      const data = await response.json()
      const text = data.choices?.[0]?.message?.content || ''
      res.json({ result: text })
    }
  } catch (error) {
    console.error('AI API error:', error)
    res.status(500).json({ error: 'Failed to generate idea' })
  }
})

app.listen(PORT, () => {
  const config = getAIConfig()
  console.log(`YomaAI server running on port ${PORT}`)
  console.log(`AI Provider: ${config.provider} | Model: ${config.model}`)
  console.log(`API Key: ${config.apiKey ? '***configured***' : '!!! MISSING !!!'}`)
})

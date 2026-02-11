export interface IdeaSetting {
  id: string
  label: string
  options: string[]
}

export const ideaSettings: IdeaSetting[] = [
  {
    id: 'genre',
    label: 'Genre',
    options: [
      'Fantasy', 'Dark Fantasy', 'Sci-Fi', 'Cyberpunk', 'Steampunk',
      'Romance', 'Horror', 'Mystery', 'Thriller', 'Comedy',
      'Drama', 'Adventure', 'Slice of Life', 'Psychological',
      'Historical', 'Supernatural', 'Mecha', 'Isekai',
      'Post-Apocalyptic', 'Magical Realism', 'Gothic', 'Noir',
    ],
  },
  {
    id: 'medium',
    label: 'Medium / Format',
    options: [
      'Manga', 'Anime', 'Light Novel', 'Web Novel', 'Book / Novel',
      'Comic', 'Webtoon', 'Visual Novel', 'Short Story', 'Film Script',
      'TV Series', 'Stage Play', 'Audio Drama', 'Game Story',
      'Graphic Novel', 'Poetry Collection', 'Screenplay', 'Web Series',
      'Musical', 'Anthology', 'Manhwa', 'Manhua',
    ],
  },
  {
    id: 'settingCountry',
    label: 'Setting Country / Region',
    options: [
      'Japan', 'South Korea', 'China', 'United States', 'United Kingdom',
      'France', 'Germany', 'Russia', 'Italy', 'Spain', 'Brazil',
      'India', 'Egypt', 'Mexico', 'Scandinavia', 'Middle East',
      'Australia', 'Canada', 'Southeast Asia', 'Central Africa',
      'Ancient Greece', 'Fictional / Fantasy World',
    ],
  },
  {
    id: 'nameOrigin',
    label: 'Character Names Origin',
    options: [
      'Japanese', 'Korean', 'Chinese', 'English', 'French',
      'German', 'Russian', 'Italian', 'Spanish', 'Arabic',
      'Indian', 'Scandinavian', 'Greek', 'Latin',
      'Fantasy / Made-up', 'Mixed / Multicultural',
    ],
  },
  {
    id: 'targetAudience',
    label: 'Target Audience',
    options: [
      'Children (6-12)', 'Teens (13-17)', 'Young Adults (18-25)',
      'Adults (25+)', 'All Ages', 'Mature / Seinen', 'Josei',
    ],
  },
  {
    id: 'tone',
    label: 'Tone / Mood',
    options: [
      'Light & Fun', 'Dark & Gritty', 'Humorous', 'Serious',
      'Melancholic', 'Uplifting', 'Mysterious', 'Romantic',
      'Epic & Grand', 'Whimsical', 'Bittersweet', 'Intense',
      'Philosophical', 'Nostalgic',
    ],
  },
  {
    id: 'era',
    label: 'Setting Era',
    options: [
      'Ancient', 'Medieval', 'Renaissance', 'Edo Period', 'Victorian',
      'World War Era', 'Modern Day', 'Near Future (2030-2100)',
      'Far Future (2100+)', 'Timeless / Ambiguous',
      'Multiple Time Periods', 'Alternate History',
    ],
  },
  {
    id: 'protagonistCount',
    label: 'Number of Main Characters',
    options: [
      'Solo (1)', 'Duo (2)', 'Small Group (3-4)', 'Party (5-6)',
      'Large Ensemble (7+)', 'Rotating Protagonists',
    ],
  },
  {
    id: 'protagonistType',
    label: 'Protagonist Type',
    options: [
      'Classic Hero', 'Anti-Hero', 'Villain Protagonist', 'Reluctant Hero',
      'Everyday Person', 'Chosen One', 'Outcast / Loner', 'Leader / Commander',
      'Trickster', 'Scholar / Investigator', 'Tragic Figure', 'Child Prodigy',
    ],
  },
  {
    id: 'conflictType',
    label: 'Main Conflict',
    options: [
      'Person vs Person', 'Person vs Nature', 'Person vs Society',
      'Person vs Self', 'Person vs Technology', 'Person vs Supernatural',
      'Person vs Fate / Destiny', 'Person vs Unknown',
      'Faction vs Faction', 'Internal Political Struggle',
    ],
  },
  {
    id: 'storyLength',
    label: 'Story Length',
    options: [
      'One-shot', 'Short (1-3 chapters)', 'Medium (10-30 chapters)',
      'Long (50-100 chapters)', 'Epic (200+ chapters)',
      'Ongoing / No set end', 'Trilogy', 'Saga (5+ volumes)',
    ],
  },
  {
    id: 'romanceLevel',
    label: 'Romance Level',
    options: [
      'None', 'Subtle Hints', 'Secondary Plot', 'Major Plot',
      'Central Theme', 'Love Triangle', 'Slow Burn', 'Forbidden Love',
    ],
  },
  {
    id: 'actionLevel',
    label: 'Action / Combat Level',
    options: [
      'None', 'Minimal', 'Moderate', 'High', 'Extreme / Non-stop',
      'Strategic / Tactical', 'Martial Arts Focus',
    ],
  },
  {
    id: 'worldBuilding',
    label: 'World Building Depth',
    options: [
      'Minimal (Real World)', 'Light', 'Moderate',
      'Deep & Detailed', 'Extremely Intricate',
      'Real World with Hidden Layer',
    ],
  },
  {
    id: 'powerSystem',
    label: 'Magic / Power System',
    options: [
      'None (Realistic)', 'Soft Magic', 'Hard Magic (Rule-based)',
      'Supernatural Powers', 'Advanced Technology', 'Psionics / Mental',
      'Mix of Magic & Tech', 'Cursed / Forbidden Arts',
      'Cultivation / Chi', 'Divine / Godly Powers',
    ],
  },
  {
    id: 'plotComplexity',
    label: 'Plot Complexity',
    options: [
      'Simple / Linear', 'Moderate Twists', 'Complex / Multi-layered',
      'Non-linear / Fragmented', 'Episodic', 'Mystery / Puzzle-like',
      'Multiple Interweaving Storylines',
    ],
  },
  {
    id: 'endingPreference',
    label: 'Ending Preference',
    options: [
      'Happy Ending', 'Bittersweet', 'Tragic', 'Open-ended',
      'Twist Ending', 'Ambiguous', 'Cyclic / Full Circle',
      'No Preference',
    ],
  },
  {
    id: 'themes',
    label: 'Core Themes',
    options: [
      'Friendship', 'Love', 'Revenge', 'Redemption', 'Power & Corruption',
      'Freedom', 'Identity / Self-discovery', 'Survival', 'Justice',
      'Family', 'Betrayal', 'Growth / Coming of Age', 'Sacrifice',
      'Loneliness', 'War & Peace', 'Hope vs Despair',
    ],
  },
  {
    id: 'narrativeStyle',
    label: 'Narrative Style',
    options: [
      'First Person', 'Third Person Limited', 'Third Person Omniscient',
      'Multiple POVs', 'Unreliable Narrator', 'Diary / Journal Format',
      'Epistolary (Letters)', 'Stream of Consciousness',
      'Documentary Style', 'Second Person',
    ],
  },
  {
    id: 'uniqueElement',
    label: 'Unique Twist / Element',
    options: [
      'Time Loop', 'Memory Manipulation', 'Parallel Universes',
      'Body Swap', 'Unreliable Reality', 'Secret Society',
      'Ancient Prophecy', 'Living Weapons', 'Sentient World',
      'Reverse Roles (Hero-Villain)', 'Dream World', 'Game-like System',
      'Forbidden Knowledge', 'Symbiotic Entities',
      'Let AI Surprise Me',
    ],
  },
]

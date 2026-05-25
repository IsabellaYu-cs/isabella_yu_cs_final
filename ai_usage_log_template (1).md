# AI Usage Log

## Entry 1

### Date
2026-04-28
### AI Tool Used
ChatGPT
### What I Asked AI
I asked for suggestions on how to improve my initial project idea based on my own concept, including an adaptive AP quiz system with topic tracking, timer, and a possible visualization feature.
### Why I Asked
I wanted feedback on whether my idea was too simple or too complex, and how to make it meet the project requirements while still being realistic to build.
### What AI Gave Me
The AI gave suggestions on how to structure the project more clearly and how to organize features such as adaptive difficulty, topic tracking, timer-based analysis, and data visualization.
### What I Used
I used the suggestions about simplifying the project scope, organizing it into clear components, and adding features like topic analysis, adaptive difficulty, and a simple bar chart for visualization.
### What I Changed or Rejected
I simplified the original idea by reducing unnecessary complexity and focusing on a smaller question set. I also did not initially include the idea of adding a joke/break mode.
### What I Still Do Not Fully Understand
I still need to better understand how to connect timer data with adaptive difficulty in a clean and simple way.
### My Next Step
My next step is to build the basic quiz system first, then gradually add adaptive difficulty, topic tracking, timer functionality, and visualization.

---

## Entry 2

### Date
2026-05-22 to 2026-05-24

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to "grill me" on my PRD template for my CS final project - an adaptive AP Microeconomics quiz system. I wanted to stress-test my design decisions and refine the project requirements through a Q&A session conducted in Chinese (for language practice).

### Why I Asked
I needed to think critically about my project design, identify gaps in my requirements, and create a detailed, well-structured PRD before starting development.

### What AI Gave Me
Claude asked me a series of probing questions about my project, one at a time, covering:
- Adaptive logic (how the system responds to correct/incorrect answers)
- Question sets and retry cycles
- Topic selection and high-frequency topics
- Data source (AP past exam PDFs)
- Topic tagging via keyword matching
- Timer functionality
- User system and data saving
- Development timeline (2 days)
- JSON data structure

Claude also updated my PRD2 file with all the refined requirements.

### What I Used
- All the adaptive logic design: sets of 3 questions, retry system with "I got it" button
- Topic-level high-frequency marking
- Automatic question extraction from PDFs
- Keyword-based topic tagging (broad topics only)
- CLI interface with topic selection
- User-controlled timer per question
- Per-user progress saving (no password, just username)
- JSON data structure with A/B/C/D/E options, topic tags, and AI-generated explanations
- 2-day development plan with priority ordering

### What I Changed or Rejected
- Removed AP Biology, focusing only on AP Microeconomics
- Removed difficulty level from question data (hard to determine consistently)
- Simplified user system: no registration or password, just enter username
- Rejected stretch feature of using time to adjust difficulty (time is for analysis only)

### What I Still Do Not Fully Understand
- How to implement the keyword matching system for topic tagging
- How to automatically extract questions from PDFs while preserving formatting
- How to generate good explanations using AI

### My Next Step
Start building the project following the 2-day development plan:
1. Day 1: Extract questions from PDFs → JSON, build basic quiz, add topic selection, implement adaptive logic
2. Day 2: Add timer, user system, final score summary, weak topic analysis, and optional break mode/charts

---

## Entry 3

### Date
2026-05-24

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to start implementing the AP Microeconomics quiz system based on our PRD2. We began with extracting questions from the AP exam PDFs I had downloaded.

### Why I Asked
I needed to start building the actual project according to the development plan we created.

### What AI Gave Me
Claude helped me:
1. Created a Python script to extract questions from AP Microeconomics PDFs (2022 exam)
2. Extracted 51 multiple-choice questions with answers
3. Implemented keyword-based topic tagging system
4. Built a basic CLI quiz program with:
   - Welcome screen with username input
   - Topic selection menu showing all 8 topics
   - Question display with A/B/C/D/E options
   - Answer checking and feedback
   - Round completion summary
   - Adaptive logic structure (retry/skip/continue)

### What I Used
- Question extraction script (extract_questions.py)
- Basic quiz program (quiz.py)
- Extracted questions in JSON format (questions.json)
- Topic tagging with keywords
- High-frequency topics: Supply & Demand, Market Structures, Cost Curves, Elasticity, Externalities & Public Goods, Factor Markets, Utility Maximization

### What I Changed or Rejected
- The 2023 PDF doesn't have an answer key, so only used 2022 questions
- Some questions had parsing issues (mixed up options) - will need to fix later
- 5 questions have no topic tags - need to improve keyword matching

### What I Still Do Not Fully Understand
- How to fix the parsing issues where options get mixed up between questions
- How to generate explanations for each question using AI
- How to properly implement the "I got it" button during retry cycles

### My Next Step
1. Fix the parsing issues in the extraction script
2. Generate explanations for each question using AI
3. Implement the full adaptive logic (retry system with "I got it" button)
4. Add timer functionality
5. Add user progress saving/loading
6. Build final summary with weak topic analysis

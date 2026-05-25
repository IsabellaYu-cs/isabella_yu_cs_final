# Final Project PRD

## Project Title

Adaptive AP Quiz & Learning Tracker System

## One Sentence Pitch

My project is a program that helps students practice AP Microeconomics questions through an adaptive quiz system that adjusts difficulty based on performance, tracks learning behavior, and provides personalized feedback and review suggestions.

## Target User

This project is for high school students who are preparing for the AP Microeconomics exam and want a structured way to practice questions, identify weak topics, and improve learning efficiency.



## Purpose

This is useful because students often practice questions without understanding their weaknesses or learning patterns. This system not only tests knowledge but also analyzes performance, tracks response time, and gives feedback on weak topics to improve studying efficiency.

## MVP

The smallest working version will be a CLI program that allows the user to select an AP Microeconomics topic from a menu, then answer multiple-choice questions with an adaptive topic system. The system works in sets of questions per topic (more for high-frequency topics). If the user answers all correctly, the system asks whether to continue with the same topic or move to a different one. If any answer is wrong, the system shows an explanation and the user must answer a new set correctly before being asked again. At any point during the retry cycle, the user can choose an "I got it" option to force-skip to the next topic. The user can also view a final score summary with weak topic analysis.

## Must Have Features

1. AP Microeconomics question set
2. Answer multiple-choice questions with correctness checking
3. Adaptive topic system in question sets:
   - Questions are ordered by difficulty within each topic
   - High-frequency exam topics have more questions per round; other topics have fewer
   - All correct in a set → ask user: continue same topic or move to next
   - Any wrong → show explanation, then require all correct in a new set before asking again
   - "I got it" button available during retry to force-skip to next topic
4. Topic-based tracking of incorrect answers to identify weak areas
5. Show explanation after each wrong answer
6. Final score summary: per-topic accuracy rate and average time per question
7. Weak topic analysis: topics where the user got wrong in the first set of 3 questions
8. Response time tracking per question: user presses start when ready, timer stops when answer is submitted, time displayed after each question


## Nice To Have Features

1. Break mode: user can switch anytime via a button in the top right corner, shows motivational messages or jokes
2. Visual chart showing performance by topic (using matplotlib or similar)

## Stretch Feature

1. Time-based analysis: show average time per topic in final summary to help identify harder or less familiar topics (longer time = less familiar or more difficult topic)

## Python Skills I Might Use

### Functions
Separate functions for quiz flow, scoring, analysis, and menu system
### Lists
Store questions and user answers
### Dictionaries
Store topics, scores, and statistics
### APIs
not required
### File I/O
- Load questions from JSON files
- Save/load each user's progress to separate JSON files (per-user data: scores, completed topics, weak topics, time records)
### OOP
Question class to structure quiz data
### Error Handling
- Handle invalid inputs for answers and menu selection

## User System

- No registration or password required
- User enters a username at startup to identify themselves
- Each user's progress saved separately in JSON files
- Backend written in Python
## Data Plan

What data does my project need?
- AP Microeconomics multiple-choice questions
- Each question includes:
    - question text
    - options (A/B/C/D/E as keys)
    - correct answer
    - topic tags (array)
    - explanation (required for adaptive feedback, AI-generated then manually reviewed)

### JSON Structure Example
```json
{
  "question": "If accounting profit is greater than zero...",
  "options": {
    "A": "The firm has no fixed cost.",
    "B": "The firm has positive economic profit.",
    "C": "The firm's total revenue exceeds its explicit cost.",
    "D": "The firm's economic profit exceeds its opportunity cost.",
    "E": "New firms will enter the industry in the long run."
  },
  "answer": "C",
  "topics": ["accounting profit", "economic profit"],
  "explanation": "Accounting profit = total revenue - explicit costs..."
}
```
Where will the data come from?
- Extracted from AP Microeconomics past exam PDFs (2022, 2023) using automatic text extraction
- Questions are in standard format: question number + text + A/B/C/E options, with separate answer key page

How will questions be tagged by topic?
- Keyword matching using broad topic keywords only (e.g., "perfect competition", "monopoly", "elasticity", "supply and demand")
- Each question can have multiple topic tags
- All matching topics are kept (no filtering by match count)
How will I store or organize the data?
- Questions stored in JSON files (organized by topic)
- Complete topic list with keywords:
  1. Basic Economic Concepts - scarcity, opportunity cost, PPC, comparative advantage
  2. Supply & Demand - supply, demand, equilibrium, surplus, shortage, price floor, price ceiling
  3. Elasticity - elasticity, price elasticity, income elasticity, cross elasticity
  4. Market Structures - perfect competition, monopoly, monopolistic competition, oligopoly, cartel
  5. Cost Curves - marginal cost, average total cost, AVC, fixed cost, variable cost, profit maximization
  6. Factor Markets - labor, capital, MRP, wage
  7. Externalities & Public Goods - externality, public good, market failure, negative externality, positive externality
  8. Utility Maximization - utility, marginal utility, budget constraint
- High-frequency topics marked at the topic level (more questions per round): Supply & Demand, Market Structures, Cost Curves, Elasticity, Externalities & Public Goods, Factor Markets, Utility Maximization
- User performance stored in Python lists and dictionaries during runtime
## First Tiny Step

The first thing I need to build is the question data structure and a simple function that displays one question and checks if the user's answer is correct.

## Possible Risk

The hardest part might be implementing the adaptive difficulty system correctly while keeping the code organized and ensuring that topic tracking and timer-based analysis work together without making the program too complex or confusing.

## Development Plan (2 days)

### Day 1
1. Extract questions from PDFs → generate JSON data with topic tags
2. Build basic CLI quiz: display question, check answer, show score
3. Add topic selection menu
4. Implement adaptive logic: sets of questions, retry system, "I got it" button

### Day 2
5. Add timer per question (user-controlled start)
6. Add user system: username input, progress saving/loading
7. Final score summary with per-topic accuracy and time
8. Weak topic analysis
9. (If time) Break mode and performance chart

### Priority Order
- Must complete: 1-7 (core functionality)
- Should complete: 8 (weak topic analysis)
- Nice to have: 9 (break mode, charts)

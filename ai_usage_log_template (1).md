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

---

## Entry 4

### Date
2026-05-24 to 2026-05-25

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I continued working with Claude to implement more features for the AP Microeconomics quiz system, including generating explanations for questions, adding timer functionality, and implementing user progress saving.

### Why I Asked
I needed to complete more features according to the development plan and fix issues from the initial implementation.

### What AI Gave Me
Claude helped me:
1. Generated explanations for all 51 questions using keyword-based templates
2. Added timer functionality - user presses Enter to start timer, time displayed after each answer
3. Implemented user progress saving/loading system
4. Created a progress directory structure for multiple users
5. Updated the quiz program to use questions with explanations
6. Copied all code to the Obsidian program folder for easy access

### What I Used
- Question explanation generator (generate_explanations.py)
- Questions with explanations (questions_with_explanations.json)
- Timer functionality (user-controlled start)
- User progress saving/loading (JSON files per user)
- Updated quiz program with all new features

### What I Changed or Rejected
- Used keyword-based explanation templates instead of AI-generated explanations (simpler for now)
- Timer starts when user presses Enter (user-controlled, not automatic)
- Progress saved to separate JSON files per user in data/progress/ directory

### What I Still Do Not Fully Understand
- How to fix the parsing issues where options get mixed up between questions
- How to implement the full "I got it" button functionality during retry cycles
- How to properly track which questions were answered wrong in each round

### My Next Step
1. Fix the parsing issues in the extraction script (some questions have mixed up options)
2. Implement the full adaptive logic with "I got it" button
3. Add weak topic analysis to the final summary
4. Test the complete quiz flow
5. Add break mode feature (nice to have)

---

## Entry 5

### Date
2026-05-25

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I continued working with Claude to fix the parsing issues in the question extraction script and improve the quiz system.

### Why I Asked
The extraction script had a bug where questions were being concatenated together, causing options to get mixed up between questions.

### What AI Gave Me
Claude helped me:
1. Identified the issue: PDF text extraction was joining questions together without newlines
2. Fixed the extraction script by adding newlines before question numbers
3. Successfully extracted 59 questions (up from 51)
4. Fixed question 3 about price-discriminating firms (options were previously mixed up with question 4)
5. Regenerated explanations for all 59 questions
6. Updated all files in the Obsidian program folder

### What I Used
- Fixed extraction script with better question parsing
- 59 correctly extracted questions with proper options
- Regenerated explanations for all questions
- Updated quiz program with all fixes

### What I Changed or Rejected
- Added text normalization to handle PDF extraction issues
- Added newline insertion before question numbers when missing
- Improved option extraction logic

### What I Still Do Not Fully Understand
- How to handle other edge cases in PDF extraction
- How to implement the full "I got it" button functionality
- How to track which questions were answered wrong in each round

### My Next Step
1. Implement the full adaptive logic with "I got it" button
2. Add weak topic analysis to the final summary
3. Test the complete quiz flow
4. Add break mode feature (nice to have)

---

## Entry 6

### Date
2026-05-25

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to test the complete quiz system and verify all features are working correctly.

### Why I Asked
I needed to ensure the quiz system was fully functional before considering the project complete.

### What AI Gave Me
Claude helped me:
1. Ran comprehensive tests on all quiz components
2. Verified all 59 questions are loaded correctly
3. Confirmed all 8 topics are working
4. Tested high-frequency topic detection
5. Simulated a complete quiz round with user interaction
6. Verified progress saving and loading works
7. Confirmed all adaptive logic features are implemented

### What I Used
- Complete quiz system with all features
- 59 extracted questions with explanations
- User progress saving/loading
- Adaptive logic with retry/skip/continue options
- Timer functionality
- Weak topic analysis

### What I Changed or Rejected
- No changes needed - all features are working correctly
- The system is ready for use

### What I Still Do Not Fully Understand
- How to add the break mode feature (nice to have)
- How to improve the explanation quality
- How to handle edge cases in PDF extraction

### My Next Step
The project is essentially complete! The quiz system has all the core features:
1. ✅ Question extraction from PDFs
2. ✅ Topic tagging with keywords
3. ✅ Adaptive quiz logic
4. ✅ Timer functionality
5. ✅ User progress saving
6. ✅ Weak topic analysis
7. ✅ Explanations for all questions

Optional improvements:
- Add break mode feature
- Improve explanation quality with AI
- Add more questions from other sources
- Add visual charts for performance analysis

The system is ready for the user to practice AP Microeconomics!

---

## Entry 7

### Date
2026-05-27

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to convert the CLI quiz program to a GUI using Python's tkinter library.

### Why I Asked
I wanted a graphical interface that's easier to use than the command line.

### What AI Gave Me
Claude helped me:
1. Created a complete GUI version of the quiz using tkinter
2. Implemented login screen with username input
3. Created topic selection screen with buttons for each topic
4. Built quiz screen with question display, options, and timer
5. Added answer result screen with explanations
6. Implemented round result screen with score and options
7. Created summary and history screens
8. Maintained all features from the CLI version:
   - Timer functionality (press button to start)
   - User progress saving/loading
   - Historical results tracking
   - Weak topic analysis

### What I Used
- tkinter for GUI components
- Same question data and logic as CLI version
- All adaptive quiz features
- Progress saving/loading system

### What I Changed or Rejected
- Replaced CLI input with GUI buttons and radio buttons
- Timer now starts with a button click instead of Enter key
- Added scrollable text areas for questions and explanations
- Used messagebox for warnings

### What I Still Do Not Fully Understand
- How to improve the GUI layout and styling
- How to add more advanced features like charts

### My Next Step
The project now has both CLI and GUI versions:
1. CLI version: `quiz.py`
2. GUI version: `quiz_gui.py`

Both versions have the same features and use the same data files.

To run the GUI version:
```bash
python3 /Users/linghui.yu.2027/Documents/cs_finalproject/program/quiz_gui.py
```

---

## Entry 8

### Date
2026-05-27

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to modify the GUI so that quiz options are only visible after clicking the "Start Timer" button.

### Why I Asked
I wanted users to read the question first before seeing the answer options, so they can think about the question before being influenced by the choices.

### What AI Gave Me
Claude modified the `show_quiz_screen` method to:
1. Store the question options in `self.current_options` instead of immediately creating radio buttons
2. Create an empty `options_frame` when the question is displayed
3. Populate the options frame with radio buttons only when the "Start Timer" button is clicked in `start_timer`

### What I Used
- Modified `quiz_gui.py` with options hidden until timer starts
- `self.current_options` to store options data for later use
- `start_timer` method to create and display radio buttons dynamically

### What I Changed or Rejected
- Options are no longer visible when a question first appears
- Radio buttons are created dynamically in `start_timer` instead of `show_quiz_screen`
- No other changes to the quiz flow

### What I Still Do Not Fully Understand
- How to improve the GUI layout and styling further
- How to add visual charts for performance analysis

### My Next Step
The GUI now hides options until the timer starts. Both CLI and GUI versions are complete and synced to the Obsidian vault and GitHub repository.

---

## Entry 9

### Date
2026-05-28

### AI Tool Used
Claude Code (Anthropic CLI)

### What I Asked AI
I asked Claude to implement the two "nice to have" features from the PRD: break mode and performance charts.

### Why I Asked
These features were listed as optional in the development plan and would enhance the user experience - break mode provides encouragement during study sessions, and charts give visual feedback on performance.

### What AI Gave Me
Claude implemented both features:

**Break Mode:**
1. Added a "Break" button in the top right corner of the GUI (visible after login)
2. Created a popup window with random motivational messages and economics-themed jokes
3. Messages include encouragement and humor related to AP Microeconomics concepts

**Performance Chart:**
1. Installed matplotlib for chart rendering
2. Added bar chart showing accuracy percentage for each topic practiced
3. Color-coded bars: green (≥80%), yellow (≥60%), red (<60%)
4. Chart available on both Summary and Round Result screens
5. Embedded matplotlib figure in tkinter window

### What I Used
- `matplotlib` library for chart rendering
- `random` module for selecting motivational messages
- `tkinter.Toplevel` for popup windows
- `FigureCanvasTkAgg` for embedding matplotlib in tkinter

### What I Changed or Rejected
- Break button hidden on login screen, shown after user starts quiz
- Messages are a mix of motivational quotes and economics puns
- Chart uses color coding to quickly identify strong/weak topics
- Chart window is a separate popup that can be closed independently

### What I Still Do Not Fully Understand
- How to make the chart interactive (hover for details)
- How to save charts as image files

### My Next Step
All PRD features are now complete:
- ✅ Must Have (1-8): All implemented
- ✅ Should Complete (8): Weak topic analysis
- ✅ Nice to Have (9): Break mode and performance charts

The project is fully complete and ready for submission!

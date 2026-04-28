# Final Project PRD

## Project Title

Adaptive AP Quiz & Learning Tracker System

## One Sentence Pitch

My project is a program that helps students practice AP Biology or AP Economics questions through an adaptive quiz system that adjusts difficulty based on performance, tracks learning behavior, and provides personalized feedback and review suggestions.

## Target User

This project is for high school students who are preparing for AP exams and want a structured way to practice questions, identify weak topics, and improve learning efficiency.



## Purpose

This is useful because students often practice questions without understanding their weaknesses or learning patterns. This system not only tests knowledge but also analyzes performance, tracks response time, and gives feedback on weak topics to improve studying efficiency.

## MVP

The smallest working version will allow the user to choose AP Biology or AP Economics, answer multiple-choice questions, receive immediate correctness feedback, and view a final score summary.

## Must Have Features

1. Choose between AP Biology and AP Economics question sets
2. Answer multiple-choice questions with correctness checking
3. Adaptive difficulty system based on performance
4. Topic-based tracking of incorrect answers
5. Final score and weak topic summary
6. Response time tracking for each question (timer-based data collection)


## Nice To Have Features

1. View explanation after each question (optional)
2. Break mode with motivational messages or jokes
3. Visual chart showing performance by topic

## Stretch Feature

1. Timer-based analysis that tracks response time and uses it to adjust difficulty or evaluate confidence level

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
- (Optional) save user progress
### OOP
Question class to structure quiz data
### Error Handling
- Handle invalid inputs for answers and menu selection
## Data Plan

What data does my project need?
- AP Biology and AP Economics multiple-choice questions
- Each question includes:
    - question text
    - options
    - correct answer
    - difficulty level
    - topic
    - explanation (optional)
Where will the data come from?
- Manually created AP-style questions based on class knowledge
- Optional: AI-generated draft questions refined by me
How will I store or organize the data?
- Questions stored in JSON files (separate for Bio and Econ)
- User performance stored in Python lists and dictionaries during runtime
## First Tiny Step

The first thing I need to build is the question data structure and a simple function that displays one question and checks if the user’s answer is correct.

## Possible Risk

The hardest part might be implementing the adaptive difficulty system correctly while keeping the code organized and ensuring that topic tracking and timer-based analysis work together without making the program too complex or confusing.



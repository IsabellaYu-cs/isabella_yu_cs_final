import json
import random
import time
import os

# High-frequency topics (more questions per round)
HIGH_FREQUENCY_TOPICS = [
    "Supply & Demand",
    "Market Structures",
    "Cost Curves",
    "Elasticity",
    "Externalities & Public Goods",
    "Factor Markets",
    "Utility Maximization"
]

# Low-frequency topics
LOW_FREQUENCY_TOPICS = [
    "Basic Economic Concepts"
]

# Questions per round: high-frequency = 5, others = 3
QUESTIONS_PER_ROUND = {
    "high": 5,
    "normal": 3
}

class RealTimeTimer:
    """Simple timer that starts when user presses Enter and stops when answer is submitted."""
    def __init__(self):
        self.start_time = None
        self.elapsed = 0

    def start(self):
        """Start the timer."""
        self.start_time = time.time()

    def stop(self):
        """Stop the timer and return elapsed time."""
        if self.start_time:
            self.elapsed = time.time() - self.start_time
        return self.elapsed

class Quiz:
    def __init__(self, questions_file):
        """Initialize the quiz with questions from JSON file."""
        with open(questions_file, 'r', encoding='utf-8') as f:
            self.all_questions = json.load(f)

        self.username = None
        self.current_topic = None
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.topic_stats = {}  # {topic: {"correct": 0, "total": 0, "time": []}}
        self.current_question_start_time = None
        self.progress_file = None
        self.timer = RealTimeTimer()

    def get_topics(self):
        """Get all available topics."""
        topics = set()
        for q in self.all_questions:
            for topic in q["topics"]:
                topics.add(topic)
        return sorted(list(topics))

    def get_questions_for_topic(self, topic):
        """Get all questions for a specific topic."""
        return [q for q in self.all_questions if topic in q["topics"]]

    def is_high_frequency(self, topic):
        """Check if a topic is high-frequency."""
        return topic in HIGH_FREQUENCY_TOPICS

    def get_questions_per_round(self, topic):
        """Get number of questions per round for a topic."""
        if self.is_high_frequency(topic):
            return QUESTIONS_PER_ROUND["high"]
        return QUESTIONS_PER_ROUND["normal"]

    def get_progress_file(self):
        """Get the progress file path for the current user."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "..", "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)
        return os.path.join(progress_dir, f"{self.username}_progress.json")

    def get_history_file(self):
        """Get the history file path for the current user."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "..", "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)
        return os.path.join(progress_dir, f"{self.username}_history.json")

    def load_progress(self):
        """Load user progress from file."""
        self.progress_file = self.get_progress_file()

        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.topic_stats = data.get("topic_stats", {})
                print(f"\nWelcome back, {self.username}! Your progress has been loaded.")
        else:
            self.topic_stats = {}
            print(f"\nHello, {self.username}! Let's start practicing.")

    def save_progress(self):
        """Save user progress to file."""
        if not self.progress_file:
            self.progress_file = self.get_progress_file()

        data = {
            "username": self.username,
            "topic_stats": self.topic_stats
        }

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_round_to_history(self, topic, correct, total, avg_time):
        """Save a completed round to history."""
        history_file = self.get_history_file()

        # Load existing history
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # Add new entry
        from datetime import datetime
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "correct": correct,
            "total": total,
            "accuracy": (correct / total * 100) if total > 0 else 0,
            "avg_time": avg_time
        }
        history.append(entry)

        # Save history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def load_history(self):
        """Load user history from file."""
        history_file = self.get_history_file()
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def display_welcome(self):
        """Display welcome message and get username."""
        print("\n" + "="*60)
        print("AP Microeconomics Adaptive Quiz System")
        print("="*60)
        print("\nWelcome! Let's get started.\n")

        self.username = input("Enter your username: ").strip()
        if not self.username:
            self.username = "default_user"

        # Load user progress
        self.load_progress()

    def display_topics(self):
        """Display available topics and let user choose."""
        topics = self.get_topics()

        print("\nAvailable Topics:")
        print("-" * 40)

        for i, topic in enumerate(topics, 1):
            questions_count = len(self.get_questions_for_topic(topic))
            is_high = self.is_high_frequency(topic)
            frequency_label = "*** HIGH FREQUENCY ***" if is_high else "(Low frequency)"
            print(f"{i}. {topic} ({questions_count} questions total) {frequency_label}")

        print("\nEnter topic number to start (or 'quit' to exit):")

        while True:
            choice = input("> ").strip()

            if choice.lower() == 'quit':
                return None

            try:
                index = int(choice) - 1
                if 0 <= index < len(topics):
                    return topics[index]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def load_questions_for_topic(self, topic):
        """Load questions for the selected topic."""
        self.current_topic = topic
        all_topic_questions = self.get_questions_for_topic(topic)

        # Shuffle and select questions for this round
        random.shuffle(all_topic_questions)
        num_questions = self.get_questions_per_round(topic)
        self.questions = all_topic_questions[:num_questions]

        self.current_index = 0
        self.score = 0
        self.total_questions = len(self.questions)
        self.correct_answers = 0

        # Initialize topic stats if not exists
        if topic not in self.topic_stats:
            self.topic_stats[topic] = {"correct": 0, "total": 0, "time": []}

    def display_question(self, question, question_num):
        """Display a single question and start timer."""
        print(f"\n{'='*60}")
        print(f"Question {question_num} of {self.total_questions}")
        print(f"Topic: {self.current_topic}")
        print(f"{'='*60}\n")

        print(question["question"])
        print()

        for letter in ["A", "B", "C", "D", "E"]:
            if letter in question["options"]:
                print(f"  {letter}. {question['options'][letter]}")

        print()

    def get_user_answer(self):
        """Get user's answer. Timer starts when user presses Enter."""
        print("Press Enter when you're ready to start the timer...")
        input()
        self.timer.start()

        while True:
            answer = input("Your answer (A/B/C/D/E or 'skip' to skip): ").strip().upper()
            if answer in ["A", "B", "C", "D", "E", "SKIP"]:
                # Stop the timer and get elapsed time
                elapsed_time = self.timer.stop()
                return answer, elapsed_time
            print("Invalid input. Please enter A, B, C, D, E, or 'skip'.")

    def check_answer(self, question, user_answer):
        """Check if the answer is correct."""
        if user_answer == "SKIP":
            return None

        is_correct = user_answer == question["answer"]
        return is_correct

    def display_result(self, question, user_answer, is_correct, elapsed_time):
        """Display the result of an answer."""
        if user_answer == "SKIP":
            print("\n*** Question Skipped ***\n")
            return

        if is_correct:
            print(f"\n*** Correct! *** (Time: {elapsed_time:.1f} seconds)\n")
        else:
            print(f"\n*** Incorrect! The correct answer is {question['answer']}. *** (Time: {elapsed_time:.1f} seconds)\n")

        # Show explanation for both correct and incorrect answers
        if question["explanation"]:
            print(f"Explanation: {question['explanation']}\n")

    def run_quiz(self):
        """Run the quiz for the current topic."""
        total_available = len(self.get_questions_for_topic(self.current_topic))
        print(f"\nStarting quiz for: {self.current_topic}")
        print(f"Questions in this round: {self.total_questions} (out of {total_available} total)")
        print("="*60)

        # Track wrong answers in this round
        self.wrong_answers = []

        for i, question in enumerate(self.questions, 1):
            # Display question
            self.display_question(question, i)

            # Get answer (timer starts automatically and stops when answer is submitted)
            user_answer, elapsed_time = self.get_user_answer()

            # Check answer
            is_correct = self.check_answer(question, user_answer)

            # Display result
            self.display_result(question, user_answer, is_correct, elapsed_time)

            # Update stats
            if user_answer != "SKIP":
                self.topic_stats[self.current_topic]["total"] += 1
                self.topic_stats[self.current_topic]["time"].append(elapsed_time)

                if is_correct:
                    self.correct_answers += 1
                    self.topic_stats[self.current_topic]["correct"] += 1
                else:
                    # Track wrong answer
                    self.wrong_answers.append({
                        "question": question,
                        "user_answer": user_answer,
                        "correct_answer": question["answer"]
                    })

                self.score += 1 if is_correct else 0

            # Pause between questions
            if i < self.total_questions:
                input("Press Enter to continue...")

    def check_round_result(self):
        """Check the result of the round and decide next action."""
        accuracy = self.correct_answers / self.total_questions if self.total_questions > 0 else 0

        # Calculate average time for this round
        topic_times = self.topic_stats[self.current_topic]["time"]
        avg_time = sum(topic_times[-self.total_questions:]) / self.total_questions if topic_times else 0

        # Save round to history
        self.save_round_to_history(
            self.current_topic,
            self.correct_answers,
            self.total_questions,
            avg_time
        )

        print(f"\n{'='*60}")
        print(f"Round Complete!")
        print(f"Topic: {self.current_topic}")
        print(f"Score: {self.correct_answers}/{self.total_questions} ({accuracy*100:.1f}%)")
        print(f"{'='*60}\n")

        # All correct - ask if want to continue or move to next topic
        if accuracy == 1.0:
            print("Great job! You got all questions correct!")
            print("\nWhat would you like to do?")
            print("1. Continue with same topic")
            print("2. Move to next topic")

            while True:
                choice = input("> ").strip()
                if choice == "1":
                    return "continue"
                elif choice == "2":
                    return "next_topic"
                else:
                    print("Please enter 1 or 2.")

        # Any wrong - show explanations and retry
        else:
            print("You got some questions wrong.")
            print("\nLet's review the explanations:\n")

            # Show explanations for wrong answers
            for item in self.wrong_answers:
                question = item["question"]
                user_answer = item["user_answer"]
                correct_answer = item["correct_answer"]

                print(f"Q: {question['question'][:80]}...")
                print(f"  Your answer: {user_answer}")
                print(f"  Correct answer: {correct_answer}")
                if question["explanation"]:
                    print(f"  Explanation: {question['explanation']}")
                print()

            print("\nYou need to answer all questions correctly to move on.")
            print("Or you can choose 'I got it' to skip to the next topic.")
            print("\n1. Retry this topic")
            print("2. I got it - skip to next topic")

            while True:
                choice = input("> ").strip()
                if choice == "1":
                    return "retry"
                elif choice == "2":
                    return "skip"
                else:
                    print("Please enter 1 or 2.")

    def display_final_summary(self):
        """Display final summary of all topics."""
        print(f"\n{'='*60}")
        print(f"Final Summary for {self.username}")
        print(f"{'='*60}\n")

        if not self.topic_stats:
            print("No topics completed yet.")
            return

        total_correct = 0
        total_questions = 0
        weak_topics = []

        for topic, stats in self.topic_stats.items():
            correct = stats["correct"]
            total = stats["total"]
            times = stats["time"]

            total_correct += correct
            total_questions += total

            accuracy = (correct / total * 100) if total > 0 else 0
            avg_time = sum(times) / len(times) if times else 0

            print(f"{topic}:")
            print(f"  Accuracy: {correct}/{total} ({accuracy:.1f}%)")
            print(f"  Average time: {avg_time:.1f} seconds per question")

            # Identify weak topics (topics where accuracy is below 100%)
            if accuracy < 100:
                weak_topics.append(topic)
                print(f"  *** Needs review ***")

            print()

        # Overall stats
        if total_questions > 0:
            overall_accuracy = total_correct / total_questions * 100
            print(f"Overall: {total_correct}/{total_questions} ({overall_accuracy:.1f}%)")

        # Weak topics analysis
        if weak_topics:
            print(f"\n{'='*60}")
            print("Weak Topics Analysis")
            print(f"{'='*60}\n")
            print("The following topics need more practice:")
            for topic in weak_topics:
                stats = self.topic_stats[topic]
                accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
                print(f"  - {topic} ({accuracy:.1f}% accuracy)")
            print("\nConsider reviewing these topics and practicing more questions.")

    def display_history(self):
        """Display historical quiz results."""
        history = self.load_history()

        print(f"\n{'='*60}")
        print(f"Quiz History for {self.username}")
        print(f"{'='*60}\n")

        if not history:
            print("No quiz history found.")
            return

        # Group by topic
        topic_history = {}
        for entry in history:
            topic = entry["topic"]
            if topic not in topic_history:
                topic_history[topic] = []
            topic_history[topic].append(entry)

        # Display by topic
        for topic, entries in topic_history.items():
            print(f"\n{topic}:")
            print("-" * 40)
            for entry in entries[-5:]:  # Show last 5 attempts
                print(f"  {entry['date']}: {entry['correct']}/{entry['total']} ({entry['accuracy']:.1f}%) - Avg time: {entry['avg_time']:.1f}s")

        # Overall statistics
        total_correct = sum(e["correct"] for e in history)
        total_questions = sum(e["total"] for e in history)
        if total_questions > 0:
            overall_accuracy = total_correct / total_questions * 100
            print(f"\n{'='*60}")
            print(f"Overall: {total_correct}/{total_questions} ({overall_accuracy:.1f}%)")
            print(f"Total rounds: {len(history)}")

    def run(self):
        """Main quiz loop."""
        self.display_welcome()

        while True:
            # Display topics and let user choose
            topic = self.display_topics()

            if topic is None:
                break

            # Load questions for the topic
            self.load_questions_for_topic(topic)

            # Run quiz rounds
            while True:
                # Run a round
                self.run_quiz()

                # Check result
                action = self.check_round_result()

                if action == "continue":
                    # Load new questions for same topic
                    self.load_questions_for_topic(topic)
                    continue
                elif action == "next_topic":
                    break
                elif action == "retry":
                    # Reload same questions (or shuffle)
                    self.load_questions_for_topic(topic)
                    continue
                elif action == "skip":
                    break

            # Save progress
            self.save_progress()

            # Ask if user wants to continue
            print("\nWould you like to:")
            print("1. Practice another topic")
            print("2. View current summary")
            print("3. View history")
            print("4. Exit")

            while True:
                choice = input("> ").strip()
                if choice == "1":
                    break
                elif choice == "2":
                    self.display_final_summary()
                    input("\nPress Enter to continue...")
                    break
                elif choice == "3":
                    self.display_history()
                    input("\nPress Enter to continue...")
                    break
                elif choice == "4":
                    self.display_final_summary()
                    print("\nThank you for using the AP Microeconomics Quiz System!")
                    return
                else:
                    print("Please enter 1, 2, 3, or 4.")

def main():
    """Main function."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    questions_file = os.path.join(script_dir, "data", "questions_with_explanations.json")

    # Check if questions file exists
    if not os.path.exists(questions_file):
        print(f"Error: Questions file not found at {questions_file}")
        print("Please run extract_questions.py first.")
        return

    # Create and run quiz
    quiz = Quiz(questions_file)
    quiz.run()

if __name__ == "__main__":
    main()

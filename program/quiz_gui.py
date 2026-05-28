import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import time
import threading
import random
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class QuizGUI:
    # Motivational messages and jokes for break mode
    BREAK_MESSAGES = [
        "You're doing great! Keep it up!",
        "Remember: every question you practice is one step closer to a 5!",
        "Take a deep breath. You've got this!",
        "Fun fact: The law of demand says the more you study, the better you score!",
        "Why did the economist break up with the mathematician? They had too many problems!",
        "What's a pirate's favorite subject? Micro-ARRR-conomics!",
        "You're like a perfectly competitive firm - efficient and productive!",
        "Keep going! Your marginal utility of studying is still positive!",
        "Remember: opportunity cost of not studying is your AP score!",
        "You're building human capital right now!",
        "Even Adam Smith would be proud of your dedication!",
        "Don't be a free rider - keep studying!",
        "Your effort is like a positive externality - it benefits everyone around you!",
        "Time to take a short break and come back refreshed!",
        "You're on the production possibilities frontier of studying!"
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("AP Microeconomics Quiz System")
        self.root.geometry("800x600")

        # Load questions
        script_dir = os.path.dirname(os.path.abspath(__file__))
        questions_file = os.path.join(script_dir, "data", "questions_with_explanations.json")

        with open(questions_file, 'r', encoding='utf-8') as f:
            self.all_questions = json.load(f)

        # Quiz state
        self.username = ""
        self.current_topic = None
        self.questions = []
        self.current_index = 0
        self.correct_answers = 0
        self.total_questions = 0
        self.topic_stats = {}
        self.timer_start = None
        self.wrong_answers = []

        # High-frequency topics
        self.high_frequency_topics = [
            "Supply & Demand",
            "Market Structures",
            "Cost Curves",
            "Elasticity",
            "Externalities & Public Goods",
            "Factor Markets",
            "Utility Maximization"
        ]

        # Create GUI
        self.create_widgets()

        # Show login screen
        self.show_login_screen()

    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Break button (top right corner, hidden initially)
        self.break_btn = ttk.Button(self.root, text="Break",
                                   command=self.show_break_mode)
        self.break_btn.place(x=710, y=10, width=80, height=30)
        self.break_btn.place_forget()  # Hide initially

    def clear_screen(self):
        """Clear all widgets from main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_break_mode(self):
        """Show a break mode window with motivational message."""
        break_window = tk.Toplevel(self.root)
        break_window.title("Break Time!")
        break_window.geometry("400x250")
        break_window.transient(self.root)
        break_window.grab_set()

        # Center the window
        break_window.update_idletasks()
        x = (break_window.winfo_screenwidth() - 400) // 2
        y = (break_window.winfo_screenheight() - 250) // 2
        break_window.geometry(f"400x250+{x}+{y}")

        # Title
        ttk.Label(break_window, text="Break Time!",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Random message
        message = random.choice(self.BREAK_MESSAGES)
        msg_label = ttk.Label(break_window, text=message,
                            font=("Arial", 12), wraplength=350, justify="center")
        msg_label.pack(pady=20)

        # Close button
        ttk.Button(break_window, text="Back to Quiz",
                  command=break_window.destroy).pack(pady=20)

    def show_chart(self, chart_data):
        """Show performance chart in a new window."""
        if not chart_data:
            messagebox.showinfo("No Data", "No performance data available to display.")
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Performance Chart")
        chart_window.geometry("700x500")
        chart_window.transient(self.root)

        # Center the window
        chart_window.update_idletasks()
        x = (chart_window.winfo_screenwidth() - 700) // 2
        y = (chart_window.winfo_screenheight() - 500) // 2
        chart_window.geometry(f"700x500+{x}+{y}")

        # Create matplotlib figure
        fig = Figure(figsize=(7, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Prepare data
        topics = list(chart_data.keys())
        accuracies = list(chart_data.values())

        # Shorten topic names for display
        short_topics = []
        for t in topics:
            if len(t) > 15:
                short_topics.append(t[:12] + "...")
            else:
                short_topics.append(t)

        # Create bar chart
        colors = ['#4CAF50' if a >= 80 else '#FFC107' if a >= 60 else '#F44336' for a in accuracies]
        bars = ax.bar(short_topics, accuracies, color=colors)

        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 1,
                   f'{acc:.1f}%', ha='center', va='bottom', fontsize=9)

        ax.set_ylabel('Accuracy (%)')
        ax.set_title(f'{self.username}\'s Performance by Topic')
        ax.set_ylim(0, 110)
        ax.axhline(y=100, color='gray', linestyle='--', alpha=0.3)

        # Rotate x labels for better readability
        ax.tick_params(axis='x', rotation=30)

        fig.tight_layout()

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Close button
        ttk.Button(chart_window, text="Close",
                  command=chart_window.destroy).pack(pady=10)

    def show_login_screen(self):
        """Show login screen."""
        self.clear_screen()

        # Title
        title_label = ttk.Label(self.main_frame, text="AP Microeconomics Quiz System",
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, pady=20)

        # Username input
        frame = ttk.Frame(self.main_frame)
        frame.grid(row=1, column=0, pady=20)

        ttk.Label(frame, text="Enter your username:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        self.username_entry = ttk.Entry(frame, font=("Arial", 12), width=20)
        self.username_entry.grid(row=0, column=1, padx=5)
        self.username_entry.focus()

        # Start button
        start_btn = ttk.Button(self.main_frame, text="Start Quiz", command=self.start_quiz)
        start_btn.grid(row=2, column=0, pady=20)

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.start_quiz())

    def start_quiz(self):
        """Start the quiz with the entered username."""
        self.username = self.username_entry.get().strip()
        if not self.username:
            self.username = "default_user"

        # Load progress
        self.load_progress()

        # Show break button after login
        self.break_btn.place(x=710, y=10, width=80, height=30)

        # Show topic selection
        self.show_topic_selection()

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
        return topic in self.high_frequency_topics

    def get_questions_per_round(self, topic):
        """Get number of questions per round for a topic."""
        if self.is_high_frequency(topic):
            return 5
        return 3

    def show_topic_selection(self):
        """Show topic selection screen."""
        self.clear_screen()

        # Title
        title_label = ttk.Label(self.main_frame, text=f"Welcome, {self.username}!",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        subtitle_label = ttk.Label(self.main_frame, text="Select a topic to practice:",
                                  font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, pady=10)

        # Topic list
        topics = self.get_topics()
        for i, topic in enumerate(topics):
            questions_count = len(self.get_questions_for_topic(topic))
            is_high = self.is_high_frequency(topic)
            label = f"{topic} ({questions_count} questions)"
            if is_high:
                label += " *** HIGH FREQUENCY ***"

            btn = ttk.Button(self.main_frame, text=label,
                           command=lambda t=topic: self.select_topic(t))
            btn.grid(row=i+2, column=0, pady=5, sticky=tk.W+tk.E)

        # History button
        history_btn = ttk.Button(self.main_frame, text="View History",
                               command=self.show_history)
        history_btn.grid(row=len(topics)+2, column=0, pady=20)

    def select_topic(self, topic):
        """Select a topic and start quiz."""
        self.current_topic = topic
        self.load_questions_for_topic(topic)
        self.show_quiz_screen()

    def load_questions_for_topic(self, topic):
        """Load questions for the selected topic."""
        all_topic_questions = self.get_questions_for_topic(topic)

        # Shuffle and select questions
        import random
        random.shuffle(all_topic_questions)
        num_questions = self.get_questions_per_round(topic)
        self.questions = all_topic_questions[:num_questions]

        self.current_index = 0
        self.correct_answers = 0
        self.total_questions = len(self.questions)
        self.wrong_answers = []

        # Initialize topic stats if not exists
        if topic not in self.topic_stats:
            self.topic_stats[topic] = {"correct": 0, "total": 0, "time": []}

    def show_quiz_screen(self):
        """Show the quiz screen with current question."""
        self.clear_screen()

        if self.current_index >= len(self.questions):
            self.show_round_result()
            return

        question = self.questions[self.current_index]

        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky=tk.W+tk.E, pady=10)

        ttk.Label(header_frame, text=f"Question {self.current_index + 1} of {self.total_questions}",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W)

        ttk.Label(header_frame, text=f"Topic: {self.current_topic}",
                 font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W)

        # Timer
        self.timer_label = ttk.Label(header_frame, text="Time: 00:00",
                                    font=("Arial", 12))
        self.timer_label.grid(row=0, column=1, rowspan=2, sticky=tk.E)

        # Question text
        question_frame = ttk.Frame(self.main_frame)
        question_frame.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)

        question_text = scrolledtext.ScrolledText(question_frame, wrap=tk.WORD,
                                                 font=("Arial", 11), height=4)
        question_text.grid(row=0, column=0, sticky=tk.W+tk.E)
        question_text.insert(tk.END, question["question"])
        question_text.config(state=tk.DISABLED)

        # Store options for later (hidden until timer starts)
        self.current_options = question["options"]
        self.selected_answer = tk.StringVar()

        # Options frame (initially empty - will be populated when timer starts)
        self.options_frame = ttk.Frame(self.main_frame)
        self.options_frame.grid(row=2, column=0, sticky=tk.W+tk.E, pady=10)

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, pady=20)

        # Start timer button
        self.start_timer_btn = ttk.Button(button_frame, text="Start Timer",
                                        command=self.start_timer)
        self.start_timer_btn.grid(row=0, column=0, padx=10)

        # Submit button
        self.submit_btn = ttk.Button(button_frame, text="Submit Answer",
                                   command=self.submit_answer, state=tk.DISABLED)
        self.submit_btn.grid(row=0, column=1, padx=10)

        # Skip button
        skip_btn = ttk.Button(button_frame, text="Skip",
                            command=lambda: self.submit_answer(skip=True))
        skip_btn.grid(row=0, column=2, padx=10)

    def start_timer(self):
        """Start the timer and show options."""
        self.timer_start = time.time()
        self.start_timer_btn.config(state=tk.DISABLED)
        self.submit_btn.config(state=tk.NORMAL)

        # Show options now that timer has started
        for i, (letter, text) in enumerate(self.current_options.items()):
            rb = ttk.Radiobutton(self.options_frame, text=f"{letter}. {text}",
                               variable=self.selected_answer, value=letter)
            rb.grid(row=i, column=0, sticky=tk.W, pady=2)

        self.update_timer()

    def update_timer(self):
        """Update the timer display."""
        if self.timer_start:
            elapsed = time.time() - self.timer_start
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)

    def submit_answer(self, skip=False):
        """Submit the answer."""
        # Stop timer
        elapsed_time = 0
        if self.timer_start:
            elapsed_time = time.time() - self.timer_start
            self.timer_start = None

        if skip:
            user_answer = "SKIP"
        else:
            user_answer = self.selected_answer.get()
            if not user_answer:
                messagebox.showwarning("Warning", "Please select an answer!")
                return

        question = self.questions[self.current_index]

        # Check answer
        is_correct = (user_answer == question["answer"])

        # Update stats
        if user_answer != "SKIP":
            self.topic_stats[self.current_topic]["total"] += 1
            self.topic_stats[self.current_topic]["time"].append(elapsed_time)

            if is_correct:
                self.correct_answers += 1
                self.topic_stats[self.current_topic]["correct"] += 1
            else:
                self.wrong_answers.append({
                    "question": question,
                    "user_answer": user_answer,
                    "correct_answer": question["answer"]
                })

        # Show result
        self.show_answer_result(question, user_answer, is_correct, elapsed_time)

    def show_answer_result(self, question, user_answer, is_correct, elapsed_time):
        """Show the result of the answer."""
        self.clear_screen()

        # Result header
        if user_answer == "SKIP":
            result_text = "Question Skipped"
            result_color = "gray"
        elif is_correct:
            result_text = "Correct!"
            result_color = "green"
        else:
            result_text = "Incorrect!"
            result_color = "red"

        result_label = ttk.Label(self.main_frame, text=result_text,
                               font=("Arial", 18, "bold"), foreground=result_color)
        result_label.grid(row=0, column=0, pady=10)

        # Time
        time_label = ttk.Label(self.main_frame, text=f"Time: {elapsed_time:.1f} seconds",
                              font=("Arial", 12))
        time_label.grid(row=1, column=0, pady=5)

        # Question details
        details_frame = ttk.Frame(self.main_frame)
        details_frame.grid(row=2, column=0, sticky=tk.W+tk.E, pady=10)

        ttk.Label(details_frame, text=f"Your answer: {user_answer}",
                 font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W)

        ttk.Label(details_frame, text=f"Correct answer: {question['answer']}",
                 font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W)

        # Explanation (show for both correct and incorrect answers)
        if question["explanation"]:
            exp_frame = ttk.Frame(self.main_frame)
            exp_frame.grid(row=3, column=0, sticky=tk.W+tk.E, pady=10)

            ttk.Label(exp_frame, text="Explanation:",
                     font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W)

            exp_text = scrolledtext.ScrolledText(exp_frame, wrap=tk.WORD,
                                                font=("Arial", 10), height=4)
            exp_text.grid(row=1, column=0, sticky=tk.W+tk.E)
            exp_text.insert(tk.END, question["explanation"])
            exp_text.config(state=tk.DISABLED)

        # Next button
        next_btn = ttk.Button(self.main_frame, text="Next Question",
                            command=self.next_question)
        next_btn.grid(row=4, column=0, pady=20)

    def next_question(self):
        """Go to next question."""
        self.current_index += 1
        self.selected_answer.set("")
        self.show_quiz_screen()

    def show_round_result(self):
        """Show the round result."""
        self.clear_screen()

        accuracy = self.correct_answers / self.total_questions if self.total_questions > 0 else 0

        # Calculate average time
        topic_times = self.topic_stats[self.current_topic]["time"]
        avg_time = sum(topic_times[-self.total_questions:]) / self.total_questions if topic_times else 0

        # Save round to history
        self.save_round_to_history(self.correct_answers, self.total_questions, avg_time)

        # Title
        title_label = ttk.Label(self.main_frame, text="Round Complete!",
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        # Score
        score_label = ttk.Label(self.main_frame,
                               text=f"Score: {self.correct_answers}/{self.total_questions} ({accuracy*100:.1f}%)",
                               font=("Arial", 14))
        score_label.grid(row=1, column=0, pady=10)

        # Topic
        topic_label = ttk.Label(self.main_frame, text=f"Topic: {self.current_topic}",
                               font=("Arial", 12))
        topic_label.grid(row=2, column=0, pady=5)

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, pady=20)

        if accuracy == 1.0:
            # All correct
            ttk.Label(self.main_frame, text="Great job! You got all questions correct!",
                     font=("Arial", 12), foreground="green").grid(row=2, column=0, pady=10)

            continue_btn = ttk.Button(button_frame, text="Continue with same topic",
                                    command=self.continue_topic)
            continue_btn.grid(row=0, column=0, padx=10)

            next_topic_btn = ttk.Button(button_frame, text="Move to next topic",
                                      command=self.show_topic_selection)
            next_topic_btn.grid(row=0, column=1, padx=10)
        else:
            # Some wrong
            ttk.Label(self.main_frame, text="You got some questions wrong.",
                     font=("Arial", 12), foreground="red").grid(row=2, column=0, pady=10)

            # Show wrong answers
            if self.wrong_answers:
                wrong_frame = ttk.Frame(self.main_frame)
                wrong_frame.grid(row=3, column=0, sticky=tk.W+tk.E, pady=10)

                ttk.Label(wrong_frame, text="Wrong answers:",
                         font=("Arial", 11, "bold")).grid(row=0, column=0, sticky=tk.W)

                for i, item in enumerate(self.wrong_answers[:3]):  # Show first 3
                    q = item["question"]
                    ttk.Label(wrong_frame,
                             text=f"Q: {q['question'][:50]}... (Correct: {item['correct_answer']})",
                             font=("Arial", 10)).grid(row=i+1, column=0, sticky=tk.W)

            retry_btn = ttk.Button(button_frame, text="Retry this topic",
                                 command=self.retry_topic)
            retry_btn.grid(row=0, column=0, padx=10)

            skip_btn = ttk.Button(button_frame, text="I got it - skip to next topic",
                                command=self.show_topic_selection)
            skip_btn.grid(row=0, column=1, padx=10)

        # Summary, chart, and history buttons
        summary_btn = ttk.Button(self.main_frame, text="View Summary",
                               command=self.show_summary)
        summary_btn.grid(row=4, column=0, pady=10)

        # Chart button with current data
        chart_data = {}
        for t, stats in self.topic_stats.items():
            if stats["total"] > 0:
                chart_data[t] = (stats["correct"] / stats["total"]) * 100

        if chart_data:
            chart_btn = ttk.Button(self.main_frame, text="View Performance Chart",
                                  command=lambda: self.show_chart(chart_data))
            chart_btn.grid(row=5, column=0, pady=5)

        history_btn = ttk.Button(self.main_frame, text="View History",
                               command=self.show_history)
        history_btn.grid(row=6, column=0, pady=5)

    def continue_topic(self):
        """Continue with the same topic."""
        self.load_questions_for_topic(self.current_topic)
        self.show_quiz_screen()

    def retry_topic(self):
        """Retry the current topic."""
        self.load_questions_for_topic(self.current_topic)
        self.show_quiz_screen()

    def show_summary(self):
        """Show final summary."""
        self.clear_screen()

        # Title
        title_label = ttk.Label(self.main_frame, text=f"Summary for {self.username}",
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        # Create text widget for summary
        summary_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD,
                                                font=("Arial", 11), height=15)
        summary_text.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)

        # Generate summary
        summary = ""
        total_correct = 0
        total_questions = 0
        weak_topics = []
        chart_data = {}  # For chart: {topic: accuracy}

        for topic, stats in self.topic_stats.items():
            correct = stats["correct"]
            total = stats["total"]
            times = stats["time"]

            total_correct += correct
            total_questions += total

            accuracy = (correct / total * 100) if total > 0 else 0
            avg_time = sum(times) / len(times) if times else 0

            summary += f"{topic}:\n"
            summary += f"  Accuracy: {correct}/{total} ({accuracy:.1f}%)\n"
            summary += f"  Average time: {avg_time:.1f} seconds per question\n"

            if accuracy < 100:
                weak_topics.append(topic)
                summary += f"  *** Needs review ***\n"

            summary += "\n"

            # Store for chart
            chart_data[topic] = accuracy

        if total_questions > 0:
            overall_accuracy = total_correct / total_questions * 100
            summary += f"Overall: {total_correct}/{total_questions} ({overall_accuracy:.1f}%)\n"

        if weak_topics:
            summary += "\nWeak Topics:\n"
            for topic in weak_topics:
                stats = self.topic_stats[topic]
                accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
                summary += f"  - {topic} ({accuracy:.1f}% accuracy)\n"

        summary_text.insert(tk.END, summary)
        summary_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        if chart_data:
            chart_btn = ttk.Button(button_frame, text="View Performance Chart",
                                  command=lambda: self.show_chart(chart_data))
            chart_btn.grid(row=0, column=0, padx=10)

        back_btn = ttk.Button(button_frame, text="Back to Topics",
                            command=self.show_topic_selection)
        back_btn.grid(row=0, column=1, padx=10)

    def show_history(self):
        """Show quiz history."""
        self.clear_screen()

        # Title
        title_label = ttk.Label(self.main_frame, text=f"History for {self.username}",
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        # Create text widget for history
        history_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD,
                                               font=("Arial", 11), height=20)
        history_text.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)

        # Load and display history
        history = self.load_history()

        if not history:
            history_text.insert(tk.END, "No quiz history found.")
        else:
            # Group by topic
            topic_history = {}
            for entry in history:
                topic = entry["topic"]
                if topic not in topic_history:
                    topic_history[topic] = []
                topic_history[topic].append(entry)

            # Display by topic
            for topic, entries in topic_history.items():
                history_text.insert(tk.END, f"{topic}:\n")
                history_text.insert(tk.END, "-" * 40 + "\n")
                for entry in entries[-5:]:  # Show last 5 attempts
                    history_text.insert(tk.END,
                        f"  {entry['date']}: {entry['correct']}/{entry['total']} "
                        f"({entry['accuracy']:.1f}%) - Avg time: {entry['avg_time']:.1f}s\n")
                history_text.insert(tk.END, "\n")

            # Overall statistics
            total_correct = sum(e["correct"] for e in history)
            total_questions = sum(e["total"] for e in history)
            if total_questions > 0:
                overall_accuracy = total_correct / total_questions * 100
                history_text.insert(tk.END, f"Overall: {total_correct}/{total_questions} "
                                          f"({overall_accuracy:.1f}%)\n")
                history_text.insert(tk.END, f"Total rounds: {len(history)}\n")

        history_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=20)

        summary_btn = ttk.Button(button_frame, text="View Summary",
                               command=self.show_summary)
        summary_btn.grid(row=0, column=0, padx=10)

        back_btn = ttk.Button(button_frame, text="Back to Topics",
                            command=self.show_topic_selection)
        back_btn.grid(row=0, column=1, padx=10)

    def load_progress(self):
        """Load user progress from file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)
        progress_file = os.path.join(progress_dir, f"{self.username}_progress.json")

        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.topic_stats = data.get("topic_stats", {})

    def save_progress(self):
        """Save user progress to file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)
        progress_file = os.path.join(progress_dir, f"{self.username}_progress.json")

        data = {
            "username": self.username,
            "topic_stats": self.topic_stats
        }

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_round_to_history(self, correct, total, avg_time):
        """Save a completed round to history."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "data", "progress")
        os.makedirs(progress_dir, exist_ok=True)
        history_file = os.path.join(progress_dir, f"{self.username}_history.json")

        # Load existing history
        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # Add new entry
        from datetime import datetime
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": self.current_topic,
            "correct": correct,
            "total": total,
            "accuracy": (correct / total * 100) if total > 0 else 0,
            "avg_time": avg_time
        }
        history.append(entry)

        # Save history
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        # Also save progress
        self.save_progress()

    def load_history(self):
        """Load user history from file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        progress_dir = os.path.join(script_dir, "data", "progress")
        history_file = os.path.join(progress_dir, f"{self.username}_history.json")

        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

def main():
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

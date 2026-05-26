import PyPDF2
import json
import re
import os

# Topic keywords mapping - more specific keywords
TOPIC_KEYWORDS = {
    "Basic Economic Concepts": ["scarcity", "opportunity cost", "ppc", "production possibilities", "comparative advantage", "absolute advantage", "specialization", "trade", "gains from trade"],
    "Supply & Demand": ["supply curve", "demand curve", "equilibrium price", "equilibrium quantity", "surplus", "shortage", "price floor", "price ceiling", "shift in demand", "shift in supply", "movement along", "market clearing"],
    "Elasticity": ["elasticity", "price elasticity of demand", "price elasticity of supply", "income elasticity", "cross-price elasticity", "elastic demand", "inelastic demand", "unit elastic", "perfectly elastic", "perfectly inelastic", "total revenue"],
    "Market Structures": ["perfect competition", "monopoly", "monopolistic competition", "oligopoly", "cartel", "price taker", "price maker", "market power", "barrier to entry", "differentiated product", "monopolist", "nash equilibrium", "dominant strategy", "game theory", "collusion"],
    "Cost Curves": ["marginal cost", "average total cost", "average variable cost", "average fixed cost", "fixed cost", "variable cost", "profit maximization", "shutdown point", "break even", "economic profit", "accounting profit", "marginal revenue", "total cost", "total revenue", "marginal product", "diminishing returns", "returns to scale", "economies of scale", "diseconomies of scale", "efficient scale"],
    "Factor Markets": ["labor market", "capital market", "marginal revenue product", "mrp", "wage rate", "factor market", "input market", "hiring decision", "marginal product of labor", "marginal product of capital", "value of marginal product", "vmpl", "minimum wage", "labor demand", "labor supply"],
    "Externalities & Public Goods": ["externality", "negative externality", "positive externality", "public good", "market failure", "free rider", "social cost", "social benefit", "marginal social cost", "marginal social benefit", "coase theorem", "property rights", "deadweight loss", "allocative efficiency", "productive efficiency", "market for lemons", "asymmetric information"],
    "Utility Maximization": ["utility", "marginal utility", "budget constraint", "indifference curve", "consumer equilibrium", "marginal utility per dollar", "diminishing marginal utility", "consumer choice", "optimal bundle", "mrs", "marginal rate of substitution"]
}

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        all_text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text.append(page_text)
        return "\n".join(all_text)

def find_questions_section(text):
    """Find the actual questions section in the text."""
    # Look for the pattern "SECTION I" followed by "Time" and "Questions"
    section_match = re.search(r'SECTION\s+I\s*\n\s*Time.*?Questions', text, re.IGNORECASE | re.DOTALL)

    if section_match:
        start_pos = section_match.end()
    else:
        # Try to find "Directions:" which appears before questions
        directions_match = re.search(r'Directions:.*?(?=\n\s*1\.\s)', text, re.DOTALL | re.IGNORECASE)
        if directions_match:
            start_pos = directions_match.end()
        else:
            # Find first question
            first_q = re.search(r'\n\s*1\.\s+', text)
            start_pos = first_q.start() if first_q else 0

    # Find where to end - look for answer key or FRQ section
    end_patterns = [
        r'Answers?\s+for\s+Multiple\s+Choice',
        r'SECTION\s+II',
        r'Free.?Response\s+Questions',
        r'Total\s+Time.*?minutes\s*\n\s*3\s+Questions'
    ]

    end_pos = len(text)
    for pattern in end_patterns:
        match = re.search(pattern, text[start_pos:], re.IGNORECASE)
        if match:
            candidate = start_pos + match.start()
            if candidate < end_pos:
                end_pos = candidate

    return text[start_pos:end_pos]

def parse_questions(text):
    """Parse questions from the text with better option handling."""
    questions = []

    # First, normalize the text by adding newlines before question numbers
    # This handles cases where PDF extraction joins questions together
    # Pattern: text followed by number (e.g., "text.4." or "text. 4.")
    text = re.sub(r'([a-zA-Z.])(\d+\.)', r'\1\n\2', text)

    # Clean up the text
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove extra newlines

    # Split by question numbers at the start of lines
    # Match: number followed by period and space
    pattern = r'(?:^|\n)\s*(\d+)\.\s+'
    splits = re.split(pattern, text)

    # splits[0] is before first question, then alternating: number, text
    for i in range(1, len(splits) - 1, 2):
        try:
            question_num = int(splits[i])
            question_text = splits[i + 1]

            # Find all options A-E
            option_pattern = r'\(([A-E])\)\s+'
            option_positions = [(m.start(), m.group(1)) for m in re.finditer(option_pattern, question_text)]

            # If we have fewer than 4 options, skip this question
            if len(option_positions) < 4:
                continue

            # Extract each option
            options = {}
            for j, (pos, letter) in enumerate(option_positions):
                # Get text from this option to the next option (or end of text)
                if j + 1 < len(option_positions):
                    next_pos = option_positions[j + 1][0]
                    option_text = question_text[pos:next_pos]
                else:
                    # For the last option, get text until the next question or end
                    # Look for next question number pattern
                    next_q_match = re.search(r'\n\s*\d+\.\s', question_text[pos:])
                    if next_q_match:
                        option_text = question_text[pos:pos + next_q_match.start()]
                    else:
                        option_text = question_text[pos:]

                # Clean up option text
                option_text = re.sub(r'^\([A-E]\)\s*', '', option_text)
                option_text = re.sub(r'\s+', ' ', option_text).strip()
                # Remove trailing text that might be part of next question
                option_text = re.split(r'\n\s*\d+\.\s', option_text)[0]
                options[letter] = option_text

            # Get question text (before first option)
            if option_positions:
                question_only = question_text[:option_positions[0][0]]
            else:
                question_only = question_text

            # Clean up question text
            question_only = re.sub(r'\s+', ' ', question_only).strip()
            # Remove hyphenation
            question_only = question_only.replace('- ', '')

            # Clean up options - remove hyphenation
            for letter in options:
                options[letter] = options[letter].replace('- ', '')

            # Only add if we have a valid question with options
            if question_only and len(options) >= 4:
                questions.append({
                    "number": question_num,
                    "text": question_only,
                    "options": options
                })
        except (ValueError, IndexError):
            continue

    return questions

def extract_answer_key(text):
    """Extract answer key from the text."""
    answers = {}

    # Find the answer key section
    answer_section = re.search(r'Answers?\s+for\s+Multiple\s+Choice\s+Questions.*?(?=\n\s*\d+\.\s|\Z)', text, re.DOTALL | re.IGNORECASE)

    if answer_section:
        answer_text = answer_section.group(0)
        # Find all number-letter pairs
        matches = re.findall(r'(\d+)\s+([A-E])', answer_text)
        for match in matches:
            question_num = int(match[0])
            answer = match[1]
            answers[question_num] = answer

    # If no answers found, try a different approach
    if not answers:
        # Look for the answer key table format
        # Find all instances of number followed by letter
        matches = re.findall(r'\b(\d+)\s+([A-E])\b', text)
        for match in matches:
            question_num = int(match[0])
            answer = match[1]
            # Only add if it looks like an answer (not part of question text)
            if 1 <= question_num <= 60:  # AP exams have 60 questions
                answers[question_num] = answer

    return answers

def tag_topics(question_text, options_text):
    """Tag a question with topics based on keyword matching."""
    topics = []
    combined_text = (question_text + " " + options_text).lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in combined_text:
                topics.append(topic)
                break  # Only add each topic once

    return topics

def process_pdf(pdf_path):
    """Process a single PDF and return questions with answers and topics."""
    print(f"Processing {pdf_path}...")

    # Extract all text
    full_text = extract_text_from_pdf(pdf_path)

    # Find and extract questions section
    questions_text = find_questions_section(full_text)

    # Parse questions
    questions = parse_questions(questions_text)

    # Extract answer key from full text
    answers = extract_answer_key(full_text)

    print(f"  Found {len(questions)} questions and {len(answers)} answers")

    # Combine questions with answers and add topics
    processed_questions = []
    for q in questions:
        q_num = q["number"]
        if q_num in answers:
            # Combine all option text for topic matching
            options_text = " ".join(q["options"].values())

            processed_questions.append({
                "question": q["text"],
                "options": q["options"],
                "answer": answers[q_num],
                "topics": tag_topics(q["text"], options_text),
                "explanation": ""  # To be filled in later
            })

    return processed_questions

def main():
    """Main function to process all PDFs and save to JSON."""
    pdf_dir = "/Users/linghui.yu.2027/Downloads/ap"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "data", "questions.json")

    all_questions = []

    # Process each PDF in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            questions = process_pdf(pdf_path)
            all_questions.extend(questions)
            print(f"  Extracted {len(questions)} questions from {filename}")

    # Remove duplicates based on question text
    seen = set()
    unique_questions = []
    for q in all_questions:
        # Use first 80 chars as key to detect duplicates
        key = q["question"][:80]
        if key not in seen:
            seen.add(key)
            unique_questions.append(q)

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_questions, f, indent=2, ensure_ascii=False)

    print(f"\nTotal questions extracted: {len(unique_questions)}")
    print(f"Saved to {output_file}")

    # Print topic distribution
    topic_counts = {}
    for q in unique_questions:
        for topic in q["topics"]:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

    print("\nTopic distribution:")
    for topic, count in sorted(topic_counts.items()):
        print(f"  {topic}: {count}")

    # Print questions with no topics
    no_topics = [q for q in unique_questions if not q["topics"]]
    if no_topics:
        print(f"\n{len(no_topics)} questions have no topic tags:")
        for q in no_topics[:5]:
            print(f"  - {q['question'][:80]}...")

if __name__ == "__main__":
    main()

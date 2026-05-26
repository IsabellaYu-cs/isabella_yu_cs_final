import json
import os

# This script generates explanations for AP Microeconomics questions
# In a real implementation, you would use an AI API to generate explanations
# For now, we'll create placeholder explanations

def generate_explanation(question, answer):
    """Generate an explanation for a question."""
    # This is a simplified version - in reality, you'd use an AI API

    question_text = question["question"]
    correct_answer = question["options"][answer]

    # Create a basic explanation template
    explanation = f"The correct answer is {answer}: {correct_answer}. "

    # Add topic-specific explanation based on keywords
    topics = question["topics"]

    if "Cost Curves" in topics:
        explanation += "This question relates to cost analysis in economics. "
        explanation += "Remember that accounting profit = total revenue - explicit costs, "
        explanation += "while economic profit = total revenue - (explicit costs + implicit costs). "
    elif "Supply & Demand" in topics:
        explanation += "This question involves supply and demand analysis. "
        explanation += "Consider how changes in price, income, or related goods affect demand and supply curves. "
    elif "Elasticity" in topics:
        explanation += "This question deals with elasticity concepts. "
        explanation += "Elasticity measures the responsiveness of quantity demanded or supplied to changes in price, income, or other factors. "
    elif "Market Structures" in topics:
        explanation += "This question relates to market structure analysis. "
        explanation += "Different market structures (perfect competition, monopoly, monopolistic competition, oligopoly) have different characteristics and outcomes. "
    elif "Externalities & Public Goods" in topics:
        explanation += "This question involves externalities and market failure. "
        explanation += "Externalities occur when production or consumption affects third parties not directly involved in the transaction. "
    elif "Factor Markets" in topics:
        explanation += "This question deals with factor markets. "
        explanation += "Factor markets involve the buying and selling of inputs like labor and capital. "
    elif "Utility Maximization" in topics:
        explanation += "This question relates to consumer choice and utility maximization. "
        explanation += "Consumers maximize utility by allocating their budget where marginal utility per dollar is equal across all goods. "
    else:
        explanation += "This question tests your understanding of basic economic concepts. "

    return explanation

def main():
    """Main function to generate explanations for all questions."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "data", "questions.json")
    output_file = os.path.join(script_dir, "data", "questions_with_explanations.json")

    # Load questions
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"Generating explanations for {len(questions)} questions...")

    # Generate explanations
    for i, question in enumerate(questions):
        if not question["explanation"]:
            question["explanation"] = generate_explanation(question, question["answer"])

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1} questions...")

    # Save questions with explanations
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(questions)} questions with explanations to {output_file}")

if __name__ == "__main__":
    main()

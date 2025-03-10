import difflib
import os
import json

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
#-------------------------FAQ--------------------#

FAQ_FILE = os.path.join(BASE_DIR, "urls", "polkadot_faq.json")

def load_faq():
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("⚠️ Invalid FAQ format! Expected a list.")
            return data
    except FileNotFoundError:
        print(f"⚠️ {FAQ_FILE} not found!")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ {FAQ_FILE} contains invalid JSON!")
        return []

faq_data = load_faq()

def get_faq_questions():
    return [entry["question"] for entry in faq_data]

def find_best_faq_match(user_question: str):
    questions = get_faq_questions()
    best_match = difflib.get_close_matches(user_question, questions, n=1, cutoff=0.5)
    
    if best_match:
        for entry in faq_data:
            if entry["question"] == best_match[0]:
                return f"**{entry['question']}**\n{entry['answer']}"
    
    return "❌ No have any question."
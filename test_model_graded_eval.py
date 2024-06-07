import pytest

from src.utils.serverLogic import twitter
from src.utils.llm.LLM import LLM

from tests.utils.eval_llm.EvalLLM import EvalLLM


def get_userdata(username, account_type):
    if account_type == "Twitter":
        profile = twitter.getTwitterProfile(username)

        if profile:
            content = []

            if "description" in profile and profile["description"]:
                content.append(profile["description"])

            for p in twitter.getUserPosts(profile["id"], 10):
                if "text" in p and p["text"]:
                    content.append(p["text"])

            content = "\n\n------------------\n".join(content)

            return content
        return None

    elif account_type == "linkedin":
        pass
    else:
        pass


def load_rag_llm():
    return LLM()


def load_evaluator_llm():
    return EvalLLM()


def test_rag_model_graded_evaluation():
    username, account_type = "elonmusk", "Twitter"
    topic = "SpaceX"
    user_data = get_userdata(username, account_type)

    if not user_data:
        print(f"user with {username} does not exist!")
    else:
        rag_llm = load_rag_llm()
        evaluator_llm = load_evaluator_llm()

        score = int(rag_llm.generate(user_data, topic).strip())

        rag_output = f"User shows {score} interest in {topic}"

        evaluator_input = {
            "topic": topic,
            "user_data": user_data,
            "rag_output": rag_output,
            "score": score,
        }
        evaluation_score = evaluator_llm.evaluate_rag_output(**evaluator_input)

    assert evaluation_score == "Yes"

import pytest
from src.utils.serverLogic import twitter
from src.utils.llm.LLM import LLM
from tests.utils.eval_llm import get_rag_output


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
        return None, None

    elif account_type == "LinkedIn":
        pass
    else:
        pass


def mock_get_llm_score(query, content):
    llm = LLM()
    response = llm.generate(query, content)

    return int(response.strip())


def test_rag_rule_based_evaluation():
    # Define sample topics and user data variations
    topics = ["SpaceX", "Cloud Computing"]
    user_data = get_userdata("elonmusk", "Twitter")

    # Define expected outputs based on predefined rules
    expected_outputs = [
        get_rag_output(80),
        get_rag_output(40),
    ]

    for topic, expected_output in zip(topics, expected_outputs):
        # Simulate LLM score
        score = mock_get_llm_score(topic, user_data)

        # Assert the RAG output matches the expected_outputs based on rules
        assert get_rag_output(score) == expected_output


test_rag_rule_based_evaluation()

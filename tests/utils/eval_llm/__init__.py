from decouple import config
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from src.utils.serverLogic import twitter

load_dotenv()
GOOGLE_API_KEY = config("PALM_API_KEY")
SYSTEM_PROMPT = """
    You are an expert tester who given an input formated under 'Input' will perform the required tasks listed under 'Task'.    

    If The user's posts talks about completely different topic and show no interest in the topic given then the score should in the range of 10-20,
    The user's posts talks about completely different topic but those topics might have something in common with the topic in question the score should be in the range of 20-30,
    The user's posts talks about topics that can be under the same category and might be interested in the topic the score should be in the range  30-60,
    The user's posts shows clear signs of being interested in the topic in question the score should be in the range 60-80,
    The user's posts mention the topic in question and suggest a high likelihood of being interested in the topic the score should be in the range 80-100,

    Input:
        Topic: {topic}
        User Data: {user_data}
        RAG Output: {rag_output}
    Task: Rate the accuracy, relevance, and coherence of the provided RAG output in the context of the given topic and user data summary. Higher scores indicate a more accurate, relevant, and well-supported RAG output.
    Output:
        Response: Based on the given information give a response by saying Yes if the overall requirements have been considered, otherwise respond by a simple No.
"""


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


def get_rag_output(score):
    if score <= 20:
        return "Different topic, Not Interested"
    elif score <= 30:
        return "Different topic, Might have something in common"
    elif score <= 60:
        return "Topics can be under the same category, Might be interested"
    elif score <= 80:
        return "Clear sign of being interested"
    elif score <= 100:
        return "High likelihood of being interested"


model = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

from src.utils.scraping import LINKEDIN_PREFIX, TWITTER_PREFIX
from src.utils.scraping.LinkedIn import LinkedIn
from src.utils.scraping.Mastodon import Mastodon
from src.utils.scraping.Twitter import Twitter
from src.utils.serverLogic.LLMServer import LLMServer

linkedIn = LinkedIn()
mastodon = Mastodon()
twitter = Twitter()
llm_server = LLMServer()

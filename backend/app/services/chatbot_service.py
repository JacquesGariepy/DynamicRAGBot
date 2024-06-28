from app.services.rag_service import RAGService
from app.services.bot_service import BotService
from app.models.user import User
from app import db
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
# from googletrans import Translator

nltk.download('punkt')
nltk.download('stopwords')

class ChatbotService:
    def __init__(self):
        self.rag_service = RAGService()
        self.bot_service = BotService()
        # self.translator = Translator()

    def process_message(self, user_id, message, language='en'):
        user = User.query.get(user_id)
        if not user:
            return "User not found. Please log in."

        # if language != 'en':
        #     message = self.translator.translate(message, dest='en').text

        tokens = word_tokenize(message.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in tokens if not w in stop_words]

        intent = self.determine_intent(filtered_tokens)
        response = self.generate_response(intent, user, filtered_tokens)

        # if language != 'en':
        #     response = self.translator.translate(response, dest=language).text

        return response

def determine_intent(self, tokens):
        intent_keywords = {
            'create_bot': ['create', 'new', 'bot'],
            'manage_bot': ['manage', 'update', 'configure', 'bot'],
            'analyze_data': ['analyze', 'interpret', 'data', 'results'],
            'troubleshoot': ['problem', 'error', 'issue', 'help'],
            'explain_feature': ['how', 'what', 'explain', 'feature'],
        }

        for intent, keywords in intent_keywords.items():
            if any(keyword in tokens for keyword in keywords):
                return intent

        return 'general_query'

    def generate_response(self, intent, user, tokens):
        if intent == 'create_bot':
            return self.guide_bot_creation(user)
        elif intent == 'manage_bot':
            return self.guide_bot_management(user)
        elif intent == 'analyze_data':
            return self.assist_data_analysis(user, tokens)
        elif intent == 'troubleshoot':
            return self.provide_troubleshooting(tokens)
        elif intent == 'explain_feature':
            return self.explain_feature(tokens)
        else:
            return self.handle_general_query(tokens)

    def guide_bot_creation(self, user):
        return "To create a new bot, go to the 'Bots' section and click on 'Create New Bot'. You'll need to provide a name and configure the bot's settings, such as the websites to scrape and the scraping frequency."

    def guide_bot_management(self, user):
        return "To manage your bots, go to the 'Bots' section. Here you can start, stop, edit, or delete your bots. Click on a specific bot to view its details and performance metrics."

    def assist_data_analysis(self, user, tokens):
        query = " ".join(tokens)
        return self.rag_service.query(query)

    def provide_troubleshooting(self, tokens):
        return "I'm sorry to hear you're experiencing an issue. Can you please provide more details about the problem? What specific error message are you seeing, or what unexpected behavior are you encountering?"

    def explain_feature(self, tokens):
        feature = " ".join(tokens)
        return f"I'd be happy to explain the {feature} feature. Could you please specify which aspect of this feature you'd like more information about?"

    def handle_general_query(self, tokens):
        query = " ".join(tokens)
        return self.rag_service.query(query)
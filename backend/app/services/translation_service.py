from googletrans import Translator

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, target_language):
        try:
            translation = self.translator.translate(text, dest=target_language)
            return translation.text
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return text  # Return original text if translation fails
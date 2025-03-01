import time
from telegram import Update
from telegram.ext import (
    Application,
)
from src.microservices.bot.services.telegram import (
    WeatherConversationBuilder,
    WeatherConversationDirector,
)
from src.core.config import settings


application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
count = 0
max_retry_count = 5


def main(count: int):
    try:
        conversation_builder = WeatherConversationBuilder(application=application)
        conversation_director = WeatherConversationDirector(
            builder=conversation_builder,
            application=application,
        )
        conversation_director.construct_conversation()
        print("Bot Service - Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"Bot Service - Error: {e}")
        print(f"Bot Service - Retry count: {count}.", "Retrying in 10 seconds...")
        time.sleep(10)
        if count < max_retry_count:
            main(count + 1)


if __name__ == "__main__":
    main(count)

from bot.bot import start, list_files, upload_file, search_button, cython, pi_button, FIRST, SECOND
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import os


def main():
    import cProfile
    import pstats

    load_dotenv()
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()
    
    application.add_handler(CommandHandler('start', start))
    with cProfile.Profile() as pr:
        application.add_handler(CommandHandler('files', list_files))
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='profiling.prof')


    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("cython", cython)],
            states={
                FIRST: [CallbackQueryHandler(search_button)],
                SECOND: [CallbackQueryHandler(pi_button)],
            },
            fallbacks=[CommandHandler("cython", cython)],
        )

    application.add_handler(conv_handler)
    
    application.add_handler(MessageHandler(filters.Document.ALL, upload_file))


    application.run_polling()


if __name__ == '__main__':
    main()
   



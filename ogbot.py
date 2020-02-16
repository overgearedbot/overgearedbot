

import logging
import telegram
from telegram.ext import Updater, CommandHandler
from wuxiaworld import is_new_chapter, parse_chapter

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# real
# chatid = -1001364922988

# test
chatid = int(<TODO_CHATID>)

chapter_id = ""

def poll_chapter(context):
    """
    # check for chapter
        # oh something new
            # retrieve chapter
            # update chapterid 
        # oh nothing new
    """
    job = context.job
    get_pinned_message = context.bot.getChat(chat_id=chatid)['pinned_message']['text']

    chapter_id = get_pinned_message.replace("Next chapter: ", "").strip()
    new_chapter = is_new_chapter(chapter_id)

    if new_chapter:
        content = parse_chapter(chapter_id)
        filepath = "/tmp/" + str(chapter_id) + ".txt"

        with open(filepath, "w+") as chapter_file:
            [ chapter_file.write(line) for line in content ]
        context.bot.send_message(job.context, text="chapter " + chapter_id + " is released!")
        with open(filepath, 'rb') as f:
            context.bot.send_document(job.context, document=f)

        pin_this_message = context.bot.send_message(job.context, text="Next chapter: " + str(int(chapter_id) + 1))
        context.bot.pinChatMessage(chat_id=chatid, message_id=pin_this_message.message_id)
        
    else:
        pass


def chapter(update, context):
    msg = str(update.message.text).replace("/chapter","Next chapter: ")
    pin_this_message = context.bot.send_message(chat_id=chatid, text=msg)
    context.bot.pinChatMessage(chat_id=chatid, message_id=pin_this_message.message_id)

    print("triggered!")
    try:
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()

        new_job = context.job_queue.run_repeating(poll_chapter, 3600, context=chatid)
        context.chat_data['job'] = new_job

        context.bot.send_message(chat_id=chatid, text="I'm looking out for new chapters!")
    except:
        context.bot.send_message(chat_id=chatid, text="something went wrong x_x")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, lets read Overgeared together!")
    context.bot.send_message(chat_id=update.effective_chat.id, text="use /chapter <id> to set the current chapter!")

def valentines(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Happy valentines, I love you dear.")

def error(update, context):
    logger.warning('update "%s" caused error "%s"', update, context.error)


def main():
    logger.info('bot started')
    updater = Updater("<TODO_BOT_TOKEN>", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("valentines", valentines))
    dp.add_handler(CommandHandler("chapter", chapter, 
                                    pass_args=True,
                                    pass_job_queue=True,
                                    pass_chat_data=True))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

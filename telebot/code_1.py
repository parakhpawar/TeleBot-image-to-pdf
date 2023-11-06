# import os
# from altair import FilterTransform
# from telegram import Bot, InputFile, Update
# # from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

# from PIL import Image

# # Telegram bot API token
# API_TOKEN = 'enter token here'

# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text('Send me the image(s) to convert to PDF.')

# def convert_to_pdf(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     image_path = r'C:\Users\parak\Desktop\telebot\images'  # Path to your local image folder
#     pdf_path = r'C:\Users\parak\Desktop\telebot\pdf'

#     images = os.listdir(image_path)
#     images = [img for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

#     pdf = Image.new('RGB', (1, 1))

#     for image in images:
#         img = Image.open(os.path.join(image_path, image))
#         pdf = pdf.convert('RGB')
#         pdf = Image.new('RGB', img.size, (255, 255, 255))
#         pdf.paste(img)
#         pdf.save(pdf_path, save_all=True, append_images=[pdf])

#     with open(pdf_path, 'rb') as pdf_file:
#         context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(pdf_file))



# def main():
#     bot = Bot(token=API_TOKEN)
#     updater = Updater(bot=bot, use_context=True)
#     dispatcher = updater.dispatcher

#     # updater = Updater(token=API_TOKEN, use_context=True)
#     # dispatcher = updater.dispatcher

#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(MessageHandler(FilterTransform.photo, convert_to_pdf))

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

from telegram import Bot, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = 'enter token here'

def convert_images_to_pdf(image_paths, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    for image_path in image_paths:
        image = Image.open(image_path)
        image_width, image_height = image.size
        c.setPageSize((image_width, image_height))
        c.drawImage(image_path, 0, 0, image_width, image_height)
        c.showPage()
    c.save()

def create_pdf_and_send(update, context):
    user_id = update.effective_user.id

    image_paths = [r'C:\Users\parak\Desktop\telebot\images\image1.jpg', r'C:\Users\parak\Desktop\telebot\images\image2.jpg']  # List of image file paths
    pdf_path = f'pdf_{user_id}.pdf'  # PDF output file path

    convert_images_to_pdf(image_paths, pdf_path)

    # Store the PDF in the user's context
    context.user_data['pdf_path'] = pdf_path
    update.message.reply_text("PDF created! Use /downloadpdf to download it.")

def download_pdf(update, context):
    user_id = update.effective_user.id

    if 'pdf_path' in context.user_data:
        pdf_path = context.user_data['pdf_path']
        with open(pdf_path, 'rb') as pdf_file:
            update.message.reply_document(document=InputFile(pdf_file))
    else:
        update.message.reply_text("No PDF found. Please create one using /createpdf.")

def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("createpdf", create_pdf_and_send))
    dp.add_handler(CommandHandler("downloadpdf", download_pdf))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()





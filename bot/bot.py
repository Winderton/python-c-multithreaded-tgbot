from __future__ import print_function

import os


import logging
from telegram import Update
from telegram.ext import ContextTypes


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.performance import linear, multithreaded, multiprocessed, linear_pi, mt_pi, mp_pi



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def creds():
        # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def list_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        service = build('drive', 'v3', credentials=creds())

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        #4.362e-06
        # l = []
        # for f in items:
        #     l.append(f.get("name"))

        print('Files:')
        #4.103e-06
        for item in items:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=item.get("name"))
            print(u'{0} ({1})'.format(item['name'], item['id']))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')



async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    newFile = await update.message.effective_attachment.get_file()
    await newFile.download(custom_path="downloaded/" + update.message.effective_attachment.file_name)


    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds())

        file_metadata = {'name': update.message.document.file_name}
        media = MediaFileUpload("downloaded/"+update.message.document.file_name,
                                mimetype=update.message.document.mime_type, resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Failure")
        print(F'An error occurred: {error}')
        file = None

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Success")

    return file.get('id')


FIRST, SECOND = range(2)


async def cython(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(u"Search", callback_data=str(FIRST))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(u"First module", reply_markup=reply_markup)

    return FIRST


async def search_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton(u"Pi", callback_data=(SECOND))]
    ]

    index = ((2**31-1) // 32 - 1)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="lin: "+linear(index))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mt: "+multithreaded(index))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mp: "+multiprocessed(index))

    #reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=u"Second module")

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

    return SECOND


async def pi_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query


    await context.bot.send_message(chat_id=update.effective_chat.id, text="lin: "+linear_pi(100000000))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mt: "+mt_pi(100000000))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="mp: "+mp_pi(100000000))


    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=u"You can add more CPU bound modules")


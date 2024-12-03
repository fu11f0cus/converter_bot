from docx2pdf import convert
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import requests
import aiofiles
import PyPDF2
from docx import Document

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start_func(message):
    chatID = message.chat.id;
    if 'docx' in message.document.file_name:
        fileinfo = await bot.get_file(message.document.file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{fileinfo.file_path}'
        response = requests.get(file_url);
        with open('saved.docx', 'wb') as out_file:
            out_file.write(response.content);
        convert('saved.docx', 'output.pdf');
        await bot.send_document(chatID, FSInputFile('output.pdf'))
    if 'pdf' in message.document.file_name:
        fileinfo = await bot.get_file(message.document.file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{fileinfo.file_path}'
        response = requests.get(file_url);
        with open('saved2.pdf', 'wb') as output:
            output.write(response.content)

        pdf_file = open('saved2.pdf', 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        output_doc = Document()
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            output_doc.add_paragraph(text)
        output_doc.save('output2.docx')
        pdf_file.close()
        await bot.send_document(chatID, FSInputFile('output2.docx'))

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    tasks = [main()]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))
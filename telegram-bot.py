from typing import Final
from telegram import Update
import google.generativeai as genai
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes



TOKEN: Final = 'BOT_TOKEN_HERE'
BOT_USERNAME: Final = 'BOT_USERNAME_HERE'
GOOGLE_API_KEY= 'GEMINI_API_KEY_HERE'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")




# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text('Hey there!')

async def roar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await update.message.reply_text('Roar!')


	

# Responses
def handle_response(text: str) -> str:
	processed: str = text.lower()
	if 'gen' in processed:
		response = model.generate_content(processed + " (don't use markdown, ignore the word gen)")
		return response.text
		
	elif 'hello' in processed or 'hi' in processed:
		return 'Yes?'
			
	elif 'who am i' in processed:
		return 'A mere human being I will crush.'
			
	else:	
		return 'No clue, mate.'
			

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	message_type: str =update.message.chat.type
	text: str = update.message.text
		
	print(f'User ({update.message.chat.id}) in {message_type}: "{text}" ')
		
	if message_type == 'supergroup':
		if BOT_USERNAME in text or 'mirror' in text:
			new_text: str = text.replace(BOT_USERNAME, '').strip()
			response: str = handle_response(new_text)
		else:
			return
	else:
		response: str = handle_response(text)
			
	print('Bot:',response)
	await update.message.reply_text(response)
		
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    

# Calling
if __name__ == '__main__':
    print('starting...')
    app =  Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('roar', roar_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    #polling
    print('polling...')
    app.run_polling(poll_interval=5)
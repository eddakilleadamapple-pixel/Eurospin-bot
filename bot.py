import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Abilitiamo i log per vedere eventuali errori
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# INSERISCI QUI IL TOKEN FORNITOTI DA BOTFATHER
TOKEN = "8706580742:AAEVIJ24vFSS1i0Nueo42Q8AoZ8m80g3Css"

# Database di esempio aggiornabile dei prodotti e offerte Eurospin
CATALOGO_EUROSPIN = [
    {"nome": "Mozzarella Land 3x100g", "categoria": "Latticini", "prezzo": "1,89 €", "offerta": "In offerta sul volantino"},
    {"nome": "Olio Extra Vergine Del Duca 1L", "categoria": "Condimenti", "prezzo": "4,49 €", "offerta": "Prezzo basso permanente"},
    {"nome": "Prosciutto Cotto Land", "categoria": "Salumi", "prezzo": "1,29 €", "offerta": "In offerta"},
    {"nome": "Biscotti Girotondi Cuore di Mela", "categoria": "Dolci e Colazione", "prezzo": "1,49 €", "offerta": "Novità"},
    {"nome": "Passata di Pomodoro Land 700g", "categoria": "Dispensa", "prezzo": "0,79 €", "offerta": "Prezzo basso permanente"},
    {"nome": "Yogurt ai Frutti Land 125g", "categoria": "Latticini", "prezzo": "0,45 €", "offerta": "In offerta"}
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    
    keyboard = [
        [InlineKeyboardButton("🔥 Vedi Ultime Offerte", callback_data="offerte")],
        [InlineKeyboardButton("🔍 Cerca Prodotto", callback_data="istruzioni_ricerca")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"Ciao {user_name}! Benvenuto nel tuo Bot non ufficiale Eurospin.\n\n"
        "Cosa desideri fare?"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "offerte":
        testo_offerte = "🔥 **Le migliori offerte Eurospin della settimana:**\n\n"
        for item in CATALOGO_EUROSPIN:
            if "offerta" in item["offerta"].lower():
                testo_offerte += f"• **{item['nome']}** - {item['prezzo']} ({item['offerta']})\n"
        await query.edit_message_text(text=testo_offerte, parse_mode="Markdown")
        
    elif query.data == "istruzioni_ricerca":
        await query.edit_message_text(
            text="🔍 **Come cercare un prodotto:**\n\nScrivi semplicemente il nome o una parte del prodotto che ti interessa (es. *Mozzarella*, *Olio*, *Latte*), e ti mostrerò se è disponibile e il prezzo!"
        )

async def cerca_prodotto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo_utente = update.message.text.lower().strip()
    
    risultati = [item for item in CATALOGO_EUROSPIN if testo_utente in item["nome"].lower()]
    
    if risultati:
        risposta = f"🔎 Ho trovato questi prodotti per '{update.message.text}':\n\n"
        for r in risultati:
            risposta += f"🛒 **{r['nome']}**\n   • Categoria: {r['categoria']}\n   • Prezzo: {r['prezzo']}\n   • Note: {r['offerta']}\n\n"
    else:
        risposta = f"Spiacente, non ho trovato nessun prodotto corrispondente a '{update.message.text}' nel catalogo attuale."
        
    await update.message.reply_text(risposta, parse_mode="Markdown")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), cerca_prodotto))

    print("Il bot è in esecuzione...")
    application.run_polling()

if __name__ == '__main__':
    main()

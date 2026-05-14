import logging
from collections import Counter
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import instaloader
import requests

# --- Configurazione Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inizializzazione Instaloader per Instagram
L = instaloader.Instaloader()

# --- Funzioni di Servizio ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕵️‍♂️ **OSINT Investigator Bot** attivo.\n\n"
        "Comandi disponibili:\n"
        "📸 /instagram <user> - Analisi profonda profilo\n"
        "📱 /phone <numero> - Investigazione cellulare\n"
        "👥 /facebook <query> - Ricerca Intelligence FB\n"
        "❓ /help - Mostra istruzioni"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🚀 **Guida ai Moduli:**\n\n"
        "1️⃣ **Instagram**: Estrae ID, bio, engagement rate, interessi (hashtag) e foto HD.\n"
        "2️⃣ **Phone**: Genera link di reverse lookup per identificare il proprietario e verifica WhatsApp/Telegram.\n"
        "3️⃣ **Facebook**: Utilizza tecniche di Google Dorking e Graph Search per trovare post e profili nascosti."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# --- MODULO 1: INSTAGRAM ULTRA ---

async def instagram_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso: /instagram <username>")
        return
    
    username = context.args[0].replace("@", "").strip()
    status = await update.message.reply_text(f"📡 Scansione profonda per @{username}...")
    
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Analisi Engagement e Hashtag sugli ultimi 15 post
        likes, count, tags = 0, 0, []
        if not profile.is_private:
            for post in profile.get_posts():
                if count >= 15: break
                likes += post.likes
                if post.caption_hashtags: tags.extend(post.caption_hashtags)
                count += 1
        
        eng_rate = (likes / count) / profile.followers * 100 if count > 0 and profile.followers > 0 else 0
        common_tags = ", ".join([f"#{t}" for t, _ in Counter(tags).most_common(5)]) if tags else "Nessuno"

        res = (
            f"👤 **PROFILO:** {profile.full_name}\n"
            f"🆔 **ID:** `{profile.userid}`\n"
            f"📝 **Bio:** _{profile.biography if profile.biography else 'Vuota'}_\n"
            f"🔗 **URL:** {profile.external_url if profile.external_url else 'Nessuno'}\n\n"
            f"📊 **METRICHE:**\n"
            f"• Follower: {profile.followers:,}\n"
            f"• Seguiti: {profile.followees:,}\n"
            f"• Engagement: `{eng_rate:.2f}%` (Media 15 post)\n\n"
            f"🛡️ **STATO ACCOUNT:**\n"
            f"• Privato: {'🔴 SÌ' if profile.is_private else '🟢 NO'}\n"
            f"• Verificato: {'🔵 SÌ' if profile.is_verified else '⚪ NO'}\n"
            f"• Business: {'🏢 ' + profile.business_category_name if profile.is_business_account else '👤 No'}\n\n"
            f"🏷️ **INTERESSI (TAG):** {common_tags}\n"
            f"🖼️ [Foto Profilo Alta Risoluzione]({profile.profile_pic_url})"
        )
        await update.message.reply_photo(profile.profile_pic_url, caption=res, parse_mode='Markdown')
        await status.delete()
    except Exception as e:
        await status.edit_text(f"⚠️ Errore Instagram: {str(e)}")

# --- MODULO 2: PHONE INVESTIGATOR ---

async def phone_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso: /phone <numero_con_prefisso>")
        return
    
    num = context.args[0].replace("+", "").strip()
    
    res = (
        f"📱 **INVESTIGAZIONE NUMERO: +{num}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **DATABASE IDENTITÀ:**\n"
        f"• [Sync.me](https://sync.me/search?number={num}) (Consigliato)\n"
        f"• [TrueCaller](https://www.truecaller.com/search/it/{num})\n"
        f"• [WhosCall](https://whoscall.com/it/search/{num})\n\n"
        f"💬 **SOCIAL CHECK:**\n"
        f"• [WhatsApp](https://wa.me/{num})\n"
        f"• [Telegram](https://t.me/+{num})\n\n"
        f"🌍 **SEARCH ENGINE INTELLIGENCE:**\n"
        f"• [Google Dork](https://www.google.com/search?q=%22%2B{num}%22+OR+%22{num}%22)\n"
        f"• [Tellows (Spam/Rating)](https://www.tellows.it/num/{num})"
    )
    await update.message.reply_text(res, parse_mode='Markdown', disable_web_page_preview=True)

# --- MODULO 3: FACEBOOK INTEL ---

async def facebook_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso: /facebook <nome_cognome_o_username>")
        return
    
    query = " ".join(context.args)
    query_enc = query.replace(" ", "+")
    
    res = (
        f"👥 **FACEBOOK INTELLIGENCE: {query}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍 **DIRETTE FB:**\n"
        f"• [Ricerca Persone](https://www.facebook.com/search/top/?q={query_enc})\n"
        f"• [Ricerca Messenger](https://www.messenger.com/t/{query_enc})\n\n"
        f"🕵️‍♂️ **GOOGLE DORKING (Post & Foto):**\n"
        f"• [Contenuti Indicizzati](https://www.google.com/search?q=site%3Afacebook.com+%22{query_enc}%22)\n"
        f"• [Menzioni e Commenti](https://www.google.com/search?q=site%3Afacebook.com+intext%3A%22{query_enc}%22)\n\n"
        f"🆔 **ANALISI ID:**\n"
        f"• [Lookup-ID.com](https://lookup-id.com/)\n"
    )
    await update.message.reply_text(res, parse_mode='Markdown', disable_web_page_preview=True)

# --- AVVIO APPLICAZIONE ---

if __name__ == '__main__':
    # Sostituisci con il tuo vero token preso da @BotFather
    TOKEN = '8475319275:AAGbmiHydxc62DlkrPx1CAoUIe-1Z6isLww'

    application = ApplicationBuilder().token(TOKEN).build()

    # Registrazione Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('instagram', instagram_lookup))
    application.add_handler(CommandHandler('phone', phone_lookup))
    application.add_handler(CommandHandler('facebook', facebook_lookup))

    print("🚀 OSINT Bot avviato con successo...")
    application.run_polling()

import instaloader
from datetime import datetime

# Inizializza
L = instaloader.Instaloader()

async def instagram_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Uso: /instagram <username>")
        return

    username = context.args[0].replace("@", "").strip()
    status_msg = await update.message.reply_text(f"🚀 **Analisi Deep-OSINT per @{username}...**")

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        # --- Calcolo Engagement Rate (Media likes sugli ultimi 10 post) ---
        total_likes = 0
        count = 0
        hashtags = []
        
        # Analizziamo solo se il profilo non è privato
        if not profile.is_private:
            for post in profile.get_posts():
                if count >= 10: break  # Limitiamo agli ultimi 10 per velocità
                total_likes += post.likes
                if post.caption_hashtags:
                    hashtags.extend(post.caption_hashtags)
                count += 1
        
        engagement = 0
        if count > 0 and profile.followers > 0:
            # Formula: ((Media Likes) / Follower) * 100
            engagement = (total_likes / count) / profile.followers * 100

        # --- Raccolta Hashtag più usati ---
        top_tags = "Nessuno"
        if hashtags:
            from collections import Counter
            most_common = Counter(hashtags).most_common(5)
            top_tags = ", ".join([f"#{tag}" for tag, _ in most_common])

        # --- Formattazione Output Potenziato ---
        report = (
            f"📥 **RISULTATI OSINT PER: @{username}**\n"
            f"---"
            f"\n👤 **IDENTITÀ**\n"
            f"  • **Nome:** {profile.full_name}\n"
            f"  • **ID:** `{profile.userid}`\n"
            f"  • **Bio:** _{profile.biography}_\n"
            f"  • **Sito:** {profile.external_url}\n"
            f"\n📊 **METRICHE SOCIAL**\n"
            f"  • **Followers:** {profile.followers:,}\n"
            f"  • **Following:** {profile.followees:,}\n"
            f"  • **Engagement Rate:** `{engagement:.2f}%`\n"
            f"  • **Post Totali:** {profile.mediacount}\n"
            f"\n🛡️ **STATO ACCOUNT**\n"
            f"  • **Privato:** {'🔴 Sì' if profile.is_private else '🟢 No'}\n"
            f"  • **Verificato:** {'🔵 Sì' if profile.is_verified else '⚪ No'}\n"
            f"  • **Business:** {'🏢 Sì' if profile.is_business_account else '👤 Personale'}\n"
            f"  • **Categoria:** {profile.business_category_name}\n"
            f"  • **Iscritto di recente:** {'⚠️ Sì' if profile.is_joined_recently else '✅ No'}\n"
            f"\n🔍 **INSIGHT CONTENUTI**\n"
            f"  • **Top Hashtag:** {top_tags}\n"
            f"  • **HD Profile Pic:** [Clicca qui per scaricare]({profile.profile_pic_url})\n"
            f"---"
            f"\n*Generato il: {datetime.now().strftime('%d/%m/%Y %H:%M')}*"
        )

        await update.message.reply_photo(
            photo=profile.profile_pic_url,
            caption=report,
            parse_mode='Markdown'
        )
        await status_msg.delete()

    except instaloader.exceptions.ProfileNotExistsException:
        await status_msg.edit_text("❌ Utente non trovato.")
    except instaloader.exceptions.QueryTooManyRequestsException:
        await status_msg.edit_text("⚠️ **Rate Limit!** Instagram ha bloccato temporaneamente la richiesta. Riprova più tardi o usa un account per il login.")
    except Exception as e:
        await status_msg.edit_text(f"💀 Errore critico: {str(e)}")

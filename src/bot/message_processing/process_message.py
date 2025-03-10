import aiohttp
import discord

from ..AI.ai_response import generate_response_with_text, generate_response_with_image_and_text   
from ..AI.pdf_respone import ProcessAttachments
from ..AI.classify_questions import classify_question_with_llm
from ..Docs.faq import get_faq_questions, find_best_faq_match
from ..Docs.scraping_blog import get_new_posts
from ..Docs.tracking_repos import get_latest_accepted_prs
from .message_history import (
    MAX_HISTORY, 
    split_and_send_messages, 
    clean_discord_message,
    update_message_history,
    get_formatted_message_history,
    message_history,)

SUMMERIZE_PROMPT = "Give me 5 bullets about"


#---------------------------------------------Discord Code-------------------------------------------------
async def process_message(bot, message):
    # Ignore messages sent by the bot or if mention everyone is used
    if message.author == bot.user or message.mention_everyone:
        return

    # Check if the bot is mentioned or the message is a DM
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        # Start Typing to seem like something happened
        cleaned_text = clean_discord_message(message.content)
        async with message.channel.typing():
            # Check for image attachments
            if message.attachments:
                # Currently no chat history for images
                for attachment in message.attachments:
                    print(f"New Image Message FROM: {message.author.name} : {cleaned_text}")
                    # these are the only image extensions it currently accepts
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        print("Processing Image")
                        await message.add_reaction('🎨')
                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('Unable to download the image.')
                                    return
                                image_data = await resp.read()
                                response_text = await generate_response_with_image_and_text(image_data, cleaned_text)
                                await split_and_send_messages(message, response_text, 1700)
                                return
                    else:
                        print(f"New Text Message FROM: {message.author.name} : {cleaned_text}")
                        await ProcessAttachments(message, cleaned_text)
                        return
            # Not an Image, check for text responses
            else:
                print(f"New Message Message FROM: {message.author.name} : {cleaned_text}")
                # Check for Reset or Clean keyword
                if "RESET" in cleaned_text or "CLEAN" in cleaned_text:
                    # End back message
                    if message.author.id in message_history:
                        del message_history[message.author.id]
                    await message.channel.send("🧼 History Reset for user: " + str(message.author.name))
                    return
                
                # Check for FAQ
                if "faq" in cleaned_text.lower():
                    faq_list = get_faq_questions()
                    formatted_faq = "\n".join(f"🔹 {faq}" for faq in faq_list)
                    best_match_response = find_best_faq_match(cleaned_text)
                    await message.channel.send(f"📚 **FAQs**\n{formatted_faq}")
                
                    if best_match_response:
                        await message.add_reaction('📚')
                        await message.channel.send(best_match_response)
                        return
                
                # Check if history is disabled, just send response
                await message.add_reaction('💬')
                if MAX_HISTORY == 0:
                    response_text = await generate_response_with_text(cleaned_text)
                    # Add AI response to history
                    await split_and_send_messages(message, response_text, 1700)
                    return

                # Add user's question to history
                update_message_history(message.author.id, cleaned_text)
                category = await classify_question_with_llm(cleaned_text)

                if category == "Trending topic":
                    new_posts = get_new_posts()
                    if new_posts:
                        response_text = "\n".join([f"📰 **{post['title']}**\n🔗 {post['link']}" for post in new_posts])
                    else:
                        response_text = "No new blog posts available at the moment."
                elif category == "New docs":
                    prs = get_latest_accepted_prs()
                    if prs:
                        response_text = "\n".join([f"📄 **{pr['title']}**\n🔗 {pr['url']}" for pr in prs])
                    else:
                        response_text = "No new documentation updates available."
                else:
                    response_text = await generate_response_with_text(get_formatted_message_history(message.author.id))

                                # Add AI response to history
                update_message_history(message.author.id, response_text)
                                # Split the Message so discord does not get upset
                await split_and_send_messages(message, response_text, 1700)

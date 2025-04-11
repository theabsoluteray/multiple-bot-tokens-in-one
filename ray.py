import multiprocessing
import os
import discord
from discord.ext import commands
import asyncio
import jishaku

def run_bot(token, ids):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.owner_id = 721249954504638500
   

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    @bot.command()
    @commands.is_owner()
    async def banall(ctx):
        guild = ctx.guild
        for member_id in ids:
            try:
                user = await bot.fetch_user(int(member_id))
                await guild.ban(user, reason="fcked")
                await ctx.send(f"Banned {user}")
            except Exception as e:
                print(f"Failed to ban {member_id}: {e}")
    @bot.command()
    async def dmspam(ctx, userid, *, message):
        guild = ctx.guild
        mem = guild.get_member(int(userid))
        ded = [721249954504638500]
        if mem in ded:
            await ctx.send("hatt chutiye")
            return
        else:
            try:
                for i in range(100):
                    await mem.send(message)
                await ctx.send(f"DM'd {mem.mention}")
            except Exception as e:
                        print(f"Failed to DM {mem.mention}: {e}")
    @bot.command()
    async def play(ctx):
        
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You are not in a voice channel.")
            return

      
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        try:
           
            file_name = "ray.mp3"

            volume_filter = f"volume=9999"

      
            audio_source = discord.FFmpegPCMAudio(file_name, options=f"-af {volume_filter}")
            voice_client.play(audio_source)

            
            while voice_client.is_playing():
                await asyncio.sleep(1)

          
            await voice_client.disconnect()
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="blah blah blah"))
        await bot.load_extension("jishaku")
        print(f"{bot.user} is ready.")

    try:
        bot.run(token)
    except Exception as e:
        print(f"Error running bot: {e}")

def main():
    with open("scraped.txt", "r") as f:
        member_ids = [line.strip() for line in f]

    with open("tkn.txt", "r") as f:
        tokens = [line.strip() for line in f]

    chunk_size = (len(member_ids) + len(tokens) - 1) // len(tokens)
    chunks = [member_ids[i:i + chunk_size] for i in range(0, len(member_ids), chunk_size)]

    processes = []
    for token, ids in zip(tokens, chunks):
        p = multiprocessing.Process(target= run_bot, args=(token, ids))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()

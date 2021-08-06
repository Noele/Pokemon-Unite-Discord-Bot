from discord.ext import commands
import discord, sys, traceback

bot = commands.Bot(command_prefix=commands.when_mentioned_or("_"), description='Pokemon Unite UK Discord bot.')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

if __name__ == '__main__':
    for extension in ["cogs.general"]:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load cog - {extension}.', file=sys.stderr)
            traceback.print_exc()

bot.run("ODcyMzMyODI5NzAxMzI4OTY3.YQoVQQ.yr6blrcshDPG5mq4KLsrZtq8Li8")

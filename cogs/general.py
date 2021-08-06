from discord.ext import commands
import discord
import requests
from urllib.parse import quote
from cogs import ImageGenerator

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generator = ImageGenerator.ImageGenerator()

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        user = ctx.author if member is None else member
        file = self.generator.GenerateTrainerCard(user)
        await ctx.send(file=file)

    @commands.command()
    async def signup(self, ctx):
        await self.addmember(ctx.author)

    async def addmember(self, member):
        payload = {
            "username": member.name,
            "profilepicture": quote(str(member.avatar_url_as(format="png"))),
            "discriminator": member.discriminator,
            "userid": member.id,
            "bottoken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ"
        }
        print(payload)

        r = requests.get("http://127.0.0.1:5000/createuser", params=payload)
        if r.status_code == 201:
            print("Signup request completed.")
            return True
        if r.status_code == 409:
            print("Server responded with error code 409; User already exists.")
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.bot.user:
            success = await self.addmember(message.author)
            if success:
                response = requests.get(f"http://127.0.0.1:5000/getuser?userid={message.author.id}&bottoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ")
                response = response.json()
                await message.channel.send(f"Hello <3, I have created you a profile ! You can edit it here http://84.66.132.152:5000/dashboard?userid={message.author.id}&token={response['token']} Do not share this link with anyone or they will be able to edit your profile without your permission !!! If you think someone knows your link, message Tachi#1823 asap")


def setup(bot):
    bot.add_cog(General(bot))
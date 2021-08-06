import io

from discord.ext import commands
import discord
import requests
import json
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
import re
import textwrap

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        user = ctx.author if member is None else member
        response = requests.get(f"http://127.0.0.1:5000/getuser?userid={user.id}&bottoken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ")
        response = response.json()

        biography = response["biography"]
        favouritepokemon = response["favouritepokemon"]
        playsbotlane = response["playsbotlane"]
        playsjungle = response["playsjungle"]
        playstoplane = response["playstoplane"]
        trainerid = response["trainerid"]
        rank = response["rank"]
        level = str(response["level"])
        profilepicture = response["profilepicture"]

        # Load Template as im
        with Image.open("C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data/Template.png") as im:
            im = im.convert("RGBA")

            # Draw the profile picture under the template, after this point, draw onto canvas, rather then im
            profilepictureImage = Image.open(requests.get(profilepicture, stream=True).raw)
            profilepictureImage.thumbnail((200, 200), Image.ANTIALIAS)

            canvas = Image.new('RGBA', im.size)
            canvas_draw = ImageDraw.Draw(canvas)
            canvas.paste(profilepictureImage, (129, 220))
            canvas.paste(im, (0, 0), im)

            # Write the level onto the template
            fnt = ImageFont.truetype('C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data/AnyConv.com__Rockwell-ExtraBold.ttf', 36)
            canvas_draw.text((135 - (8 * len(level)), 63), level, font=fnt, fill=(255, 255, 255))

            # Write the username onto the template
            fnt.size = 46
            canvas_draw.text((355, 302), user.name, font=fnt, fill=(255, 255, 255))

            # Write the username onto the template
            fnt.size = 46
            canvas_draw.text((699, 36), trainerid, font=fnt, fill=(255, 255, 255))

            # Write the biography onto the template
            biographyfont = ImageFont.truetype('C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data/AnyConv.com__Rockwell-ExtraBold.ttf', int(14 + (14 - (len(biography) / 10))) if int(14 + (14 - (len(biography) / 10))) != 0 else 1)
            para = textwrap.wrap(biography, width=25 - (9 - (24 - biographyfont.size)))
            MAX_W, MAX_H = 314, 146
            biographytextImage = Image.new('RGBA', (MAX_W, MAX_H), (0, 0, 0, 0))
            draw = ImageDraw.Draw(biographytextImage)

            # Textwrapping
            current_h, pad = 0, 10
            for line in para:
                w, h = draw.textsize(line, font=biographyfont)
                draw.text(((MAX_W - w) / 2, current_h), line, font=biographyfont)
                current_h += h + pad

            canvas.paste(biographytextImage, (309, 407), biographytextImage)

            # Add cup to image
            cup = Image.open(f"C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data/Cups/{rank if rank != 'Beginner' else 'Great' }.png")
            cup = cup.convert("RGBA")
            cupwidth, cupheight = cup.size
            canvas.paste(cup, (790 - int((cupwidth / 2)), 471 - int((cupheight / 2))), cup)

            # Add pokemon to image
            pokemon = Image.open(f"C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data/Pokemon/{favouritepokemon}.png")
            pokemon = pokemon.convert("RGBA")
            pokemon.thumbnail((250, 250), Image.ANTIALIAS)
            pokemonwidth, pokemonheight = pokemon.size
            canvas.paste(pokemon, (529 - int((pokemonwidth / 2)), 163 - int((pokemonheight / 2))), pokemon)

            # Send image
            arr = io.BytesIO()
            canvas.save(arr, format='PNG')
            arr.seek(0)
            discord_file = discord.File(arr, "profile.png")
            await ctx.send(file=discord_file)

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
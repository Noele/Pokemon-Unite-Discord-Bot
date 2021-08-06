import io
import discord
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap


class ImageGenerator:
    def __init__(self):
        self.path = "C:/Users/spice/PycharmProjects/Pokemon Unite Discord Bot/data"
        self.font = "/fonts/AnyConv.com__Rockwell-ExtraBold.ttf"
        self.bot_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.cThIIoDvwdueQB468K5xDc5633seEFoqwxjF_xSJyQQ"

    def GenerateTrainerCard(self, user: discord.Member):
        response = requests.get(f"http://127.0.0.1:5000/getuser?userid={user.id}&bottoken={self.bot_token}")
        response = response.json()

        biography = response["biography"]
        favouritepokemon = response["favouritepokemon"]
        played_positions = ["Top" if response["playstoplane"] else None, "Mid" if response["playsjungle"] else None,
                            "Bot" if response["playsbotlane"] else None]
        trainerid = response["trainerid"]
        rank = response["rank"]
        level = str(response["level"])
        profilepicture = response["profilepicture"]

        # Load Template as im
        with Image.open(f"{self.path}/Template.png") as im:
            im = im.convert("RGBA")

            canvas = self.ApplyProfilePicture(profilepicture, im)
            canvas_draw = ImageDraw.Draw(canvas)

            # Write the level onto the template
            self.ApplySimpleText(canvas_draw, level, 135 - (8 * len(level)), 63, "AnyConv.com__Rockwell-ExtraBold.ttf",
                                 36)

            # Write the username onto the template
            self.ApplySimpleText(canvas_draw, user.name, 355, 302, "AnyConv.com__Rockwell-ExtraBold.ttf", 36)

            # Write the trainer id onto the template
            self.ApplySimpleText(canvas_draw, trainerid, 699, 36, "AnyConv.com__Rockwell-ExtraBold.ttf", 36)

            # Write the biography onto the template
            self.ApplyBiography(biography, canvas)

            # Add cup to image
            self.ApplyCup(rank, canvas)

            # Add pokemon to image
            self.ApplyPokemon(favouritepokemon, canvas)

            # Add Lane Positions to image
            self.ApplyLanePositions(played_positions, canvas)

            # Return image
            arr = io.BytesIO()
            canvas.save(arr, format='PNG')
            arr.seek(0)
            return discord.File(arr, "profile.png")

    def ApplyProfilePicture(self, profilepicture, image):
        # Draw the profile picture under the template, after this point, draw onto canvas, rather then im
        profilepictureImage = Image.open(requests.get(profilepicture, stream=True).raw)
        profilepictureImage.thumbnail((200, 200), Image.ANTIALIAS)

        canvas = Image.new('RGBA', image.size)
        canvas.paste(profilepictureImage, (129, 220))
        canvas.paste(image, (0, 0), image)
        return canvas

    def ApplySimpleText(self, canvas, text, x, y, font, fontsize):
        fnt = ImageFont.truetype(f"{self.path}/fonts/{font}", fontsize)
        canvas.text((x, y), text, font=fnt, fill=(255, 255, 255))

    def ApplyBiography(self, biography, canvas):
        biographyfont = ImageFont.truetype(f'{self.path}{self.font}', int(14 + (14 - (len(biography) / 10))) if int(
            14 + (14 - (len(biography) / 10))) != 0 else 1)
        para = textwrap.wrap(biography, width=25 - (9 - (24 - biographyfont.size)))
        MAX_W, MAX_H = 314, 146
        biographytextImage = Image.new('RGBA', (MAX_W, MAX_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(biographytextImage)

        # Textwrapp
        # ing
        current_h, pad = 0, 10
        for line in para:
            w, h = draw.textsize(line, font=biographyfont)
            draw.text(((MAX_W - w) / 2, current_h), line, font=biographyfont)
            current_h += h + pad

        canvas.paste(biographytextImage, (309, 407), biographytextImage)

    def ApplyCup(self, rank, canvas):
        cup = Image.open(f"{self.path}/Cups/{rank if rank != 'Beginner' else 'Great'}.png")
        cup = cup.convert("RGBA")
        cup_width, cup_height = cup.size
        canvas.paste(cup, (790 - int((cup_width / 2)), 471 - int((cup_height / 2))), cup)

    def ApplyPokemon(self, pokemon, canvas):
        pokemon_image = Image.open(f"{self.path}/Pokemon/{pokemon}.png")
        pokemon_image = pokemon_image.convert("RGBA")
        pokemon_image.thumbnail((250, 250), Image.ANTIALIAS)
        pokemonwidth, pokemonheight = pokemon_image.size
        canvas.paste(pokemon_image, (529 - int((pokemonwidth / 2)), 163 - int((pokemonheight / 2))), pokemon_image)

    def ApplyLanePositions(self, positions, canvas):
        for x, position in enumerate(positions):
            if position:
                position_image = Image.open(f"{self.path}/Lane Positions/{position}.png")
                position_image = position_image.convert("RGBA")
                position_image.thumbnail((50, 50), Image.ANTIALIAS)
                position_width, position_height = position_image.size
                canvas.paste(position_image,
                             (141 - int((position_width / 2)), (430 - int((position_height / 2))) + 50 * x),
                             position_image)

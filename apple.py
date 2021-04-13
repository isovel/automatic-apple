__authors__ = 'aejb'

import discord
from discord.ext import commands
from random import randint
import datetime
import pickledb


class apple(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def any_apples(self, id):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        db.dump()
        if existing_apples >= 1:
            return True
        else:
            return False

    @commands.command()
    async def sniff(self, ctx):
        """------ sniffs for any apples that might be lying around"""
        sniff_roll = randint(0, 4)
        if 0 <= sniff_roll <= 2 or self.any_apples('ground') is False:
            await ctx.send("you didn't find any apples :(")
        else:
            ground_apples = self.get_apples('ground')
            await ctx.send(f"you found {ground_apples} apples!")
            self.give_apples(ctx.author.id, ground_apples)
            self.give_apples('ground', int(-1 * ground_apples))

    @commands.command()
    async def throw(self, ctx, thrown_at: discord.Member):
        """------ throw an apple at a friend (with a mention!)"""
        throw_roll = randint(0, 3)
        if self.any_apples(ctx.author.id) is False:
            await ctx.send("you haven't got any apples to throw :(")
            return
        self.give_apples(ctx.author.id, -1)
        if throw_roll == 0:
            await ctx.send("you missed, sorry :(")
            self.give_apples('ground', 1)
        elif throw_roll == 1:
            await ctx.send(f"{thrown_at.mention} caught the apple!")
            self.give_apples(thrown_at.id, 1)
        else:
            await ctx.send(f"you hit {thrown_at.mention} with an apple.... which disappeared")

    @commands.command()
    async def count(self, ctx, *, other_user: discord.Member = False):
        """------ tells you how many apples you have"""
        if other_user is False:
            apple_count = self.get_apples(str(ctx.author.id))
            if apple_count is False:
                result = "you don't have any apples :("
            else:
                result = f"you've got {str(apple_count)} apple{'s' if apple_count > 1 else ''}!"
        else:
            apple_count = self.get_apples(str(other_user.id))
            if apple_count is False:
                result = f"{other_user.display_name} doesn't have any apples :("
            elif apple_count == 1:
                result = f"{other_user.display_name} has {str(apple_count)} apple!"
            else:
                result = f"{other_user.display_name} has {str(apple_count)} apples!"
        await ctx.send(result)

    @commands.command()
    async def rank(self, ctx, *, other_user: discord.Member = False):
        """------ tells you your rank on the apple leaderboard"""
        if other_user is False:
            apple_count = self.get_apples(str(ctx.author.id))
            if apple_count is False:
                result = "you don't have any apples :("
            elif apple_count == 1:
                result = f"you've got {str(apple_count)} apple!"
            else:
                result = f"you've got {str(apple_count)} apples!"
        else:
            apple_count = self.get_apples(str(other_user.id))
            if apple_count is False:
                result = f"{other_user.display_name} doesn't have any apples :("
            elif apple_count == 1:
                result = f"{other_user.display_name} has {str(apple_count)} apple!"
            else:
                result = f"{other_user.display_name} has {str(apple_count)} apples!"
        await ctx.send(result)

    @commands.command()
    async def leaderboard(self, ctx):
        """------ show the apple leaderboard"""
        arr = self.get_sorted_db()
        embed = discord.Embed(title="apple leaderboard", colour=discord.Colour(0xDE2A42), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Page uhhhhhh idk, maybe like uh 1?", icon_url="https://raw.githubusercontent.com/aejb/automatic-apple/master/apple.png")
        wah_rankings = ''
        wah_apple_counts = ''
        for user in arr[:10]:
            wah_rankings += f"{self.get_rank(user[0])}) <@{user[0]}>\n"
            wah_apple_counts += f"{user[1]} apples\n"
        wah_rankings = wah_rankings[:-1]
        wah_apple_counts = wah_apple_counts[:-1]
        embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬", value=wah_rankings, inline=True)
        embed.add_field(name="▬▬▬▬▬▬", value=wah_apple_counts, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def top(self, ctx, show_num: int = 5):
        """------ show the top apple collectors"""
        arr = self.get_sorted_db()
        embed = discord.Embed(title="apple leaderboard", colour=discord.Colour(0xDE2A42), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Top {show_num}", icon_url="https://raw.githubusercontent.com/aejb/automatic-apple/master/apple.png")

        embed.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬", value=f"1) {arr[0][0]}\n2) {arr[1][0]}\n3) {arr[2][0]}\n4) {arr[3][0]}\n5) {arr[4][0]}", inline=True)
        embed.add_field(name="▬▬▬▬▬▬", value=f" {arr[0][1]} apples\n {arr[1][1]} apples\n {arr[2][1]} apples\n {arr[3][1]} apples\n {arr[4][1]} apples", inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def pls(self, ctx):
        """------ looks for apples"""
        roll = randint(1, 101)
        if 1 <= roll <= 2:
            result = ("woah! you found an extra shiny apple! that's worth four apples!✨🍎✨", True, 4)
        elif roll == 3:
            result = ("oh my god you found a GOLD APPLE! that's worth SEVEN apples! 🌟🌟🍎🌟🌟", True, 7)
        elif 4 <= roll <= 14:
            result = ("hey nice apple! that's gotta be worth three apples! 💫🍎💫", True, 3)
        elif 15 <= roll <= 16:
            result = ("oh dear. you found a rotten apple :( you let another apple go bad! 🤢🍎🤢", True, -1)
        elif 17 <= roll <= 25:
            result = ("oh neat! two apples! 🍎🍎", True, 2)
        elif 26 <= roll <= 30:
            result = ("you found a green apple. it is the enemy. remove it at once. 🚫🍏🚫", False)
        elif 31 <= roll <= 80:
            result = ("here u go: 🍎", True, 1)
        else:
            result = ("no apples, sorry :(", False)
        await ctx.send(result[0])
        if result[1]:
            self.give_apples(ctx.author.id, result[2])

    def give_apples(self, id, new_apples):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        total_apples = existing_apples + new_apples
        db.set(str(id), total_apples)
        db.dump()

    def get_apples(self, id):
        db = pickledb.load('appledb', False)
        existing_apples = db.get(str(id))
        db.dump()
        return existing_apples

    def get_sorted_db(self):
        db = pickledb.load('appledb', False)
        keys = db.getall()
        arr = []
        for k in keys:
            if k == 'ground':
                continue
            v = db.get(k)
            arr.append((k, v))
        db.dump()
        arr.sort(reverse=True, key=lambda n: n[1])
        return arr

    def get_rank(self, id):
        arr = self.get_sorted_db()
        apple_count = self.get_apples(id)
        return arr.index((str(id), apple_count)) + 1


def setup(bot):
    bot.add_cog(apple(bot))

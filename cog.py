__authors__ = 'aejb'
import json
import math
import numpy
import typing

import discord
import aiohttp
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from random import randint


class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def has_mod(ctx):
        return ctx.guild.get_role(569846811796176916) in ctx.author.roles

    @commands.command()
    async def ping(self, ctx):
        """------ a simple ping-pong command"""
        latency_rounded = str("internal heartbeat latency = " + str(round(self.bot.latency, 1)) + "ms")
        embed = discord.Embed()
        embed.add_field(name=latency_rounded,
                        value="pong!",
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(569846811796176916)
    async def verify(self, ctx, member: discord.Member):
        """------ adds the verified role to a user"""
        await member.add_roles(member.guild.get_role(604623818358652951))
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    @verify.error
    async def verify_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have the permissions to verify a user.')
            await ctx.message.add_reaction('\N{CROSS MARK}')
        if isinstance(error, commands.BadArgument):
            await ctx.send('That user was not found in this guild. Have an apple.')
            await ctx.message.add_reaction('\N{CROSS MARK}')

    @commands.command()
    async def pls(self, ctx):
        """------ gives you an apple"""
        roll=randint(1, 101)
        if roll==1:
            await ctx.send("woah! you found an extra shiny apple! ✨🍎✨")
        elif roll==2 or roll==3:
            await ctx.send("oh my god you found a GOLD APPLE! 🌟🌟🍎🌟🌟")
        elif 4<=roll<=14:
            await ctx.send("hey nice apple dude! 💫🍎💫")
        elif roll==15 or roll==16:
            await ctx.send("oh dear. you found a rotten apple :( 🤢🍎🤢")
        elif 17<=roll<=25:
            await ctx.send("oh neat! two apples! 🍎🍎")
        elif 26<=roll<=30:
            await ctx.send("you found a green apple. it is the enemy. remove it at once. 🚫🍏🚫")
        elif roll==31:
            await ctx.send("well you didnt find an apple but you found an appley sergal 🧀🐧")
        else:
            await ctx.send("here u go: 🍎")

def setup(bot):
    bot.add_cog(moderation(bot))
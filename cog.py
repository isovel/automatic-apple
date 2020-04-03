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


class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
    async def find(self, ctx, user_mention: discord.Member):
        await user_mention.add_roles(604623818358652951)
        await ctx.send(str(user_mention))

def setup(bot):
    bot.add_cog(moderation(bot))
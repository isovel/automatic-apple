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

def setup(bot):
    bot.add_cog(moderation(bot))
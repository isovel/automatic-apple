__authors__ = 'aejb'

## requires d.py 1.0
## requires python3.6
import discord
from discord.ext import commands
import traceback
import sys
from datetime import datetime

now = datetime.now()

initial_extensions = ['cog']


def gettoken():
    token_file = open("token.txt", "r")
    token_string = token_file.read()
    token_token = token_string.split("\n")
    bot_token = str(token_token[0])
    return bot_token


bot_token = gettoken()

description = "here to help with your apples."
bot = commands.Bot(command_prefix=["apl "], description=description)

if __name__ == '__main__':
    for extension in initial_extensions:
        # noinspection PyBroadException
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("Failed to load" + extension, file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That command does not exist, or the cog did not properly load.')
        await ctx.message.add_reaction('\N{CROSS MARK}')
    else:
        raise error


@bot.event
async def on_message_delete(ctx):
    await ctx.guild.get_channel(695630766477934632).send(
        "Message by `{author}` deleted from `{channel}` at `{time}`\n > {content}".format(author=ctx.author,
                                                                                          channel=ctx.channel.name,
                                                                                          time=now.strftime(
                                                                                              "%I:%M:%S%p"),
                                                                                          content=discord.utils.escape_markdown(
                                                                                              ctx.content)))


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.embed==after.embed: return
    elif len(str(discord.utils.escape_markdown(before.content))) < 2000 and len(
            str(discord.utils.escape_markdown(after.content))) < 2000:
        await before.guild.get_channel(695630766477934632).send("Message by `{author}` edited in `{channel}` at `"
                                                                "{time}`\n**Before:**\n> {before}\n**After:**\n> "
                                                                "{after}".format(author=before.author,
                                                                                 channel=before.channel.name,
                                                                                 time=now.strftime("%I:%M:%S%p"),
                                                                                 before=discord.utils.escape_markdown(
                                                                                     before.content),
                                                                                 after=discord.utils.escape_markdown(
                                                                                     after.content)))
    else:
        await before.guild.get_channel(695630766477934632).send("Message by `{author}` edited in `{channel}` at `"
                                                                "{time}`".format(author=before.author,
                                                                                 channel=before.channel.name,
                                                                                 time=now.strftime("%I:%M:%S%p")))
        await before.guild.get_channel(695630766477934632).send(
            "**Before**\n> {before}".format(before=discord.utils.escape_markdown(before.content)))
        await before.guild.get_channel(695630766477934632).send(
            "**After**\n> {after}".format(after=discord.utils.escape_markdown(after.content)))


bot.run(bot_token)

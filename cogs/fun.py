import discord
import os
import random
import time
import asyncio
from discord.ext import commands
from discord.utils import get

class Fun (commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):

        author = ctx.message.author
        responses = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]

        _8ball = discord.Embed(
            title = ":8ball: MAGIC 8BALL",
            colour = discord.Colour.blue()
        )

        _8ball.add_field(name="Question:", value=f'{question}', inline=False)
        _8ball.add_field(name="Answer:", value=f'{random.choice(responses)}', inline=False)

        _8ball.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=_8ball)

    @commands.command(aliases=['di', 'roll'], pass_context=True)
    async def dice(self, ctx):

        author = ctx.message.author
        genNumber = random.randrange(0, 7, 1)

        dice_final = discord.Embed(
            title = ":game_die: DICE",
            colour = discord.Colour.blue()
        )

        dice_final.add_field(name="You rolled a...", value=f'{genNumber}', inline=False)

        dice_final.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=dice_final)

def setup(client):
    client.add_cog(Fun(client))

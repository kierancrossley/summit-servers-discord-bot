import discord
import os
import random
import time
import asyncio
from discord.ext import commands
from discord.utils import get

class Administration (commands.Cog):

    # Technical commands

    @commands.command(aliases=['m'], pass_context=True)
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager')
    async def maintainance(self, ctx):

        author = ctx.message.author
        channel = client.get_channel(status_channel_id)

        status = discord.Embed(
            title = f':tools: Bot is now down for maintainance.',
            colour = discord.Colour.red()
        )

        await ctx.message.delete()
        await channel.send(embed=status)
        print(f'[STATUS] {author} set bot to maintainance mode.')

        # Embed command

        @commands.command()
        @commands.has_permissions(manage_messages=True)
        async def embed(self, ctx, embed_content_color, *, embed_content):

            embed_content_title, embed_content_desc = embed_content.split('desc=')
            author = ctx.message.author

            new_val = embed_content_color.replace("#", "")
            colour = '0x' + new_val

            embed_msg = discord.Embed(
                title = f'{embed_content_title}',
                description = f'{embed_content_desc}',
                colour = discord.Colour(int(colour, base=16))
            )

            # embed_msg.add_field(name="", value=f'{embed}')

            await ctx.message.delete()
            await ctx.send(embed=embed_msg)
            print(f'[EMBED] {author} made an embed of {embed}')

        # Status command

        @commands.command()
        @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager')
        async def status(self, ctx, *, status="with the Summit community"):

            author = ctx.message.author
            status_message = f'{status}. | {global_prefix}help'

            status_update = discord.Embed(
                title = f':white_check_mark: Status set to {status}.',
                colour = discord.Colour.orange()
            )

            status_update.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)

            await ctx.message.delete()
            await ctx.send(embed=status_update, delete_after=10)
            await client.change_presence(activity=discord.Game(name=status_message))
            print(f'[STATUS] Status set to {status} by {author}.')

def setup(client):
    client.add_cog(Administration(client))

import discord
import os
import random
import time
import asyncio
from discord.ext import commands
from discord.utils import get

# In-file configuration

suggestion_channel_id = 658462177115504661
log_channel_id = 665652891725463583

class Moderation (commands.Cog):

    def __init__(self, client):
        self.client = client

    # Purge command

    @commands.command(aliases=['purge', 'delete'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        channel_name = ctx.channel.name
        amount = round(amount, 1)

        purge_success = discord.Embed(
            title = f':white_check_mark: Sucessfully purged {amount} messages.',
            colour = discord.Colour.green()
        )

        purge_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

        purge_log = discord.Embed(
            title = f':clipboard: MODERATION LOG',
            colour = discord.Colour.orange()
        )

        purge_log.add_field(name="Moderator action:", value="Purge", inline=True)
        purge_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
        purge_log.add_field(name="Purged messages:", value=f'{amount}', inline=True)
        purge_log.add_field(name="Purged channel:", value=f'#{channel_name}', inline=True)

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=purge_success, delete_after=5)
        await channel.send(embed=purge_log)
        print(f'[MODERATION] {author} purged {amount} message(s) in #{ctx.channel}.')

    @commands.command()
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager', '🛡️ Staff Manager', '👾 Discord Moderator')
    async def kick(self, ctx, member : discord.Member, *, reason="breaking the rules"):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        kick_success = discord.Embed(
            title = f':white_check_mark: Sucessfully kicked {member}.',
            description = f'{member} has been kicked by {author} for {reason}.',
            colour = discord.Colour.green()
        )

        kick_pm = discord.Embed(
            title = f':skull_crossbones: Whoops! You have been kicked!',
            description = f'You were kicked by {author} for {reason}.',
            colour = discord.Colour.red()
        )

        kick_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

        kick_log = discord.Embed(
            title = f':clipboard: MODERATION LOG',
            colour = discord.Colour.red()
        )

        kick_log.add_field(name="Moderator action:", value="Kick", inline=True)
        kick_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
        kick_log.add_field(name="Kicked user:", value=f'{member}', inline=True)
        kick_log.add_field(name="Kick reason:", value=f'{reason}', inline=True)

        await ctx.message.delete()
        await member.send(embed=kick_pm)
        await member.kick(reason=reason)
        await ctx.send(embed=kick_success, delete_after=15)
        await channel.send(embed=kick_log)
        print(f'[MODERATION] {author} kicked {member} for {reason}.')

    @commands.command()
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager', '🛡️ Staff Manager', '👾 Discord Moderator')
    async def mute(self, ctx, member : discord.Member, *, reason="breaking the rules"):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        mute_role = discord.utils.get(member.guild.roles, name='🚫 Muted')

        mute_success = discord.Embed(
            title = f':white_check_mark: Sucessfully muted {member}.',
            description = f'{member} has been muted by {author} for {reason}.',
            colour = discord.Colour.green()
        )

        mute_pm = discord.Embed(
            title = f':skull_crossbones: Whoops! You have been muted!',
            description = f'You were muted by {author} for {reason}.',
            colour = discord.Colour.red()
        )

        mute_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

        mute_log = discord.Embed(
            title = f':clipboard: MODERATION LOG',
            colour = discord.Colour.red()
        )

        mute_log.add_field(name="Moderator action:", value="Mute", inline=True)
        mute_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
        mute_log.add_field(name="Muted user:", value=f'{member}', inline=True)
        mute_log.add_field(name="Mute reason:", value=f'{reason}', inline=True)

        await ctx.message.delete()
        await member.send(embed=mute_pm)
        await member.add_roles(mute_role)
        await ctx.send(embed=mute_success, delete_after=15)
        await channel.send(embed=mute_log)
        print(f'[MODERATION] {author} muted {member} for {reason}.')

    @commands.command()
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager', '🛡️ Staff Manager', '👾 Discord Moderator')
    async def unmute(self, ctx, member : discord.Member):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        mute_role = discord.utils.get(member.guild.roles, name='🚫 Muted')

        unmute_success = discord.Embed(
            title = f':white_check_mark: Sucessfully unmuted {member}.',
            description = f'{member} has been unmuted by {author}.',
            colour = discord.Colour.green()
        )

        unmute_pm = discord.Embed(
            title = f':confetti_ball: Yay! You have been unmuted!',
            description = f'You were unmuted by {author}.',
            colour = discord.Colour.green()
        )

        unmute_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

        unmute_log = discord.Embed(
            title = f':clipboard: MODERATION LOG',
            colour = discord.Colour.green()
        )

        unmute_log.add_field(name="Moderator action:", value="Unmute", inline=True)
        unmute_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
        unmute_log.add_field(name="Unmuted user:", value=f'{member}', inline=True)

        await ctx.message.delete()
        await member.send(embed=unmute_pm)
        await member.remove_roles(mute_role)
        await ctx.send(embed=unmute_success, delete_after=15)
        await channel.send(embed=unmute_log)
        print(f'[MODERATION] {author} muted {member} for {reason}.')

    @commands.command()
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager', '🛡️ Staff Manager', '👾 Discord Moderator')
    async def ban(self, ctx, member : discord.Member, *, reason="breaking the rules"):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        ban_success = discord.Embed(
            title = f':white_check_mark: Sucessfully banned {member}.',
            description = f'{member} has been banned by {author} for {reason}.',
            colour = discord.Colour.green()
        )

        ban_pm = discord.Embed(
            title = f':skull_crossbones: Whoops! You have been banned!',
            description = f'You were banned by {author} for {reason}.',
            colour = discord.Colour.red()
        )

        ban_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

        ban_log = discord.Embed(
            title = f':clipboard: MODERATION LOG',
            colour = discord.Colour.red()
        )

        ban_log.add_field(name="Moderator action:", value="Ban", inline=True)
        ban_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
        ban_log.add_field(name="Banned user:", value=f'{member}', inline=True)
        ban_log.add_field(name="Ban reason:", value=f'{reason}', inline=True)

        await ctx.message.delete()
        await member.send(embed=ban_pm)
        await member.ban(reason=reason)
        await ctx.send(embed=ban_success, delete_after=15)
        await channel.send(embed=ban_log)
        print(f'[MODERATION] {author} banned {member} for {reason}.')

    @commands.command()
    @commands.has_any_role('root', '🏆 Community Owner', '🛡️ Community Manager', '🛡️ Staff Manager', '👾 Discord Moderator')
    async def unban(self, ctx, *, member):

        author = ctx.message.author
        channel = self.client.get_channel(log_channel_id)

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            unban_success = discord.Embed(
                title = f':white_check_mark: Sucessfully unbanned {member}.',
                description = f'{user.mention} has been unbanned by {author}.',
                colour = discord.Colour.green()
            )

            unban_success.set_footer(text=f'Moderated by {author}', icon_url=ctx.author.avatar_url)

            error_unbanning = discord.Embed(
                title = f':skull_crossbones: An error has occured.',
                description = f'I could not unban {user.mention}!',
                colour = discord.Colour.red()
            )

            unban_log = discord.Embed(
                title = f':clipboard: MODERATION LOG',
                colour = discord.Colour.red()
            )

            unban_log.add_field(name="Moderator action:", value="Unban", inline=True)
            unban_log.add_field(name="Moderated by:", value=f'{author}', inline=True)
            unban_log.add_field(name="Unbanned user:", value=f'{member}', inline=True)

            await ctx.message.delete()

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(embed=unban_success, delete_after=15)
                await channel.send(embed=unban_log)
                print(f'[MODERATION] {author} unbanned {member}.')

    @commands.command()
    @commands.has_role('👤 Member')
    async def suggest(self, ctx, *, suggestion):

        author = ctx.message.author
        channel = self.client.get_channel(suggestion_channel_id)

        yes_emoji = self.client.get_emoji("✔")
        no_emoji = self.client.get_emoji("❌")

        suggestion = discord.Embed(
            title = f':clipboard: SUGGESTION',
            description = f'{suggestion}',
            colour = discord.Colour.green()
        )

        suggestion.set_footer(text=f'Suggested by {author}', icon_url=ctx.author.avatar_url)

        await ctx.message.delete()
        suggestion_msg = await channel.send(embed=suggestion)
        await suggestion_msg.add_reaction("✔")
        await suggestion_msg.add_reaction("❌")
        print(f'[SUGGESTION] {author} made a suggestion.')

    @commands.command(aliases=['server', 'sinfo', 'si'], pass_context=True, invoke_without_command=True)
    async def serverinfo(self, ctx, *, msg=""):

        author = ctx.message.author

        if ctx.invoked_subcommand is None:
            if msg:
                server = None
                try:
                    float(msg)
                    server = self.bot.get_guild(int(msg))
                    if not server:
                        return await ctx.send(
                                              self.bot.bot_prefix + 'Server not found.')
                except:
                    for i in self.bot.guilds:
                        if i.name.lower() == msg.lower():
                            server = i
                            break
                    if not server:
                        return await ctx.send(self.bot.bot_prefix + 'Could not find server. Note: You must be a member of the server you are trying to search.')
            else:
                server = ctx.message.guild

            online = 0
            for i in server.members:
                if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    online += 1
            all_users = []
            for user in server.members:
                all_users.append('{}#{}'.format(user.name, user.discriminator))
            all_users.sort()
            all = '\n'.join(all_users)

            channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            role_count = len(server.roles)
            emoji_count = len(server.emojis)

            em = discord.Embed(
                title = ":gear: SERVER INFO",
                colour = discord.Colour.green()
            )

            em.add_field(name='Name', value=server.name)
            em.add_field(name='Owner', value=server.owner, inline=False)
            em.add_field(name='Members', value=server.member_count)
            em.add_field(name='Currently Online', value=online)
            em.add_field(name='Text Channels', value=str(channel_count))
            em.add_field(name='Number of roles', value=str(role_count))
            em.add_field(name='Number of emotes', value=str(emoji_count))
            em.add_field(name='Region', value=server.region)
            em.add_field(name='Verification Level', value=str(server.verification_level))
            em.add_field(name='ServerID', value=server.id, inline=False)
            em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
            em.set_thumbnail(url=server.icon_url)
            em.set_footer(text=f'Requested by {author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=em)
            print(f'[INFORMATION] {author} requested server information.')

def setup(client):
    client.add_cog(Moderation(client))

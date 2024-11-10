import discord
from discord.ext import commands

class Greetings(commands.Cog, description="Greeting Members"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Sup {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'You {member.name}~')
        else:
            await ctx.send(f'Sup {member.name}... This feels familiar.')
        self._last_member = member

async def setup(client):
    await client.add_cog(Greetings(client))

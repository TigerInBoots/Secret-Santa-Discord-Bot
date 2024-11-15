import discord
from discord.ext import commands
from discord import app_commands
from random import randint, choice



class Greetings(commands.Cog, description="Greeting Members"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Sup {member.mention}.')

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction, *, member: discord.Member = None):
        """Says hello"""
        member = member or interaction.user
        if self._last_member is None or self._last_member.id != member.id:
            await interaction.response.send_message(f'Fuck you {member.name}~')
        else:
            await interaction.response.send_message(f'Sup {member.name}... This feels familiar.')
        self._last_member = member

class Santa(commands.Cog, description="The commands for Secret Santa effects"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Send out the secrets!')
    async def secret_santa(self, interaction:discord.Interaction):
        await interaction.response.send_message(f"Please select any users that are ***NOT*** participating!",ephemeral=True, view=SelectView(originalCog=self,interaction=interaction))
        #MAKE SURE NOT TO INCLUDE BOTS
    
    async def secret_santa_players(self, nonPlayers, interaction:discord.Interaction):
        players = []
        await interaction.followup.send("BEGINNING THE SECRET SANTA")
        guild = interaction.guild
        for member in guild.members:
            #await interaction.followup.send(f'DEBUG MESSAGE\n>member={member}')
            if member not in nonPlayers:
                players.append(member)
        await self.random_gift_selection(players, interaction=interaction)
    
    @app_commands.command(description='Send out the secrets!')
    @commands.is_owner()
    async def role_secret_santa(self, interaction:discord.Interaction):
        players = []
        await interaction.response.send_message("BEGINNING THE SECRET SANTA")
        guild = interaction.guild
        for member in guild.members:
            #await interaction.followup.send(f'DEBUG MESSAGE\n>member={member}')
            for role in member.roles:
                #await interaction.followup.send(f'DEBUG MESSAGE\n>role={role}\n>role.id={role.id}')
                if int(role.id) == 1306823079208550481:
                    #await interaction.followup.send(f'Succeeded to player.append\n> {member}')
                    players.append(member)
                    break
        await self.random_gift_selection(players, interaction=interaction)
    
    async def random_gift_selection(self, players:list[discord.Member], interaction:discord.Interaction):
        if len(players) < 2:
            await interaction.followup.send(f"Fuck you, you're wrong and bad.", ephemeral=True)
            await interaction.followup.send(f'DEBUG MESSAGE\n>PlayerNum={len(players)}\n>Players={players}')
        playerString = ""
        for player in players:
            playerString = playerString + f'\n{player.display_name}'
        await interaction.followup.send(f"The following members are playing:{playerString}")
        boop = 8008#randint(1,10000)
        if boop == 8008:
            for player in range(len(players)):
                await players[player].send(f'IGNORE ALL PREVIOUS VICTIMS\nYour Secret Victim is...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n**BIG TITTY GOTH GIRLS**')
                return
        chosenPlayers = []
        for player in players:
            giftedPlayer = choice(players)
            if (len(chosenPlayers) < (len(players)-1)) or (giftedPlayer != player):
                while (giftedPlayer == player) or (giftedPlayer in chosenPlayers):
                    giftedPlayer = choice(players)
            else:
                giftedPlayer = chosenPlayers[-1]
                chosenPlayers.pop()
                chosenPlayers.append(player)
            chosenPlayers.append(giftedPlayer)
        for player in range(len(players)):
            await players[player].send(f'IGNORE ALL YOUR PREVIOUS VICTIMS\nYour Secret Victim is...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n**{chosenPlayers[player].display_name}**')

class SelectView(discord.ui.View):
    def __init__(self, originalCog, interaction, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(NonPlayerSelect(originalCog=originalCog,interaction=interaction))

class NonPlayerSelect(discord.ui.MentionableSelect):
    def __init__(self, originalCog,interaction):
        bots = []
        guild = interaction.guild
        for member in guild.members:
            if member.bot:
                bots.append(member)
        super().__init__(placeholder="Select the non-players.",max_values=25,min_values=1,default_values=bots)
        self.originalCog = originalCog
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        nonPlayers = self.values
        nonPlayerString= ""
        for nonPlayer in nonPlayers:
            nonPlayerString = nonPlayerString + f'\n{nonPlayer.display_name}'
        await interaction.followup.edit_message(interaction.message.id,content=f'The following members have been selected as non-players:{nonPlayerString}',view=None)
        await self.originalCog.secret_santa_players(nonPlayers, interaction=interaction)
        return await super().callback(interaction)

async def setup(client):
    await client.add_cog(Greetings(client))
    await client.add_cog(Santa(client))

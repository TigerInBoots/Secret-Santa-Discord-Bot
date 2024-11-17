import discord
from discord.ext import commands
from discord import app_commands
from random import randint, choice
from os import path

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
    @commands.is_owner()
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
    
    @app_commands.command(description='Remove a player from the active players.')
    @app_commands.describe(rem_player='Player to be removed!')
    @commands.is_owner()
    async def remove_player(self, interaction:discord.Interaction, rem_player:discord.Member):
        playersFile = open(f'{path.dirname(path.dirname(path.realpath(__file__)))}\\data\\currentPlayers.txt',"r")
        playersLine = playersFile.readline()
        players = (playersLine.split("!"))[0:-1:]
        memberGroups = [memberDuo.split(",") for memberDuo in list(players)]
        chosenPlayers = [discord.utils.get(interaction.guild.members, name=memberDuo[1]) for memberDuo in memberGroups]
        players = [discord.utils.get(interaction.guild.members, name=memberDuo[0]) for memberDuo in memberGroups]
        playersFile.close()
        if rem_player not in players:
            return await interaction.response.send_message("This member is not a current player.", ephemeral=True)
        for player in range(len(players)):
            if chosenPlayers[player] == rem_player:
                savedPlayer = [players[player],player]
            if players[player] == rem_player:
                savedChosenPlayer = chosenPlayers[player]
                players.pop(player)
                chosenPlayers.pop(player)
        if savedPlayer[0] != savedChosenPlayer:
            chosenPlayers[savedPlayer[1]] = savedChosenPlayer
            await savedPlayer[0].send(f"YOU HAVE BEEN REASSIGNED. YOUR NEW VICTIM IS {savedChosenPlayer.display_name}.\n\nPLEASE CONSULT {rem_player.display_name}, AS THEY MAY ALREADY HAVE GIFT IDEAS.")
        else:
            if len(players) == 1:
                return await self.end_session(interaction=interaction)
            chosenPlayers[savedPlayer[1]] = chosenPlayers[-1]
            chosenPlayers[-1] = savedChosenPlayer
            await savedPlayer[0].send(f"YOU HAVE BEEN REASSIGNED. YOUR NEW VICTIM IS {chosenPlayers[savedPlayer[1]].display_name}.\n\nPLEASE CONSULT {players[-1].display_name}, AS THEY MAY ALREADY HAVE GIFT IDEAS.")
            await players[-1].send(f"YOU HAVE BEEN REASSIGNED. YOUR NEW VICTIM IS {savedChosenPlayer.display_name}.\n\nPLEASE CONSULT {rem_player.display_name}, AS THEY MAY ALREADY HAVE GIFT IDEAS.")
        combinedPlayers = ''
        for player in range(len(players)):
            combinedPlayers = combinedPlayers + f'{players[player].name},{chosenPlayers[player].name}!'
        playersFile = open(f'{path.dirname(path.dirname(path.realpath(__file__)))}\\data\\currentPlayers.txt',"w")
        playersFile.write(combinedPlayers)
        playersFile.close()
        return await interaction.response.send_message(f'{rem_player.mention} was removed from play!\n{rem_player.display_avatar}')

    
    @app_commands.command(description='End Secret Santa session.')
    @commands.is_owner()
    async def end_session(self, interaction:discord.Interaction):
        playersFile = open(f'{path.dirname(path.dirname(path.realpath(__file__)))}\\data\\currentPlayers.txt',"w")
        playersFile.close()
        await interaction.response.send_message("The Secret Santa has ended.")

    async def random_gift_selection(self, players:list[discord.Member], interaction:discord.Interaction):
        if len(players) < 2:
            await interaction.followup.send(f"Fuck you, you're wrong and bad.", ephemeral=True)
        playerString = ""
        for player in players:
            playerString = playerString + f'\n> {player.mention}'
        await interaction.followup.send(f"The following members are playing:{playerString}")
        boop = randint(1,10000)
        if boop == 8008:
            playersFile = open(f'{path.dirname(path.dirname(path.realpath(__file__)))}\\data\\currentPlayers.txt',"w")
            combinedPlayers = ''
            for player in range(len(players)):
                combinedPlayers = combinedPlayers + f'{players[player].name},BIG TITTY GOTH GIRLS!' 
            playersFile.write(combinedPlayers)
            playersFile.close()
            for player in range(len(players)):
                await players[player].send(f'IGNORE ALL PREVIOUS VICTIMS\nYour Secret Victim is...\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n**BIG TITTY GOTH GIRLS**')
            return
        chosenPlayers = []
        if len(players) == 2:
            chosenPlayers.append(players[1])
            chosenPlayers.append(players[0])
        else:
            for player in players:
                giftedPlayer = choice(players)
                if (len(chosenPlayers) < (len(players)-1)) or (giftedPlayer != player) or (giftedPlayer not in chosenPlayers):
                    while (giftedPlayer == player) or (giftedPlayer in chosenPlayers):
                        giftedPlayer = choice(players)
                else:
                    if chosenPlayers[-1] == player:
                        giftedPlayer = chosenPlayers[-2]
                        gifted2Player = chosenPlayers[-1]
                        chosenPlayers.pop()
                        chosenPlayers.pop()
                        chosenPlayers.append(player)
                        chosenPlayers.append(gifted2Player)
                    else:
                        giftedPlayer = chosenPlayers[-1]
                        chosenPlayers.pop()
                        chosenPlayers.append(player)
                chosenPlayers.append(giftedPlayer)

        playersFile = open(f'{path.dirname(path.dirname(path.realpath(__file__)))}\\data\\currentPlayers.txt',"w")
        combinedPlayers = ''
        for player in range(len(players)):
            combinedPlayers = combinedPlayers + f'{players[player].name},{chosenPlayers[player].name}!' 
        playersFile.write(combinedPlayers)
        playersFile.close()
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

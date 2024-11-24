# The Secret Santa Discord Bot
## Current Commands:
### Greetings:
#### on_member_join (listener)
When a new member joins the guild, messages the system channel with "Sup, @{member.name}".
#### hello
Slash command to send a member (default is yourself) the message "Fuck you {member.name}~". 
If the command is used on the same member more than once, in a row, sends "Sup {member.name}... This feels familiar." instead.
### Secret Santa:
These commands are for the purpose of determining the players of a Secret Santa, within a server.
#### secret_santa
Slash command that does the following:
- Sends the commander a list of the users in the guild (with the bots pre-selected) which only the commander can see, for the commander to choose who will not participate.
- Once members are selected and the commander has clicked off the list, the list dissapears. It is replaced by a text with the users that were selected.
- Sends a message to the channel that says "BEGINNING THE SECRET SANTA".
- Collects all members that were **not** selected in the list, and makes them players.
- The slash command then calls the asynchronous function random_gift_selection, which randomly assigns the players to eachother and DMs each player.
#### role_secret_santa
Slash command that does the following:
- Sends a message to the channel that says "BEGINNING THE SECRET SANTA".
- Collects all members that have a selected role to be the players.
- The slash command then calls the asynchronous function random_gift_selection, which randomly assigns the players to eachother and DMs each player.

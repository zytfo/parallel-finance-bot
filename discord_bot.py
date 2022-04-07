import discord.ext.commands as commands
from discord_components import DiscordComponents, Button

import config
from tracker import get_message

TOKEN = config.DISCORD_TOKEN
GUILD = config.DISCORD_GUILD

client = commands.Bot(command_prefix="!")
DiscordComponents(client)


@client.command()
async def prices(ctx):
    message = get_message(is_telegram=False)
    sent_message = await ctx.send(message, components=[
        [Button(label="Update", style=2, emoji="🔄", custom_id="refresh")]
    ])
    while True:
        try:
            interaction = await client.wait_for("button_click", check=lambda i: i.custom_id == "refresh")
            await sent_message.edit(get_message(is_telegram=False))
            await interaction.respond()
        except:
            pass


client.run(TOKEN)

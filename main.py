import json
import random
import discord
import requests
from discord import *
from hold import *
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive, TOKEN, ID

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



def load_epic_data():
    try:
        with open("epic.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_epic_data(epic_data):
    with open("epic.json", "w") as file:
        json.dump(epic_data, file)
epic = load_epic_data()


class abot(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=ID))
        self.synced = True
        print('The bot is online.')


bot = abot()
tree = app_commands.CommandTree(bot)






@tree.command(name='bot-starter', description='Sends the website for the bot to start it', guild=discord.Object(id=ID))
async def commands_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Bot Starter',
        description='''If I'm down go [here](https://im-not-a-bot.killerqueencode.repl.co)''',
        color=0x3498db)
    
    await interaction.response.send_message(embed=embed)




@tree.command(name='invite', description='Sends an invite', guild=discord.Object(id=ID))
async def invite_command(interaction: discord.Interaction):
    invite_embed = discord.Embed(
        title="Server Invite",
        description="Here's the invite link to the server [Invite Link](https://discord.gg/WxdX99HjJY)",
        color=0x3498db)

    invite_embed.set_footer(text="https://discord.gg/WxdX99HjJY")

    await interaction.response.send_message(embed=invite_embed)


@tree.command(name='flip', description='This will flip a coin', guild=discord.Object(id=ID))
async def flip_command(interaction: discord.Interaction):
    coin_sides = ['Heads', 'Tails']
    result = random.choice(coin_sides)
    await interaction.response.send_message(f"The coin landed on **{result}**!")


@tree.command(name='ping', description='Check bot response time', guild=discord.Object(id=ID))
async def ping_command(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! Bot latency is {latency}ms.", ephemeral=True)


@tree.command(name='roll', description='Roll a dice', guild=discord.Object(id=ID))
async def roll_command(interaction: discord.Interaction):
    dice_result = random.randint(1, 6)
    await interaction.response.send_message(f"You rolled a {dice_result}!")


@tree.command(name='epic', description='Sends your epic', guild=discord.Object(id=ID))
async def epic_command(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    epic = load_epic_data()
    if user_id in epic:
        epic_name = epic[user_id]["name"]
        user_mention = interaction.user.mention
        user_profile_pic_url = interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url

        embed = discord.Embed(
            title='Epic',
            description=f'```{epic_name}```',
            color=0x3498db)
        
        embed.set_thumbnail(url=user_profile_pic_url)

        await interaction.response.send_message(user_mention, embed=embed)


@tree.command(name='ping_bot', description='Ping the Fortnite bots', guild=discord.Object(id=ID))
async def ping_bots_command(interaction: discord.Interaction):
    website = "https://reverse-taxi.killerqueencode.repl.co"

    await interaction.response.send_message(':arrows_clockwise: Pinging reverse taxi...', ephemeral=True)

    try:
        response = requests.get(website)
        response.raise_for_status()

        await interaction.edit_original_response(content=":white_check_mark: Reverse taxi is online.")
    except requests.RequestException as e:

        await interaction.edit_original_response(content=":warning: Reverse taxi is offline. Pinging the website...")


        for _ in range(3):
            try:
                response = requests.get(website)
                response.raise_for_status()
                await interaction.edit_original_response(content=":white_check_mark: Reverse taxi is online.")
                break 
            except requests.RequestException:
                continue 
        else:
            await interaction.edit_original_response(content=":x: Website is still offline after multiple pings.")


#roles


@tree.command(name='epic-role', description='Links your epic with discord', guild=discord.Object(id=ID))
async def link_epic_command(interaction: discord.Interaction, name: str):
    if isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message('This command cannot be used in a thread.', ephemeral=True)
        return

    user = interaction.user
    epic_role = discord.utils.get(interaction.guild.roles, name='epic')

    if epic_role:
        if epic_role in user.roles:
            await interaction.response.send_message(f'you already have the {epic_role.mention} role, but I updated your epic.', ephemeral=True)
        else:
            await user.add_roles(epic_role)
            await interaction.response.send_message(f'you now have the {epic_role.mention} role!', ephemeral=True)

    epic[str(interaction.user.id)] = {"name": name, "user": str(interaction.user)}
    save_epic_data(epic)



@tree.command(name='endgame-role', description='Get the endgame role', guild=discord.Object(id=ID))
async def endgame_role_command(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message('This command cannot be used in a thread.', ephemeral=True)
        return

    existing_threads = [thread for thread in interaction.guild.threads if thread.name.startswith(f"Endgame Role - {interaction.user.display_name}")]
    moderation_role = discord.utils.get(interaction.guild.roles, name='moderation')
    endgame_role = discord.utils.get(interaction.guild.roles, name='endgame')
    user = interaction.user
    user_id = str(interaction.user.id)
    epic = load_epic_data()
    epic_name = epic[user_id]["name"]

    if endgame_role:
        if endgame_role in user.roles:
            await interaction.response.send_message(f'you already have the {endgame_role.mention} role!', ephemeral=True)
        elif existing_threads:
            await interaction.response.send_message(f'you already have an open thread for the Endgame Role request!', ephemeral=True)
        else:
            thread_name = f"Endgame Role - {user.display_name}"
            thread = await interaction.channel.create_thread(name=thread_name, auto_archive_duration=60)

            await thread.add_user(user)


            embed = discord.Embed(
                title='Endgame role',
                description=f'epic = ```{epic_name}```\n\n{user.mention}, send proof of power level in this thread',
                color=0x3498db)
            
            embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRuBwP5M_TZEO1CM7TfT9aVFKGeeWQI6vaeA&usqp=CAU')

            await thread.send(moderation_role.mention, embed=embed)
            await interaction.response.send_message(f'a thread has been created for you. Please check it.', ephemeral=True)


@tree.command(name='roles', description='Menu for roles', guild=discord.Object(id=ID))
async def roles_command(interaction: discord.Interaction):

    embed = discord.Embed(
        title='roles',
        description='</epic-role:1155376018085908618>\n</endgame-role:1155376018085908620>',
        color=0x3498db)

    await interaction.response.send_message(embed=embed)


#test


@tree.command(name='test_command', description='test command', guild=discord.Object(id=ID))
async def test_command(interaction: discord.Interaction):


    general_button = Button(label='General Rules')
    Privacy_button = Button(label='Privacy Rules')
    stw_button = Button(label='Save The World Rules')
    

    async def general_button_callback(interaction):
        await interaction.response.send_message(embed=general_rules, ephemeral=True)

    async def Privacy_button_callback(interaction):
        await interaction.response.send_message(embed=Privacy_rules, ephemeral=True)

    async def stw_button_callback(interaction):
        await interaction.response.send_message(embed=stw_rules, ephemeral=True)


    general_button.callback = general_button_callback
    Privacy_button.callback = Privacy_button_callback
    stw_button.callback = stw_button_callback
    

    view = View()
    view.add_item(general_button)
    view.add_item(Privacy_button)
    view.add_item(stw_button)

    await interaction.response.send_message(embed=server_rules, view=view)





#polls
@bot.event
async def on_message(message):
    channel = str(message.channel)

    if channel == "🗽polls":
        await message.add_reaction('👍')
        await message.add_reaction('👎')


    

keep_alive()
bot.run(TOKEN)

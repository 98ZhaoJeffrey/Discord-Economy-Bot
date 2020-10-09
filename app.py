import discord
from discord.ext import commands
from datetime import datetime, timedelta
from time import sleep

startup_extensions = ['cogs.gambling', 'cogs.accounts', 'cogs.market']
#dictionary to relate users to their money

client = commands.Bot(command_prefix = '$')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
            print(f'{extension} has been loaded')
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.remove_command('help')

@client.event
async def on_ready():
    #changes the game the bot is playing and declears that the bot is online
    await client.change_presence(activity=discord.Game("Use $help to get started | The New York Stock Exchange"))
    print("Bot is ready")

@client.command()
async def online(ctx):
    #sends in the discord that the bot is online
    await ctx.send('We have logged in as {0.user}'.format(client))

'''
#help menu
@client.command()
async def help(ctx):
'''
#testing commands
"""
@client.command()
async def getUser(ctx, reciever: discord.Member):
    if(reciever in userMoney):
        await ctx.send('{}'.format(reciever.mention))
"""

@client.command()
async def getDict(ctx):
    user = ctx.message.author
    await ctx.send(str(user))

@client.command()
async def getUser(ctx, member : discord.Member):
     user = ctx.message.author
     await ctx.send(f'{member.mention}: name is {type(member)} or {member}')
     await ctx.send(f'{user.mention}: name is {type(user)} or {user}')


@client.command()
async def editEmbed(ctx):
    m = discord.Embed(
        title = "Crash",
        description = """The multiplier will contiously rise which is how much you will get in return unless it crashs before you stop it""",
        colour = discord.Colour.blue()
    )
    M = discord.Embed(
        title = "Crashed",
        
        colour = discord.Colour.blue()
    )
    
    message = await ctx.send(embed=m)
    sleep(2)
    await message.edit(embed=M)

client.run(discord bot key)

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


@client.command()
async def help(ctx):
    user = ctx.message.author
    await ctx.send(embed=discord.Embed(
        title = "Help menu",
        description = "() = optional\n [] = required\n\n" + 
            "====== Account Commands ======\n\n" +
            "`register`\n Use this to register yourself in the database\n" +
            "`balance (other user)`\n Get the balance of your account or include the name of the person's account you want to see\n" +
            "`transfer [amount:integer][other user]`\n Transfer some amount of money to another user\n" +
            "`daily`\n Use this command once every 24 hours to get a small bonus\n\n" +
            "====== Market Commands ======\n\n" + 
            "`sell [name of item][price per unit: integer][quantity: integer]`\n Put an item that you want to sell on the market\n" +
            "`buy [id of the item][quantity: integer]`\n Buy an item from another user\n" +
            "`remove [id of the item]` Remove the item that you own from the market\n" +
            "`market (keyword of item)`\n Returns a list of items owned by you or returns all items with the keyword\n\n" +
            "====== Gambling Commands ======\n\n" +
            "`slots (bet:integer)`\n Gives a description of the game. Give it a bet to actually play slots\n" +
            "`roulette (bet:integer) (betType: what you want to bet on)`\n Gives a description of the game. Give it a bet and bet type (color or number) to actually play roulette\n" +
            "`flip (bet:integer)`\n Gives a description of the game. Give it a bet to play coinflip\n" +
            "`crash (bet:integer) (limit: integer)`\n Gives a description of the game. Give it a bet and a limit(between 1 and 30) to bail before the crash\n",
        color=0xff6f00,
    ))



client.run(Your key goes here)


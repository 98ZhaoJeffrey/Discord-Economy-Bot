import discord
from discord.ext import commands
from random import random, randint
from time import sleep

slots = {
        "diamond": "💎",
        "bag": "💰",
        "redHeart": "🧡",
        "greenHeart": "💚"
        } 
        
flips = {
        "redCircle": "🔴", 
        "blueCircle": "🔵" 
        }
Emoji = {
        "yes":"🇾",
        "no":"🇳",
        "dice":"🎲",
        "stop":"🛑"
        }

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slots(self, ctx, bet: int = None):
        user = ctx.message.author
        if(bet == None):
                message = discord.Embed(
                title = "Crash",
                description = """Bet some money and hope that the slots machine spits out a winner""",
                colour = discord.Colour.yellow()
                )
        else:
            outcome = []
            for i in range(2):
                outcome[i] = random.choice(slots)
            #conditions for winning

    @commands.command()
    async def crash(self, ctx, bet: int = None):
        user = ctx.message.author
        multiplier = randint(10,300)
        if(bet == None):
            message = discord.Embed(
                title = "Crash",
                description = "The multiplier will contiously rise which is how much you will get in return unless it crashs before you stop it",
                colour = discord.Colour.blue(),
                thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish'
                )
            ctx.send(embed=message)
        else:
            increment = 0
            message = discord.Embed(
                title = "Crash",
                description = f'Current multiplier | {increment}',
                colour = discord.Colour.blue(),
                thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish'
                )
            m = ctx.send(embed=message)
            while(increment < multiplier):
                sleep(0.1)
                await m.ctx.edit(embed = discord.Embed(
                    title = "Crash",
                    description = f'Current multiplier | {increment}',
                    colour = discord.Colour.blue(),
                    thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish')
                )
                increment += 0.1
            await m.ctx.edit(embed = discord.Embed(
                title = "Crash",
                description = f'Current multiplier | CRASHED',
                colour = discord.Colour.blue(),
                thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish')
            )
            #make the embed message have the multiplier change going up
            #once it reaches the multiplier, it crashes

    @commands.command
    async def roulette(self, ctx, bet: int = None, betType: str = None):
        user = ctx.message.author
        multiplier = 0
        message = discord.Embed(
            title = "Roulette",
            description = "Pick a number or a color and hope that it matches your bet. All even numbers are red except for 0 and all odd numbers are black except for 37. 0 and 37 are green",
            colour = discord.Colour.green(),
            thumbnail="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_10454910_computer-generated-roulette-wheel-with-numbers-and-colours.html&psig=AOvVaw3Pl7aOXMB-NQO1m8lx-0VY&ust=1599186106026000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIjlqdD2y-sCFQAAAAAdAAAAABAn"
        )
        if(betType or bet == None):
            await ctx.send(message)
        else:
            Message = discord.Embed(
                title = "Roulette",
                description = "Rolling the roulette wheel...",
                colour = discord.Colour.green(),
                thumbnail="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_10454910_computer-generated-roulette-wheel-with-numbers-and-colours.html&psig=AOvVaw3Pl7aOXMB-NQO1m8lx-0VY&ust=1599186106026000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIjlqdD2y-sCFQAAAAAdAAAAABAn"
            )
            number = random.randint(0,37)
            #bets (red, black, green, number)(38 numbers)
            m = await ctx.send(message)
            sleep(1)
            try:
                betType = int(betType)
                if(betType == number):              
                    multiplier = 38
            except TypeError:
                if(number == 0 or number == 37 and betType.lower() == 'green'):
                    multiplier = 19
                elif (number % 2 == 0 and number != 0 and betType.lower() == 'red') or (number % 2 == 1 and number != 37 and betType.lower() == 'black'):
                    multiplier = 2
                
            if(multiplier == 0):
                description = "Sorry but you lost this time. Better luck next time!"
            else:
                description = f'Congrulations you won {bet*multiplier}! Please come again!'
            m.edit(embed=discord.Embed(
                title = f"Roulette results|{user}",
                description = description,
                colour = discord.Colour.green(),
                thumbnail="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_10454910_computer-generated-roulette-wheel-with-numbers-and-colours.html&psig=AOvVaw3Pl7aOXMB-NQO1m8lx-0VY&ust=1599186106026000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCIjlqdD2y-sCFQAAAAAdAAAAABAn")
            )

    @commands.command
    async def roller(self, ctx, bet: int):
        user = ctx.message.author
        message = discord.Embed(
            title = "High Rollers",
            description = "Roll a dice and climb that many steps. You can either roll one or two die. If you roll higher than the bot you win but you lose if you don't. Also try to not go over 7 If you get exactly 7 you win tenfold.",
            colour = discord.Colour.red()
        )
        message.set_thumbnail(url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fgilkalai.wordpress.com%2F2017%2F09%2F07%2Ftyi-30-expected-number-of-dice-throws%2F&psig=AOvVaw3s4nOmPi2bGVeA266lP17i&ust=1599270107465000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMDQ3cmvzusCFQAAAAAdAAAAABAD")
        rolls = []
        botRolls = []

        #roll again conditions: lower than user roll, if roll is less than 4
        if (botRolls[0] < rolls[0] or botRolls[0] < 4):
            botRolls[1] = random.randint(1,6) 
        #don't roll again condition: roller 4 or higher and roll higher than user
        if(botRolls[0] >= 4 and botRolls[0] > rolls[0]):
            print('stop')
        #ask if they want to roll the die again
        #lose if your rolls is over 7
        if(rolls[0]+rolls[1] > 7):
            print('lose')
        #bot is higher than you but didn't go over
        if(rolls[0]+rolls[1] < botRolls[0] + botRolls[1] and botRolls[0]+botRolls[1] < 7):
            print('lose')
        #roll is the same or higher than the bot
        if(rolls[0]+rolls[1] >= botRolls[0] + botRolls[1] and rolls[0]+rolls[1] < 7):
            print('win')

        #your roll is exactly 7
        if(rolls[0]+rolls[1] == 7):
            print('win')

        #coinflip
        @commands.command()
        async def flip(self, ctx, bet: int = None):
            user = ctx.message.author
            multiplier = 1
            embed = discord.Embed(
                title = "Coin flip",
                description = """Pick either the red or blue circle and hope that the coin lands on your side. Winning yields double your bet but losing loses everything. After every consectutive win, you can either continue and double your current wins or just keep your current winnings.""",
                colour = discord.Colour.blue(),
                thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish'
                )
            
            flip = (randint(0,1))
            message = await ctx.send(embed=embed)

            message.edit(embed= discord.Embed(
                title = "Coin flip",
                description = f"Flip result: {random.choice(slots)}",
                colour = discord.Colour.blue(),
                thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish')
                )
def setup(bot):
    bot.add_cog(Gamble(bot))                

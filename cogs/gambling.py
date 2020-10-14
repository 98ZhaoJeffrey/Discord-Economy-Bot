from random import randint
import discord
from discord.ext import commands
import random 
from random import randint
from time import sleep
import traceback
import sys
sys.path.append(sys.path[0] + "/..")
from databridge import userBridge

userbridge = userBridge()

slots = {
        "diamond": "💎",
        "bag": "💰",
        "red": "🧡",
        "green":"💚"
        } 
        
coin = [
        "🔴", 
        "🔵" 
        ]
question = "❓"

class User():
    def __init__(self, game):
        self.game = game

class Crash():
    def __init__(self, user, bet):
        self.user = user
        self.bet = bet
        self.multiplier = randint(10,300)
        self.increment = 0
        self.run = True
    def run(self):
        self.increment +=0.1
        sleep(0.1)
    def stop(self):
        if(self.run != True):
            self.run = False

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slots(self, ctx, bet: int = None):
        user = ctx.message.author
        if(bet == None):
            await ctx.send(embed=discord.Embed(
                title = f"Slots | User: {user}",
                description = "Bet some money and hope that the slots machine spits out a winner",
                color=0xfbff05
                ))
        else:
            try:
                dbUser = userbridge.Get(str(user)).to_dict()
                dbUser['balance'] -= bet
                message = await ctx.send(embed=discord.Embed(
                    title = f"Slots | User: {user}",
                    description = "Slots spinning...\n|" + (f" {question} ")*3 + "|",
                    color=0xfbff05
                    ))
                outcome = [question]*3
                for i in range(3):
                    outcome[i] = slots[random.choice(list(slots))]
                    if i == 2:
                        outcomeString = ''
                        multiplier = 0
                        if ((outcome[0] == outcome[1]) and outcome[1] == outcome[2]):
                            outcomeString = f'You won '
                            if outcome[0] == slots['diamond']:
                                multiplier = 50
                            elif outcome[0] == slots['bag']:
                                multiplier = 20
                            elif outcome[0] == slots['red']:
                                multiplier = 10
                            else:
                                multiplier = 5
                            outcomeString += f"{multiplier*bet} credits"
                        else:
                            outcomeString = "You lost this time, try again later!"
                        await message.edit(embed=discord.Embed(
                            title = f"Slots | User: {user}",
                            description = f"Slots spun\n| {outcome[0]} {outcome[1]} {outcome[2]} |\n" + outcomeString,
                            color=0xfbff05
                        ))
                        dbUser['balance'] += multiplier*bet
                    else: 
                        await message.edit(embed=discord.Embed(
                            title = f"Slots | User: {user}",
                            description = f"Slots spinning...\n| {outcome[0]} {outcome[1]} {outcome[2]} |",
                            color=0xfbff05
                        ))
                    sleep(0.5)
                userbridge.Update(dbUser)
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()

    @commands.command()
    async def roulette(self, ctx, bet: int = None, betType = None):
        user = ctx.message.author
        if(betType == None or bet == None):
            await ctx.send(embed=discord.Embed(
                title = "Roulette",
                description = "Pick a number or a color and hope that it matches your bet. All even numbers are red except for 0 and all odd numbers are black except for 37. 0 and 37 are green",
                colour = 0x05ff2f
            ))
        else:
            try:
                dbUser = userbridge.Get(str(user)).to_dict()
                dbUser['balance'] -= bet
                message = await ctx.send(embed=discord.Embed(
                    title = "Roulette",
                    description = "Rolling the roulette wheel...",
                    colour = 0x05ff2f
                ))
                number = random.randint(0,37)
                sleep(1)
                multiplier = 0
                try:
                    betType = int(betType)
                    if(betType == number):              
                        multiplier = 38
                except:
                    if(number == 0 or number == 37 and betType.lower() == 'green'):
                        multiplier = 19
                    elif (number % 2 == 0 and number != 0 and betType.lower() == 'red') or (number % 2 == 1 and number != 37 and betType.lower() == 'black'):
                        multiplier = 2
                    
                if(multiplier == 0):
                    description = f'Result: {number}. Sorry but you lost this time. Better luck next time!'
                else:
                    description = f'Result: {number}. Congrulations you won {bet*multiplier} credits! Please come again!'
                    dbUser['balance'] += bet*multiplier
                await message.edit(embed=discord.Embed(
                    title = f"Roulette results|{user}",
                    description = description,
                    colour = 0x05ff2f
                ))
                userbridge.Update(dbUser)
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()
    @commands.command()
    async def flip(self, ctx, bet: int = None):
        user = ctx.message.author
        
        if bet == None:
            await ctx.send(embed=discord.Embed(
                title = "Coin flip",
                description = "Pick either the red or blue circle and hope that the coin lands on your side. It's double or nothing",
                colour = 0x8000ff
                ))
        else:
            try:
                dbUser = userbridge.Get(str(user)).to_dict()
                dbUser['balance'] -= bet
                flip = (randint(0,1))
                outcomeString = ''
                if flip == 0:
                    outcomeString += "Sorry but you lost this time."
                else:
                    outcomeString += "You just doubled your wage!"
                    dbUser['balance'] += 2*bet
                await ctx.send(embed=discord.Embed(
                    title = f"Coin flip|{user}",
                    description = f"Flip result: {coin[flip]} " + outcomeString,
                    colour = 0x8000ff
                    ))
                userbridge.Update(dbUser)
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()
    @commands.command()
    async def crash(self, ctx, bet: int = None, limit: int = None):
        user = ctx.message.author
        if(bet == None or limit == None):
            await ctx.send(embed=discord.Embed(
                title = "Crash",
                description = "The multiplier will contiously rise which is how much you will get in return unless it crashs before you stop it. Max multipler is 30",
                colour = 0x05b4ff
                ))
        else:
            try:
                dbUser = userbridge.Get(str(user)).to_dict()
                dbUser['balance'] -= bet
                message = await ctx.send(embed=discord.Embed(
                        title = f"Crash|{user}",
                        description = "Starting crash...",
                        colour = 0x05b4ff
                    ))
                crasher = random.randint(1,30)
                iterator = 0
                sleep(1)
                while(True):
                    iterator += 1
                    sleep(0.75)
                    await message.edit(embed=discord.Embed(
                        title = f"Crash|{user}",
                        description = f"Multiplier: {iterator}",
                        colour = 0x05b4ff
                    ))
                    if (iterator == limit):
                        await message.edit(embed=discord.Embed(
                                title = f"Crash|{user}",
                                description = f"Congrats, you've won {bet*limit} credits. It was supposed to crash at {crasher}. Please come again!",
                                colour = 0x05b4ff
                            ))
                        dbUser['balance'] += bet*limit
                        break
                    elif (iterator > crasher):
                        await message.edit(embed=discord.Embed(
                                title = f"Crash|{user}",
                                description = f"Sorry, but the crasher crashed at {crasher} this time",
                                colour = 0x05b4ff
                            ))
                        break
                userbridge.Update(dbUser)
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()

def setup(bot):
    bot.add_cog(Gamble(bot))                

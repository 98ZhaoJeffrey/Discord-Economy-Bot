import discord
from discord.ext import commands
from datetime import datetime, timedelta
from random import random, randint, uniform
from time import sleep
import traceback
import sys
sys.path.append(sys.path[0] + "/..")
from databridge import *

userbridge = userBridge()
itembridge = itemBridge()

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Buying and Selling Functions
    @commands.command()
    async def sell(self, ctx, name, price : int, quantity: int):
        user = ctx.message.author
        #item that they want to sell
        item = {'name': name, 'quantity' : quantity, 'price': price, 'owner': str(user)}
        try:
            itembridge.Add(item)
            await ctx.send(f'Your item: {name} is now on the market')
        except:
            await ctx.send(f'Your item: {name} could not be added')
            traceback.print_exc()
        
    @commands.command()
    async def buy(self, ctx, id: int, quantity: int):
        user = ctx.message.author
        try:
            dbUser = userbridge.Get(str(user)).to_dict()
            dbItem = itembridge.GetByID(id).to_dict()
            dbReciever = userbridge.Get(dbItem['owner']).to_dict()
            if(dbItem['quantity'] < quantity):
                await ctx.send(f'There are/is only {dbItem["quantity"]} avaliable')
            else:
                if(dbUser['balance'] < dbItem['price']*quantity):
                    await ctx.send(f"You don't have enough credits to buy. Come back with {dbItem['price']*quantity - dbUser['balance']} more credits")
                else:
                    dbUser['balance'] -= dbItem['price']*quantity
                    dbReciever['balance'] += dbItem['price']*quantity
                    dbItem['quantity'] -= quantity
                    userbridge.Update(dbUser)
                    userbridge.Update(dbReciever)
                    itembridge.Update(dbItem)
                    await ctx.send(f"Successful bought {dbItem['name']} from {dbItem['owner']}")
        except AttributeError:
            await ctx.send('This item does not exist')
        except:
            await ctx.send('There was an error')
            traceback.print_exc()

    @commands.command()
    async def remove(self, ctx, id: int):
        user = ctx.message.author
        try:
            dbItem = itembridge.GetByID(id).to_dict()
            dbItem['quantity'] = 0
            itembridge.Update(dbItem)
            await ctx.send(f'Your item {dbItem["name"]} has been removed from the market')
        except:
            await ctx.send('There was an error')
            traceback.print_exc()
    @commands.command()
    #returns the items the user is selling or queries for the items that contains the keyword
    async def market(self, ctx, name = None):
        user = ctx.message.author
        if(name == None):
            try:
                dbItem = itembridge.GetByUser(str(user))
                embedString = ''
                for item in dbItem:
                    embedString += f'iid: {item.iid} | Name: {item.name} | Quantity : {item.quantity} | Price: {item.price}\n'
                message = discord.Embed(
                    title = f"Items sold by {user}",
                    description = embedString,
                    color=0xdd12f8,
                    thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish'
                )
                await ctx.send(embed=message)
            except:
                 await ctx.send('There was an error')
                 traceback.print_exc()
        else:
            try:
                dbItem = itembridge.GetByItemName(name)
                embedString = ''
                for item in dbItem:
                    item = item.to_dict()
                    embedString += f"iid: {item['iid']} | Name: {item['name']} | Quantity : {item['quantity']} | Price: {item['price']} | Owner: {item['owner']}\n"
                message = discord.Embed(
                    title = f"Items sold with keyword: {name}",
                    description = embedString,
                    color=0xdd12f8,
                    thumbnail='https://mma.prnewswire.com/media/1096637/Royal_Canadian_Mint_The_Royal_Canadian_Mint_Launches_its_Largest.jpg?p=publish'
                )
                await ctx.send(embed=message)
            except:
                 await ctx.send('There was an error')
                 traceback.print_exc()

def setup(bot):
    bot.add_cog(Market(bot))     


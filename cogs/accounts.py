import traceback
from datetime import timedelta
import discord
from discord.ext import commands
from datetime import datetime

import sys
sys.path.append(sys.path[0] + "/..")
from databridge import *

userbridge = userBridge()
itembridge = itemBridge()


class Accounts(commands.Cog):

    @commands.command(aliases = ['reg'])
    #register
    async def register(self, ctx):
        user = ctx.message.author
        try:
            dbUser = userbridge.Get(str(user))
            if(dbUser != None):
                await ctx.send(f"{user.mention} is already registered")
            else:
                userDict = {'username': str(user), 'balance': 1000, 'dropDate' : None}
                userbridge.Add(userDict)
                await ctx.send(f"{user.mention} is now registered")
        except:
            await ctx.send(f"There was an error, try again later")
            traceback.print_exc()
    
    @commands.command(aliases = ['bal'])
    #balance of either the user or someone else
    async def balance(self, ctx, member: discord.Member=None):
        #check own bal
        if (member == None):
            user = ctx.message.author
            try:
                dbUser = userbridge.Get(str(user))
                #check if the user has been registered
                if(dbUser):
                    await ctx.send(f"{user.mention} has {dbUser.balance} credit(s)")
                else:
                    await ctx.send(f"{user.mention} has not been registered yet. Use $register")
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()
        #check bal of other user
        else:
            try:
                dbMember = userbridge.Get(str(member))
                if(dbMember):
                    await ctx.send(f"{member} has {dbMember.balance} credit(s)")
                else:
                    await ctx.send(f"{member} has not been registered yet. They should use $register")
            except:
                await ctx.send(f"There was an error, try again later")
                traceback.print_exc()
    
    #Tranfer money
    @commands.command()
    async def transfer(self, ctx, amount: int, reciever: discord.Member):
        user = ctx.message.author
        try:
            dbUser = (userbridge.Get(str(user))).to_dict()
            dbReciever = (userbridge.Get(str(reciever))).to_dict()
            if (amount < 0):
                await ctx.send('You can only tranfer an positive integer amount of credits')
            else:
                if(amount > dbUser['balance']):
                    await ctx.send(f'Cannot transfer {amount} credit(s) since your account does not have that much')
                else:
                    dbUser['balance'] -= amount
                    dbReciever['balance'] += amount
                    userbridge.Update(dbUser)
                    userbridge.Update(dbReciever)
                    await ctx.send(f"{amount} credit(s) has been successfully tranfered")
        except AttributeError:
            await ctx.send(f'{reciever} has not been registered so you cannot send the user credits')
            traceback.print_exc()
        except:
            await ctx.send(f"There was an error, try again later")
            traceback.print_exc()
    #daily drops
    @commands.command()
    async def daily(self, ctx):
        user = ctx.message.author
        try:
            dbUser = userbridge.Get(str(user)).to_dict()
            dropdate = userbridge.Get(str(user)).last_dropdate
            #if this is the first time the user has used the daily command
            if(dropdate == None):
                dbUser['dropDate'] = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                dbUser['balance'] += 200000
                userbridge.Update(dbUser)
                await ctx.send('Since this your first time recieving the daily drop, here is a 20,000 drop. Come back in 24 hours to recieve another drop')
            else:
                #must be more than one day that elasped
                #time diff is the time that has currently elasped
                timeDiff = datetime.now() - datetime.strptime(str(dropdate), '%Y-%m-%d %H:%M:%S') 
                if(timeDiff >= timedelta(days=1)):
                    dbUser['dropDate'] = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                    await ctx.send(f"Here is your daily drop of 500 credits {user.mention}")
                    dbUser['balance'] += 500
                    userbridge.Update(dbUser)
                else:
                    #Take 1 day worth of time and subtract the amount of time that has already passed and convert it to seconds
                    seconds = (timedelta(days=1) - timeDiff).total_seconds()
                    hours = seconds // 3600
                    mins = (seconds-(3600*hours))//60 
                    await ctx.send(f"Sorry, your daily drop is not yet ready. Come back in {hours} hour(s) and {mins} minute(s)")
        except:
            await ctx.send(f"There was an error, try again later")
            traceback.print_exc()
def setup(bot):
    bot.add_cog(Accounts(bot))    
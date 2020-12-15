import discord
import os
import random
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
import Config 
from itertools import cycle 
import asyncio
from asyncio import sleep

client = commands.AutoShardedBot(command_prefix=['.'], shard_count=1, case_insensitive=True)
client.load_extension("cogs.Example")
@client.event
async def on_ready():
    print('Bot is connected to discord!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')


@client.command(aliases= ['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)


@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        await ctx.send (f'Banned {member.mention}') 


@client.command()
async def unban(ctx, *, member):
    if ctx.author.guild_permissions.ban_members:
        banned_users = await ctx.guild.bans()
        member_name , member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.banned_users

            if(user.name , user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {member.mention}')
                return

async def change_status():
    while True:
        await  client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Status 1'))
        await sleep(10)
        await  client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'Status 2'))
        await sleep(10)
@client.event
async def on_ready():
    client.loop.create_task(change_status())

client.run(Config.token)

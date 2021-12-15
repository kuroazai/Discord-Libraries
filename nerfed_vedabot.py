# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:28:12 2019

@author: Kuro Azai
"""

import discord
import random
import urban
import serverstatus
import stockML
import mineropp
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is ready.')
    # Get all channels


async def on_member_join(member):
    print("{} Member Joined!".format(member.display_name))
    await client.add_roles("Citizen")


@client.event
async def on_message(message):

    if message.content.startswith('!role'):
        target = message.mentions[0]
        embed = discord.Embed()
        embed = discord.Embed(title="{} Roles".format(target.display_name),
                              color=0x8f06c1)
        embed = discord.Embed(description="Here's a list of the users current roles")
        embed.set_thumbnail(url=target.avatar_url)

        roles = target.roles
        txt = 'Roles : '
        for x in roles:
            txt + ' ' + str(x) + ','
        embed.add_field(name="User Roles : ", value=x, inline=False)

        await message.channel.send(embed=embed)
    # baka
    if message.content.startswith('!mibtc'):
        channel = message.channel
        if "admin" in str(message.author.roles):
            msg = mineropp.get_workers('ua7hyo3mngdd')
            await channel.send(msg)
        else:
            await channel.send('No. ' + message.author.display_name)

    # Admin
    if message.content.startswith('!giveaway'):
        channel = message.channel
        usrs = client.guilds
        for role in usrs:
            pass
        rng = random.randint(0, usrs-1)
        if "admin" in message.author.roles:
            await channel.send("{} has won the give away wow!".format(usrs[rng]))

    # Stock Prediction Interaction
    if message.content.startswith('!stock'):
        channel = message.channel
        b = message.content.split()
        stock = b[1]
        short = b[2]
        long = b[3]
        sdate = b[4]
        edate = b[5]
        data = stockML.VEDAML(stock,
                              int(short),
                              int(long),
                              sdate,
                              edate)
        # Load the image
        embed = discord.Embed()
        embed = discord.Embed(title="VEDA STOCK PREDICTOR", color=0x8f06c1)
        img = 'https://wallpapercave.com/wp/wp2734664.jpg'

        embed.set_thumbnail(url=img)
        # embed.set_image('GraphKun.png')

        embed.add_field(name="Accuracy", value=data[0], inline=True)
        embed.add_field(name="Predictions", value=data[1], inline=True)
        embed.add_field(name="Profit", value=data[2], inline=True)

        embed.set_footer(text="VEDA - Powered by doritos and monster energy")
        await message.channel.send(embed=embed)
        await channel.send(file=discord.File('GraphKun.png'))

    # User Interaction
    if message.content.startswith('!hello'):
        channel = message.channel
        await channel.send('Hello ' + message.author.display_name)

    # urban dictionary
    if message.content.startswith('!urban'):
        channel = message.channel
        b = message.content.split('!urban')
        msg = urban.parser(b[1])
        await channel.send('Meaning :\n' + msg)

    # server interaction
    if message.content.startswith('!sstat'):
        # run function
        channel = message.channel
        if serverstatus.server_status():
            await channel.send('The server is running! ' + message.author.display_name)
        else:
            await channel.send('The server isnt running :( ' + message.author.display_name)

    if message.content.startswith('!sstart'):
        channel = message.channel
        if "admin" in str(message.author.roles):
            await channel.send(str(serverstatus.server_start()) + message.author.display_name)
        else:
            await channel.send('No. ' + message.author.display_name)

    if message.content.startswith('!srestart'):
        channel = message.channel
        if "admin" in str(message.author.roles):
            await channel.send(str(serverstatus.server_restart()) + message.author.display_name)
        else:
            await channel.send('No. ' + message.author.display_name)

    if message.content.startswith('!sstop'):
        channel = message.channel
        if "admin" in str(message.author.roles):
            await channel.send(str(serverstatus.server_stop()) + message.author.display_name)
        else:
            await channel.send('No. ' + message.author.display_name)

    if message.content.startswith('!help'):
        embed = discord.Embed()
        embed = discord.Embed(title="VEDA functions", color=0x8f06c1)
        img = 'https://wallpapercave.com/wp/wp2734664.jpg'
        embed.set_thumbnail(url=img)

        embed.add_field(name="!role @member", value='*ALL MEMBERS* \nShows users roles. \nExample "!role @romanianmig21"', inline=True)
        embed.add_field(name="!urban", value='*ALL MEMBERS* \nGets the first urban reference of given string \nExample "!urban leng"', inline=True)

        embed.add_field(name="!stock", value='*ALL MEMBERS* \nGives prediction of a stock using some fancy MLs. \nInputs quandlcode shortMA LongMA  startdate endate. \nExample "!stock ECB/EURUSD  20 200 2019/01/01 2021/01/01"', inline=False)

        embed.add_field(name="!roles", value='*ALL MEMBERS* \nShows your roles.', inline=False)
        embed.add_field(name="!avatar @member", value='*ALL MEMBERS* \n\nRetrieves a targeted users avatar \nExample "!avatar @romanianmig21"', inline=False)

        embed.add_field(name="!clr x", value='*ADMIN ONLY* \nClears x number of messages. \nExample "!clr 69"', inline=False)
        embed.add_field(name="!sstart", value='*ADMIN ONLY* \nStarts Fivem Server', inline=False)
        embed.add_field(name="!sstop", value='*ADMIN ONLY* \nStarts Fivem Server', inline=False)
        embed.add_field(name="!srestart", value='*ADMIN ONLY* \nStarts Fivem Server', inline=False)

        await message.channel.send(embed=embed)



    # Delete Massages
    if message.content.startswith('!clr'):
        await message.delete()
        channel = message.channel
        usr = message.author.display_name
        if "admin" in str(message.author.roles):
            txt = message.content.split()
            x = int(txt[1])
            print(x)
            channel = message.channel
            await channel.purge(limit=x)
        else:
            txt = "you have no mana".format(usr)
            await channel.send(message.author.display_name + str(txt))

    if message.content.startswith('!avatar'):
        usr = message.author
        if message.mentions:
            usr = message.mentions[0]

        channel = message.channel
        embed = discord.Embed(
                        title = "Yoink my avatar now! ",
                        description = '{}'.format(usr.display_name),
                        colour = discord.Colour.blue()
                )
        embed.set_image(url=usr.avatar_url)
        await message.channel.send(embed=embed)

    if message.content.startswith('!roles'):
        channel = message.channel
        for x in message.author.roles:
            print(x)
        if "admin" in str(message.author.roles):
            embed = discord.Embed(
                    title = "{} roles".format(message.author.display_name),
                    description = "'Great power comes with great power abuse'",
                    colour = discord.Colour.blue()
            )
            counter = 1
            for x in message.author.roles:
                embed.add_field(name = "Role #" + str(counter), value = x.name, inline=True)
                embed.set_thumbnail(url=message.author.avatar_url)
                counter += 1
            await channel.send(embed=embed)
        else:
            pass


client.run('')

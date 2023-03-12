import discord 
import random
import os

from discord import FFmpegPCMAudio
from discord.ext import commands
from discord import Color 


token = "INSERT TOKEN HERE"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '#ST', intents = intents)

def main():
    @client.remove_command('help')

    @client.event 
    async def on_ready():
        print("Bot is online")

    @client.event 
    async def on_member_join(member):
        print(member + " has joined the Simple Tutors Server")

    @client.event 
    async def on_member_remove(member):
        print(member + " has left the Simple Tutors Server")

    @client.command(aliases = ['hi', 'greetings'])
    async def hello(ctx):
        await ctx.send('Hi')

    @client.command()
    async def displayEmbed(ctx):
        embed = discord.Embed(title = "Simple Tutors Bot", description = "This bot was created in order to moderate the server for better performance for the consumers.\nUse # symbol as the command prefix to access the bot's commands", colour = discord.Colour.purple)
        embed.set_footer(text = "SIMPLE TUTORS")
        await ctx.send(embed = embed)
    
    @client.group(invoke_without_command = True)
    async def help(ctx):
        embed = discord.Embed(
            title = "Help",
            description = "Use #SThelp for an extended list of commands that can be used",
            color = Color.blue()
        )
        embed.add_field(name = "Moderation (Admins only)", value = "Kick\nBan\nUnban")
        embed.add_field(name = "Fun", value = "8ball\nguess")
        embed.add_field(name = "Voice commands", value = "joinwithmusic\njoin\nleave")
        embed.add_field(name = "Help commands", value = "help_8ball\nhelp_guess\nhelp_join\nhelp_joinwithmusic\nhelp_leave")

        await ctx.send(embed = embed)

    @client.command()
    @commands.has_role("Admins")
    async def kick(ctx, member : discord.Member, *, reason = None):
        await member.kick(reason = reason)

    @client.command()
    @commands.has_role("Admins")
    async def ban(ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'Banned {member.mention}')

    @client.command()
    @commands.has_role("Admins")
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#ST")
        for ban_entry in banned_users:
            user = ban_entry.user    
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return 

    @client.command()
    async def help_8ball(ctx):
        embed = discord.Embed(
            title = "8 ball command",
            description = "This command allows for you to ask a yes or no question and await for a response",
            color = Color.brand_green()
        )
        embed.add_field(name = "Syntax", value = "#ST8ball <question>")

        await ctx.send(embed = embed)

    @client.command(aliases = ['8ball'])
    async def _8ball(ctx, *, question):
        responses = [
        'It is certain', 
        'Without a doubt', 
        'Outlook is good', 
        'Signs point to yes', 
        'Ask again later', 
        "Do not count on it", 
        "Outlook is not good", 
        "My sources say no", 
        "Very doubtful", 
        "Cannot predict now"]

        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @_8ball.error
    async def test_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):

            await ctx.send("Please enter a a statement for this command to work")

    @client.command()
    async def help_guess(ctx):
        embed = discord.Embed(
            title = "guess command",
            description = "this guessing game command is inputting a number to see if it matches with the random computer generated number",
            color = Color.brand_green()
        )
        embed.add_field(name = "Syntax", value = "STguess <number>")

        await ctx.send(embed = embed)


    @client.command(aliases = ['guess'])
    async def _guess(ctx, *, question):
        rand = random.randint(1, 100)
        if(question == rand):
            await ctx.send(f'You guessed right, the number was {rand}')
        else:
            await ctx.send(f'{question} was not the right number, the number was {rand}, better luck next time')

    @_guess.error
    async def guess_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a number for the command to work")

    @client.command()
    async def help_join(ctx):
        embed = discord.Embed(
            title = "join command",
            description = "this command allows for the bot to join voice channel",
            color = Color.brand_green()
        )
        embed.add_field(name = "Syntax", value = "#STjoin")

        await ctx.send(embed = embed)

    @client.command()
    async def help_joinwithmusic(ctx):
        embed = discord.Embed(
            title = "join with music command",
            description = "this command allows for the bot to join voice channel and play study music",
            color = Color.brand_green()
        )
        embed.add_field(name = "Syntax", value = "#STjoinwithmusic")

        await ctx.send(embed = embed)

    @client.command()
    async def help_leave(ctx):
        embed = discord.Embed(
            title = "leave command",
            description = "this command allows for the bot to leave voice channel",
            color = Color.brand_green()
        )
        embed.add_field(name = "Syntax", value = "#STleave")

        await ctx.send(embed = embed)

    @client.command(pass_context = True)
    async def joinwithmusic(ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('lofi-study-112191.mp3')
            player = voice.play(source)
            await ctx.send("ST bot is now playing some music for better study time")
        else:
            await ctx.send("You are not currently in a voice channel, you must be in a voice channel in order to run this command")

    @client.command(pass_context = True)
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
        else:
            await ctx.send("You are not currently in a voice channel, you must be in a voice channel in order to run this command")

    @client.command(pass_context = True)
    async def leave(ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('ST bot has left the voice channel')
        else:
            await ctx.send("ST bot is not currently in the voice channel")
    
    @client.command()
    async def load(ctx, extension):
        client.load_extension()

    @client.command()
    async def unload(ctx, extension):
        client.unload_extension()

    for filename in os.listdir('./DiscordCommands'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


    client.run(token)

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(f"{type(err).__name__} : {err}")
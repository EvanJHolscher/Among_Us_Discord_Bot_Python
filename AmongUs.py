import discord
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = '.', intents = intents)

@client.event
async def on_ready(): 
    await client.change_presence(status=discord.Status.online,activity = discord.Game('I AM GOD'))
  
    print('Bot is ready.')
    
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments')

@client.command()
async def ping(contex):
    await contex.send(f'Pong! {client.latency*1000}ms')

@client.command()
async def clear(contex, amount = 1):
    await contex.channel.purge(limit=amount+2)

@client.command()
async def silence(ctx,member : discord.Member, * , reason =None):
    test = True  
    guild = ctx.guild
    tracking = ctx.author
    if tracking.voice == None:
         test = False
    else :
        channel = tracking.voice.channel
        test = True
    if test == True:
          await member.edit(deafen = True, mute = True)
    else:
        await ctx.send('No user')
        
@client.command(pass_context=True)
@commands.has_role("GFA Team")
async def button(ctx):
    channel = ctx.message.author.voice.channel
    member = channel.members
    for member in channel.members: 
        role = discord.utils.find(lambda r: r.name == 'Ghost', ctx.message.guild.roles)
        voice_state = member.voice
        if role in member.roles:
            await member.edit(mute = True, deafen = False)
        elif voice_state is not None:
            await member.edit(mute = False, deafen = False)

@client.command(pass_context=True)
@commands.has_role("GFA Team")

async def play(ctx):
    channel = ctx.message.author.voice.channel
    member = channel.members
    for member in channel.members: 
        role = discord.utils.find(lambda r: r.name == 'Ghost', ctx.message.guild.roles)
        voice_state = member.voice
        if role in member.roles:
            await member.edit(mute = False, deafen = False)
        elif voice_state is not None:
            await member.edit(mute = True, deafen = True)

@client.command(pass_context=True)
@commands.has_role("GFA Team")

async def lobby(ctx):
    channel = ctx.message.author.voice.channel
    member = channel.members
    for member in channel.members: 
        role = discord.utils.find(lambda r: r.name == 'Ghost', ctx.message.guild.roles)
        voice_state = member.voice
        if voice_state is None:
          x = 0
        if role in member.roles:
             await member.remove_roles(role)
             await member.edit(mute = False, deafen = False)
        elif voice_state is not None:
            await member.edit(mute = False, deafen = False)

@client.command()       
async def kill(ctx, *, given_name=None):
    await ctx.channel.purge(limit=1)
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id
            vc = client.get_channel(wanted_channel_id)
            member = vc.members
            for member in vc.members:
                await member.edit(mute = True, deafen = True)

@client.command()
async def send(ctx, *, channel: discord.VoiceChannel):
    for members in ctx.author.voice.channel.members:
        await members.move_to(channel)

@client.command()
async def easteregg(ctx, user: discord.Member, amount = 1):
    await ctx.channel.purge(limit=amount)
    await user.edit(mute = True)
    await ctx.send("I think you are muted " + user.mention)

@client.command()
async def speak(ctx, user:discord.Member, *, string):
    await ctx.channel.purge(limit=1)
    await ctx.send(string + " " + user.mention)

@speak.error 
async def clear_error(ctx, error):
    await ctx.channel.purge(limit = 1)
    await ctx.send('Please enter in format: .speak @name text')

###############################################################################
client.run('Token')

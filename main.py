import discord
from discord.ext import commands
from itertools import cycle
import random
import requests
import os
from webserver import keep_alive
import io
import contextlib
import textwrap
from traceback import format_exception
import subprocess
import string

PREFIX = '>'
OWNER_ID = 722481147287830589
BOT_TOKEN = os.environ['BOT_TOKEN']
# ID_CLIENT_JDOODLE = os.environ['ID_CLIENT_JDOODLE']
# SECRET_CLIENT_JDOODLE = os.environ['SECRET_CLIENT_JDOODLE']
no_permission = 'You do not have enough permissions to use this command!'
green = 0x09ff00
active_dm_sessions = []
error_in_channel = None

status = cycle(['plying', 'watching', 'streaming'])
intents = discord.Intents.all()
intents.members = True
eval_allowed = [722481147287830589]
premix_id = 849651282985091153

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="DMS for suggestions, bugreports or anything to improve"))
    print("bot is ready.")
    try:
      with open('log.txt', 'r') as file:
        args = file.readlines()
        args = args[0].split(' ')
        if args[0] == 'True':
          with open('log.txt', 'w') as file:
            file.write('')
            channel = bot.get_channel(int(args[1]))
            await channel.send(f'Bot restarted successfully, new ping {round(bot.latency*1000)}ms')
    except:
      pass

class util(commands.HelpCommand):
  @bot.command()
  async def ping(ctx):
      await ctx.reply(f'Pong! {round(bot.latency*1000)}ms')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    possible_values = ['It is certain',
                        'It is decidedly so',
                        'Without a doubt',
                        'Yes, definitely',
                        'You may rely on it',
                        'As I see it, yes',
                        'Most likely',
                        'Outlook good',
                        'Yes',
                        'Signs point to yes',
                        'Reply hazy try again',
                        'Ask again later',
                        'Better not tell you now',
                        'Cannot predict now',
                        'Concentrate and ask again',
                        'Don\'t count on it',
                        'My reply is no',
                        'My sources say no',
                        'Outlook not so good',
                        'Very doubtful']
    embedded = discord.Embed()
    embedded.color = 0x3b93ff
    embedded.title = 'Mgaic 8ball'
    embedded.description = f'Question: {question}\nAnswer: {random.choice(possible_values)}'
    await ctx.send(embed=embedded)


@bot.command(aliases=['del'])
async def clear(ctx, amount=1):
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount+1)
    elif not ctx.author.guild_permissions.manage_messages:
        await ctx.reply(no_permission)
    else:
      await ctx.send(amount, 'is not a number.')

@bot.command()
async def kick(ctx, member:discord.Member, *, reason='None'):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        embedded = discord.Embed()
        embedded.color = 0xff002b
        embedded.title = 'kick'
        embedded.description = f'\"{member.display_name}\" was kicked.\nKicked by: {ctx.author.name}#{ctx.author.discriminator}\nReason: {reason}'
        await ctx.send(embed=embedded)
    else:
        await ctx.reply(no_permission)

@bot.command()
async def ban(ctx, member:discord.Member, *, reason='None'):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        embedded = discord.Embed()
        embedded.color = 0xff002b
        embedded.title = 'Ban'
        embedded.description = f'\"{member.display_name}\" was Banned.\nBanned by: {ctx.author.name}#{ctx.author.discriminator}\nReason: {reason}'
        await ctx.send(embed=embedded)
    else:
        await ctx.reply(no_permission)

@bot.command()
async def unban(ctx, id: int):
  if ctx.author.guild_permissions.ban_members:
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send("User was succsesuccessfully unbaned")
  else:
      await ctx.reply(no_permission)

@bot.command()
async def mute(ctx, member:discord.Member, *, reason='None'):
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name='Muted')
    if ctx.author.guild_permissions.manage_roles:
      await member.add_roles(mutedrole, reason=reason)
      embedded = discord.Embed()
      embedded.color = 0xff002b
      embedded.title = 'Mute'
      embedded.description = f'{member.name}#{member.discriminator} was muted.\nMuted by: {ctx.author.name}#{ctx.author.discriminator}\nReason: {reason}'
      await ctx.send(embed=embedded)
    else:
      await ctx.reply(no_permission)

@bot.command()
async def unmute(ctx, member:discord.Member):
  if ctx.author.guild_permissions.manage_roles:
    guild = ctx.guild
    mutedrole = discord.utils.get(guild.roles, name='Muted')
    await member.remove_roles(mutedrole)
    embedded = discord.Embed()
    embedded.color = 0xff002b
    embedded.title = 'Unmute'
    embedded.description = f'{member.name}#{member.discriminator} was unmuted.\nUnmuted by: {ctx.author.name}#{ctx.author.discriminator}'
    await ctx.send(embed=embedded)
  else:
    await ctx.reply(no_permission)


@bot.command(aliases=['random'])
async def r(ctx, *, values):
    values = values.split(' ')
    await ctx.reply(random.choice(values))

@bot.command()
async def say(ctx, *, message):
  if '@' in message:
    if ctx.author.guild_permissions.mention_everyone:
      await ctx.channel.purge(limit=1)
      await ctx.send(message)
    else:     
      await ctx.channel.purge(limit=1)
      await ctx.send('You cant have @ in your say command, maybe try running the command again without a @')
  else:
    await ctx.channel.purge(limit=1)
    await ctx.send(message)

@bot.command()
async def dumb(ctx):
    await ctx.send('here is 11 reasons why linux is better than windows and also why your dumb')
    await ctx.send('https://itsfoss.com/linux-better-than-windows/')

@bot.command()
async def stop(ctx):
    if ctx.author.guild_permissions.administrator:
      await ctx.send("bot closed")
      await bot.close()
    elif not ctx.author.guild_permissions.administrator:
      await ctx.reply(no_permission)

@bot.command()
async def av(ctx, member: discord.Member=None):
    if member == None:
      await ctx.send(ctx.author.avatar_url)
    else:
      await ctx.send(member.avatar_url)

@bot.command()
async def meme(ctx):
    r = requests.get('https://memes.blademaker.tv/api?lang=en')
    res = r.json()

    embedded = discord.Embed()
    embedded.color = green
    embedded.title = res['title']
    url = res['image']
    embedded.set_image(url = url)
    await ctx.send(embed = embedded)

@bot.command()
async def kill(ctx, member:discord.Member=None, spesific=None):
    if member == None:
        await ctx.send('Alright but who do i kill? you?')
    elif member == ctx.author:
        await ctx.send('Lets not do that please \U0001f603')
    else:
        urls = ['https://thumbs.gfycat.com/HollowSoreGrayling-max-1mb.gif',
        'https://animemangatalks.com/wp-content/uploads/2020/07/zenitsu-light.gif',
        'https://i.pinimg.com/originals/ff/2d/cd/ff2dcd44504000e320c21ae5682b5369.gif',
        'https://i.pinimg.com/originals/50/ba/2b/50ba2be29f18e860c7d9373610894862.gif',
        'https://media1.tenor.com/images/9df512e6a2bce6011493459ccf0cde56/tenor.gif?itemid=5283911',
        'https://i0.wp.com/24.media.tumblr.com/8e5c6a04a61c678d3c3412d30f1108b2/tumblr_mpvke66dxK1swj0zko1_500.gif?resize=650,400',
        'https://media.tenor.com/images/f3f4e488947f6aa40faed44ad8ae0723/tenor.gif',
        'https://thumbs.gfycat.com/DisguisedHeartyAmericanbulldog-max-1mb.gif',
        'https://media1.giphy.com/media/MugllcR6Gq8Y8/200.gif',
        'https://media1.tenor.com/images/31686440e805309d34e94219e4bedac1/tenor.gif?itemid=4790446']

        if spesific != None:
            if spesific == 'sexy':
                i = 0
            elif spesific == 'zen':
                i = 1
            elif spesific == 'wasted':
                i = 2
            elif spesific == 'slash':
                i = 3
            elif spesific == 'minato':
                i = 6
            elif spesific == 'susano':
                i = -2
            elif spesific == "smash":
                i = -1
            embedded = discord.Embed()
            embedded.title = 'OOF'
            embedded.color = green
            embedded.set_image(url=urls[i])
            await ctx.send(embed=embedded)
        else:    
          embedded = discord.Embed()
          embedded.title = 'OOF'
          embedded.color = green
          embedded.set_image(url=random.choice(urls))
          await ctx.send(embed=embedded)

@bot.command()
async def kiss(ctx, member:discord.Member=None):
    if member == None:
        await ctx.send('Alright but who do you want to Kiss? me? \U0001f633')
    else:
        urls = ['https://images6.fanpop.com/image/photos/40100000/giphy-6-naruto-shippuuden-40192027-320-240.gif',
        'https://media1.giphy.com/media/G3va31oEEnIkM/giphy.gif',
        'https://media2.giphy.com/media/bGm9FuBCGg4SY/giphy.gif',
        'https://i.pinimg.com/originals/2b/52/71/2b5271e20fa65925e07d0338fa290135.gif',
        'https://media1.tenor.com/images/d0cd64030f383d56e7edc54a484d4b8d/tenor.gif?itemid=17382422',
        'https://media1.tenor.com/images/b04461d8957a51ca5278a289dc142419/tenor.gif?itemid=17569270',
        'https://24.media.tumblr.com/5d51b3bbd64ccf1627dc87157a38e59f/tumblr_n5rfnvvj7H1t62gxao1_500.gif',
        'http://37.media.tumblr.com/7bbfd33feb6d790bb656779a05ee99da/tumblr_mtigwpZmhh1si4l9vo1_500.gif',
        'https://i.pinimg.com/originals/2b/3c/d2/2b3cd2c1583508ecfad5f7893dc2faf0.gif']

        embedded = discord.Embed()
        embedded.title = f'UwU \'{member.name}\' and \'{ctx.author.name}\' sitting on a tree......'
        embedded.color = green
        embedded.set_image(url=random.choice(urls))
        await ctx.send(embed=embedded)

@bot.command()
async def fuck(ctx, member:discord.Member=None):
    if member == None:
        await ctx.send('Alright but who do wanna fuck? me? \U0001f633')
    else:
        urls = ['https://carnivorouslreviews.files.wordpress.com/2018/08/interlocking.gif',
        'https://i.pinimg.com/originals/9d/92/1a/9d921ae2f69420beb68dcf083d7e0f43.gif',
        'https://media1.giphy.com/media/1NmaHBw350mly/giphy.gif',
        'https://media.tenor.com/images/5d1d30a0a3c56c8440290183ba47c57e/tenor.gif',
        'https://i.pinimg.com/originals/91/fd/fd/91fdfd64234b0c293e4763f706ab8507.gif',]

        embedded = discord.Embed()
        embedded.title = 'Damnnnn....... \U0001f975'
        embedded.color = green
        embedded.set_image(url=random.choice(urls))
        await ctx.send(embed=embedded)

@bot.command()
async def pastebin(ctx):
  await ctx.send('https://paste.pydis.com/')

@bot.command()
async def hug(ctx, member:discord.Member=None, spesific=None):
  if member == None:
    await ctx.send('Alright but who do wanna hug? me? \U0001f633')
  elif spesific == 'floro':
    embedded = discord.Embed()
    embedded.title = 'AWWWW.......'
    embedded.color = green
    embedded.set_image(url='https://gfycat.com/repentantpettyjackrabbit')
  elif spesific == 'cat':
    embedded = discord.Embed()
    embedded.title = 'AWWWW.......'
    embedded.color = green
    embedded.set_image(url='https://media.tenor.com/images/2d45b2e842cac286aa91cec91a7a17d7/tenor.gif')
  else:
    urls = ['https://i.pinimg.com/originals/51/2a/f3/512af31e377153959dbad5b888d22af1.gif', 'https://i.pinimg.com/originals/e2/c9/7a/e2c97a3b7a1ac0ec5bcecc0c18c61209.gif', 'http://33.media.tumblr.com/680b69563aceba3df48b4483d007bce3/tumblr_mxre7hEX4h1sc1kfto1_500.gif', 'https://i.pinimg.com/originals/16/46/f7/1646f720af76ea58853ef231028bafb1.gif', 'https://acegif.com/wp-content/uploads/anime-hug.gif']
    embedded = discord.Embed()
    embedded.title = 'AWWWW.......'
    embedded.color = green
    embedded.set_image(url=random.choice(urls))
  await ctx.send(embed=embedded)

@bot.command()
async def eval(ctx, *, a):
  if ctx.author.id in eval_allowed:
    b = a.replace(a[0:3], '')
    code = b.replace(a[-1:-4], '')

    local_variables = {
        "discord": discord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
            )

            obj = await local_variables["func"]()
            result = f"{stdout.getvalue()}\n-- {obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))

    await ctx.send(result)
  else:
    await ctx.send(no_permission)

@bot.command()
async def cat(ctx, type=None):
  if type == None:
    await ctx.send('do you want a gif or a img spesify it as >cat img or >cat gif')
  if type == "img":
    r = requests.get('https://api.thecatapi.com/v1/images/search')
    res = r.json()
    myline = res[0]['url']
    embedded = discord.Embed()
    embedded.title = 'Cats!'
    embedded.color = green
    embedded.set_image(url=myline)
    await ctx.send(embed=embedded)
  elif type == 'gif':
    r = requests.get('http://thecatapi.com/api/images/get?format=json&type=gif')
    res = r.json()
    myline = res[0]['url']
    embedded = discord.Embed()
    embedded.title = 'Cats!'
    embedded.color = green
    embedded.set_image(url=myline)
    await ctx.send(embed=embedded)

@bot.command()
async def origix(ctx):
  lines = open('cat.txt').read().splitlines()
  myline = random.choice(lines)
  await ctx.send(myline)

@bot.command()
async def owo(ctx):
  lines = open('furry.txt').read().splitlines()
  myline = random.choice(lines)
  embedded = discord.Embed()
  embedded.title = 'Furries!'
  embedded.color = green
  embedded.set_image(url=myline)
  await ctx.send(embed=embedded)

@bot.command()
async def meow(ctx):
  await ctx.send('meowwwwwwwwwwwwwwwww')

@bot.command()
async def bean(ctx, member:discord.Member, *, reason='None'):
    embedded = discord.Embed()
    embedded.color = 0xff002b
    embedded.title = 'Bean'
    embedded.description = f'\"{member.display_name}\" was Beaned.\nBeaned by: {ctx.author.name}#{ctx.author.discriminator}\nReason: {reason}'
    await ctx.send(embed=embedded)

@bot.command()
async def sen(ctx):
    await ctx.send('SenPaii Simps for Origix >:)')

@bot.command()
async def nasty(ctx):
    await ctx.send('"Cats are Nasty" - ~~SenPaii~~')

@bot.command()
async def afk(ctx, *, reason='AFK'):
  if '@' not in reason:
    with open('afk.txt', 'a') as file:
      file.write(f'{ctx.author.id},{ctx.guild.id},~{reason}\n')
    try:
      await ctx.author.edit(nick=f'{ctx.author.display_name} (AFK)')
    except:
      pass
    await ctx.send(f'Your afk status has been changed, {ctx.author.display_name}.')
  else:
    await ctx.reply('You cant have @ in your afk, Try running the command again without any @')

@bot.command()
async def warn(ctx, member:discord.Member=None, *, reason='None'):
  if ctx.author.guild_permissions.ban_members:
    if member:
      id_sections = []
      for i in range(4):
          number_of_char = random.randint(0, 4)
          section = ''
          for i in range(number_of_char):
              section += random.choice(string.ascii_letters)

          for i in range(4-number_of_char):
              section += str(random.randint(0, 9))
          
          id_sections.append(section)

      id = f'{id_sections[0]}-{id_sections[1]}-{id_sections[2]}-{id_sections[3]}'
      embedded = discord.Embed()
      embedded.color = 0xfcf803
      embedded.title = 'Warn'
      embedded.description = f'\"{member.display_name}\" was Warned.\nWarned by: {ctx.author.name}#{ctx.author.discriminator}\nReason: {reason}'
      embedded.set_footer(text = id)
      with open("warns.txt", "a") as file:
        file.write(f'{member.id},{member.guild.id},{ctx.author.id},{id},~{reason}\n')
      await ctx.send(embed=embedded)
    else:
      embedded = discord.Embed()
      embedded.color = 0xff0000
      embedded.title = 'Warn'
      embedded.description = f'You were successfully warned for not giving a user to warn :)'
      await ctx.send(embed=embedded)
  else:
    await ctx.send(no_permission)

@bot.command(aliases=['warning', 'warns', 'warnnings', 'warnning'])
async def warnings(ctx, member:discord.Member=None):
  warnings = f'{member.id},{member.guild.id}'
  warns = 0
  embedded = discord.Embed()
  embedded.color = 0xfcf803
  embedded.title = f'Warnings for {member.display_name}#{member.discriminator}'
  with open('warns.txt', 'r') as file:
    for line in file:
      warns+=1
      if line.__contains__(warnings):
        embedded.add_field(name=f"ID: {line.split(',')[3]} | Warned by {bot.get_user(int(line.split(',')[2])).display_name}#{bot.get_user(int(line.split(',')[2])).discriminator}", value=f"Reason: {line.split('~')[1]}")
      else:
        pass
  await ctx.send(embed=embedded)
    

@bot.command()
async def error(ctx, *, value):
  if ctx.author.id in eval_allowed:
    if value == 'true' or value == 'True':
      error_in_channel = True
      await ctx.send('error changed to true')
    elif value == 'false' or value == 'False':
      error_in_channel = False
      await ctx.send('error changed to false')
    else:
      await ctx.send('invalid value')
  else:
    await ctx.send(no_permission)

@bot.command()
async def send(ctx, id, *, msg):
  if ctx.author.id == OWNER_ID:
    await bot.get_user(int(id)).send(msg)
  else:
    await ctx.send(no_permission)

@bot.command(aliases=['reboot', 'rs', 'rb'])
async def restart(ctx):
  if ctx.author.id in eval_allowed:
    await ctx.send('Rebooting bot . . .')
    with open('log.txt', 'w') as file:
      file.write(f'True {ctx.channel.id}')
    subprocess.call(["bash", "-c", "source ~/.profile; " + 'python main.py'])

@bot.command(aliases=['snippes', 'ss'])
async def snippets(ctx):
  embedded = discord.Embed()
  embedded.color = green
  embedded.title = 'Snippets'
  embedded.add_field(name="-> pastebin", value="```https://paste.pydis.com/```")
  embedded.add_field(name="-> Read file", value="```with open(\"file.txt\", \"r\") as file:```")
  embedded.add_field(name="-> kill values", value="```sexy\nzen\nwasted\nslash\nminato\nsusano\nsmash```")
  embedded.add_field(name="-> java template", value="```java\npublic class Main{\n\tpublic static void main(String[] args){\n\t\tSystem.out.println(\"Hello, world!\");\n\t}\n}```")
  await ctx.send(embed=embedded)

@bot.command(aliases=['java', 'j'])
async def javac(ctx, *, a):
  if a.startswith('```java'):
    a = a[:0] + '' + a[7:]
    code = a[:-3]
  else:
    b = a.replace(a[0:3], '')
    code = b.replace(a[-1:-4], '')

  program = {
    'script' : code,
    'language': "java",
    'versionIndex': "0",
    'clientId': JDOODLE_CLIENT_ID,
    'clientSecret': JDOODLE_CLIENT_SECRET,
}

  r = requests.post('https://api.jdoodle.com/v1/execute', json=program)

  output = r.json()["output"]
  await ctx.send("```java\n" + output + "```")

@bot.command(aliases=['py'])
async def python(ctx, *, a):
  if a.startswith('```python'):
    a = a[:0] + '' + a[9:]
    code = a[:-3]
  elif a.startswith('```py'):
    a = a[:0] + '' + a[5:]
    code = a[:-3]
  else:
    b = a.replace(a[0:3], '')
    code = b.replace(a[-1:-4], '')

  program = {
    'script' : code,
    'language': "python3",
    'versionIndex': "0",
    'clientId': JDOODLE_CLIENT_ID,
    'clientSecret': JDOODLE_CLIENT_SECRET,
}

  r = requests.post('https://api.jdoodle.com/v1/execute', json=program)

  output = r.json()["output"]
  await ctx.send("```py\n" + output + "```")

@bot.command(aliases=['node', 'npm', 'js'])
async def nodejs(ctx, *, a):
  if a.startswith('```js'):
    a = a[:0] + '' + a[4:]
    code = a[:-3]
  elif a.startswith('```javascript'):
    a = a[:0] + '' + a[14:]
    code = a[:-3]
  else:
    b = a.replace(a[0:3], '')
    code = b.replace(a[-1:-4], '')

  program = {
    'script' : code,
    'language': "nodejs",
    'versionIndex': "0",
    'clientId': JDOODLE_CLIENT_ID,
    'clientSecret': JDOODLE_CLIENT_SECRET,
}

  r = requests.post('https://api.jdoodle.com/v1/execute', json=program)

  output = r.json()["output"]
  await ctx.send("```js\n" + output + "```")

@bot.command()
async def help(ctx, helpcatogory=None):
    if helpcatogory == None:
        embedded = discord.Embed()
        embedded.color = green
        embedded.title = 'Help general'
        embedded.description = f'PREFIX = \">\"\nThere are three catogries of command do >help <catogary> to get help on that catogary\nIf you need any more help understanding or using the command you can contact subgamer\n<> - refers to required feild these have to be there for the command to run and\n() - refers to optional feild the command will run without these too'
        embedded.add_field(name='fun', value='8ball, say, dumb, meme, kill, kiss, fuck, hug, cat, owo, origix, meow, sen, nasty')
        embedded.add_field(name='utils', value='ping, del, random,  av, help, bean, afk, warn, python, javac, js')
        embedded.add_field(name='admin', value='kick, ban, unban,  mute, unmute, stop')
        await ctx.send(embed=embedded)
    elif helpcatogory == 'fun':
        embedded = discord.Embed()
        embedded.color = green
        embedded.title = 'help <fun>'
        embedded.add_field(name='8ball <question>', value='Gives you the answer of the magic 8ball on the question')
        embedded.add_field(name='say <message>', value='Says something as the bot and deletes your command')
        embedded.add_field(name='dumb', value='Corrects dumb people thats about it')
        embedded.add_field(name='meme', value='Shows you a random meme')
        embedded.add_field(name='kill <@person to kill>', value='Kills the mentioned user')
        embedded.add_field(name='kiss <@person to kiss>', value='Kisses the mentioned user')
        embedded.add_field(name='fuck <@person to fuck>', value='Fucks the mentioned user')
        embedded.add_field(name='hug <@mention to hug>', value='Hugs the mentioned user')
        embedded.add_field(name='owo', value='sends a furry gif')
        embedded.add_field(name='cat <img or gif>', value='sends a cat img or gif')
        embedded.add_field(name='origix', value='sends a origix quote')
        embedded.add_field(name='bean <@mention to bean> <reason>', value='BEANNNNNN')
        embedded.add_field(name='meow', value='MEOWWWWWWWWWWWWW............')
        embedded.add_field(name='sen', value='created for Senpaii')
        embedded.add_field(name='nasty', value='created for Senpaii')
        channel = await ctx.author.create_dm()
        await channel.send(embed=embedded)
        await ctx.send('A dm was sent with the cmds and thier descrpition')
    elif helpcatogory == 'utils':
        embedded = discord.Embed()
        embedded.color = green
        embedded.title = 'help <utils>'
        embedded.add_field(name='ping', value='Pings the bot to see if its online or not and to see the latency')
        embedded.add_field(name='del <number of messages to delete>', value='Deletes the number of messages mesntioned')
        embedded.add_field(name='random <...> (....', value='Chooses a random option from the given choices')
        embedded.add_field(name='stop', value='Stops the bot use this whenever mistakly a large command is triggered or if the bot starts misbehaving')
        embedded.add_field(name='av', value='Shows you pfp')
        embedded.add_field(name='afk (reason for afk)', value='Sets the afk and notifies if they are afk')
        embedded.add_field(name='warn <@mention to warn> (reason)', value='warns the user mentioned with the reason.')
        embedded.add_field(name='javac ```java\nCODE TO RUN HERE```', value='runs the java code.')
        embedded.add_field(name='python ```python\nCODE TO RUN HERE```', value='runs the python code.')
        embedded.add_field(name='js ```js\nCODE TO RUN HERE```', value='runs the nodejs code.')
        embedded.add_field(name='help (catogory)', value='Shows the info about cmd or cmds in a spesific catogory')
        channel = await ctx.author.create_dm()
        await channel.send(embed=embedded)
        await ctx.send('A dm was sent with the cmds and thier descrpition')
    elif helpcatogory == 'admin':
        embedded = discord.Embed()
        embedded.color = green
        embedded.title = 'help <admin>'
        embedded.add_field(name='kick <@person to kick> (reason)', value='Kicks the mentioned user with or without reason')
        embedded.add_field(name='ban <@person to ban> (reason)', value='Bans the mentioned user with or without reason')
        embedded.add_field(name='unban <name_of_user#tag_of_user>', value='unbans the given user need to use it like >unban someone#6969')
        embedded.add_field(name='mute <@person to be muted> (reason)', value='Mutes the mentioned user with or without reason')
        embedded.add_field(name='unmute <@person to umute>', value='Unmutes a perviously muted person')
        channel = await ctx.author.create_dm()
        await channel.send(embed=embedded)
        await ctx.send('A dm was sent with the cmds and thier descrpition')

if error_in_channel:
  @bot.event
  async def on_command_error(ctx, error):
    channel = bot.get_channel(890455382181416990)
    if ctx.guild == None:
      await channel.send(f'log: {error} from DMS.')
    else:
      await channel.send(f'log: {error} from server: {ctx.guild.name}')
else:
  pass

@bot.listen("on_message")
async def _my_msg_listneer(message):
  if message.author.id != premix_id:
    if message.content.startswith('<@!849651282985091153'):
      await message.channel.send('My prefix is >')
      
    elif message.content.startswith('>'):
      channel = bot.get_channel(890455582342021200)
      try:
        await channel.send(f'{message.author.name}#{message.author.discriminator} ({message.guild.name}): {message.content}')
      except:
        pass
    with open('afk.txt', 'r') as file:
        lines = file.readlines()
    for i in lines:
        try:
          if str(message.author.id) in i and str(message.guild.id) in i and '>afk' not in message.content and message.author.id != premix_id:
            lines.pop(lines.index(i))

            with open('afk.txt', 'w') as file:
                file.write('')

            with open('afk.txt', 'a') as file:
                for i in lines:
                    file.write(i)
            nick = message.author.display_name.split(' (AFK)')

            try:
              await message.author.edit(nick=nick[0])
            except:
              pass
              
            await message.channel.send(f'Welcome back, {message.author.display_name}', delete_after=7)
        except:
          pass

    if message.mentions:
        with open('afk.txt', 'r') as file:
          lines = file.readlines()
          for i in lines:
            for a in message.mentions:
              if str(a.id) in i and str(a.guild.id) in i:
                  reason = i.split('~')
                  await message.channel.send(f'({a.display_name}) is afk : {reason[1]}')

    elif message.guild == None:
      await message.channel.send('under construction maybe suggest to subgamer directly')
      # if message.author.id not in active_dm_sessions:
      #   embedded = discord.Embed()
      #   embedded.color = green
      #   embedded.title = 'Any suggestions?'
      #   embedded.description = 'Is there any suggestion, bugreports or anything I can improve that you wanna inform?\nreply with "yes" or "no"'
      #   await message.channel.send(embed=embedded)
      #   msg = await bot.wait_for("message") # wait_for is a coro
      #   if msg.content == "yes":
      #       embedded = discord.Embed()
      #       embedded.color = green
      #       embedded.title = 'What would you like to inform?'
      #       embedded.description = 'Alright, great what would you like to inform you to inform message me one of these catogories\n"suggestion"\n"bugreport"\n"other"'
      #       await message.channel.send(embed=embedded)
      #       if msg.author.id not in active_dm_sessions:
      #         active_dm_sessions.append(msg.author.id)
      #       msg = await bot.wait_for("message")
      #       if msg.content == 'suggestion':
      #           await message.channel.send('Ok goahead i am listening, please try to be desciptive as possible')
      #           msg = await bot.wait_for("message")
      #           await message.channel.send('ok thanks, your suggestion was heard I might contact you if your suggestion was implented or if I did not understand it.')
      #           channel = bot.get_channel(867678259004571659)
      #           url = msg.jump_url
      #           await channel.send(f'{message.author.name} ({url}): {msg}')
      #       elif msg.content == 'bugreport':
      #           await message.channel.send('Ok goahead i am listening, please try to be desciptive as possible')
      #           msg = await bot.wait_for("message")
      #           await message.channel.send('ok thanks, your repot was heard I might contact you if the bug was fixed or if I did not understand it.')
      #           channel = bot.get_channel(867680105962799105)
      #           url = msg.jump_url
      #           await channel.send(f'{message.author.name} ({url}): {msg}')
      #       elif msg.content == 'other':
      #           await message.channel.send('Ok goahead i am listening, please try to be desciptive as possible')
      #           msg = await bot.wait_for("message")
      #           await message.channel.send('ok thanks, your repot was heard.')
      #           channel = bot.get_channel(867680501753708584)
      #           url = msg.jump_url
      #           await channel.send(f'{message.author.name} ({url}): {msg}')
      #       else:
      #           await message.channel.send('Soory i didn\'t quite get that, please choose from the option given and maybe try sending the message again')
      #   elif msg.content == "no":
      #       await message.channel.send('Ok, no problem have a nice day!')
      #       return
      #   else:
      #       await message.channel.send('Soory i didn\'t quite get that, please choose from the option given')
      #       return

    
keep_alive()
bot.run(BOT_TOKEN)
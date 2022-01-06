import asyncio
import discord
from discord.ext import commands
import random

# game words
words = ["نجاری",
         "عطاری",
         "قصابی",
         "بیمارستان",
         "تیمارستان",
         "قبرستان",
         "پارچه فروشی",
         "مسجد",
         "سوپرمارکت",
         "بازار",
         "کاباره",
         "مبل فروشی",
         "املاک",
         "حرم",
         "اسباب بازی فروشی",
         "بهشت",
         "جهنم",
         "برزخ",
         "باغ",
         "کاخ",
         "طویله",
         "مزرعه",
         "گاوداری",
         "گلخانه",
         "گل فروشی",
         "لباس فروشی",
         "درمانگاه",
         "داروخانه",
         "دفتر وکالت",
         "خانه سالمندان",
         "مدرسه",
         "دانشگاه",
         "دادگاه",
         "شهرداری",
         "عطر فروشی",
         "رستوران",
         "قهوه خانه",
         "زیردریایی",
         "گالری نقاشی",
         "دیزی سرا",
         "کله پاچه فروشی",
         "کافه",
         "موبایل فروشی",
         "بانک",
         "بیمه",
         "استخر",
         "دستشویی",
         "باغ وحش",
         "آزمایشگاه",
         "جنگل",
         "دریا",
         "اقیانوس",
         "مرداب",
         "خشکشویی",
         "صحرا",
         "کویر",
         "آتلیه عکاسی",
         "نمایشگاه کتاب",
         "گیم نت",
         "صحافی",
         "آشپزخانه",
         "پادگان",
         "فرودگاه",
         "شهربازی",
         "شالیزار",
         "خیاطی",
         "کوه",
         "دره",
         "آهنگری",
         "گالری اتومبیل",
         "فروشگاه",
         "کلیسا",
         "آرایگشاه",
         "تالار عروسی",
         "بازار میوه",
         "سیرک",
         "سینما",
         "بورس",
         "دماوند",
         "پارکینگ",
         "موزه",
         "هتل",
         "تعمیرگاه",
         "ساحل",
         "آسیا",
         "اروپا",
         "آفریقا",
         "استرالیا",
         "آمریکا جنوبی",
         "آمریکا شمالی",
         "آمریکا مرکزی",
         "مطب",
         "هایپر مارکت",
         "آب انبار",
         "پالایشگاه",
         "معدن",
         "قهوه خانه",
         "چراگاه",
         "باشگاه",
         "ورزشگاه",
         "مترو",
         "دامپزشکی",
         "کلوپ شبانه",
         "طلا فروشی",
         "پمپ بنزین",
         "نقاشی",
         'ایستگاه راه آهن',
         "دندان پزشکی",
         "ایستگاه اتوبوس",
         "نمایشگاه کتاب",
         "نیروگاه اتمی",
         "آکواریم",
         "رصدخانه",
         "خوابگاه",
         "ساعت سازی",
         "سونا",
         "جکوزی",
         "کبابی",
         "سفارت",
         "پاساژ",
         "صرافی"]

# a dictionary of games
games = {}

# creates the client
prefix = 'spy.'
client = commands.Bot(command_prefix=prefix)


# player. not users! user are linked to players in the Game object.
class player:

    def __init__(self, name):
        self.name = name
        self.wins = 0.0
        self.spy = False
        self.suspicions = 0
        self.vote = False
        self.knows = True

    # adds to players wins for scoreboard
    def wins(self):
        self.wins += 1

    # re-initiates player spy status
    def replay(self):
        self.spy = False

    # sets the player as the spy
    def setSpy(self):
        self.spy = True
        self.knows = False

    # Game object. all the game properties are in stored in this object.


class Game:
    def __init__(self):
        self.GameStarted = False
        self.players = {}
        self.gameMessage = None
        self.startMessage = None
        self.channel = None
        self.votes = {}
        self.spy = None
        self.word = None
        self.answerMessage = None

    # adds a player to the players list.
    async def addPlayer(self, member):
        self.players[member] = player(member.name)
        # print(f'player {member.name} is added')

    # removes a player from players list.
    async def removePlayer(self, member):
        self.players.pop(member)
        # print(f'player {member.name} is removed')

    # assign the spy by random from players list.
    async def assignSpy(self):
        spyMember = random.choice(list(self.players.keys()))
        self.spy = self.players[spyMember]
        self.spy.setSpy()

    # finds and return the most suspicious player.
    def mostVoted(self):
        voted = player('sb')
        for culprit in self.players.values():
            if culprit.suspicions > voted.suspicions:
                voted = culprit

        return voted

    # sends all users DMs. the spy will receive "you are the SPY" and the rest will receive the game word
    async def sendUserMessages(self):
        for user in self.players.keys():
            if self.players[user] is self.spy:
                await user.send('شما جاسوس هستید')
            else:
                await user.send(self.word)

    # re-initiates the game object, sends the gameMessage and start the game.
    async def startgame(self):
        await asyncio.sleep(1)
        await self.channel.send('۱')
        await asyncio.sleep(1)
        await self.channel.send('۲')
        await asyncio.sleep(1)
        await self.channel.send('۳')
        self.word = random.choice(words)
        # checks if the game has begun and send relative message
        if not self.GameStarted:
            self.GameStarted = True
            self.gameMessage = await self.channel.send(
                'هشدار به تمامی بازیکنان \nتوجه کنید \nیک جاسوس بین ماست!')

            await self.assignSpy()
            await self.sendUserMessages()
            listOfPlayers = 'بازیکنان \n'
            # n = 0
            # character = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
            # for player in self.players.values():
            #     listOfPlayers += f'{n} : {player.name} \n'
            #     reaction = await self.gameMessage.add_reaction(character[n])
            #     self.votes[character[n]] = player
            #     n += 1

            await self.channel.send(listOfPlayers)

        else:
            await self.channel.send('بازی شروع شده، سعی کنید جاسوس را پیدا کنید')

    # resets the game properties.
    def reset(self):
        self.spy = None
        self.GameStarted = False

    # finishes the game and reloads the game object.
    async def finishGame(self):
        # if self.spy.knows:
        #     await self.channel.send(f' باختید جاسوس  '
        #                             f'{self.spy.name} '
        #                             f' کلمه را پیدا کرد ')
        # else:
        #     if self.spy is self.mostVoted():
        #         for player in self.players.values():
        #             if not player.spy:
        #                 await self.channel.send(
        #                     f' جاسوس '
        #                     f' {self.spy.name}!  '
        #                     f' بود '
        #                     f'تبریک میگم '
        #                     f' {player.name}! '
        #                     f'  جاسوس رو پیدا کردی ')
        #                 player.wins += 0.5
        #             else:
        #                 player.wins -= 0.5
        #     else:
        #         await self.channel.send(
        #             f'زمان تموم شد و جاسوس رو پیدا نکردیم جاسوس '
        #             f'{self.spy.name} '
        #             f' بود ')
        #         self.spy.wins += 1.0

        self.reset()


# resends the startMessage
async def callStartMessage(game):
    channel = game.channel
    game.startMessage = await channel.send('آماده اید؟')
    await game.startMessage.add_reaction('➕')


# This event makes sure that the bot is online
@client.event
async def on_ready():
    print('ربات جاسوس آنلاین شد '
          '  {0} '.format(client.user))


# these events trigger by adding reactions and handles the game joining and adding votes.
@client.event
async def on_raw_reaction_add(payload):
    guild = await client.fetch_guild(payload.guild_id)
    game = games[guild]
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = await client.fetch_user(payload.user_id)
    reaction = payload.emoji
    # print('reaction added')
    if message.id == game.startMessage.id:
        if not game.GameStarted:
            if not member.bot:
                await game.addPlayer(member)
            # else:
            #     print('this player is a bot!!!!')
        else:
            await channel.send('بازی شروع شده بود')
            await message.remove_reaction(reaction, member)

    elif message.id == game.gameMessage.id:
        if not member.bot and not game.players[member].vote:
            game.votes[reaction.name].suspicions += 1
            game.players[member].vote = True
        elif not member.bot and game.players[member].vote:
            for reactionCnt in message.reactions:
                if reactionCnt.emoji != reaction.name:
                    await message.remove_reaction(reactionCnt, member)

    elif message.id == game.gameMessage.id:
        if not member.bot:
            await game.finishGame()


# These events trigger by removing reactions and handles the game leaving and removing votes.
@client.event
async def on_raw_reaction_remove(payload):
    guild = await client.fetch_guild(payload.guild_id)
    game = games[guild]
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = await client.fetch_user(payload.user_id)
    reaction = payload.emoji
    # print('reaction removed')
    if message.id == game.startMessage.id:
        if not game.GameStarted:
            if not member.bot:
                await game.removePlayer(member)
            # else:
            #     print('this player is a bot!!!!')

    elif message.id == game.gameMessage.id:
        game.votes[reaction.name].suspicions -= 1
        game.players[member].vote = False


# makes the bot ready
@client.command()
async def playspy(ctx):
    guild = ctx.message.guild
    game = Game()
    games[guild] = game
    game.channel = await guild.create_text_channel('محل برگزاری بازی جاسوس')
    everyoneRole = guild.get_role(guild.id)
    await game.channel.set_permissions(everyoneRole, read_messages=True, send_messages=False)
    await callStartMessage(game)


# Starts the Game
@client.command()
async def startspy(ctx):
    guild = ctx.message.guild
    game = games[guild]

    await game.startgame()


# this command finishes and resets the game
@client.command()
async def finishspy(ctx):
    guild = ctx.message.guild
    game = games[guild]
    await game.finishGame()


# this command gets the spy's answer and adds the verification reaction
# @client.command()
# async def Answer(ctx):
#     guild = ctx.message.guild
#     game = games[guild]
#     if ctx.message.author == game.spy:
#         game.answerMessage = await ctx.message.channel.send(
#             f'جاسوس خودش رو لو داد حالا باید ببینیم که درست حدس زده '
#             f'{ctx.message.content} '
#             f'کلمه این بود؟')
#         await game.answerMessage.add_reaction('➕')
#
#     else:
#         await ctx.message.delete()
#         await ctx.message.channel.send('آخه بشر تو مگه جاسوسی که اینجا چت میکنی؟')

# receives the token generated by discord as string. My token is regenerated!

client.run('Discord-Bot-Token')

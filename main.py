import discord
from discord.ext import commands
import json
from keep_alive import keep_alive
from random import randint


#the discord bot
bot = commands.Bot(command_prefix="$", help_command=commands.DefaultHelpCommand(no_category = 'All Commands'), activity=discord.Game('$help'), case_insensitive=True)


#authors: Karen + Bonnie
@bot.command(name = 'about', description = 'Description of who Tina Bot is')
async def bot_about(ctx): 
  about_me = "Hi there! My name is Tina, and I'm a Quarantine Discord Bot." "This means I provide services particularly suited to support you during the COVID-19 pandemic lockdown. These services include:"

  features = {'symptoms screening form':'daily school and child care screening form to ensure that you are safe to go to school/childcare', 'indoor activity suggestions' : 'activity suggestions that follow social distancing guidelines','news updates':'browse through news articles about covid', 'point system': 'accumulate points by completing activities and compete for the top 10 spots on the leaderboard!'}
  
  embed=discord.Embed(title= "**ABOUT ME**", description = about_me, color=0xbf75e1)
  
  for key in features:
    
    embed.add_field(name = key, value = features[key], inline=False) 

  embed.set_author(name="User Manual", url="https://docs.google.com/document/d/1YpndrMHj5RrOeom7BnfjpeX3gfu5hX2UOFiasF0mrvk/edit?usp=sharing")

  embed.set_footer(text="My code is written in Python and I was created by two high school students. It was nice meeting you! I hope to see you around soon :)")

  await ctx.reply(embed=embed)


#authors: Bonnie + Karen
@bot.command(name = 'activity', description = 'This command allows you to select activity suggestions that follow social distancing guidelines. Each category has an acronym (call the command to view them) and will return a random activity suggestion. We encourage you to try the activity! (100 points)')
async def suggest_activity(ctx):
  social_distance_activities = {'e':[['20 pushups', '20 sit ups', '20 squats', '20-minute yoga routine'], 'exercise'], 
  'oga' : [['Gartic Phone', 'skribbl.io', 'League of Legends', 'Valorant', 'Google Halloween 2018 Doodle'], 'online group activities'], 
  'iaa' : [["Plan tomorrow's outfit", 'Clean your keyboard', 'Do a puzzle', 'Cook a meal'], 'individual analog activities'], 'ioa' : [['Organize your folders', "Explore all of my (Tina bot's) features", 'Watch a TED Talk', "Watch a Youtube video about a topic you've never heard of"], 'individual online activities'], 'mh' : [['Find a new anime', 'Learn an instrument', 'Try making a new recipe', "Watch Disney's latest movie", 'Make a new Spotify playlist'], 'media/hobbies']}

  activity_categories = discord.Embed(title=f"{ctx.author}'s Social-Distancing Activity Suggestion", description=f"Choose what type of activity you'd like suggested! This list is for {ctx.author}'s suggestion only. Use $activity to generate your own.")
  for category in social_distance_activities:
    activity_categories.add_field(name = social_distance_activities[category][1], value = "Type '" + category + "' into the chat to select", inline = False)
  
  await ctx.reply(embed = activity_categories)

  def activity_check(answer):
    return answer.content in social_distance_activities.keys() and answer.author.id == ctx.author.id
  
  answer = await bot.wait_for('message', check = activity_check)

  answer = answer.content

  activity = social_distance_activities[answer][0][randint(0, len(social_distance_activities[answer][0]) - 1)]
  suggestion = discord.Embed(title="Here's your suggestion!", description=activity)
  await ctx.reply(embed=suggestion)

  await updatepoint(ctx.author.id, 100)
  await ctx.reply(f"Just for requesting this activity (please try to do it, though!) {ctx.author} gets 100 points.")


#author: Karen 
@bot.command(name = 'article', description = '''This command returns a random news article about the pandemic. To view the article, click the link at the top. After reading through, there is an option to answer a comprehension question to gain points. Note that 'True' and 'False' are case sensitive. (100 points)''')
async def random_article(ctx):
  articles = [ ['https://toronto.ctvnews.ca/ontario-enters-step-1-of-covid-19-reopening-your-top-questions-answered-1.5466150', 'Ontario enters Step 1 of COVID-19 reopening. Your top questions answered', 'CTV News', 'This article outlines in detail the current outdoor and gathering restrictions in Ontario as of 6/11.', 'Outdoor gatherings and public events are permitted with a maximum of 15 people.', 'False'], ['https://www.vanityfair.com/news/2021/06/the-lab-leak-theory-inside-the-fight-to-uncover-covid-19s-origins', 'The Lab-Leak Theory: Inside the Fight to Uncover COVID-19’s Origins', 'Vanity Fair', 'This article debunks various myths about the origin of COVID-19 and provides a detailed history of its true origins.', 'The virus causing the global pandemic had leaked from one of the WIV’s labs irun by Shi Zhengli and her colleagues in China.','False'
  ],    ['https://www.weforum.org/agenda/2020/05/covid-19-taking-gaming-and-esports-next-level/', 'COVID-19 is taking gaming and esports to the next level', 'World Economic Forum', 'This article covers the effects of the pandemic on the gaming industry, both positives and negatives.', 'Esports revenues have decreased during the pandemic.','True'],['https://www.bayshore.ca/2020/12/11/10-good-things-that-came-out-of-2020/', '10 Good Things That Came Out of 2020 ', 'Bayshore Healthcare', 'This article lists various social and environmental benefits that have resulted from the COVID-19 pandemic in 2020.', 'About 60% of respondents had changed their opinion on whether or not they’d arrange for themselves or an older loved one to live in a nursing or retirement home.','True']]

  article = articles[randint(0, len(articles) - 1)] 
  randomarticle = discord.Embed(title=f"Read this article by {article[2]}! (click here to open)", url = article[0])
  randomarticle.add_field(name = article[1], value = article[3])

  randomarticle.add_field(name = 'did you read the article? then answer this question for points', value = article[4], inline = False)

  randomarticle.set_footer(text = 'Type in True or False')

  await ctx.reply(embed = randomarticle)

  def answer_check(answer):
    return answer.content == 'True' or answer.content == 'False' and answer.author.id == ctx.author.id
  
  answer = await bot.wait_for('message', check = answer_check)
  answer = answer.content
  if answer == article[5]:
    await ctx.reply('You got it!! :D')
    await updatepoint(ctx.author.id, 100)
    await ctx.reply(f"For answering correctly, {ctx.author} gets 100 points.")
  else:
    await ctx.reply(f"Very sad. {ctx.author} failed, so no points awarded :(.")


#authors: Bonnie + Karen
@bot.command(name = 'daily', description = 'Collect 500 coins everyday (24 hour cooldown)')
@commands.cooldown(1, 60*60*24, 
commands.BucketType.user)
async def daily(ctx):
  # with open('pointstorage.json', 'r') as f:
  #   users = json.load(f)
  # if ctx.author.id not in users:
  #   users[str(ctx.author.id)] = {'points' : 0}

  # with open("pointstorage.json", 'w') as f:
  #   json.dump(users, f)

  dailypoints = 500

  await ctx.reply(f"{dailypoints} daily points collected for {ctx.author}!")

  await updatepoint(ctx.author.id, dailypoints)

#author: Bonnie
@daily.error
async def daily_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(title=f"Slow down, bro.",description=f"You can try again in {int(error.retry_after / 3600)} hours and {int((error.retry_after - (int(error.retry_after / 3600) * 3600)) // 60)} minutes.", color=0xbf75e1)
    await ctx.reply(embed = em)

#author: Bonnie
@bot.command(name = "leaderboard", description = 'Displays top 10 users in the server (amount of points)')
async def display_leaderboard(ctx):
  with open('pointstorage.json', 'r') as f:
    users = json.load(f)
  
  points = []
  for user in users:
    points.append({'id': user, 'points' : users[user]['points']})

  points.sort(key = lambda x: x['points'], reverse = True)

  em = discord.Embed(title = "Top 10 Points", description = "Top 10 non-zero point amounts in this server")
  for i in range(10):
    if i == len(points):
      break
    if points[i]['points'] == 0:
      continue
    user = await bot.fetch_user(int(points[i]['id']))
    em.add_field(name = f"{i + 1}. {user}", value = f"{points[i]['points']}", inline = False)

  await ctx.send(embed = em)


#author: Bonnie
@bot.command(name = 'mypoints', description = 'Displays how many points you have')
async def display_my_points(ctx):
  with open('pointstorage.json', 'r') as f:
    users = json.load(f)
  if str(ctx.author.id) not in users:
    await ctx.reply(f"{ctx.author}, you have 0 points.")
  else:
    await ctx.reply(f"{ctx.author}, you have {users[str(ctx.author.id)]['points']} points.")


#author: Bonnie
@bot.command(name = 'screening', description = '''daily school and child care screening form to ensure that you are safe to go to school/childcare. Reactions: '✅' = yes, '❌' = No, '🔄' = Restart (Cannot restart after survey gives a response)(24 h cooldown) (100 points)''')
@commands.cooldown(1, 60*60*24, 
commands.BucketType.user)
async def screening_form(ctx):
  questions = [
    "In the last 14 days, have you travelled outside of Canada?",
    "Has a doctor, health care provider, or public health unit told you that you should currently be isolating (staying at home)?", 
    "In the last 14 days, have you been identified as a “close contact” of someone who currently has COVID-19?",
    "In the last 14 days, have you received a COVID Alert exposure notification on your cell phone?",
    "Are you currently experiencing any of these symptoms: Fever/chills, cough/barking cough, shortness of breath, decrease/loss of taste/smell, sore throat/difficulty swallowing, runny/stuffy nose, headache, nauseau, vomiting, diarrhea, extreme tiredness, or muscle aches?",
    "Is anyone you live with currently experiencing any new COVID-19 symptoms and/or waiting for test results after experiencing symptoms?"]
  sick = False

  def check(reaction, user):
    return user == ctx.message.author and str(reaction.emoji) == '✅' or user == ctx.message.author and str(reaction.emoji) == '❌' or user == ctx.message.author and str(reaction.emoji) == '🔄'

  run = True
  while run:
    run = False
    for i in range(len(questions)):
      embed=discord.Embed(title= f"{ctx.author.name}'s COVID-19 Screening Form", description=questions[i], color=0xbf75e1)
      
      embed.set_author(name="Official Survey Link", url="https://covid-19.ontario.ca/school-screening/")

      embed.set_footer(text=f"Question {i + 1}/{6}")

      msg = await ctx.send(embed=embed)
      await msg.add_reaction('✅')
      await msg.add_reaction('❌')
      await msg.add_reaction('🔄')

      reaction, user = await bot.wait_for('reaction_add', check=check)
      
      if str(reaction) == '🔄':
        run = True
        break
      if str(reaction) == '✅':
        bad = discord.Embed(title="Not good. You are at risk.", description="1. Contact the school/child care to let them know about this result. \n2. You must isolate (stay home) for 14 days immediately after your return except for a medical emergency. \n3. Follow the advice of public health. \n 4. Retake this screening every day before going to school/child care.")
        bad.set_author(name="Contact your local public health unit or doctor/health care provider for more advice. (link here.)", url="https://www.health.gov.on.ca/en/common/system/services/phu/locations.aspx")
        bad.add_field(name = 'wish to redo the screening form?', value = 'go to official survey by [clicking here](https://covid-19.ontario.ca/school-screening/)')
        sick = True
        await ctx.send(embed = bad)
        break
        
  if not sick:
    good = discord.Embed(title="All good! You're probably fine.", description="Continue to be cautious, wear a mask, etc.")
    good.add_field(name = 'wish to redo the screening form?', value = 'go to official survey by [clicking here](https://covid-19.ontario.ca/school-screening/)')
    await ctx.send(embed = good)

  await updatepoint(ctx.author.id, 100)
  await ctx.send(f"{ctx.author.mention} got 100 points for doing the screening form today.")  

#author: Bonnie
@screening_form.error
async def screening_form_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    slowdown = discord.Embed(title=f"Slow down, bro.",description=f"You've taken today's survey already. You can try again in {int(error.retry_after / 3600)} hours and {int((error.retry_after - (int(error.retry_after / 3600) * 3600)) // 60)} minutes.", color=0xbf75e1)
    slowdown.add_field(name = 'wish to redo the screening form?', value = 'go to official survey by [clicking here](https://covid-19.ontario.ca/school-screening/)')
    await ctx.reply(embed = slowdown)    


#authors: Karen + Bonnie
async def updatepoint(userID, change):
  with open('pointstorage.json', 'r') as f:
    users = json.load(f)

  if str(userID) in users:
    users[str(userID)]['points'] += change  
  else:
    users[str(userID)] = {'points': change}

  with open('pointstorage.json', 'w') as f:
    json.dump(users, f)


keep_alive()
bot.run()

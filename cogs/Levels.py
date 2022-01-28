import json
import discord
from replit import db
from discord.ext import commands



class Levels(commands.Cog):
  """Commands used for user level information"""

  def __init__(self, bot):
    self.bot = bot
    self.lvl_roles = False
    self.roles = None
    self.setup_complete = False


  # event: On Member Join
  @commands.Cog.listener()
  async def on_member_join(self, member):
    
    users = db[f'{member.guild.id}']['levels']['users']
    await self.update_data(users, member)
    db[f'{member.guild.id}']['levels']['users'] = users


  # event: On Message
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot == False:

      
      users = db[f'{message.author.guild.id}']['levels']['users']

      await self.update_data(users, message.author)
      await self.add_experience(users, message.author, 5)
      await self.level_up(users, message.author, message)
      
      db[f'{message.author.guild.id}']['levels']['users'] = users
        
  ## func: Update User Data
  async def update_data(self, users, user):
    if not f'{user.id}' in users:
      users[f'{user.id}'] = {}
      users[f'{user.id}']['experience'] = 0
      users[f'{user.id}']['level'] = 1

  ## func: Add Experience
  async def add_experience(self, users, user, exp):
    users[f'{user.id}']['experience'] += exp

  ## func: Level Up Algorithm
  async def level_up(self, users, user, message):
    
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 3.5))

    if lvl_start < lvl_end:
      users[f'{user.id}']['level'] = lvl_end
      await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}!')

      ## Level Roles Logic
#      if self.lvl_roles:
#        if users[f'{user.id}']['level'] == 5:
#          await user.add_roles(self.roles['level 5'])
#        elif users[f'{user.id}']['level'] == 10:
#          await user.add_roles(self.roles['level 10'])
#        elif users[f'{user.id}']['level'] == 15:
#          await user.add_roles(self.roles['level 15'])
#        elif users[f'{user.id}']['level'] == 20:
#          await user.add_roles(self.roles['level 20'])
#        elif users[f'{user.id}']['level'] == 25:
#          await user.add_roles(self.roles['level 25'])


  # cmd: Toggle Level Roles 
  @commands.has_permissions(administrator=True)
  @commands.command(hidden=True, aliases=['lr'])
  async def levelroles(self, ctx, setting=None):
    
    if str(setting).lower() in ['true', 'enable', 'on']:
      self.lvl_roles = True
      await ctx.send(f'Level Autoroles set to: `{self.lvl_roles}`') 
      
    elif str(setting).lower() in ['disable', 'off', 'false']:
      self.lvl_roles = False
      await ctx.send(f'Level Autoroles set to: `{self.lvl_roles}`')
      
    else:
      await ctx.send('Please use `enable` or `disable`')



  # cmd: Get Level
  @commands.command()
  async def level(self, ctx, member: discord.Member = None):
    """Get user level"""
    
    if member == None:
      id = ctx.message.author.id
      users = db[f'{ctx.guild.id}']['levels']['users']
      lvl = users[str(id)]['level']

      await ctx.send(f'{ctx.message.author.mention} you are at level {lvl}!')

    else:
      id = member.id
      db[f'{member.guild.id}']['levels']['users'] = users
      lvl = users[str(id)]['level']
      
      await ctx.send(f'{member} is at level {lvl}!') 
  

  # cmd: Leaderboard


    # user_list = []
    # leaderboard = {}
    
    # for user_id in list(users):
    #   user_exp = users[str(user_id)]['experience']
    #   leaderboard[user_exp] = int(user_id)
    #   user_list.append(user_exp)

    # sorted_users = sorted(user_list,reverse=True)
    # em = discord.Embed(title = f'Top {x} highest leveled members in {ctx.guild.name}')

    # index = 1
    # for exp_value in sorted_users:

    #   id_ = leaderboard[exp_value]
    #   member = self.bot.get_user(user_id)

    #   em.add_field(name = f'{index}: {member}' , value = f'{exp_value}', inline=False)
      
    #   if index == x:
    #     break
    #   else:
    #     index += 1
        
    # await ctx.send(embed = em)



def setup(bot):
  bot.add_cog(Levels(bot))
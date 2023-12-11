import asyncio
from siegeapi import Auth
from siegeapi import player
import os
import json
import discord


class rainbow:
  async def get_stats(player_name:str):
    auth =  Auth(os.getenv('EMAILUBI'), os.getenv('CONTRAUBI'))
    playerOp = await auth.get_player(name=player_name)
    print(f"Name: {playerOp.name}")
    print(f"Tiempo jugado: {playerOp.total_time_played}")
    print(f"Profile pic URL: {playerOp.profile_pic_url}")
    print(f"Level: {playerOp.level}")
    embeds=[]
    colores=discord.Colour.random()
    embed = discord.Embed(title=f"Rainbow 6 stats for {playerOp.name}", description="", color=colores)
    embed2 = discord.Embed(title=f"Pagina 2", description="", color=colores)
    try:
      await playerOp.load_summaries()
      await playerOp.load_playtime()
      embed.add_field(name="Name", value=f"{playerOp.name}", inline=True)
      embed.add_field(name="Level", value=f"{playerOp.level}", inline=True)
      embed.add_field(name="Xp", value=f"{playerOp.xp}", inline=True)
      embed.add_field(name="Total Time Played", value=f"{playerOp.total_time_played_hours}", inline=True)
      
      
      
      print("------------------------------------------------------------")
      for key, value in playerOp.casual_summary.items():
        # print(f"---{key} : {value}-----")
        for role, summary_data in value.items():
          # print(f"---------{role} : {summary_data}----------")
          if(role == "all" and key==29): #29 es la season actual segun la api esta poronga
            embed.add_field(name="Matches Played", value=f"{summary_data.matches_played}", inline=True)
            embed.add_field(name="Rounds Played", value=f"{summary_data.rounds_played}", inline=True)
            embed.add_field(name="Matches Won", value=f"{summary_data.matches_won}", inline=True)
            embed.add_field(name="Matches Lost", value=f"{summary_data.matches_lost}", inline=True)
            embed.add_field(name="Rounds Won", value=f"{summary_data.rounds_won}", inline=True)
            embed.add_field(name="Rounds Lost", value=f"{summary_data.rounds_lost}", inline=True)
            embed.add_field(name="Kills", value=f"{summary_data.kills}", inline=True)
            embed.add_field(name="Assists", value=f"{summary_data.assists}", inline=True)
            embed.add_field(name="Deaths", value=f"{summary_data.death}", inline=True)
            embed.add_field(name="Headshots", value=f"{summary_data.headshots}", inline=True)
            embed.add_field(name="Melee Kills", value=f"{summary_data.melee_kills}", inline=True)
            embed.add_field(name="Team Kills", value=f"{summary_data.team_kills}", inline=True)
            embed.add_field(name="Opening Kills", value=f"{summary_data.opening_kills}", inline=True)
            embed.add_field(name="Opening Deaths", value=f"{summary_data.opening_deaths}", inline=True)
            embed.add_field(name="Revives", value=f"{summary_data.revives}", inline=True)
            embed.add_field(name="Distance Travelled", value=f"{summary_data.distance_travelled}", inline=True)
            embed.add_field(name="Win-Loss Ratio", value=f"{summary_data.win_loss_ratio}", inline=True)
            embed.add_field(name="Kill-Death Ratio", value=f"{summary_data.kill_death_ratio}", inline=True)
            embed.add_field(name="Headshot Accuracy", value=f"{summary_data.headshot_accuracy}", inline=True)

            
            embed2.add_field(name="Kills Per Round", value=f"{summary_data.kills_per_round}", inline=True)
            embed2.add_field(name="Rounds With a Kill", value=f"{summary_data.rounds_with_a_kill}", inline=True)
            embed2.add_field(name="Rounds With Multi-Kill", value=f"{summary_data.rounds_with_multi_kill}", inline=True)
            embed2.add_field(name="Rounds With KOST", value=f"{summary_data.rounds_with_kost}", inline=True)
            embed2.add_field(name="Rounds Survived", value=f"{summary_data.rounds_survived}", inline=True)
            embed2.add_field(name="Rounds With an Ace", value=f"{summary_data.rounds_with_an_ace}", inline=True)
            embed2.add_field(name="Rounds With Clutch", value=f"{summary_data.rounds_with_clutch}", inline=True)
            embed2.add_field(name="Time Alive Per Match", value=f"{summary_data.time_alive_per_match}", inline=True)
            embed2.add_field(name="Time Dead Per Match", value=f"{summary_data.time_dead_per_match}", inline=True)
            embed2.add_field(name="Distance Per Round", value=f"{summary_data.distance_per_round}", inline=True)

      print("voy a cargar ranked v2")
      await playerOp.load_ranked_v2()

      embed2.add_field(name="Casual Season 31: Matches Won", value=f"{playerOp.casual_profile.wins}", inline=True)
      embed2.add_field(name="Casual Season 31: Matches Lost", value=f"{playerOp.casual_profile.losses}", inline=True)
      embed2.add_field(name="Casual Season 31: Matches Abandons", value=f"{playerOp.casual_profile.abandons}", inline=True)
      embed2.add_field(name="Casual Season 31: Kills", value=f"{playerOp.casual_profile.kills}", inline=True)
      embed2.add_field(name="Casual Season 31: Deaths", value=f"{playerOp.casual_profile.deaths}", inline=True)

      embed2.add_field(name="Ranked Season 31: Max rank", value=f"{playerOp.ranked_profile.max_rank}",inline=True)
      embed2.add_field(name="Ranked Season 31: Rank", value=f"{playerOp.ranked_profile.rank}",inline=True)
      embed2.add_field(name="Ranked Season 31: Prev Rank Points", value=f"{playerOp.ranked_profile.prev_rank_points}",inline=True)
      embed2.add_field(name="Ranked Season 31: Next Rank Points", value=f"{playerOp.ranked_profile.next_rank_points}",inline=True)
      embed2.add_field(name="Ranked Season 31: Matches Won", value=f"{playerOp.ranked_profile.wins}", inline=True)
      embed2.add_field(name="Ranked Season 31: Matches Lost", value=f"{playerOp.ranked_profile.losses}", inline=True)
      embed2.add_field(name="Ranked Season 31: Matches Abandons", value=f"{playerOp.ranked_profile.abandons}", inline=True)
      embed2.add_field(name="Ranked Season 31: Kills", value=f"{playerOp.ranked_profile.kills}", inline=True)
      embed2.add_field(name="Ranked Season 31: Deaths", value=f"{playerOp.ranked_profile.deaths}", inline=True)

      print("Termine de cargar lo de la season 31")
      embeds.append(embed)
      embeds.append(embed2)
      print("------------------------------------------------------------")
      embed.set_image(url=playerOp.profile_pic_url)
    except Exception as err:
      print(err)
      try: 
        print("Intentando cargar lo de la season 31 ---- Version corta por que la larga no deja")
        embed = discord.Embed(title=f"Rainbow 6 stats for {playerOp.name} : Version corta por que la larga no deja", description="", color=discord.Colour.random())
        print("voy a cargar progreso")
        await playerOp.load_progress()
        print("voy a cargar playtime")
        await playerOp.load_playtime()
        print("voy a cargar ranked v2")
        await playerOp.load_ranked_v2()
        print("voy a buscar por casual summary")
        embed.add_field(name="Name", value=f"{playerOp.name}", inline=True)
        embed.add_field(name="Level", value=f"{playerOp.level}", inline=True)
        embed.add_field(name="Xp", value=f"{playerOp.xp}", inline=True)
        embed.add_field(name="Total Time Played", value=f"{playerOp.total_time_played_hours}", inline=True)
        embed.add_field(name="Casual Season 31: Matches Won", value=f"{playerOp.casual_profile.wins}", inline=True)
        embed.add_field(name="Casual Season 31: Matches Lost", value=f"{playerOp.casual_profile.losses}", inline=True)
        embed.add_field(name="Casual Season 31: Matches Abandons", value=f"{playerOp.casual_profile.abandons}", inline=True)
        embed.add_field(name="Casual Season 31: Kills", value=f"{playerOp.casual_profile.kills}", inline=True)
        embed.add_field(name="Casual Season 31: Deaths", value=f"{playerOp.casual_profile.deaths}", inline=True)

        embed.add_field(name="Ranked Season 31: Max rank", value=f"{playerOp.ranked_profile.max_rank}",inline=True)
        embed.add_field(name="Ranked Season 31: Rank", value=f"{playerOp.ranked_profile.rank}",inline=True)
        embed.add_field(name="Ranked Season 31: Prev Rank Points", value=f"{playerOp.ranked_profile.prev_rank_points}",inline=True)
        embed.add_field(name="Ranked Season 31: Next Rank Points", value=f"{playerOp.ranked_profile.next_rank_points}",inline=True)
        embed.add_field(name="Ranked Season 31: Matches Won", value=f"{playerOp.ranked_profile.wins}", inline=True)
        embed.add_field(name="Ranked Season 31: Matches Lost", value=f"{playerOp.ranked_profile.losses}", inline=True)
        embed.add_field(name="Ranked Season 31: Matches Abandons", value=f"{playerOp.ranked_profile.abandons}", inline=True)
        embed.add_field(name="Ranked Season 31: Kills", value=f"{playerOp.ranked_profile.kills}", inline=True)
        embed.add_field(name="Ranked Season 31: Deaths", value=f"{playerOp.ranked_profile.deaths}", inline=True)
        embed.set_image(url=playerOp.profile_pic_url)
        embeds.append(embed)
      except Exception as err:
        print("-----------ERROR en cargar lo de la season 31")
        print(err)
        embed = discord.Embed(title="Error", description="Algo salio mal xd arreglalo facu.", color=discord.Colour.random())
      
      
      
    await auth.close() 
    print("voy a devolver el embed")
    return embeds


class utilitis:
  async def fix_element(elem:str):
    if elem[-1] == ':':
        return '"{}":'.format(elem[:-1])
    else:
        return elem





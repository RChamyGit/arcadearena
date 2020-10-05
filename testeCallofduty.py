import asyncio

import callofduty
from callofduty import Mode, Platform, Title

#
# def SearchActivisionPlayer(IdActvision):
#     return IdActvision
#
# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     return what
#
def say(IdActvision):
    SearchActivisionPlayer(IdActvision)

class SearchActivisionPlayer():
    def __init__(self, IdActvision):
        # client = await callofduty.Login("arcadearenaofc@gmail.com", "ArcadeArena2020")
        async def main(IdActvision):
            print(IdActvision)
            client = await callofduty.Login("arcadearenaofc@gmail.com", "ArcadeArena2020")
            results = await client.SearchPlayers(Platform.Activision, IdActvision, limit=3)
            searchPlayer = results[0]
            profile = await searchPlayer.profile(Title.ModernWarfare, Mode.Warzone)
            level = profile["level"]
            wins = profile['lifetime']['mode']['br']['properties']["wins"]
            kd = profile['lifetime']['mode']['br']['properties']["kdRatio"]
            kills = profile['lifetime']['mode']['br']['properties']["kills"]
            topFive = profile['lifetime']['mode']['br']['properties']["topFive"]
            deaths = profile['lifetime']['mode']['br']['properties']["deaths"]

            # #
            print(f"\n{searchPlayer.username} ({searchPlayer.platform.name})")
            print(f"Level: {level}, K/D Ratio: {round(kd, 2)}, Wins: {wins} , Kills:{kills}, TopFive:{topFive}, Deaths:{deaths}")
            # return  ({'username':f'{searchPlayer.username}'},
            #          {'plataform': f'{searchPlayer.platform.name}',
            #           'level': f'{level}',
            #           'K/D Ratio':f'{round(kd, 2)}',
            #           'Wins': f'{wins}',
            #           'Kills': f'{kills}',
            #           'TopFive': f'{topFive}',
            #           'Deaths': f'{deaths}'
            #           }
            #          )
        asyncio.get_event_loop().run_until_complete(main(IdActvision))



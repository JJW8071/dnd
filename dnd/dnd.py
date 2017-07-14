import discord
import aiohttp
import json
from __main__ import send_cmd_help
from .utils import chat_formatting as chat
from discord.ext import commands

BASEURL = 'http://dnd5eapi.co/api/'

class DND:
    '''D&D Lookup Stuff'''

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def dnd(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @dnd.command(name='spells')
    async def lookup_spells(self, spell=None):
        '''Lookup Spells'''
        if spell is not None:
            print('initiate name query')
        url = '{}{}'.format(BASEURL, 'spells')
        print(url)
        await self.bot.say('URL lookup: '+url)
        await _present_list(self, url)
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")



            # em=discord.Embed(color=discord.Color.red(),title='Spells',description='{} found'.format(count))
            # em.add_field(name='Name',value='\n'.join(r['name'] for r in results))
            # await self.bot.say(embed=em)



    @dnd.command(name='classes')
    async def lookup_classes(self, klass=None):
        '''Lookup Classes'''
        baseurl = BASEURL+'classes'
        #Your code will go here
        await self.bot.say("Lookup Classes initiated.")
        await self.bot.say("<{}>".format(baseurl))

    @dnd.command(name='monsters')
    async def lookup_monsters(self, monster=None):
        '''Lookup Monsters'''
        baseurl = BASEURL+'monsters'
        #Your code will go here
        await self.bot.say("Lookup Monsters initiated.")
        await self.bot.say("<{}>".format(baseurl))

    @dnd.command(name='equipment')
    async def lookup_equipment(self, equiped=None):
        '''Lookup Equpiment'''
        baseurl = BASEURL+'equipment'
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")
        await self.bot.say("<{}>".format(baseurl))


async def _get_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print('_get_file('+url+')')
            json_file = await response.json()
            if json_file is not None:
                return json_file

async def _present_list(self, url):
    json_file = await _get_file(url)
    urllength = len(url)
    print(urllength)
    await self.bot.say('{}'.format(urllength))
    if json_file is not None:
        count = json_file['count']
        results = json_file['results']
        package = []
        for i in range(0,int(count)):
            c = i+1
            package.append('{} {}'.format(c, results[i]['name']))

        # for i, r in enumerate(results):
        #     package.append('{} {}'.format(i, r['name']))

        pages = chat.pagify('\n'.join(package), delims=['\n'], escape=True, shorten_by=8, page_length=500)
        for page in pages:
            await self.bot.say(chat.box(page))
    return


def setup(bot):
    bot.add_cog(DND(bot))

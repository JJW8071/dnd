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
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")
        json_file = await _get_file(url)
        if json_file is not None:
            print(json_file)
            count=json_file['count']
            pring(count)
            results = json_file['results']
            await self.bot.say('count: {}'.format(count))
            package = '{}'.join(results['name'])


            for page in chat.pagify(package, delims=['\n']):
                await self.bot.say(box(page))

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


def setup(bot):
    bot.add_cog(DND(bot))

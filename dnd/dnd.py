import discord
import aiohttp
from __main__ import send_cmd_help
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
        url = '{}{}'.format(BASEURL, 'spells')
        print(url)
        await self.bot.say('URL lookup: '+url)
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")
        file_txt = _get_file(url)
        if file_txt is not None:
            print(file_text)
            await self.bot.say('Debug: Text file arrived.')

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
            file_txt = await response.text()
            if file_txt is not None:
                return file_txt


def setup(bot):
    bot.add_cog(DND(bot))

import discord
import aiohttp
from discord.ext import commands

class DND:
    """D&D Lookup Stuff"""
    baseurl = "http://dnd5eapi.co/api/"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def dnd(self, ctx, *, hargs=''):
        if ctx.invoked_subcommand is None:
            await self.bot.say('DEBUG: hargs = '+ hargs)
            return

    @dnd.command()
    async def spells(self, hargs):
        """Lookup Spells"""
        baseurl = self.baseurl+'spells'
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")
        await self.bot.say("<{}>".format(baseurl))

    @dnd.command()
    async def classes(self, hargs):
        """Lookup Classes"""
        baseurl = self.baseurl+'classes'
        #Your code will go here
        await self.bot.say("Lookup Classes initiated.")
        await self.bot.say("<{}>".format(baseurl))

    @dnd.command()
    async def monsters(self, hargs):
        """Lookup Monsters"""
        baseurl = self.baseurl+'monsters'
        #Your code will go here
        await self.bot.say("Lookup Monsters initiated.")
        await self.bot.say("<{}>".format(baseurl))

    @dnd.command()
    async def equipment(self, hargs):
        """Lookup Equpiment"""
        baseurl = self.baseurl+'equipment'
        #Your code will go here
        await self.bot.say("Lookup Spells initiated.")
        await self.bot.say("<{}>".format(baseurl))

    async def _get_file(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_txt = await response.text()
                if file_txt is not None:
                    await self.bot.say('DEBUG: Got the file.')


def setup(bot):
    bot.add_cog(DND(bot))
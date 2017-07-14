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

    @dnd.command(name='spells', pass_context=True)
    async def lookup_spells(self, ctx, spell=None):
        '''Lookup Spells'''
        CHANNEL = ctx.message.channel
        CATEGORY = 'Spells'
        if spell is None:
            url = '{}{}'.format(BASEURL, CATEGORY)
            menu_pages = await _present_list(self, url, CATEGORY)
            ## // process menu_pages
            await self.cogs_menu(menu_pages)

        elif spell is not None:
            await self.bot.say('spell: {}'.format(spell))

    #
    # @dnd.command(name='classes', pass_context=True)
    # async def lookup_classes(self, klass=None):
    #     '''Lookup Classes'''
    #     baseurl = BASEURL+'classes'
    #     #Your code will go here
    #     await self.bot.say("Lookup Classes initiated.")
    #     await self.bot.say("<{}>".format(baseurl))
    #
    # @dnd.command(name='monsters', pass_context=True)
    # async def lookup_monsters(self, monster=None):
    #     '''Lookup Monsters'''
    #     baseurl = BASEURL+'monsters'
    #     #Your code will go here
    #     await self.bot.say("Lookup Monsters initiated.")
    #     await self.bot.say("<{}>".format(baseurl))
    #
    # @dnd.command(name='equipment', pass_context=True)
    # async def lookup_equipment(self, equiped=None):
    #     '''Lookup Equpiment'''
    #     baseurl = BASEURL+'equipment'
    #     #Your code will go here
    #     await self.bot.say("Lookup Spells initiated.")
    #     await self.bot.say("<{}>".format(baseurl))

    async def cogs_menu(self, ctx, menu_pages: list, message: discord.Message=None, page=0, timeout: int=30):
        """menu control logic for this taken from
           https://github.com/Lunar-Dust/Dusty-Cogs/blob/master/menu/menu.py"""
        cog = menu_pages[page]
        if not message:
            message =\
                await self.bot.send_message(ctx.message.channel, embed=cog)
            await self.bot.add_reaction(message, "⬅")
            await self.bot.add_reaction(message, "❌")
            await self.bot.add_reaction(message, "➡")
        else:
            message = await self.bot.edit_message(message, embed=cog)
        react = await self.bot.wait_for_reaction(
            message=message, user=ctx.message.author, timeout=timeout,
            emoji=["➡", "⬅", "❌"]
        )
        if react is None:
            try:
                try:
                    await self.bot.clear_reactions(message)
                except:
                    await self.bot.remove_reaction(message, "⬅", self.bot.user)
                    await self.bot.remove_reaction(message, "❌", self.bot.user)
                    await self.bot.remove_reaction(message, "➡", self.bot.user)
            except:
                pass
            return None
        reacts = {v: k for k, v in numbs.items()}
        react = reacts[react.reaction.emoji]
        if react == "next":
            next_page = 0
            if page == len(menu_pages) - 1:
                next_page = 0  # Loop around to the first item
            else:
                next_page = page + 1
            return await self.cogs_menu(ctx, menu_pages, message=message,
                                        page=next_page, timeout=timeout)
        elif react == "back":
            next_page = 0
            if page == 0:
                next_page = len(menu_pages) - 1  # Loop around to the last item
            else:
                next_page = page - 1
            return await self.cogs_menu(ctx, menu_pages, message=message,
                                        page=next_page, timeout=timeout)
        else:
            try:
                return await\
                    self.bot.delete_message(message)
            except:
                pass



async def _get_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print('_get_file('+url+')')
            json_file = await response.json()
            if json_file is not None:
                return json_file

async def _present_list(self, url, category):
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

        pages = chat.pagify('\n'.join(package), delims=['\n'], escape=True, shorten_by=8, page_length=750)
        menu_pages = []
        for page in pages:
            em=discord.Embed(color=discord.Color.red(), Title=category, descriptoin=page)
            em.footer(text='From dnd5eapi.co',icon_url='http://www.dnd5eapi.co/public/favicon.ico')
            menu_pages.append(em)
            return menu_pages


def setup(bot):
    bot.add_cog(DND(bot))

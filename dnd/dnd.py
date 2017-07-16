import discord
import aiohttp
import json
from __main__ import send_cmd_help
from .utils import chat_formatting as chat
from discord.ext import commands

numbs = {
    "rewind" : "⏪",
    "next": "➡",
    "back": "⬅",
    "fast_forward": "⏩",
    "exit": "❌",
}

BASEURL = 'http://dnd5eapi.co/api/'
SELECTION = 'Enter selection for more {}information.'.format(CATEGORY)
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
    async def lookup_spells(self, ctx, *, search=None):
        '''Lookup Spells'''
        CATEGORY = 'Spells'
        await self._process_category(ctx, search, CATEGORY)

    @dnd.command(name='features', pass_context=True)
    async def lookup_features(self, ctx, *, search=None):
        '''Lookup Features'''
        CATEGORY = 'Features'
        await self._process_category(ctx, search, CATEGORY)

    @dnd.command(name='classes', pass_context=True)
    async def lookup_classes(self, ctx, *, search=None):
        '''Lookup classes'''
        CATEGORY = 'classes'
        await self._process_category(ctx, search, CATEGORY)

    @dnd.command(name='monsters', pass_context=True)
    async def lookup_monsters(self, ctx, *, search=None):
        '''Lookup Monsters'''
        CATEGORY = 'Monsters'
        await self._process_category(ctx, search, CATEGORY)

    @dnd.command(name='equipment', pass_context=True)
    async def lookup_equipment(self, ctx, *, search=None):
        '''Lookup equipment'''
        CATEGORY = 'equipment'
        await self._process_category(ctx, search, CATEGORY)


    async def _process_category(self, ctx, search, CATEGORY):
        if search is None:
            url = '{}{}'.format(BASEURL, CATEGORY)
            menu_pages = await _present_list(self, url, CATEGORY)
            await self.bot.say('{} pages'.format(len(menu_pages)))
            await self.cogs_menu(ctx, menu_pages, message=None, page=0, timeout=30, CATEGORY)
        elif search is not None:
            if ' ' in search:
                search = search.replace(' ', '+')
            search = search.replace(' ','+')
            url = '{}{}/?name={}'.format(BASEURL, CATEGORY, search)
            json_file = await _get_file(url)
            await self.bot.say('{} search: <{}>'.format(CATEGORY, json_file['results'][0]['url']))

    async def cogs_menu(self, ctx, cog_list: list, message: discord.Message=None, page=0, timeout: int=30, CATEGORY=''):
        """menu control logic for this taken from
           https://github.com/Lunar-Dust/Dusty-Cogs/blob/master/menu/menu.py"""
        cog = cog_list[page]
        if not message:
            message =\
                await self.bot.send_message(ctx.message.channel, embed=cog)
            await self.bot.add_reaction(message, "⏪")
            await self.bot.add_reaction(message, "⬅")
            await self.bot.add_reaction(message, "❌")
            await self.bot.add_reaction(message, "➡")
            await self.bot.add_reaction(message, "⏩")
        else:
            message = await self.bot.edit_message(message, embed=cog)
        react = await self.bot.wait_for_reaction(
            message=message, user=ctx.message.author, timeout=timeout,
            emoji=["➡", "⬅", "❌", "⏪", "⏩"]
        )
        if react is None:
            try:
                await self.bot.say(SELECTION.format(CATEGORY+' '))
                answer = await self.bot.wait_for_message(timeout=timeout, author=ctx.message.author)
                if answer is not None:
                    await self.bot.say('Process choice for choice: {}'.format(answer))
                try:
                    await self.bot.clear_reactions(message)
                except:
                    await self.bot.remove_reaction(message,"⏪", self.bot.user)
                    await self.bot.remove_reaction(message, "⬅", self.bot.user)
                    await self.bot.remove_reaction(message, "❌", self.bot.user)
                    await self.bot.remove_reaction(message, "➡", self.bot.user)
                    await self.bot.remove_reaction(message,"⏩", self.bot.user)
                    # Write URL item processing function (CATEGORY, URL)
            except:
                pass
            return None
        elif react is not None:
            reacts = {v: k for k, v in numbs.items()}
            react = reacts[react.reaction.emoji]
            if react == "next":
                next_page = (page + 1) % len(cog_list)
                return await self.cogs_menu(ctx, cog_list, message=message,
                                            page=next_page, timeout=timeout)
            elif react == "back":
                next_page = (page - 1) % len(cog_list)
                return await self.cogs_menu(ctx, cog_list, message=message,
                                            page=next_page, timeout=timeout)
            elif react == "rewind":
                next_page = (page - 5) % len(cog_list)
                return await self.cogs_menu(ctx, cog_list, message=message,
                                                page=next_page, timeout=timeout)
            elif react == "fast_forward":
                next_page = (page + 5) % len(cog_list)
                return await self.cogs_menu(ctx, cog_list, message=message,
                                                page=next_page, timeout=timeout)
            else:
                await self.bot.say(SELECTION.format(CATEGORY+' '))
                answer = await self.bot.wait_for_message(timeout=10, author=ctx.message.author)
                if answer is not None:
                    await self.bot.say('Process choice for choice: {}'.format(answer))
                    # Write URL item processing function (CATEGORY, URL)
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
    if json_file is not None:
        results = json_file['results']
        package = []
        for i in range(0,int(json_file['count'])):
            c = i+1
            package.append('{} {}'.format(c, json_file['results'][i]['name']))

        pages = chat.pagify('\n'.join(package), delims=['\n'], escape=True, shorten_by=8, page_length=350)
        menu_pages = []

        for page in pages:
            em=discord.Embed(color=discord.Color.red(), title=category, description=chat.box(page))
            em.set_footer(text='From dnd5eapi.co',icon_url='http://www.dnd5eapi.co/public/favicon.ico')
            menu_pages.append(em)

        return menu_pages


def setup(bot):
    bot.add_cog(DND(bot))

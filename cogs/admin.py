from discord.ext import commands
import discord
import contextlib
import discord
import traceback
import io
import time
import datetime
import math
import asyncio
import inspect
import random
import textwrap
from discomaton.factories import bookbinding
import async_timeout
from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import copy
from typing import Union
import datetime
from collections import Counter
global admin_perm_id
admin_perm_id = [404708655578218511]


class Admin():
	def __init__(self, bot):
		self.bot = bot
		self._last_result = None
		self.session = set()


	def cleanup_code(self, content):
		"""Remove code blocks"""
		if content.startswith('```') and content.endswith('```'):
			return '\n'.join(content.split('\n')[1:-1])





	def is_owner(ctx):
		if ctx.author.id in admin_perm_id:
			return True
		return False

	def cleanup_code(self, content):
		'Automatically removes code blocks from the code.'
		if content.startswith('```') and content.endswith('```'):  # remove ```py\n```
			return '\n'.join(content.split('\n')[1:(-1)])
		return content



	@commands.command()
	@commands.is_owner()
	async def say(self, ctx, *, message):
		'Make me say something'
		await ctx.send(message)


	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, *, module):
		"""Unload a module"""
		try:
			t = await ctx.send('<a:AtomicalLoading:474600867274686464> | Loading...')
			self.bot.unload_extension(module)
		except Exception as e:
			await t.edit(content=f'```py\n{traceback.format_exc()}\n```')
		else:
			await t.edit(content=f'<:AtomicalSucces:474568904170274826> | Module `{module}` Succesfully Reloaded!')



	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, *, module):
		"""Load a module"""
		try:
			t = await ctx.send('<a:AtomicalLoading:474600867274686464> | Loading...')
			self.bot.load_extension(module)
		except Exception as e:
			await t.edit(content=f'```py\n{traceback.format_exc()}\n```')
		else:
			await t.edit(content=f'<:AtomicalSucces:474568904170274826> | Module `{module}` Sucesfully Loaded!')

	@commands.command(name='reload', aliases=['r'])
	@commands.is_owner()
	async def _reload(self, ctx, *, module):
		"""Reloads a module."""
		try:
			t = await ctx.send('<a:AtomicalLoading:474600867274686464> | Loading...')
			self.bot.unload_extension(module)
			self.bot.load_extension(module)
		except Exception as e:
			await t.edit(content=f'```py\n{traceback.format_exc()}\n```')
		else:
			await t.edit(content=f'<:AtomicalSucces:474568904170274826> | Module `` {module} `` Succefully Reloaded')





	@commands.command(aliases=['nick'])
	@commands.is_owner()
	async def botnick(self, ctx, *, nick):
		'Change the botnick'
		if nick is None:
			return await ctx.send('<:AtomicalQuestion:474576686873051136> | Hey, please do `a?botnick <nick>`')
		if nick == 'reset':
			await ctx.me.edit(nick='')
			return await ctx.send('<:AtomicalSucces:474568904170274826> | Nick succefully reseted')
		if nick == 'Atomical' and ctx.me.nick is None:
			return await ctx.send('<:AtomicalError:474568988186247178> | That is my default nick')
		if nick == 'reset' and ctx.me.nick is None:
			return await ctx.send('<:AtomicalError:474568988186247178> | My nick is already default')
		if nick is not None:
			await ctx.me.edit(nick=nick)
			return await ctx.send(f"<:AtomicalSucces:474568904170274826> | Bot's nick succefully changed to **{nick}**")







	@commands.command()
	@commands.is_owner()
	async def shutdown(self, ctx):
		'Kills the bot'
		await ctx.send('<:AtomicalDied:474576415363170305> | Shutting down...')
		await ctx.bot.logout()


	@commands.command(pass_context=True, aliases = ['exec', 'evaluate', 'execute'], name='eval')
	async def _eval(self, ctx, *, body: str):
		"""Evaluates a code"""

		env = {
		    'bot': self.bot,
			'ctx': ctx,
			'channel': ctx.channel,
			'author': ctx.author,
			'guild': ctx.guild,
			'message': ctx.message,
			'_': self._last_result
		}


		env.update(globals())

		body = self.cleanup_code(body)
		stdout = io.StringIO()

		to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

		try:
			exec(to_compile, env)
		except Exception as e:
			return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

		func = env['func']
		try:
			with redirect_stdout(stdout):
				ret = await func()
		except Exception as e:
			value = stdout.getvalue()
			await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
		else:
			value = stdout.getvalue()
			try:
				await ctx.message.add_reaction(':AtomicalSucces:474568904170274826')
			except:
				pass


			if ret is None:
				if value:
					await ctx.send(f'```py\n{value}\n```')
			else:
				self._last_result = ret
				await ctx.send(f'```py\n{value}{ret}\n```')








def setup(bot):
	    bot.add_cog(Admin(bot))

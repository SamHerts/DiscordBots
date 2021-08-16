import discord
import sys
import traceback
from discord.ext import commands

from utils.BTsettings import Discord_Token

# Discord Bot Setup
BulletTankDescription = "Bullet Tank Discord Bot - By SamH."

bot = commands.Bot(command_prefix='?',
                   case_insensitive=True,
                   description=BulletTankDescription)


@bot.event
async def on_ready():
    """
    Triggers when bot starts.
    """
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=f"Ready to start a new Game!"))


@bot.event
async def on_command_error(ctx, error):
    """
    The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound, )

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'Load':  # Check if the command being invoked is 'tag list'
            await ctx.send('I could not find that Cog. Please try again.')

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)


@commands.command(name='load', hidden=True)
@commands.is_owner()
async def LoadCog(ctx, *, cog: str):
    """
    Command which Loads a Module.
    """
    try:
        bot.load_extension(f'Cogs.{cog}')
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


@commands.command(name='unload', hidden=True)
@commands.is_owner()
async def UnloadCog(ctx, *, cog: str):
    """
    Command which Unloads a Module.
    """
    try:
        bot.unload_extension(f'Cogs.{cog}')
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


@commands.command(name='reload', hidden=True)
@commands.has_role("Administrator")
async def ReloadCog(ctx, *, cog: str):
    """
    Command which Reloads a Module.
    """
    try:
        bot.unload_extension(f'Cogs.{cog}')
        bot.load_extension(f'Cogs.{cog}')
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')

if __name__ == "__main__":
    bot.run(Discord_Token)

import discord
import sys
import os
import traceback
from asyncio import sleep
# from pathlib import Path
from discord.ext import commands

from utils.BTsettings import Discord_Token

cwd = os.getcwd()
cwd = str(cwd)
print(f"{cwd}\n-----")

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

    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'LoadCog':  # Check if the command being invoked is 'Load'
            await ctx.send('I could not find that Cog. Please try again.')

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(
            ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)
        raise error


@bot.command(
    name='load', description="Load all/one of the bots cogs!", hidden=True
)
@commands.is_owner()
async def load(ctx, cog=None):
    if not cog:
        # No cog, means we reload all cogs
        async with ctx.typing():
            embed = discord.Embed(
                title="Loading all cogs!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )

            for ext in os.listdir("./BulletTank/Cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.load_extension(f"Cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Loaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to Load: `{ext}`",
                            value=e,
                            inline=False
                        )
                    await sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # load the specific cog
        async with ctx.typing():
            embed = discord.Embed(
                title=f"Loading {cog}!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./Cogs/{ext}".strip()):
                # if the file does not exist
                embed.add_field(
                    name=f"Failed to Load: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    bot.load_extension(f"Cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Loaded: `{ext}`",
                        value='\uFEFF',
                        inline=False
                    )
                except Exception:
                    desired_trace = traceback.format_exc()
                    print(desired_trace)
                    embed.add_field(
                        name=f"Failed to Load: `{ext}`",
                        value=desired_trace,
                        inline=False
                    )
            await ctx.send(embed=embed)


@bot.command(
    name='unload', description="Unload all/one of the bots cogs!", hidden=True
)
@commands.is_owner()
async def unload(ctx, cog=None):
    if not cog:
        # No cog, means we reload all cogs
        async with ctx.typing():
            embed = discord.Embed(
                title="Unloading all cogs!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            for ext in os.listdir("./Cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.unload_extension(f"Cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Unloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to Unload: `{ext}`",
                            value=e,
                            inline=False
                        )
                    await sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # load the specific cog
        async with ctx.typing():
            embed = discord.Embed(
                title=f"Unloading {cog}!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./Cogs/{ext}"):
                # if the file does not exist
                embed.add_field(
                    name=f"Failed to Unload: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    bot.unload_extension(f"Cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Unloaded: `{ext}`",
                        value='\uFEFF',
                        inline=False
                    )
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f"Failed to Unload: `{ext}`",
                        value=desired_trace,
                        inline=False
                    )
            await ctx.send(embed=embed)


@bot.command(
    name='reload', description="Reload all/one of the bots cogs!", hidden=True
)
@commands.is_owner()
async def reload(ctx, cog=None):
    if not cog:
        # No cog, means we reload all cogs
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            for ext in os.listdir("./Cogs/"):
                if ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        bot.unload_extension(f"Cogs.{ext[:-3]}")
                        bot.load_extension(f"Cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception as e:
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=e,
                            inline=False
                        )
                    await sleep(0.5)
            await ctx.send(embed=embed)
    else:
        # reload the specific cog
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=0x808080,
                timestamp=ctx.message.created_at
            )
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./Cogs/{ext}"):
                # if the file does not exist
                embed.add_field(
                    name=f"Searching in path: `{os.path}`",
                    value="This path does not exist",
                    inline=False
                )
                embed.add_field(
                    name=f"Failed to reload: `{ext}`",
                    value="This cog does not exist.",
                    inline=False
                )

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    bot.unload_extension(f"Cogs.{ext[:-3]}")
                    bot.load_extension(f"Cogs.{ext[:-3]}")
                    embed.add_field(
                        name=f"Reloaded: `{ext}`",
                        value='\uFEFF',
                        inline=False
                    )
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value=desired_trace,
                        inline=False
                    )
            await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(Discord_Token)

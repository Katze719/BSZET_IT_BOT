import discord
from .simple_embed import simple_embed
from .settings import GuildSettings
from typing import Callable, Coroutine, TypeVar, Any
from functools import wraps
from .log import logger

T = TypeVar('T', bound=Callable[..., Coroutine[Any, Any, Any]])

def admin_required(func: T) -> T:
    """
    Decorator that checks if the user invoking the command is an admin.

    Parameters:
        func (T): The function to be decorated.

    Returns:
        T: The decorated function.

    Raises:
        ValueError: If the context parameter is missing or not the first argument.

    Notes:
        - This decorator checks if the user invoking the command has the 'administrator' permission in the guild.
        - If the user is not an admin, it sends an error message to the user and returns early.
        - If the user is an admin, it calls the decorated function with the given arguments and returns its result.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        logger.info(f"Checking if {ctx.user} is an admin...")
        if not ctx.user.guild_permissions.administrator:
            logger.info(f"{ctx.user} is not an admin.")
            await ctx.response.send_message(embed=simple_embed("Error", "You are not an admin."), ephemeral=True)
            return
        logger.info(f"{ctx.user} is an admin.")
        return await func(*args, **kwargs)
    return wrapper

def experimental(func: T) -> T:
    """
    Decorator that checks if the experimental features are activated for the guild.

    Parameters:
        func (T): The function to be decorated.

    Returns:
        T: The decorated function.

    Raises:
        ValueError: If the context parameter is missing or not the first argument.

    Notes:
        - This decorator checks if the experimental features are activated for the guild by checking the "beta_programm" setting in the GuildSettings.
        - If the experimental features are not activated, it sends an error message to the user and returns early.
        - If the experimental features are activated, it calls the decorated function with the given arguments and returns its result.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        logger.info(f"Checking if {ctx.guild} has activated experimental features...")
        if GuildSettings(ctx.guild).get("beta_programm") != True:
            logger.info(f"{ctx.guild} has not activated experimental features.")
            await ctx.response.send_message(embed=simple_embed('Error', "Experimental Features are not activated."))
            return

        logger.info(f"{ctx.guild} has activated experimental features.")
        return await func(*args, **kwargs)
    return wrapper

def needs_class(func: T) -> T:
    """
    Decorator that checks if the guild has set a class.

    Parameters:
        func (T): The function to be decorated.

    Returns:
        T: The decorated function.

    Raises:
        ValueError: If the context parameter is missing or not the first argument.

    Notes:
        - This decorator checks if the guild has set a class by checking the "class" setting in the GuildSettings.
        - If the guild has not set a class, it sends an error message to the user and returns early.
        - If the guild has set a class, it calls the decorated function with the given arguments and returns its result.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        logger.info(f"Checking if {ctx.guild} has set a class...")
        if not GuildSettings(ctx.guild).get("class"):
            logger.info(f"{ctx.guild} has not set a class.")
            await ctx.response.send_message(embed=simple_embed('Error', "Class is not set.\n Set it with `/set class <classname>`"))
            return
        
        logger.info(f"{ctx.guild} has set a class.")
        return await func(*args, **kwargs)
    return wrapper

import discord
from .simple_embed import simple_embed
from .settings import GuildSettings
from typing import Callable, Coroutine, TypeVar, Any
from functools import wraps

T = TypeVar('T', bound=Callable[..., Coroutine[Any, Any, Any]])

def admin_required(func: T) -> T:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message(embed=simple_embed("Error", "You are not an admin."), ephemeral=True)
            return
        return await func(*args, **kwargs)
    return wrapper

def experimental(func: T) -> T:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        if GuildSettings(ctx.guild).get("beta_programm") != True:
            await ctx.response.send_message(embed=simple_embed('Error', "Experimental Features are not activated."))
            return

        return await func(*args, **kwargs)
    return wrapper

def needs_class(func: T) -> T:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        ctx = args[0]
        if not isinstance(ctx, discord.Interaction):
            raise ValueError("Context parameter missing or not first argument.")
        
        if not GuildSettings(ctx.guild).get("class"):
            await ctx.response.send_message(embed=simple_embed('Error', "Class is not set.\n Set it with `/set class <classname>`"))
            return

        return await func(*args, **kwargs)
    return wrapper

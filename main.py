from discord.utils import get
from bt_utils.cache_handler import cache
import commands
from bt_utils.console import *
from bt_utils import handleJson
from bt_utils.config import cfg
from dhooks import Webhook, Embed
from others import welcome, role_reaction
from others.message_conditions import check_message
from discord.errors import LoginFailure
import discord

client = discord.Client()
SHL = Console(prefix="BundestagsBot")
handleJson.BASE_PATH = __file__
cfg.reload()


@client.event
async def on_member_join(member):
    SHL.output(f"Send Welcome to {member.display_name}.")
    await member.send(embed=welcome.create_embed())
    # member did not accept dm
    for role in cfg.options.get("roles_on_join", []):
        r = get(client.get_guild(531445761733296130).roles, id=int(role))  # TODO: replace guildID
        await member.add_roles(r)


@client.event
async def on_raw_reaction_add(payload):
    await role_reaction.reaction_add(client, payload)


@client.event
async def on_raw_reaction_remove(payload):
    await role_reaction.reaction_remove(client, payload)


@client.event
async def on_message(message):
    if not await check_message(client, message):  # check basic conditions like length and not responding to himself
        return 0

    if message.content.lower().startswith(str(cfg.options["invoke_normal"]).lower()):
        params = commands.parse(message.content, False)
        if params[0].lower() in commands.commands.keys():
            await commands.commands[params[0].lower()](client, message, params[1:])

    elif message.content.lower().startswith(str(cfg.options["invoke_mod"]).lower()):
        params = commands.parse(message.content, True)
        if params[0].lower() in commands.mod_commands.keys():
            await commands.mod_commands[params[0].lower()](client, message, params[1:])


@client.event
async def on_ready():
    # console related
    # ================================================
    SHL.output(f"{red}========================{white}")
    SHL.output("Logged in as")
    SHL.output(client.user.name)
    SHL.output(f"Online in {len(client.guilds)} Guilds.")
    SHL.output(f"{red}========================{white}")

    # discord related
    # ================================================
    if cfg.options.get("use_game", False):
        game = discord.Game(name=cfg.options.get("game_name", "Hello world"))
        await client.change_presence(activity=game)
        SHL.output(f"{game.name} als Status gesetzt.")

    # WebHooks
    # ================================================
    if cfg.options.get("use_webhooks", False):
        template = cfg.options["on_ready"]
        embed = Embed(
            title=template["title"],
            description=template["description"],
            thumbnail_url=template["thumbnail_url"],
            color=int(template["color"], 16)
        )
        for name, link in cfg.options["webhooks"].items():
            Webhook(link).send(embed=embed)
            SHL.output(f"Webhook {name} sent.")

try:
    SHL.output(f"Logging in.")
    client.run(cfg.options["BOT_TOKEN"], reconnect=cfg.options.get("use_reconnect", False))
except LoginFailure:
    SHL.output(f"{red}========================{white}")
    SHL.output(f"{red}Login failure!{white}")
    SHL.output(f"{red}Please check your token.{white}")
except KeyError:
    SHL.output(f"{red}========================{white}")
    SHL.output(f"{red}'BOT_TOKEN' not found in config files!")
except:
    SHL.output(f"{red}========================{white}")
    SHL.output(f"{red}Something went wrong{white}")

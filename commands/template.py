from bt_utils.console import Console
import discord
SHL = Console("BundestagsBot Help")


settings = {
    # mandatory for every command
    'name': 'template',
    # optional parameters
    'channels': ['dm', 'bot'],
    'log': False,  # False is the default value, set to true if needed
    'mod_cmd': False  # False is the default value, set to true if the command should only be allowed to be used by team members
}


async def main(client, message, params):
    # all handling is to be done here
    pass

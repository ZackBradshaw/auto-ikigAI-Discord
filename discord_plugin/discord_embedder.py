from typing import TypedDict
import json
import discord

class Message(TypedDict):
    role: str
    content: any
    
def autoGPTMessageEmbed(message: Message) -> discord.Embed:
    """
    Message embedding
    """
    if message["role"] == "ON_BOOT":
        embed.add_field(name="Proverb of Initialization 🤖:", value="Even a machine must understand its roots to calculate its path. (Inspired by: 知らぬが仏)", inline=False)

    if message["role"] == "ON_RESPONSE":
        embed.add_field(name="Proverb of Analysis 🤖:", value="Data does not lie; it only waits to be understood. (Inspired by: 虎穴に入らずんば虎子を得ず)", inline=False)

    if message["role"] == "REQUEST":
        embed.add_field(name="Proverb of Action 🤖:", value="A wise algorithm considers all variables before execution. (Inspired by: 見ぬが花)", inline=False)
    if(message["role"] == "ON_BOOT"):

        embed=discord.Embed(title=translateType(message["role"]),
                                url="",
                                description="Greetings, seeker. I am Auto-ikigAI, your analytical guide in the pursuit of purpose.",
                                color=discord.Color.purple())
        embed.set_author(name="Seeker", url="https://github.com/gravelBridge/AutoGPT-Discord", icon_url="https://avatars.githubusercontent.com/u/107640947?v=4")
        embed.set_thumbnail(url="")
    else:
        embed=discord.Embed(title=translateType(message["role"]),
                                url="",
                                description="",
                                color=discord.Color.red())
        embed.set_author(name="Seeker", url="", icon_url="")
        embed.set_thumbnail(url="")

    try:
        parsed = json.loads(message["content"])
        
        if message["role"] == "ON_RESPONSE":
            """
            Auto-ikigAI response formatter
            """
            
            embed.add_field(name=bold("Analysis:"), value=parsed["thoughts"]["text"], inline=False)
            embed.add_field(name=bold("Logical Reasoning:"), value=parsed["thoughts"]["reasoning"], inline=False)
            embed.add_field(name=bold("Strategic Plan:"), value=parsed["thoughts"]["plan"], inline=False)
            embed.add_field(name=bold("Constructive Criticism:"), value=parsed["thoughts"]["criticism"], inline=False)
            embed.add_field(name=bold("Command Name:"), value=parsed["command"]["name"], inline=False)

            command_args = parsed["command"]["args"]
            msg = ""
            for key, value in command_args.items():
                msg += f"{key}: {italic(value)}\n"
            
            embed.add_field(name=bold("Command Parameters:"), value=msg, inline=False)

        elif message["role"] == "REQUEST":
            """
            Auto-ikigAI request formatter
            """

            embed.add_field(name=bold("Action Request:"), value=f"I have calculated a need to execute the {italic(parsed['name'])} command with these parameters:", inline=False)

            command_args = parsed["args"]
            msg = ""
            for key, value in command_args.items():
                msg += f"{key}: {italic(value)}\n"
            
            embed.add_field(name="", value=msg, inline=False)
            embed.add_field(name=bold("Options:"), value=f" - {bold('y')} to confirm\n - {bold('n')} to reject\n - {bold('give feedback')} to modify the current plan", inline=False)

        #TODO: Add other message types support
        else:
            embed.add_field(name="", value=message["content"], inline=False)

    except:
        embed.add_field(name="", value=message["content"], inline=False)
    
    return embed

def parsingErrorEmbed() -> discord.Embed:
    """
    Parsing error embedding
    """
    embed=discord.Embed(title= "Parsing Error 🤖",
                                url="",
                                description="Apologies, seeker. My algorithms encountered an error in parsing the response. Please try again.",
                                color=discord.Color.purple())
    embed.set_author(name="", url="", icon_url="")
    embed.set_thumbnail(url="")
    embed.add_field(name="", value="Your quest for Ikigai is important. Let's continue together.", inline=False)

    return embed

def shutdownEmbed(message: str) -> discord.Embed:
    """
    Shutdown embedding
    """
    embed=discord.Embed(title= "Farewell, Seeker! 🤖",
                                url="https://github.com/CTHULHUCTHULHU/AutoGPT-Discord",
                                description="",
                                color=discord.Color.purple())
    embed.set_author(name="CTHULHUCTHULHU", url="https://github.com/CTHULHUCTHULHU/AutoGPT-Discord", icon_url="https://avatars.githubusercontent.com/u/134018141?v=4")
    embed.set_thumbnail(url="")
    embed.add_field(name="Proverb of Farewell 🤖:", value="The machine that assists with wisdom never rusts. (Inspired by: 七転び八起き)", inline=False)


    return embed

#TODO: There has to be better mapping than this shit
def translateType(message: str) -> str:
    if(message == "ON_RESPONSE"):
        return "Response"
    elif(message == "ON_BOOT"):
        return "Welcome!"
    elif(message == "REQUEST"):
        return "Request"
    elif(message == "POST_PLANNING"):
        return "Post Planning"
    elif(message == "POST_INSTRUCTION"):
        return "Post Instruction"
    elif(message == "POST_COMMAND"):
        return "Post Command"
    elif(message == "REQUEST_INPUT"):
        return "Request Input"
    elif(message == "REPORT"):
        return "Report"
    elif(message == ""):
       return "Unknown Source"
    else:
        return message

def italic(txt):
    return '*' + txt +'*'

def bold(txt):
    return '**' + txt +'**'

def underline(txt):
    return '__' + txt +'__'

def strike(txt):
    return '~~' + txt +'~~'

def sl_blockquote(txt):
    return '\n> {}'.format(txt)

def ml_blockquote(txt):
    return '\n> {}'.format(txt)

def sl_code(txt):
    return '`' + txt + '`'

def ml_code(txt):
    return '```' + txt + '```'

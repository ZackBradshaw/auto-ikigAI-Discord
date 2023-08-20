import discord
import os
from typing import TypedDict
from colorama import Fore
from discord.ext import tasks, commands
from .discord_embedder import autoGPTMessageEmbed, parsingErrorEmbed, shutdownEmbed
import json
import time

description = "An AutoGPT discord bot that allows users to interact with their AutoGPT instance through discord."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


BOT_TOKEN = ""
AUTHORIZED_USER_IDS = []
BOT_PREFIX = ""
CHANNEL_ID = ""

userReply = []
messagesToSend = []
waitingForReply = [False]

finishedLoggingIn = [False]

class Message(TypedDict):
    role: str
    content: str

class AutoGPT_Discord(commands.Cog):

    async def on_ready(self):

        print(Fore.GREEN + f'Bot logged in as {self.user} (ID: {self.user.id})')
        print(Fore.GREEN + '------')
        finishedLoggingIn[0] = True

    async def setup_hook(self) -> None:
        self.background.start()
    

    @tasks.loop(seconds=1) 
    async def background(self):
        channel = self.get_channel(int(CHANNEL_ID))

        if len(messagesToSend) > 0:
            for message in messagesToSend:
                try:
                    await channel.send(embed = autoGPTMessageEmbed(message))
                except:
                    try:
                        await channel.send("```" + message["role"] + message["content"] + "```")
                    except:
                        await channel.send(embed = parsingErrorEmbed())
                messagesToSend.remove(message)
        
        if waitingForReply[0]:
            def check(m):
                return str(m.author.id) in AUTHORIZED_USER_IDS and m.channel == channel
        
            print(Fore.YELLOW + "Waiting for user to reply via discord...")
            user_input = await self.wait_for("message", check = check)
        
            print(Fore.GREEN + "User replied: " + user_input.content)

            userReply.append(user_input.content)

            waitingForReply[0] = False


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith(BOT_PREFIX + "shutdown") and str(message.author.id) in AUTHORIZED_USER_IDS:
            await message.reply(embed = shutdownEmbed("AutoGPT Discord Bot going back to sleep. Bye!"))
            os._exit(0)
        
        elif message.content.startswith(BOT_PREFIX + "shutdown"):
            await message.reply(embed = shutdownEmbed("You aren't authorized dummy >:("))

    @background.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


def required_info_set():
    global BOT_TOKEN
    global AUTHORIZED_USER_IDS
    global BOT_PREFIX
    global CHANNEL_ID
    global ASK_FOR_INPUT
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    authUsers = os.getenv("AUTHORIZED_USER_IDS")
    AUTHORIZED_USER_IDS = authUsers.split(",")
    BOT_PREFIX = os.getenv("BOT_PREFIX")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    ASK_FOR_INPUT = os.getenv("ASK_FOR_INPUT")

    return BOT_TOKEN and AUTHORIZED_USER_IDS and BOT_PREFIX and CHANNEL_ID and ASK_FOR_INPUT
    
def commandUnauthorized(feedback):
    return "This command was not authorized by the user. Do not try it again. Here is the provided feedback: " + feedback

    @commands.command(name="start", description="Start Auto-GPT with optional parameters")
        async def start_auto_gpt(self, ctx, gpt4only: bool = False, gpt3only: bool = False):
            # Check permissions (replace with appropriate logic)
            if str(ctx.author.id) not in AUTHORIZED_USER_IDS:
                await ctx.send("You do not have permission to execute this command.")
                return
    
            # Build the docker command
            command = ["docker-compose", "run", "-u", "root", "--rm", "auto-gpt"]
            if gpt4only:
                command.append("--gpt4only")
            if gpt3only:
                command.append("--gpt3only")
    
            # Run the command
            try:
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    await ctx.send("Auto-GPT has been started successfully.")
                else:
                    await ctx.send(f"An error occurred: {result.stderr}")
            except Exception as e:
                await ctx.send(f"An unexpected error occurred: {str(e)}")

def run_bot():
    global client
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    client = commands.Bot(command_prefix=BOT_PREFIX, description=description, intents=intents)
    client.add_cog(AutoGPT_Discord(client))
    client.run(BOT_TOKEN)

def wait_for_user_input(name, args):
    #TODO: Thats sus, probably can do without dumps nesting
    messagesToSend.append(Message(role="REQUEST", content=json.dumps({'name': name, 'args': args})))
    waitingForReply[0] = True

    while waitingForReply[0]:
        time.sleep(1)

    if userReply[0].lower() == "y":
        userReply.pop(0)
        return "Authorized"
    if userReply[0].lower() == "n":
        userReply.pop(0)
        return "Unauthorized"
    else:
        return userReply.pop(0)

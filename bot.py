import discord
import query_sd
import asyncio

CMD = '/sd '
IMG_PATH = ''
USER_MENTION = None
NEW_IMG = False
PROMPT = ''

async def send_message(message, user_message, user):
    try:
        ret = query_sd.add_query(user_message, user)
        await message.channel.send(ret)
    except Exception as e:
        print(e)


'''called by query_sd.call_sd() once stable diffusion is done'''
def post_sd_output(path, user, prompt):
    global IMG_PATH, NEW_IMG, USER_MENTION, PROMPT
    IMG_PATH = path
    USER_MENTION = user
    NEW_IMG = True
    PROMPT = prompt


def run_discord_bot():
    TOKEN = 'MTA0NzczMDQ1NDQzMTc5NzI2OA.GyMD76.VTE5ZflTR1Qzx83tcPsw7gWnPvHXlUgKYOZi_Q'
    channel_id = 1047724047506620470 # right click channel, copy ID
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    async def post_sd():
        global NEW_IMG
        while True:
            if NEW_IMG:
                NEW_IMG = False
                channel = client.get_channel(channel_id)
                await channel.send(f'{USER_MENTION} prompt: "{PROMPT}"', file=discord.File(IMG_PATH))
            await asyncio.sleep(1)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        print(client.users)
        client.loop.create_task(post_sd())

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        mention_user = message.author.mention
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} sent "{user_message}" in channel "{channel}"')

        if user_message[0:len(CMD)] == CMD:
            user_message = user_message[len(CMD):]
            print(f'user {username} requested "{user_message}" in channel "{channel}"')
            await send_message(message, user_message, mention_user)

    client.run(TOKEN)
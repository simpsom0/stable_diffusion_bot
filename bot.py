import discord
import query_sd
import asyncio

CMD = '/sd '
IMG_PATH = ''
USER_MENTION = None
NEW_IMG = False
PROMPT = ''
HELP_MSG = 'Hello! I run stable diffusion prompts, type \'/sd\' <prompt> where <prompt> is what you want to generate an image of'
RES_MSG = 'see https://invoke-ai.github.io/InvokeAI/features/CLI/ for a full list of arguments you can use\n\tsome useful ones are:\n\t\t-s 1-300: increases the number of steps (default: 50)\n\t\t-n 1-20: specifies the number of images to output\n\t\t-U 1,2, or 4: upscales the output image by a factor of 1, 2, or 4'

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


def start_discord_bot(run):
	while run.is_set():
		try:
			run_discord_bot()
		except:
			print('bot crashed, restarting...')


def run_discord_bot():
	TOKEN = 'MTA0NzczMDQ1NDQzMTc5NzI2OA.GQncXi.8KApWA5TDs6oHgxzW_pw4YlU-j_FCiZiAgAw5w'
	channel_id = 1049426852852269137 # right click channel, copy ID
	intents = discord.Intents.default()
	intents.message_content = True
	client = discord.Client(intents=intents)

	async def post_sd():
		global NEW_IMG
		while True:
			if NEW_IMG:
				NEW_IMG = False
				channel = client.get_channel(channel_id)
				if IMG_PATH == 'err':
					await channel.send(f'{USER_MENTION} prompt: "{PROMPT}" caused an error. Please try again (don\'t break me please, im fragile)') 
				else:
					await channel.send(f'{USER_MENTION} prompt: "{PROMPT}"', file=discord.File(IMG_PATH))
			await asyncio.sleep(1)

	@client.event
	async def on_ready():
		print(f'{client.user} is now running!')
		# print(client.users)
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
			# sends the status
			if user_message[len(CMD):len(CMD)+6] == 'status':
				status = query_sd.get_status()
				await message.channel.send(status)
			elif user_message[len(CMD):len(CMD)+4] == 'help':
				status = query_sd.get_status()
				await message.channel.send(f'{HELP_MSG}\n\n{RES_MSG}')
			# starts sd process
			else:
				user_message = user_message[len(CMD):]
				print(f'user {username} requested "{user_message}" in channel "{channel}"')
				await send_message(message, user_message, mention_user)

	client.run(TOKEN)

import glob
import os
import subprocess
from time import sleep
import bot

PROMPTS = []
USERS = []
MAX_QUEUE_SIZE = 100
RUNNING = False
CUR_PROMPT = ''
PYTHON_EXE = '/home/csguest/anaconda3/bin/python3.9'

'''called by bot.send_message'''
def add_query(message, user):
	global PROMPTS, USERS
	t_prompts = len(PROMPTS)
	
	if t_prompts <  MAX_QUEUE_SIZE:
		print('adding to queue...')
		PROMPTS.append(message)
		USERS.append(user)
		print(f'queue: {PROMPTS}')
		if RUNNING:
			return f'added "{message}" to queue in slot {t_prompts+2}'
		return f'added "{message}" to queue in slot {t_prompts+1}'
	else:
		return 'I am too busy right now, please wait until a previous prompt finishes then resubmit\nlove you, bye!'


def start_sd(run):
	while run.is_set():
		try:
			call_sd(run)
		except:
			print('stable_diffusion crashed... restarting')


'''looping function that checks for new instances of PROMPTS, then runs SD'''
def call_sd(run):
	global PROMPTS, USERS, RUNNING, CUR_PROMPT
	new_prompt = False

	while run.is_set():
		if len(PROMPTS) != 0 and not new_prompt:
			CUR_PROMPT = PROMPTS.pop(0)
			user = USERS.pop(0)
			new_prompt = True

		if new_prompt:
			new_prompt = False
			RUNNING = True
			cmd = f'source /home/csguest/anaconda3/etc/profile.d/conda.sh && conda activate invokeai && python {os.getcwd()}/InvokeAI/scripts/invoke.py --from_file "{os.getcwd()}/prompt.txt" && conda deactivate'
			# print('this is me, calling stable diffusion...')
			print(f'prompt: {CUR_PROMPT}')
			os.system('rm prompt.txt')
			with open('prompt.txt', 'w') as fp:
				fp.write(CUR_PROMPT)

			# print(os.getcwd())
			# print(cmd)
			try:
				p = subprocess.Popen(
					cmd,
					shell=True,
					cwd=f'{os.getcwd()}/InvokeAI/',
					executable='/bin/bash',
					stdout=subprocess.PIPE, 
					stderr=subprocess.PIPE
				)
				out, err = p.communicate(timeout=600)
				p.kill()
			except subprocess.TimeoutExpired:
				print('timeout expireeded')
				p.kill()
				out, err = p.communicate()
				# needs to be handled by parent try-catch
				print('first exception hit')
				raise Exception('AHHHHHHHHHHHHHHHH')
				break;

			# un comment this to debug
			# throws error on printing 'err' if blank
			# try:
			# 	print('\n')
			# 	print('out:')
			# 	print(out.decode('ascii'))
			# 	print('err:')
			# 	print(err.decode('ascii'))
			# 	print('\n')
			# except:
			# 	print('o well')
			# print('finished calling SD')

			try:
				# returns full path to imgs
				imgs = glob.glob(f'{os.getcwd()}/outputs/*.png')

				if len(imgs) > 0:
					# post all images to discord
					for i in range(len(imgs)):
						os.system(f'mv {imgs[i]} ./outputs/output{i}.png')
						bot.post_sd_output(f'./outputs/output{i}.png', user, CUR_PROMPT)
						sleep(4)
					sleep(5) # should wait until the bot has posted to the channel
					# delete all images
					for i in range(len(imgs)):
						os.system(f'rm ./outputs/output{i}.png')
				else:
					bot.post_sd_output('err', user, CUR_PROMPT)
			except Exception as e:
				# have this handled by parent try catch
				print('second exception hit')
				print(e)
				break

			CUR_PROMPT = ''
			RUNNING = False
		sleep(1)


def get_status():
	return f'running: "{CUR_PROMPT}"'

def clean_up():
	pass

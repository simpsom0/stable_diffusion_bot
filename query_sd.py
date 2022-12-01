import os
from time import sleep
import bot

PROMPTS = []
USERS = []
MAX_QUEUE_SIZE = 6
PYTHON_EXE = 'need the absolute path to the pc\'s python.exe'


'''called by bot.send_message'''
def add_query(message, user):
    global PROMPTS, USERS
    t_prompts = len(PROMPTS)
    
    if t_prompts <  MAX_QUEUE_SIZE:
        print('adding to queue...')
        PROMPTS.append(message)
        USERS.append(user)
        return f'added "{message}" to queue in slot {t_prompts+1}/{MAX_QUEUE_SIZE}'
    else:
        return 'I am too busy right now, please wait until a previous prompt finishes then resubmit\nlove you, bye!'


'''looping function that checks for new instances of PROMPTS, then runs SD'''
def call_sd():
    global PROMPTS, USERS
    prompt = ''
    new_prompt = False

    while True:
        if len(PROMPTS) != 0 and not new_prompt:
            prompt = PROMPTS.pop(0)
            user = USERS.pop(0)
            print(f'call_sd: grabbed prompt: {prompt}')
            new_prompt = True

        if new_prompt:
            new_prompt = False

            print('this is me, calling stable diffusion...')
            print(f'prompt: {prompt}')
            bot.post_sd_output('images/patrick.jpg', user, prompt)
            # call stable diffusion
            # os.system(
            #     f'{PYTHON_EXE} ./scripts/invoke.py --from_file \"prompts/cur_prompt.txt\"'
            # )
            prompt = ''
        sleep(1)

def get_progress():
    pass
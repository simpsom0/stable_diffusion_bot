from time import sleep
import bot
import query_sd
import threading
import os
import signal

THREADS = []
PID = None
RUN = threading.Event()

def main():
	global PID, RUN

	RUN.set()
	THREADS.append(threading.Thread(target=bot.start_discord_bot, args=[RUN]))
	THREADS.append(threading.Thread(target=query_sd.start_sd, args=[RUN]))

	for thread in THREADS:
		thread.start()
	for thread in THREADS:
		thread.join()


def backup(prompts, users):
	global THREADS

	with open('backup/prompts.txt', 'w') as fp:
		for prompt in prompts:
			fp.write(f'{prompt}\n')
	with open('backup/users.txt', 'w') as fp:
		for user in users:
			fp.write(f'{user}\n')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		RUN.clear()
		for thread in THREADS:
			print(f'thread alive?: {thread.is_alive()}')
			# thread.join()
		

import bot
import query_sd
import threading

THREADS = []
# RUN_SD = threading.Event()

def main():
    # bot.run_discord_bot()
    THREADS.append(threading.Thread(target=bot.run_discord_bot))
    THREADS.append(threading.Thread(target=query_sd.call_sd, daemon=True))

    # with the event flag, this will run the threads
    for thread in THREADS:
        thread.start()

    for thread in THREADS:
        thread.join()


if __name__ == '__main__':
    # RUN_SD.set()

    try:
        main()
    except KeyboardInterrupt:
        # RUN_SD.clear()

        # for thread in THREADS:
        #     thread.join()
        # print('threads (hopefully) successfully closed')

        for thread in THREADS:
            print(f'thread alive?: {thread.is_alive()}')
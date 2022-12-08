# stable_diffusion_bot

## Instructions

- the code as is, will not run.
  - this is a repository that holds the scripts used solely for the bot
- in order to run this code, you will need to clone the following repo into this directory
  - https://github.com/invoke-ai/InvokeAI
  - meaning, the cloned code needs to be in a folder with the name 'InvokeAI'
  - there are various steps you need to follow in order to get it up and running
    - their installation documentation is pretty straightforward
      - https://invoke-ai.github.io/InvokeAI/installation/INSTALL_MANUAL/?h=install+conda
- the code is stored on /Users/csguest/Documents/COSI-Stable-Diffusion-Bot/
  - there is a tmux session running the bot in the background

## Code Structure

- there are three files:
  - main.py
    - spawns two threads - one to run the bot, and one to call the stable diffusion script
      - there might be a non-multithreaded way to do it, but this was a very quick build and I didn't want to deal with the I/O hanging while stable diffusion ran
  - bot.py
    - main driver for the discord bot
    - run_discord_bot() has all the discord interaction functions
    - send_message() is used to update the prompt queue in query_sd.py
    - post_sd_output() is called from query_sd.py once the image generation is finished
  - query_sd.py
    - main driver for the stable diffusion script
    - call_sd() is where the actual calling the script happens
      - it updates a prompt file, then calls the stable diffusion script with that as an input

## Improvements to be made

- I need to double check that this is actually utilizing the dual GPU's that computer has
  - I'm suspicious it isn't, and if I'm right the speed can increase by orders of magnitude
- The commands need to not be plain text
- Some of my error handling is redundant and unecessary, would be worth cleaning that up
  - overall a good amount of this can be optimized, this project was rushed
- Prompts that are multiple lines need to be reduced to one long one, otherwise each line will be a prompt
- Empty quotes breaks it for some reason, that could just be not allowed
- There should be hard caps to some of the options (like -n so 100 images can't be requested and clog the queue)

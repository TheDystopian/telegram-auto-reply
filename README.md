# Telegram Auto Replier

This is a project, that I made for fun

Idea was to reply on tiktok links as "cringe!". Then I decided to expand the program functionality, because why not. Now it's very configurable - you can select multiple various words to detect, multiple replies, multiple chats to monitor, multiple chats to report in (admin chats) and made come kind of setup script 

Based on [Telethon library](https://github.com/LonamiWebs/Telethon)

## Dependencies
[Telethon](https://github.com/LonamiWebs/Telethon) - `pip install telethon`

Tk - `pip install tk` - optional (for File Chooser GUI)

## First start 
You will need to get a Telegram App API ID and Telegram App API Hash.
Here's a [manual from Telegram](https://core.telegram.org/api/obtaining_api_id) how to get them. Remember to keep them as a secret!

Type `python AutoReply.py` in the terminal to launch auto reply script.

Setup script will launch automatically. It will guide you.
After setup, Telethon will ask you to sign in to create session file

Type `python config.py` in the terminal to configure. Config can be changed on the fly. To update it, you will need to enter `#update` to the admin chat. Then you will see options as a list. To update exact option, type `#update <OptionToUpdate>` in admin chat. If you want to update everything from list, type `#update all`.
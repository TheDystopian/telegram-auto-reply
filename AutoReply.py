import os

# Random that gives unique results each time (resets when there's no variants)
memory_reply = []
memory_files = []

def unique_result(randomize_array,memory_type):
    if len(memory_type) == len(randomize_array):
        memory_type.clear()
    from random import choice 

    randomize = choice(randomize_array)
    while randomize in memory_type:
        randomize = choice(randomize_array)
    memory_type.append(randomize)
    return randomize

# Get chat name
def chat_name(chat):
    try:
        name = str(chat.title)
    except AttributeError:
        name = str(chat.username)
    return name

# Get Config
def ConfUpd():
    from configparser import ConfigParser
    from ast import literal_eval

    config = ConfigParser()

    if not os.path.exists('options.ini'):
        from subprocess import call
        call(["python", "config.py"])
    
    config.read('options.ini')

    for sect in config.sections():
        for key,val in config.items(sect):
            if val.startswith('[') and val.endswith(']'):
                globals()[key] = literal_eval(val)
            else:
                globals()[key] = val

def main():
    from telethon.sync import TelegramClient, events
    from re import findall
    with TelegramClient(os.getlogin(), api_id, api_hash) as client:
        print('Auto response active')
        # Update config on "!upd"
        @client.on(events.NewMessage(chats=chat_rep, pattern='!upd$'))
        async def confupd(event):
            ConfUpd()
            await event.reply('Config updated')

        # Monitoring
        @client.on(events.NewMessage(chats=chat_mon, pattern='^(?!\!upd$)'))
        async def response_handler(event):
            for i in range(len(pattern_array)):
                if findall(pattern_array[i], event.message.message) != []:
                    print('Trigger word detected')

                    chat = await event.get_chat()
                    username = await event.get_sender()
                    reply = unique_result(reply_array,memory_reply)
                    await event.reply(f'{reply}'.format(u=username.username))
                    
                    if src_dir is not None:
                        file_reply = unique_result([f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir,f))],memory_files)
                        await client.send_file(chat,os.path.join(src_dir,file_reply),reply_to=event.message)

                    for i in range(len(chat_rep)):
                        await client.send_message(chat_rep[i],f'Trigger word detected in "{chat_name(chat)}"\nIt was sent by "{str(username.username)}" \nReplied with file "{file_reply}"')
                    break

        client.run_until_disconnected()

if __name__ == "__main__":
    ConfUpd()
    main()
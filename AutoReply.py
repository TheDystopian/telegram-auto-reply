from dataclasses import dataclass

# Random that gives unique results each time (resets when there's no variants left)
memory_reply = []
memory_files = []

async def unique_result(randomize_array,memory_type):
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

# Programs's core - auto replier
def AutoReply():
    from telethon.sync import TelegramClient, events
    with TelegramClient(os.getlogin(), api_id.val, api_hash.val) as client:
        print('Auto response active')

        # Update config on #update
        @client.on(events.NewMessage(chats=chat_adm.val, pattern='^#update'))
        async def confupd(event):

            # You can write to the admin chat what to update
            upd_dict = {'chat_mon':[1,'monitored','chats','monitor','monitored chats'],
                        'chat_adm':[2,'admin','chats','admin chats'],
                        'pattern_array':[3,'trigger','words','trigger words'],
                        'reply_array':[4,'replies']
            }

            # "#update" detection
            if event.message.message in '#update':
                await event.respond('Update:\n1 - Monitored chats\n2 - Admin chats\n3 - Trigger words\n4 - Replies')
            else:
                # find what to update
                for key in upd_dict.keys():
                    if event.message.message.replace('#update ','').lower() in upd_dict[key]:
                        # Call update method and report 
                        globals()[key].update()
                        await event.reply(f'Updated {upd_dict[key][-1]}')
        
        # Monitorind monitored chat  
        @client.on(events.NewMessage(chats=chat_mon.val, pattern='^(?!\#update)'))
        async def response_handler(event):
            # Find trigger word in new message
            for patterns in pattern_array:
                if event.message.message.find(patterns):
                    print('Trigger word detected')

                    # Send reply
                    chat = await event.get_chat()
                    username = await event.get_sender()
                    await event.reply(f'{await unique_result(reply_array.val,memory_reply)}'.format(u=username.username))

                    # Send file
                    if src_dir is not None:
                        file_reply = await unique_result([f for f in os.listdir(src_dir.val) if os.path.isfile(os.path.join(src_dir.val,f))],memory_files)
                        await client.send_file(chat,os.path.join(src_dir.val,file_reply),reply_to=event.message)

                    # Report to all admin chats
                    for report in chat_adm.val:
                        await client.send_message(report,f'Trigger word detected in "{chat_name(chat)}"\nIt was sent by "{str(username.username)}" \nReplied with file "{file_reply}"')

        client.run_until_disconnected()

# Data class for cofig values
# sect - section, key - key, val - value
# .update - updates config
@dataclass
class vals:
    
    sect: str
    key: str
    val: int

    def __post_init__(self):
        if self.val.startswith('['):
            self.val = literal_eval(self.val)

    def update(self):
        config.read('options.ini')
        if self.val == list: self.val = literal_eval(config.get(self.sect,self.key))
        else: self.val = config.get(self.sect,self.key)


if __name__ == "__main__":
    # Detect first start by searching config file
    import os
    if not os.path.exists('options.ini'):
        from subprocess import call
        call(["python", "config.py"])
    

    # initialize config
    from configparser import ConfigParser
    from ast import literal_eval

    config = ConfigParser()
    config.read('options.ini')
    
    for sect in config.sections():
        for key,value in config.items(sect):
            globals()[key] = vals(sect,key,value)

    # Start Auto Reply
    AutoReply()
    print("A'right, I completed my job. Exiting...\n")

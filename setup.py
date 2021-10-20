from os import path

# Universal Confirmation Function
def confirm(phrase, default=None):
    # True/False Dictionary
    yes_no = {'yes':{'yes','y', 'ye'},'no':{'no','n'}}
    
    if default is True:
        yes_no['yes'].add('')
        phrase += ' [Y/n]: '
    elif default is False:
        yes_no['no'].add('')
        phrase += ' [y/N]: '
    elif default is None: phrase += ' [y/n]: '
    else: raise TypeError

    while True:
        choice = input(phrase).lower()
        if choice in yes_no['yes']: return True
        elif choice in yes_no['no']: return False
        else: print('Wrong input!')

# Universal Input Function
def input_verify(phrase, phrase_confirm='', phrase_add='', phrase_int_or_string='',doesnt_meet_cond_str='Wrong Input!',is_int=False, multiple=False, askvalid=True,cond='True',confirm_default=[True,True,True]):
    if is_int is None: int_unknown = True
    else: int_unknown = False
    if multiple: out_arr = []

    while True:
        if int_unknown: is_int = confirm(phrase_int_or_string, confirm_default[2])
        if not is_int:
            out = input(phrase)
        else:
            while True:
                try:
                    out = int(input(phrase))
                    break
                except ValueError:
                    print('Wrong Input!')
        
        # Eval is slow, but I can't find any other solutions to make dynamic if statement 
        if not eval(cond.format(out=out)):
            print(doesnt_meet_cond_str)
            continue
        if not askvalid or confirm(phrase_confirm.format(out=out), confirm_default[0]):
            if not multiple: return out
            out_arr.append(out)
        if not confirm(phrase_add.format(out=out), confirm_default[1]):
            return out_arr

# Function dictionary
conf_dict = {'API': ['api_id','api_hash'],
             'Files':['src_dir'],
             'Chats':['chat_mon','chat_rep'],
             'Patterns':['pattern_array'],
             'Replies':['reply_array']}

def API():
    return [input_verify('Enter Telegram API ID (You can get it from my.telegram.com)\n', 'Use Telegram API ID "{out}"?',is_int=True),\
        input_verify('Enter Telegram API Hash (You can get it from my.telegram.com)\n','Use Telegram API Hash "{out}"', cond='len(out) == 32',doesnt_meet_cond_str='Entered Telegram API Hash is not 32 chars long!\n')]


def Files():
    if confirm('Choose folder to post media from?', default=True):
        while True:
            if confirm('Use GUI to choose folder (Tk required. Install with "pip install Tk")?', True):
                from tkinter import Tk, filedialog
                from platform import system
                if system() == 'Windows':
                    # Fix scaling in Windows
                    from ctypes import windll
                    windll.shcore.SetProcessDpiAwareness(1)
                tk = Tk()
                tk.withdraw()
                tk.attributes('-topmost', True)
                while True:
                    src_dir = filedialog.askdirectory()
                    if confirm(f'Take media from "{src_dir}"?',True): break
            else:
                src_dir = input_verify('Enter directory\n','Take media from {out}?',doesnt_meet_cond_str='Wrong folder!',cond='path.exists({out})')
            return [src_dir]
    else:
        return ['None']

def Chats():
    return [input_verify('Enter chat to monitor\n', 'Add "{out}" to the list of monitored chats?', 'Add more chats to monitor?', 'Enter monitored chat by User ID?',is_int=None, multiple=True, confirm_default=[True,False,False]),\
        input_verify('Enter chat to report in\n', 'Add "{out}" to the list of chats to report in?', 'Add more chats to report in?', 'Enter chat to report in by User ID?',is_int=None, multiple=True,confirm_default=[True,False,False])]

def Patterns():
    return [input_verify('Enter trigger phrase\n', 'Add "{out}" to trigger phrases?', 'Add more trigger phrases?', multiple=True,confirm_default=[True,False])]

def Replies():
    return [input_verify('Enter reply phrase (Add {u} to show username)\n', 'Add "{out}" to list of replies?', 'Add more replies?', multiple=True,confirm_default=[True,False])]

def main():
    # Read Config
    from configparser import ConfigParser
    config = ConfigParser()

    FirstSetup = False
    if path.exists('options.ini'):
        config.read('options.ini')
    else:
        print('First start detected')
        FirstSetup = True

    # Ask user to set up things
    if not FirstSetup:
        choice_array = input_verify('Which setting you want to change\n1.Telegram API ID and hash\n2.Dir to send files from on trigger\n3.Monitored and report chats\n5.Trigger phrases\n6.Replies\n', 'Choose option {out}?', 'Change more options?',is_int=True, askvalid=True,multiple=True,cond='{out} in range(1,6) and {out} % 1 == 0',confirm_default=[True,False])
    else:
        choice_array = [1, 2, 3, 4, 5]
        for key in list(conf_dict.keys()):
            config.add_section(key)

    # Execute functions by set order
    for choice in choice_array:
        merge_list = globals()[list(conf_dict.keys())[choice-1]]()
        for val_num,vals in enumerate(list(conf_dict.values())[choice-1]):
            config[list(conf_dict.keys())[choice-1]][vals] = str(merge_list[val_num])
        
        
    # Write changes
    with open('options.ini', 'w') as confwrite:
        confwrite.write('# This config was autogenerated by setup of NoTT MK3\n\n')
        config.write(confwrite)
    print('Setup completed, Enjoy!\n')

if __name__ == "__main__":
    main()
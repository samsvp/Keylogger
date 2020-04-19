def read_key(key):
    '''
    Returns a string formated key from pynput
    '''

    #dicionário com as teclas a serem traduzidas
    translate_keys = {
        "Key.space": " ",
        "Key.shift_r": "",
        "Key.shift_l": "",
        "Key.enter": "\n",
        "Key.alt": "",
        "Key.esc": "",
        "Key.cmd": "",
        "Key.caps_lock": "",
    }

    #remove single quotes
    keydata = str(key).replace("'", "")

    for key in translate_keys:
        keydata = keydata.replace(key, translate_keys[key])

    return keydata

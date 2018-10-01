import unicodedata, re
import os

all_chars = (chr(i) for i in range(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in {'Cc'})

control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s):
    return unicodedata.normalize("NFKD", control_char_re.sub('', s))


def get_file_id(file_path):
    try:
        return os.stat(file_path).st_ino
    except FileNotFoundError:
        return None

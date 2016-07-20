import imghdr
import os
import re
import struct


def new_line_per_sentence(text):
    return text.replace('.\n', '.').replace('.', '.\n')


def split_on_new_line(text):
    return [i.strip() for i in text.splitlines()]


def list_to_string(items):
    return '\n\n'.join(items)


def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0)
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                fhandle.seek(1, 1)
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:
                return
        else:
            return
        return width, height


def is_portrait(fname):
    sizes = get_image_size(fname)
    return sizes[0] < sizes[1]


def get_path_to_image(code):
    base_dir = 'X:\Xedo Support\Bridal Designers Info\Mori Lee'

    p = re.compile('^{}\D'.format(code))

    preferred = None
    all_images = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # if file.startswith("{}-".format(code)):
            if(p.match(file)):
                filename = os.path.join(root, file)
                all_images.append(filename)

                if is_portrait(filename):
                    if not preferred:
                        preferred = filename
                    else:
                        size_pref = get_image_size(preferred)
                        area_preferred = size_pref[0] * size_pref[1]

                        size_new = get_image_size(filename)
                        area_new = size_new[0] * size_new[1]

                        if area_new > area_preferred:
                            preferred = filename

    if not preferred and len(all_images) > 0:
        preferred = all_images[0]
    return preferred, all_images
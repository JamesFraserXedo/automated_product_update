def new_line_per_sentence(text):
    return text.replace('.\n', '.').replace('.', '.\n')


def split_on_new_line(text):
    return [i.strip() for i in text.splitlines()]


def list_to_string(items):
    return '\n\n'.join(items)

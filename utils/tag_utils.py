TAG_MAP = {
    "[HOST]": "ZXHOSTZX",
    "[GUEST]": "ZXGUESTZX",
    "[NARRATOR]": "ZXNARRATORZX"
}


REVERSE_TAG_MAP = {
    v: k for k, v in TAG_MAP.items()
}


def preserve_tags(text):

    for tag, placeholder in TAG_MAP.items():
        text = text.replace(tag, placeholder)

    return text


def restore_tags(text):

    for placeholder, tag in REVERSE_TAG_MAP.items():
        text = text.replace(placeholder, tag)

    return text

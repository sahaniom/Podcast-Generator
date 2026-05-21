import random


HOST_NAMES = [
    "Aarav",
    "Rohan",
    "Kabir",
    "Arjun",
    "Vivaan"
]

GUEST_NAMES = [
    "Ananya",
    "Riya",
    "Meera",
    "Diya",
    "Sanya"
]


def assign_speaker_names():

    host = random.choice(HOST_NAMES)
    guest = random.choice(GUEST_NAMES)

    while guest == host:
        guest = random.choice(GUEST_NAMES)

    return {
        "[HOST]": f"[{host}]",
        "[GUEST]": f"[{guest}]",
        "[NARRATOR]": "[Narrator]"
    }


def replace_speaker_tags(script):

    speaker_map = assign_speaker_names()

    for old, new in speaker_map.items():
        script = script.replace(old, new)

    return script

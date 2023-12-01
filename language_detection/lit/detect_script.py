def detect_script(text):
    script_ranges = {
        "Bengali/Assamese": ((0x0980, 0x09FF),),
        "Tamil": (
            (0x0B80, 0x0BFF),
            (0x11FC0, 0x11FFF),
        ),
        "Telugu": ((0x0C00, 0x0C7F),),
        "Kannada": ((0x0C80, 0x0CFF),),
        "Malayalam": ((0x0D00, 0x0D7F),),
        "Gujarati": ((0x0A80, 0x0AFF),),
        "Odia": ((0x0B00, 0x0B7F),),
        "Punjabi": ((0x0A00, 0x0A7F),),
        "Devanagari": (
            (0x0900, 0x097F),
            (0xA8E0, 0xA8FF),
            (0x11B00, 0x11B5F),
        ),
        "Latin": ((0x0020, 0x007E),),
    }

    for script, ranges in script_ranges.items():
        if any(start <= ord(char) <= end for char in text for start, end in ranges):
            return script

    return "Other"

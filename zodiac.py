# zodiac.py

from datetime import datetime

ZODIAC_DATES = [
    ((1, 20), (2, 18), "Aquarius"),
    ((2, 19), (3, 20), "Pisces"),
    ((3, 21), (4, 19), "Aries"),
    ((4, 20), (5, 20), "Taurus"),
    ((5, 21), (6, 20), "Gemini"),
    ((6, 21), (7, 22), "Cancer"),
    ((7, 23), (8, 22), "Leo"),
    ((8, 23), (9, 22), "Virgo"),
    ((9, 23), (10, 22), "Libra"),
    ((10, 23), (11, 21), "Scorpio"),
    ((11, 22), (12, 21), "Sagittarius"),
    ((12, 22), (1, 19), "Capricorn")
]

def get_zodiac_sign(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        month, day = dt.month, dt.day
        for (m1, d1), (m2, d2), sign in ZODIAC_DATES:
            if (m1, d1) <= (m2, d2):
                if (month, day) >= (m1, d1) and (month, day) <= (m2, d2):
                    return sign
            else:
                if (month, day) >= (m1, d1) or (month, day) <= (m2, d2):
                    return sign
        return "Aries"
    except:
        return "Leo"

def get_time_insight(time_str: str) -> str:
    try:
        hour = int(time_str.split(":")[0])
        if 4 <= hour < 12: return "A fresh dawn energizes your spirit. Begin boldly."
        if 12 <= hour < 17: return "Your focus peaks now. Act with clarity."
        if 17 <= hour < 21: return "Emotions flow deeply. Connect and reflect."
        return "The night amplifies your intuition. Dream without limits."
    except:
        return "The universe supports you at all hours."
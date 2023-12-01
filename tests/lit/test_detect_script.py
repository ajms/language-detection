import pytest

from language_detection.lit.detect_script import detect_script

scripts = {
    "Devanagari": "भारतीय संस्कृति बहुत विविध और समृद्ध है।",
    "Bengali": "ভারতীয় সংস্কৃতি অনেকটা বিবিধ এবং সমৃদ্ধ।",
    "Tamil": "இந்திய கலாச்சாரம் மிகவும் பல மற்றும் சம௃த்தியானது.",
    "Telugu": "భారతీయ సంస్కృతి చాలా వివిధమైనది మరియు సమృద్ధిశాలినది.",
    "Kannada": "ಭಾರತೀಯ ಸಂಸ್ಕೃತಿ ಅನೇಕ ವಿವಿಧ ಮತ್ತು ಸಮೃದ್ಧವಾದದ್ದು.",
    "Malayalam": "ഇന്ത്യൻ സംസ്കാരം വളരെ വിവിധമാണും സമൃദ്ധമാണും.",
    "Gujarati": "ભારતીય સંસ્કૃતિ ઘણી વિવિધ અને સમૃદ્ધ છે.",
    "Odia": "ଭାରତୀୟ ସଂସ୍କୃତି ଅତି ବିଵିଧ ଏବଂ ସମୃଦ୍ଧ ଅଛି।",
    "Punjabi": "ਭਾਰਤੀ ਸੱਭਿਆਚਾਰ ਬਹੁਤ ਵਿਵਿਧ ਅਤੇ ਸਮ੃ਦ੍ਧ ਹੈ।",
    "Assamese": "ভাৰতীয় সংস্কৃতি বহুত বিভিন্ন আৰু সমৃদ্ধ।",
}


@pytest.mark.parametrize("script, text", scripts.items())
def test_detect_script(script: str, text: str):
    assert script in detect_script(text)

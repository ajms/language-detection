import asyncio

import aiohttp


async def send_requests(text: str, semaphore: asyncio.Semaphore):
    batch_url = "http://localhost:3000/combined_lid"
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.post(batch_url, data=text) as response:
                response_data = await response.json()
                print(response_data)
                return response_data


async def main(batch: list[str]):
    semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent requests
    coroutines = [send_requests(text, semaphore) for text in batch]
    results = await asyncio.gather(*coroutines)
    return results


if __name__ == "__main__":
    batch = {
        "English": "The quick brown fox jumps over the lazy dog, showcasing its agility and speed while the dog remains calm and relaxed.",
        "Spanish": "El rápido zorro marrón salta sobre el perro perezoso, mostrando su agilidad y velocidad mientras que el perro permanece tranquilo y relajado.",
        "French": "Le renard brun rapide saute par-dessus le chien paresseux, montrant son agilité et sa vitesse tandis que le chien reste calme et détendu.",
        "German": "Der schnelle braune Fuchs springt über den faulen Hund und zeigt dabei seine Wendigkeit und Geschwindigkeit, während der Hund ruhig und entspannt bleibt.",
        "Russian": "Быстрая коричневая лиса перепрыгивает через ленивую собаку, демонстрируя свою ловкость и скорость, в то время как собака остается спокойной и расслабленной.",
        "Arabic": "الثعلب البني السريع يقفز فوق الكلب الكسول، يظهر لياقته وسرعته بينما يظل الكلب هادئًا ومسترخيًا.",
        "Hindi": "तेज भूरी लोमड़ी सुस्त कुत्ते पर कूदती है, अपनी दक्षता और गति दिखाती हुई, जबकि कुत्ता शांत और आराम से रहता है।",
        "Italian": "La volpe marrone veloce salta sopra al cane pigro, mostrando la sua agilità e velocità mentre il cane rimane calmo e rilassato.",
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

    print(asyncio.run(main(list(batch.values()))))

# Marathi2India — BHASHINI API bridge (starter)

ही API bridge फाइल आहे; API key समाविष्ट नाही. BHASHINI API key प्रत्येक वापरकर्त्याला स्वतःच्या खात्यातून मिळवावी लागते.

## आधी हे करा
1. BHASHINI onboarding: https://bhashini.gov.in/
2. अधिकृत API docs: https://tts.bhashini.ai/openapi/ui/
3. BHASHINI ULCA/UDYAT pipeline setup आणि API credentials: https://bhashini.gitbook.io/bhashini-apis/pre-requisites-and-onboarding
4. तुमच्या account मधील translation pipeline configuration response मधून `callbackURL`, auth header/value आणि Marathi→target language साठी translation `serviceId` मिळवा. हे values तुमच्या account/model वर अवलंबून असतात; या पॅकेजमध्ये बनावट values नाहीत.

## सर्व्हरवर चालवा
ही पायरी hosted Python service वर करावी लागेल; फक्त Samsung फोनवर ZIP उघडल्याने API चालणार नाही.
1. `app.py`, `requirements.txt`, `.env.example` सर्व्हर/hosting प्रकल्पात upload करा.
2. hosting dashboard मध्ये environment variables सेट करा (`.env.example` मधील नावे).
3. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Health check: `GET /`
5. Translate endpoint: `POST /api/translate`

Request JSON:
{"text":"मला इंग्रजी शिकायचे आहे","source":"mar_Deva","target":"eng_Latn"}

Response JSON:
{"translation":"I want to learn English."}

## PWA मध्ये जोडणी
तुमच्या `index.html` मधील `const API_URL=""` ऐवजी सर्व्हरची HTTPS URL + `/api/translate` द्या.
उदा. `https://YOUR-SERVER.example/api/translate`
हे उदाहरण URL आहे; तो प्रत्यक्ष सर्व्हर नाही.

## सुरक्षितता
- API key कधीही `index.html` किंवा GitHub public repository मध्ये ठेवू नका.
- `ALLOWED_ORIGIN` मध्ये तुमच्या वेबसाइटचा नेमका HTTPS origin लिहा.
- BHASHINI pipeline configuration / service ID भाषा जोडीप्रमाणे बदलू शकते; २२ भाषांमध्ये उपलब्धता स्वतंत्रपणे तपासा.
- Grammar correction / Professional English endpoint या bridge मध्ये अजून समाविष्ट नाही; त्यासाठी वेगळी सुरक्षित AI सेवा जोडावी लागेल.

FROM python
WORKDIR /piperpextestbot
COPY . /piperpextestbot

RUN pip install --no-cache-dir -r requirements.txt


ENV TELEGRAM_ACCESS_TOKEN = 7887521281:AAHDyoUpCmCjkMoXB4Xh53TZYODxQuUQvwE
ENV BASICURL = https://genai.hkbu.edu.hk/general/rest
ENV MODELNAME = gpt-4-o-mini
ENV APIVERSION = 2024-05-01-preview
ENV GPT_ACCESS_TOKEN = ae68d010-92d4-4730-af02-84a20f05b7d1

CMD python chatbot.py
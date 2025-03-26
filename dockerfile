
FROM python
WORKDIR /piperpextestbot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV BASICURL=https://genai.hkbu.edu.hk/general/rest \
    MODELNAME=gpt-4-o-mini \
    APIVERSION=2024-05-01-preview

CMD ["python", "chatbot.py"]
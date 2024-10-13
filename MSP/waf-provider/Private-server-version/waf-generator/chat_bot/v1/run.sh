python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install langchain-google-genai google-generativeai


# ---------------------------
cd chat-box/python/lib/python3.8/site-packages/
pip install -r requirements.txt --platform manylinux2014_x86_64 -t . --only-binary=:all: --upgrade
zip -r ../chat.zip .
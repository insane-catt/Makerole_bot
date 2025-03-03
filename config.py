# 言語設定
LANG = "jp" # jp or en

# TOKENの読出しをするやつです

from dotenv import load_dotenv
load_dotenv()

import os

TOKEN = os.getenv(LANG.upper() + "MAKEROLE")
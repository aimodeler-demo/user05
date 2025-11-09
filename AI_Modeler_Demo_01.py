!ls /repos

!cd /repos

import os
import openai
import tiktoken

openai.api_key = os.getenv("OPENAI_API_KEY")

LLM_MODEL="gpt-4o"

TOKENIZER = tiktoken.encoding_for_model("text-embedding-3-small")

EMBED_MODEL="text-embedding-3-small"

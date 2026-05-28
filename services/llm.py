from openai import AzureOpenAI, AsyncAzureOpenAI
from models import Project
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2025-03-01-preview",
    )


async def analyze_ppt(ppt_text: str):
    response = await client.chat.completions.parse(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You analyze PowerPoint presentations and must return structured output that matches the schema exactly. "
                        "Classify service, domain, scope, and type using only the allowed enum values from the schema."
                        "Do not populate tags key"
                        "Do not invent new labels, synonyms, or free-text categories."
                    )
                },
                {
                    "role": "user",
                    "content": f"""
                        Analyze this PowerPoint content and summarize it clearly.

                        PowerPoint content:
                        {ppt_text}
                    """
                }
            ],
            response_format=Project
        )
    result = response.choices[0].message.parsed
    return result

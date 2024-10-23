from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException
from openai import OpenAI
from typing import Optional
from app.core.config import settings


class WebsiteService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def fetch_website_content(self, url: str) -> tuple[str, str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.title.string if soup.title else "No title found"

            # Clean content
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            text = soup.body.get_text(separator="\n", strip=True)

            return title, text
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch website content: {str(e)}"
            )

    def generate_summary(self, title: str, content: str) -> str:
        try:
            system_prompt = (
                "You are an assistant that analyzes website contents "
                "and provides a short summary, ignoring navigation related text. "
                "Respond in markdown."
            )

            user_prompt = (
                f"You are looking at a website titled {title}. "
                "The contents of this website is as follows; "
                "please provide a short summary in markdown. "
                "If it includes news or announcements, summarize these too.\n\n"
                f"{content}"
            )

            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,  # Add to settings
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            return response.choices[0].message.content

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate summary: {str(e)}"
            )

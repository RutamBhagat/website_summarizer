# app/services/brochure_service.py
from typing import List, Dict, Optional, AsyncGenerator
import uuid
import requests
import json
from bs4 import BeautifulSoup
from fastapi import HTTPException
from openai import OpenAI
from app.core.config import settings


class Website:
    """Class to handle website content fetching and parsing."""

    def __init__(self, url: str):
        self.url = url
        self.title: str = ""
        self.text: str = ""
        self.links: List[str] = []
        self._fetch_content()

    def _fetch_content(self) -> None:
        """Fetch and parse website content."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract title
            self.title = soup.title.string if soup.title else "No title found"

            # Clean and extract text
            if soup.body:
                for tag in soup.body(["script", "style", "img", "input"]):
                    tag.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)

            # Extract links
            self.links = [
                link.get("href") for link in soup.find_all("a") if link.get("href")
            ]

        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to fetch website content: {str(e)}"
            )

    def get_contents(self) -> str:
        """Get formatted website contents."""
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


class BrochureService:
    """Service to generate company brochures."""

    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.link_system_prompt = """
            You are provided with a list of links found on a webpage.
            You are able to decide which of the links would be most relevant to include in a brochure about the company,
            such as links to an About page, or a Company page, or Careers/Jobs pages.
            You should respond in JSON as in this example:
            {
                "links": [
                    {"type": "about page", "url": "https://full.url/goes/here/about"},
                    {"type": "careers page", "url": "https://another.full.url/careers"}
                ]
            }
        """
        self.brochure_system_prompt = """
            You are an assistant that analyzes the contents of several relevant pages from a company website
            and creates a short brochure about the company for prospective customers, investors and recruits.
            Respond in markdown. Include details of company culture, customers and careers/jobs if you have the information.
        """

    def _get_relevant_links(self, website: Website) -> Dict:
        """Get relevant links from website."""
        try:
            user_prompt = (
                f"Here is the list of links on the website of {website.url} - "
            )
            user_prompt += """please decide which of these are relevant web links for a brochure about the company,
                          respond with the full https URL in JSON format.
                          Do not include Terms of Service, Privacy, email links.\n"""
            user_prompt += "\n".join(website.links)

            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.link_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to analyze website links: {str(e)}"
            )

    def _get_all_details(self, url: str) -> str:
        """Gather all relevant website details."""
        result = "Landing page:\n"
        website = Website(url)
        result += website.get_contents()

        links = self._get_relevant_links(website)
        for link in links["links"]:
            result += f"\n\n{link['type']}\n"
            link_website = Website(link["url"])
            result += link_website.get_contents()

        return result[:20_000]  # Truncate if more than 20,000 characters

    async def generate_brochure(self, company_name: str, url: str) -> str:
        """Generate a company brochure."""
        try:
            user_prompt = f"You are looking at a company called: {company_name}\n"
            user_prompt += (
                "Here are the contents of its landing page and other relevant pages; "
            )
            user_prompt += "use this information to build a short brochure of the company in markdown.\n"
            user_prompt += self._get_all_details(url)

            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.brochure_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate brochure: {str(e)}"
            )

    async def stream_brochure(
        self, company_name: str, url: str
    ) -> AsyncGenerator[str, None]:
        """Generate a company brochure with streaming response."""
        try:
            user_prompt = f"You are looking at a company called: {company_name}\n"
            user_prompt += (
                "Here are the contents of its landing page and other relevant pages; "
            )
            user_prompt += "use this information to build a short brochure of the company in markdown.\n"
            user_prompt += self._get_all_details(url)

            # Create the stream
            stream = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.brochure_system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            # Stream the response using SSE format
            for chunk in stream:
                if content := chunk.choices[0].delta.content:
                    # Format as SSE with proper JSON encoding
                    yield f"data: {json.dumps(content)}\n\n"

            # Send stream termination signal
            yield "data: [DONE]\n\n"

        except Exception as e:
            # Format error as SSE
            error_message = json.dumps({"error": str(e)})
            yield f"data: {error_message}\n\n"
            yield "data: [DONE]\n\n"
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate streaming brochure: {str(e)}",
            )

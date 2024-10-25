## Instant Website Insights

Transform any webpage into a concise summary with AI. Save hours of reading in seconds by simply entering a URL and letting advanced language models distill key insights for you. **No sign-up required** and instant results!

**Backend:** [Website Summarizer API](https://website-summarizer-iorx.onrender.com/docs)  
**Frontend:** [Instant Website Insights UI](https://website-summarizer-frontend.vercel.app)

---

## Demo Video

[Placeholder for Demo Video]

---

## How It's Made

**Tech used:** HTML, CSS, JavaScript, Python, BeautifulSoup, OpenAI API

The project architecture is built around modular components for scalability and efficiency:

- **Web Scraping & Parsing:** We use BeautifulSoup to handle raw HTML parsing, extracting only the relevant content while removing unnecessary elements like ads, navigation bars, and scripts.
- **AI Summarization:** Powered by OpenAI's GPT-4, the system processes cleaned HTML to deliver concise summaries, with prompt engineering ensuring consistent and high-quality outputs.
- **Frontend & Backend:** The frontend is a simple Next.js web interface that allows users to input URLs and see instant results, while the FASTAPI backend API handles web scraping, data cleaning, and OpenAI interactions. The frontend is hosted on Vercel, and the backend on Render.

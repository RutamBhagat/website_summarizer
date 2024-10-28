# BrochureCraft: Instant Brochure & Website Summarizer

BrochureCraft is an AI-powered tool designed to instantly generate professional brochures and insightful summaries from any webpage. With its user-friendly interface, BrochureCraft simplifies content extraction, providing businesses, marketers, and researchers with instant, shareable marketing materials.

**Backend:** [Website Summarizer API](https://website-summarizer-iorx.onrender.com/docs)  
**Frontend:** [Instant Website Insights UI](https://website-summarizer-frontend.vercel.app)

---

## Demo Video

https://github.com/user-attachments/assets/b2c0afad-f7ec-4f92-b6bb-253a9d911152

---

## How It Works

BrochureCraft offers two main tools:

1. **Brochure Generator** – Converts website content into a well-organized, professional brochure format, ideal for prospective clients, investors, or new recruits.
2. **Instant Summarizer** – Quickly extracts and summarizes key insights from any webpage.

## Key Features

- **Professional Brochures**: Automatically arranges website content into a sleek brochure, emphasizing company culture, services, and career opportunities.
- **Concise Summaries**: Summarizes webpage content, news, or announcements into a digestible, high-level overview.
- **Streaming Responses**: Provides real-time feedback with a typewriter animation for a dynamic user experience.

## Tech Stack

- **Frontend**: Next.js, TailwindCSS, shadcn/ui components
- **Backend**: FastAPI, Async processing
- **AI Integration**: OpenAI for content generation
- **Styling**: TailwindCSS for responsive design
- **UI Components**: shadcn/ui for consistency and polish

## Optimizations

- **Responsive Design**: Developed with Next.js for optimized loading and a smooth user experience.
- **Content Filtering**: Removes irrelevant content (e.g., navigation) to focus on meaningful website insights.

## Example Use Cases

BrochureCraft is perfect for:

- **Marketing Teams**: Quickly create brochures and summaries to showcase services or company values.
- **Sales Professionals**: Equip yourself with high-quality, on-demand brochures for prospective clients.
- **Researchers**: Generate concise summaries of articles or industry news for fast information gathering.

## Getting Started

1. **Clone the Repositories**
   ```bash
   ##### for frontend
   git clone https://github.com/RutamBhagat/website_summarizer_frontend
   ##### for backend
   git clone https://github.com/RutamBhagat/website_summarizer
   ```
2. **Environment Setup**
   - Add your OpenAI API key in `.env` files in both repositories.
3. **Install Dependencies**

   ```bash
   ##### for frontend
   cd website_summarizer_frontend
   npm i -g bun
   bun install
   ##### for backend
   cd ../website_summarizer
   pipx install pdm
   pdm install
   ```

4. **Run the Application**
   ##### for frontend
   - Start the frontend: `bun run dev`
   ##### for backend
   - Start the backend: `pdm run uvicorn app.main:app --reload`

## Lessons Learned

BrochureCraft’s development focused on:

- **Efficient Web Scraping**: Parsing web content quickly and accurately using beautifulsoup4.
- **Optimized Async Processing**: Managing asynchronous tasks for faster response times.
- **UI & UX**: Crafting a clean, user-friendly interface that provides streaming feedback.

## Future Enhancements

- **Enhanced Web Compatibility**: Improve scraping for sites with dynamic content (e.g., React/SPA).
- **Multi-Language Support**: Provide summaries and brochures in various languages.
- **Template Customization**: Offer brochure style and format options.

## Contributing

Contributions are welcome! Feel free to fork the repository, submit pull requests, or suggest ideas in the Issues section.

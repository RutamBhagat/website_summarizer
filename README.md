# BrochureCraft: Instant Brochure & Website Summarizer

## Overview

BrochureCraft is an AI-powered tool designed to instantly generate professional brochures and insightful summaries from any webpage. The project combines modern web technologies with AI capabilities to provide businesses, marketers, and researchers with instant, shareable marketing materials. The system features a FastAPI backend for efficient processing and a Next.js frontend for optimal user experience.

**Live** [Live Deployment](https://vercel.com/api/toolbar/link/website-summarizer-frontend.vercel.app)

**Backend:** [Website Summarizer API](https://website-summarizer-iorx.onrender.com/docs)

**Frontend:** [Instant Website Insights UI](https://website-summarizer-frontend.vercel.app)

## Demo Video

https://github.com/user-attachments/assets/b2c0afad-f7ec-4f92-b6bb-253a9d911152

## Key Features

- **Brochure Generator**: Built an automated system that converts website content into well-organized, professional brochure formats using OpenAI integration.
- **Instant Summarizer**: Developed a feature that quickly extracts and summarizes key insights from any webpage.
- **Streaming Responses**: Implemented real-time feedback with typewriter animation for enhanced user experience.
- **Content Filtering**: Created intelligent filtering mechanisms to remove irrelevant content and focus on meaningful website insights.

## Technologies Used

- **Frontend**: Next.js, TailwindCSS, shadcn/ui components for a responsive and polished user interface
- **Backend**: FastAPI with async processing capabilities for efficient request handling
- **AI Integration**: OpenAI API integration for advanced content generation and summarization
- **Development Tools**: Git for version control, PDM for Python dependency management, Bun for JavaScript package management

## Challenges and Learnings

A significant challenge was implementing efficient web scraping that could handle various website structures while maintaining fast response times. The solution involved optimizing async processing and creating robust parsing algorithms using beautifulsoup4. Additionally, integrating streaming responses with OpenAI's API required careful consideration of rate limits and error handling.

## Example Use Cases

BrochureCraft is perfect for:

- **Marketing Teams**: Quickly create brochures and summaries to showcase services or company values.
- **Sales Professionals**: Equip yourself with high-quality, on-demand brochures for prospective clients.
- **Researchers**: Generate concise summaries of articles or industry news for fast information gathering.

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker (optional)
- Git

### Frontend Setup

```bash
   # Clone repository
   git clone https://github.com/RutamBhagat/website_summarizer_frontend
   cd website_summarizer_frontend

   # Install dependencies
   npm install

   # Start development server
   npm run dev
```

### Backend Setup

```bash
   # Backend
   git clone https://github.com/RutamBhagat/website_summarizer
   cd website_summarizer

   pipx install pdm

   pdm install

   source .venv/bin/activate

   pdm run uvicorn app.server:app --reload
```

#### If you want to setup using Docker

```bash
   # Remove the old container if present
   docker rm website-summarizer-container

   # Build the new image with no cache
   docker build --no-cache -t website-summarizer-app .

   # Run the container
   docker run -d -p 8000:8000 --name website-summarizer-container website-summarizer-app
```

## Outcome

BrochureCraft successfully provides a streamlined solution for generating marketing materials and content summaries. The application demonstrates significant efficiency improvements in content processing and presentation, making it valuable for marketing teams, sales professionals, and researchers who need quick access to well-formatted materials.

# Screenshots

![1](https://github.com/user-attachments/assets/c9aae5ef-13e8-4227-96d9-51d462a256be)
![2](https://github.com/user-attachments/assets/b630996c-7d40-4b62-b3b5-61d8b3ed7344)
![3](https://github.com/user-attachments/assets/a1a05859-2b1d-4dec-a431-b847311c6d46)
![4](https://github.com/user-attachments/assets/bfc8b74d-d958-412b-8654-b925a015aa98)


# CareerSpark AI Service

This is a FastAPI-based service that provides AI functionality for the CareerSpark job application automation system.

## Features

- Form analysis for job applications
- Automatic generation of responses for form fields
- Analysis of job application page content
- Integration with Ollama for AI capabilities

## Getting Started

### Prerequisites

- Python 3.11 or newer
- Docker and Docker Compose (optional, for containerized deployment)
- Ollama (optional, or can be run via Docker)

### Environment Setup

Create a `.env` file in the root directory with the following variables:

```
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
API_PORT=8000
```

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/careerspark-ai-service.git
   cd careerspark-ai-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Service

#### Local Development

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

#### Using Docker Compose

```bash
docker-compose up -d
```

This will start both the AI service and an Ollama instance.

## API Endpoints

### GET `/`

- Returns a simple status message to verify the service is running.

### POST `/analyze-form`

- Analyzes a job application form structure.
- Request body: `AIRequest` object.

### POST `/generate-responses`

- Generates responses for job application form fields based on resume data.
- Request body: `AIRequest` object.

### POST `/analyze-page`

- Analyzes page content to determine if submission is complete or which button to click.
- Request body: JSON with `pageContent` and optional `jobApplicationId`.

## Project Structure

```
ai_service/
├── app/
│   ├── models/         # Pydantic data models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── main.py             # FastAPI application
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker configuration
```

## License

[MIT License](LICENSE)
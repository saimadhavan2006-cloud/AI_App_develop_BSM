# AI Sentiment Automation

An AI-powered customer feedback analysis system that classifies text sentiment, recommends follow-up actions, stores analysis results in SQLite, and visualizes feedback trends through an interactive dashboard.

## Features

- **AI sentiment classification:** Uses a pretrained DistilBERT model to classify feedback as positive or negative.
- **Confidence scoring:** Returns a confidence score for each prediction.
- **Automated action recommendations:** Suggests recording positive feedback or flagging negative feedback for customer-support review.
- **REST API:** Built with FastAPI, including interactive API documentation.
- **Persistent storage:** Saves sentiment results and suggested actions in SQLite.
- **Feedback history:** Retrieves previously analyzed feedback through an API endpoint.
- **Interactive dashboard:** Visualizes sentiment distribution and confidence scores.
- **Feedback search and filtering:** Search stored feedback and filter by sentiment.
- **Input validation:** Rejects empty feedback and inputs exceeding 5,000 characters.
- **Automated tests:** Tests API health, sentiment predictions, and input validation.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| API framework | FastAPI |
| Data validation | Pydantic |
| NLP model | DistilBERT |
| Machine learning | Hugging Face Transformers, PyTorch |
| Database | SQLite |
| Data analysis | Pandas |
| Dashboard | Streamlit |
| API testing | FastAPI TestClient, pytest |

## Architecture

1. **Input:** A user submits customer feedback through the REST API.
2. **Validation:** Pydantic validates the input text.
3. **Inference:** The pretrained DistilBERT model predicts positive or negative sentiment.
4. **Decision logic:** The application selects a suggested action based on the predicted sentiment.
5. **Persistence:** The prediction, confidence score, feedback, and suggested action are saved to SQLite.
6. **Visualization:** The Streamlit dashboard reads stored records and displays analytics and feedback history.

## Project Structure

```text
ai-automation/
├── app.py          # FastAPI application and sentiment analysis
├── dashboard.py    # Streamlit analytics dashboard
├── database.py     # SQLite database operations
├── test_api.py     # API tests
└── README.md       # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version supported by the dependencies
- Git
- Internet access for the initial download of the pretrained model

### 1. Clone the repository

```powershell
git clone https://github.com/saimadhavan2006-cloud/AI_App_develop_BSM.git
cd AI_App_develop_BSM/ai-automation
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the packages used by the application:

```powershell
python -m pip install fastapi "uvicorn[standard]" transformers torch pandas streamlit httpx pytest
```

The pretrained model may be downloaded automatically the first time the application loads it.

### 4. Start the API

```powershell
python -m uvicorn app:app --reload
```

Open these URLs in your browser:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Interactive Swagger documentation: http://127.0.0.1:8000/docs

### 5. Analyze feedback

Send a `POST` request to `/analyse` with a JSON body:

```json
{
  "text": "I love this product! It is excellent."
}
```

Example response:

```json
{
  "id": 1,
  "text": "I love this product! It is excellent.",
  "sentiment": "POSITIVE",
  "confidence": 0.99,
  "suggested_action": "Record as positive feedback",
  "saved_to_database": true
}
```

The confidence value is illustrative; actual predictions depend on the model output.

Negative feedback receives the suggested action `Flag for customer support review`.

### 6. Retrieve feedback history

Send a `GET` request to:

```text
http://127.0.0.1:8000/history?limit=50
```

The `limit` parameter accepts values from 1 to 100 and defaults to 50.

### 7. Launch the dashboard

Open a second terminal in the project directory, activate the virtual environment, and run:

```powershell
streamlit run dashboard.py
```

The dashboard displays:

- Total analyses
- Positive and negative feedback counts
- Average confidence score
- Sentiment distribution
- Confidence score chart
- Searchable and filterable feedback history

The dashboard reads the SQLite database directly, so the API and dashboard must use the same database file.

## Run Tests

With the virtual environment activated, run:

```powershell
python -m pytest test_api.py -v
```

The tests cover the API root, health check, positive and negative predictions, confidence values, suggested actions, and invalid inputs.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check that the API is responding |
| GET | `/health` | Return API health information |
| POST | `/analyse` | Analyze and save feedback |
| GET | `/history` | Retrieve saved analyses |

## Limitations

- The model classifies text into positive or negative sentiment; it does not provide a neutral category.
- Suggested actions are stored recommendations, not integrations with external customer-support systems.
- The confidence score represents the model's prediction score and should not be interpreted as a guarantee of correctness.
- The pretrained model runs on the CPU in the current configuration.
- The dashboard reads SQLite directly rather than calling the history API.

## Future Improvements

- Add neutral sentiment classification.
- Integrate customer-support notifications and workflow automation.
- Add date-range filters and trend analysis.
- Expand automated tests for database failures and API error handling.
- Add authentication and access controls for production use.
- Support deployment with environment-based configuration.

## Author

**B. Sai Madhavan**

AI App Development | Natural Language Processing | Backend Development

# Intellibus Kids - AI Health Assistant

A specialized AI healthcare assistant that generates personalized medical reports and meal plans for children with specific medical conditions.

## 🌟 Features

- **Medical Report Generation**: Creates comprehensive medical reports tailored to specific medical conditions
- **Personalized Meal Plans**: Generates 7-day meal plans with breakfast, lunch, and dinner options that consider:
  - The specific medical condition
  - Dietary restrictions and allergies
  - Calorie requirements
- **Ingredient Lists**: Provides organized shopping lists categorized by produce, groceries, and dry goods
- **API Access**: Easy-to-use REST API for integration with frontends or other services

## 📋 Requirements

- Python 3.9 or higher
- pip (Python package installer)
- Google Gemini API key (for LLM functionality)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/zariacs/intellibus-kids.git
cd intellibus-kids
```

### 2. Environment Setup

Create a `.env` file in the `AI` directory with the following content:

```
# LLM Keys
GEMINI_API_KEY="your_gemini_api_key_here"
MODEL_NAME=gemini-1.5-pro

# Debug settings
DEBUG=True
LOG_LEVEL=INFO
```

### 3. Install Dependencies

```bash
cd AI
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m uvicorn api.main:app --reload
```

The API will be available at http://127.0.0.1:8000

## 📚 API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📝 Using the API

### Generate a Medical Report

Make a POST request to `/api/v1/generate_report` with patient information:

```json
{
  "name": "Sarah Johnson",
  "condition": "Type 2 Diabetes",
  "age": 12,
  "gender": "Female",
  "weight": 45.5,
  "height": 150.3,
  "allergies": [
    "dairy",
    "shellfish"
  ],
  "medications": [
    "Metformin 500mg"
  ],
  "symptoms": [
    "frequent urination",
    "increased thirst",
    "fatigue"
  ],
  "dietary_preferences": [
    "low-carb",
    "gluten-free"
  ]
}
```

The response will include a markdown-formatted medical report with:
- Patient details
- Definition of the condition
- Challenges faced by the patient
- A 7-day meal plan with breakfast, lunch, and dinner (including calorie counts)
- Organized ingredient lists

## 🧩 Project Structure

```
AI/
├── api/                 # API endpoints and routes
├── config/              # Configuration settings
├── models/              # Data models
├── services/            # Business logic services
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── pyproject.toml       # Project metadata
```

## 🔧 Testing

To test the report generation functionality without using the API:

```bash
cd AI
python -c "from services.report_generation import test_patient_report; test_patient_report()"
```

## 🛠️ Development

### Adding New Features

If you want to extend the functionality:

1. For new API endpoints: Add to `api/patient_report.py`
2. For data model changes: Modify `models/report.py`
3. For service logic changes: Update `services/report_generation.py`

### Project Configuration

The project uses:
- **LangChain**: For LLM interactions and agent frameworks
- **LangGraph**: For constructing agent-based workflows
- **FastAPI**: For API endpoints
- **Pydantic**: For data validation and settings management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
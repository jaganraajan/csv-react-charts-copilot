# csv-react-charts-copilot

A full-stack application featuring a React frontend with CSV data visualization and an AI-powered chatbot, backed by a Python FastAPI server with Azure OpenAI integration.

## Features

- **📊 CSV Data Visualization**: Upload CSV files and visualize them with interactive charts
- **💬 AI Chatbot**: Chat with an AI assistant powered by Azure OpenAI
- **📈 Multiple Chart Types**: Switch between line and bar charts
- **🎨 Modern UI**: Clean, responsive design with gradient styling
- **⚡ Fast Development**: Vite for frontend, FastAPI for backend

## Project Structure

```
.
├── frontend/          # React + TypeScript + Vite application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.tsx        # AI chatbot component
│   │   │   ├── Chatbot.css
│   │   │   ├── ChartPanel.tsx     # CSV upload & chart display
│   │   │   └── ChartPanel.css
│   │   ├── App.tsx                # Main application component
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   └── package.json
│
└── backend/           # Python FastAPI server
    ├── main.py        # FastAPI application with Azure OpenAI
    ├── requirements.txt
    └── .env.example
```

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Azure OpenAI** account with API access

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Configure your Azure OpenAI credentials in `.env`:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   ```

6. Run the backend server:
   ```bash
   python main.py
   # or
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. (Optional) Create a `.env` file if you need to customize the API URL:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## Usage

### Chatbot
- Type your question in the chat input at the bottom of the left sidebar
- Press "Send" or hit Enter to submit
- The AI assistant will respond using Azure OpenAI

### CSV Upload & Visualization
- Click "Choose CSV File" in the right panel
- Select a CSV file from your computer (you can use `sample-data.csv` included in the repository)
- The chart will automatically update with your data
- Switch between line and bar chart views using the chart type buttons
- If no file is uploaded, a demo chart with sample data is displayed

**Sample CSV Format:**
```csv
month,sales,revenue,profit
January,4500,3200,2800
February,3800,2900,2400
March,5200,4100,3500
```

## API Endpoints

### Backend API

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `POST /api/chat` - Chat with AI assistant
  - Request body: `{ "message": "your question" }`
  - Response: `{ "response": "AI response" }`

## Technologies Used

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Recharts** for data visualization
- **Axios** for API calls
- **CSS3** with custom styling

### Backend
- **FastAPI** for the web framework
- **Uvicorn** as ASGI server
- **Azure OpenAI** for AI capabilities
- **Pydantic** for data validation
- **Python-dotenv** for environment management

## Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
python main.py                    # Run with auto-reload
# or
uvicorn main:app --reload        # Run with uvicorn
```

## Environment Variables

### Backend (.env)
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Your Azure OpenAI deployment name

### Frontend (.env)
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Troubleshooting

### Chatbot not responding
- Ensure the backend is running
- Check that Azure OpenAI credentials are correctly configured in `backend/.env`
- Verify the API URL in the frontend matches the backend URL

### CORS errors
- Make sure the backend CORS settings include your frontend URL
- Default allowed origins: `http://localhost:5173` and `http://localhost:3000`

### CSV upload not working
- Ensure your CSV file is properly formatted with headers in the first row
- Check browser console for any error messages

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
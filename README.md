# csv-react-charts-copilot

A full-stack application featuring a React frontend with CSV data visualization and an AI-powered chatbot with LangGraph agent, backed by a Python FastAPI server with Azure OpenAI integration.

## Features

- **📊 CSV Data Visualization**: Upload CSV files and visualize them with interactive charts
- **🤖 AI Chatbot with LangGraph Agent**: Intelligent CSV analysis assistant powered by Azure OpenAI
- **🔧 Three CSV Analysis Tools**:
  - `read_csv_tool`: Read and display CSV metadata (shape, columns, preview)
  - `analyze_csv_column`: Detailed statistics for numeric and categorical columns
  - `query_csv_data`: Natural language queries (count rows, list columns, summary stats, etc.)
- **📤 CSV File Upload**: Upload your own CSV files for analysis directly in the chatbot
- **📈 Multiple Chart Types**: Switch between line and bar charts
- **🔍 Langfuse Integration**: Optional agent tracing and observability for debugging and monitoring
- **🎨 Modern UI**: Clean, responsive design with gradient styling
- **⚡ Fast Development**: Vite for frontend, FastAPI for backend

## Project Structure

```
.
├── frontend/          # React + TypeScript + Vite application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot.tsx        # AI chatbot with file upload
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
    ├── main.py        # FastAPI application with LangGraph agent
    ├── csv_agent.py   # LangGraph agent with CSV tools
    ├── demo_data.csv  # Demo CSV file for testing
    ├── requirements.txt
    └── .env.example
```

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+
- **Azure OpenAI** account with API access
- **Langfuse** account (optional, for tracing and observability)

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

6. (Optional) Configure Langfuse for agent tracing in `.env`:
   ```env
   LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key-here
   LANGFUSE_SECRET_KEY=sk-lf-your-secret-key-here
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
   
   To get Langfuse credentials:
   - Sign up at [cloud.langfuse.com](https://cloud.langfuse.com)
   - Create a new project
   - Copy your API keys from the project settings

7. Run the backend server:
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

### CSV Analysis Chatbot with LangGraph Agent

The chatbot now features an intelligent agent that can analyze CSV files using three specialized tools:

#### Getting Started
1. **Upload a CSV file** (optional):
   - Click the "📄 Upload CSV File" button in the chatbot header
   - Select a CSV file from your computer
   - Or use the included `backend/demo_data.csv` file automatically

2. **Ask questions about your data**:
   - "Show me the CSV data" - See file info and preview
   - "Analyze the price column" - Get detailed statistics
   - "How many rows are there?" - Count rows
   - "What's the average revenue?" - Calculate aggregates
   - "List all columns" - See column names
   - "Show unique values in category" - Get distinct values

#### Available Tools

1. **read_csv_tool**: Displays CSV shape, column names, and first 5 rows
2. **analyze_csv_column**: Provides statistics for any column
   - Numeric: mean, std, min, quartiles, max, missing values
   - Categorical: unique values, value counts, missing values
3. **query_csv_data**: Handles natural language queries for common operations

#### Agent Flow
```
User Query → LangGraph Agent → Tool Selection → Tool Execution → Agent Response
```

The agent automatically decides which tool(s) to use based on your question, executes them, and provides a natural language response.

#### Langfuse Tracing (Optional)

When Langfuse is configured, the application provides complete observability of the agent graph flow:

- **Trace every agent execution**: See the full conversation flow with tool calls
- **Monitor performance**: Track latency and token usage for each step
- **Debug issues**: View detailed logs of tool invocations and responses
- **Analyze patterns**: Understand how users interact with the CSV agent

To view traces:
1. Configure Langfuse credentials in `.env` (see Backend Setup step 6)
2. Run the application and interact with the chatbot
3. Visit your Langfuse dashboard at [cloud.langfuse.com](https://cloud.langfuse.com)
4. View detailed traces, including:
   - User queries
   - Agent decisions
   - Tool invocations and results
   - Final responses
   - Timing and token metrics

The agent graph flow is automatically tracked without any code changes required!

### CSV Upload & Visualization (Chart Panel)
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

- `GET /` - Root endpoint (returns API status)
- `GET /health` - Health check endpoint (shows agent configuration status and Langfuse status)
- `POST /api/upload-csv` - Upload CSV file for analysis
  - Accepts: multipart/form-data with `file` field
  - Response: `{ "message": "success message", "filename": "uploaded_file.csv" }`
- `POST /api/chat` - Chat with LangGraph AI agent
  - Request body: `{ "message": "your question" }`
  - Response: `{ "response": "AI agent response" }`
  - The agent automatically uses uploaded CSV or demo data
  - All interactions are traced in Langfuse if configured

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
- **LangGraph** for building the AI agent with StateGraph pattern
- **LangChain** for tool binding and Azure OpenAI integration
- **Langfuse** for agent tracing and observability (optional)
- **Azure OpenAI** for LLM capabilities
- **Pandas** for CSV data analysis
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
**Required:**
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Your Azure OpenAI deployment name

**Optional (for Langfuse tracing):**
- `LANGFUSE_PUBLIC_KEY` - Your Langfuse public key (from cloud.langfuse.com)
- `LANGFUSE_SECRET_KEY` - Your Langfuse secret key
- `LANGFUSE_HOST` - Langfuse host URL (default: https://cloud.langfuse.com)

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
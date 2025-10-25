import { useState } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './ChartPanel.css';

// Demo data for the chart
const demoData = [
  { month: 'Jan', sales: 4000, revenue: 2400, profit: 2400 },
  { month: 'Feb', sales: 3000, revenue: 1398, profit: 2210 },
  { month: 'Mar', sales: 2000, revenue: 9800, profit: 2290 },
  { month: 'Apr', sales: 2780, revenue: 3908, profit: 2000 },
  { month: 'May', sales: 1890, revenue: 4800, profit: 2181 },
  { month: 'Jun', sales: 2390, revenue: 3800, profit: 2500 },
];

interface CSVData {
  [key: string]: string | number;
}

export default function ChartPanel() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [csvData, setCsvData] = useState<CSVData[]>([]);
  const [chartType, setChartType] = useState<'line' | 'bar'>('line');

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setUploadedFile(file);
      parseCSV(file);
    }
  };

  const parseCSV = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target?.result as string;
      const lines = text.split('\n');
      const headers = lines[0].split(',').map((h) => h.trim());

      const data: CSVData[] = [];
      for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
          const values = lines[i].split(',');
          const row: CSVData = {};
          headers.forEach((header, index) => {
            const value = values[index]?.trim();
            // Try to parse as number, otherwise keep as string
            row[header] = isNaN(Number(value)) ? value : Number(value);
          });
          data.push(row);
        }
      }
      setCsvData(data);
    };
    reader.readAsText(file);
  };

  const dataToDisplay = csvData.length > 0 ? csvData : demoData;

  return (
    <div className="chart-panel">
      <div className="chart-header">
        <h2>📊 Data Visualization</h2>
      </div>

      <div className="upload-section">
        <div className="upload-card">
          <h3>📁 Upload CSV File</h3>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            className="file-input"
            id="csv-upload"
          />
          <label htmlFor="csv-upload" className="upload-button">
            {uploadedFile ? `Selected: ${uploadedFile.name}` : 'Choose CSV File'}
          </label>
          {uploadedFile && (
            <p className="file-info">
              📄 {csvData.length} rows loaded
            </p>
          )}
        </div>

        <div className="chart-controls">
          <label>Chart Type:</label>
          <div className="button-group">
            <button
              className={chartType === 'line' ? 'active' : ''}
              onClick={() => setChartType('line')}
            >
              📈 Line Chart
            </button>
            <button
              className={chartType === 'bar' ? 'active' : ''}
              onClick={() => setChartType('bar')}
            >
              📊 Bar Chart
            </button>
          </div>
        </div>
      </div>

      <div className="chart-container">
        <h3>{csvData.length > 0 ? 'Your Data' : 'Demo Chart'}</h3>
        <ResponsiveContainer width="100%" height={400}>
          {chartType === 'line' ? (
            <LineChart data={dataToDisplay}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={Object.keys(dataToDisplay[0] || {})[0]} />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(dataToDisplay[0] || {})
                .slice(1)
                .map((key, index) => (
                  <Line
                    key={key}
                    type="monotone"
                    dataKey={key}
                    stroke={['#8884d8', '#82ca9d', '#ffc658'][index % 3]}
                    strokeWidth={2}
                  />
                ))}
            </LineChart>
          ) : (
            <BarChart data={dataToDisplay}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={Object.keys(dataToDisplay[0] || {})[0]} />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(dataToDisplay[0] || {})
                .slice(1)
                .map((key, index) => (
                  <Bar
                    key={key}
                    dataKey={key}
                    fill={['#8884d8', '#82ca9d', '#ffc658'][index % 3]}
                  />
                ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}

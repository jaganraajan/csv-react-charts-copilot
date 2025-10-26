import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './Chatbot.css';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      const errorMessage: Message = {
        role: 'system',
        content: 'Please upload a CSV file.',
      };
      setMessages((prev) => [...prev, errorMessage]);
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/api/upload-csv`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadedFile(response.data.filename);
      
      const successMessage: Message = {
        role: 'system',
        content: `✅ CSV file "${response.data.filename}" uploaded successfully! You can now ask questions about your data.`,
      };
      setMessages((prev) => [...prev, successMessage]);
    } catch (error) {
      console.error('Error uploading file:', error);
      const errorMessage: Message = {
        role: 'system',
        content: 'Failed to upload CSV file. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: input,
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend is running and Azure OpenAI is configured.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h2>💬 CSV Analysis Assistant</h2>
        <p>Upload a CSV file and ask questions about your data!</p>
        <div className="file-upload-section">
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
            id="csv-file-input"
          />
          <label htmlFor="csv-file-input" className="upload-button">
            📄 Upload CSV File
          </label>
          {uploadedFile && (
            <span className="uploaded-file-name">
              Current: {uploadedFile}
            </span>
          )}
        </div>
      </div>
      <div className="chatbot-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>👋 Hello! I can help you analyze CSV data.</p>
            <p>Upload a CSV file or try asking about the demo data:</p>
            <ul style={{ textAlign: 'left', marginTop: '10px' }}>
              <li>"Show me the CSV data"</li>
              <li>"Analyze the price column"</li>
              <li>"How many rows are there?"</li>
              <li>"What's the average revenue?"</li>
            </ul>
          </div>
        )}
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${
              message.role === 'user'
                ? 'user-message'
                : message.role === 'system'
                ? 'system-message'
                : 'assistant-message'
            }`}
          >
            <div className="message-avatar">
              {message.role === 'user' ? '👤' : message.role === 'system' ? '📢' : '🤖'}
            </div>
            <div className="message-content">{message.content}</div>
          </div>
        ))}
        {loading && (
          <div className="message assistant-message">
            <div className="message-avatar">🤖</div>
            <div className="message-content typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form className="chatbot-input" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me about your CSV data..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

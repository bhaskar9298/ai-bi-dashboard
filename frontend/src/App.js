import React, { useState } from 'react';
import axios from 'axios';
import ChartView from './components/ChartView';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Example queries
  const exampleQueries = [
    'show total sales by category',
    'average price per region',
    'total revenue by quarter',
    'top 5 products by sales amount',
    'sales distribution by region'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/generate_chart`, {
        prompt: query
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuery(example);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI-Driven BI Dashboard</h1>
        <p className="subtitle">Ask questions in natural language, get instant visualizations</p>
      </header>

      <main className="App-main">
        <div className="query-section">
          <form onSubmit={handleSubmit} className="query-form">
            <div className="input-group">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., show total sales by category last quarter"
                className="query-input"
                disabled={loading}
              />
              <button 
                type="submit" 
                className="submit-button"
                disabled={loading}
              >
                {loading ? '⏳ Processing...' : '🚀 Generate'}
              </button>
            </div>
          </form>

          <div className="examples">
            <p className="examples-label">Try these examples:</p>
            <div className="examples-grid">
              {exampleQueries.map((example, idx) => (
                <button
                  key={idx}
                  onClick={() => handleExampleClick(example)}
                  className="example-button"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Processing your query through AI agents...</p>
            <div className="loading-steps">
              <div className="step">📋 Analyzing schema...</div>
              <div className="step">🤖 Generating MongoDB query...</div>
              <div className="step">⚡ Executing query...</div>
              <div className="step">📊 Creating visualization...</div>
            </div>
          </div>
        )}

        {result && result.success && (
          <ChartView result={result} />
        )}

        {result && !result.success && (
          <div className="error-message">
            <h3>❌ Query Failed</h3>
            <p>{result.error || 'Unknown error occurred'}</p>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by LangChain, MongoDB, and React | Built with ❤️</p>
      </footer>
    </div>
  );
}

export default App;

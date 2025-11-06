import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChartView from './components/ChartView';
import DataUpload from './components/DataUpload';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dataSourceInfo, setDataSourceInfo] = useState(null);
  const [showUpload, setShowUpload] = useState(false);

  // Example queries for reconciliation data
  const exampleQueries = [
    'show total amount by status',
    'reconciliation records by month',
    'average transaction amount by type',
    'top 10 records by amount',
    'status distribution breakdown',
    'monthly reconciliation trend'
  ];

  // Fetch data source info on mount
  useEffect(() => {
    fetchDataSourceInfo();
  }, []);

  const fetchDataSourceInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/data-source`);
      setDataSourceInfo(response.data);
      
      // Auto-show upload if no data
      if (!response.data.has_data) {
        setShowUpload(true);
      }
    } catch (err) {
      console.error('Failed to fetch data source info:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    // Check if data exists
    if (dataSourceInfo && !dataSourceInfo.has_data) {
      setError('No data available. Please upload JSON data first.');
      setShowUpload(true);
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

  const handleUploadSuccess = () => {
    fetchDataSourceInfo();
    setShowUpload(false);
    setError(null);
    setResult(null);
  };

  const handleClearData = async () => {
    if (!window.confirm('Are you sure you want to clear all data?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/clear-data`);
      fetchDataSourceInfo();
      setResult(null);
      setError(null);
      alert('Data cleared successfully');
    } catch (err) {
      alert('Failed to clear data: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>📊 Reconciliation DataFlow Dashboard Agent</h1>
        <p className="subtitle">AI-Powered Reconciliation Data Analysis (Prototype 1)</p>
        
        {/* Data Source Status */}
        <div className="data-status">
          {dataSourceInfo && (
            <>
              {dataSourceInfo.has_data ? (
                <div className="status-badge status-active">
                  ✅ Data Loaded: {dataSourceInfo.record_count} records
                  <button 
                    className="status-button"
                    onClick={() => setShowUpload(!showUpload)}
                    title="Upload new data"
                  >
                    📤 Upload New
                  </button>
                  <button 
                    className="status-button status-danger"
                    onClick={handleClearData}
                    title="Clear all data"
                  >
                    🗑️ Clear
                  </button>
                </div>
              ) : (
                <div className="status-badge status-inactive">
                  ⚠️ No Data Loaded
                  <button 
                    className="status-button"
                    onClick={() => setShowUpload(true)}
                  >
                    📤 Upload JSON Data
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </header>

      <main className="App-main">
        {/* Upload Section */}
        {showUpload && (
          <DataUpload 
            apiUrl={API_URL}
            onSuccess={handleUploadSuccess}
            onCancel={() => setShowUpload(false)}
          />
        )}

        {/* Query Section */}
        {dataSourceInfo && dataSourceInfo.has_data && (
          <div className="query-section">
            <form onSubmit={handleSubmit} className="query-form">
              <div className="input-group">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask a question about your reconciliation data..."
                  className="query-input"
                  disabled={loading}
                />
                <button 
                  type="submit" 
                  className="submit-button"
                  disabled={loading}
                >
                  {loading ? '⏳ Processing...' : '🚀 Analyze'}
                </button>
              </div>
            </form>

            <div className="examples">
              <p className="examples-label">💡 Try these example queries:</p>
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
        )}

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {/* Loading Display */}
        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Processing your query through AI agents...</p>
            <div className="loading-steps">
              <div className="step">📋 Analyzing data schema...</div>
              <div className="step">🤖 Generating MongoDB query...</div>
              <div className="step">⚡ Executing aggregation...</div>
              <div className="step">📊 Creating visualization...</div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {result && result.success && (
          <ChartView result={result} />
        )}

        {result && !result.success && (
          <div className="error-message">
            <h3>❌ Query Failed</h3>
            <p>{result.error || 'Unknown error occurred'}</p>
          </div>
        )}

        {/* Data Source Info */}
        {dataSourceInfo && dataSourceInfo.has_data && dataSourceInfo.sample_fields && (
          <div className="data-info">
            <h3>📝 Available Data Fields</h3>
            <div className="fields-list">
              {dataSourceInfo.sample_fields
                .filter(f => !f.startsWith('_'))
                .map((field, idx) => (
                  <span key={idx} className="field-tag">{field}</span>
                ))}
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Reconciliation DataFlow Dashboard Agent v1.0 | Powered by LangChain, MongoDB & React</p>
      </footer>
    </div>
  );
}

export default App;

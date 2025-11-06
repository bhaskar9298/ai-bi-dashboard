import React, { useState } from 'react';
import axios from 'axios';
import './DataUpload.css';

function DataUpload({ apiUrl, onSuccess, onCancel }) {
  const [file, setFile] = useState(null);
  const [jsonText, setJsonText] = useState('');
  const [uploadMode, setUploadMode] = useState('file'); // 'file' or 'text'
  const [dropExisting, setDropExisting] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.json')) {
        setError('Please select a JSON file');
        return;
      }
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleFileDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      if (!droppedFile.name.endsWith('.json')) {
        setError('Please drop a JSON file');
        return;
      }
      setFile(droppedFile);
      setError(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const validateJson = (text) => {
    try {
      JSON.parse(text);
      return true;
    } catch {
      return false;
    }
  };

  const handleUpload = async () => {
    setError(null);
    setUploadResult(null);

    if (uploadMode === 'file' && !file) {
      setError('Please select a file');
      return;
    }

    if (uploadMode === 'text' && !jsonText.trim()) {
      setError('Please enter JSON data');
      return;
    }

    if (uploadMode === 'text' && !validateJson(jsonText)) {
      setError('Invalid JSON format');
      return;
    }

    setUploading(true);

    try {
      let response;

      if (uploadMode === 'file') {
        // Upload file
        const formData = new FormData();
        formData.append('file', file);
        formData.append('drop_existing', dropExisting);

        response = await axios.post(`${apiUrl}/upload-json`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      } else {
        // Upload text
        const formData = new FormData();
        formData.append('json_data', jsonText);
        formData.append('drop_existing', dropExisting);

        response = await axios.post(`${apiUrl}/ingest-json-text`, formData);
      }

      setUploadResult(response.data);
      
      // Auto-close after success
      setTimeout(() => {
        if (onSuccess) {
          onSuccess();
        }
      }, 2000);

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const loadSampleData = () => {
    const sampleJson = {
      "records": [
        {
          "id": "TXN001",
          "date": "2024-01-15",
          "type": "payment",
          "status": "reconciled",
          "amount": 1250.50,
          "source": "Bank A",
          "destination": "Account 123",
          "category": "revenue"
        },
        {
          "id": "TXN002",
          "date": "2024-01-16",
          "type": "refund",
          "status": "pending",
          "amount": 320.00,
          "source": "Account 456",
          "destination": "Customer",
          "category": "expense"
        },
        {
          "id": "TXN003",
          "date": "2024-01-17",
          "type": "payment",
          "status": "reconciled",
          "amount": 2100.75,
          "source": "Bank B",
          "destination": "Account 789",
          "category": "revenue"
        }
      ]
    };
    
    setJsonText(JSON.stringify(sampleJson, null, 2));
    setUploadMode('text');
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <div className="upload-header">
          <h2>📤 Upload Reconciliation Data</h2>
          <button className="close-button" onClick={onCancel}>✕</button>
        </div>

        {/* Mode Selection */}
        <div className="mode-selector">
          <button
            className={`mode-button ${uploadMode === 'file' ? 'active' : ''}`}
            onClick={() => setUploadMode('file')}
          >
            📁 Upload File
          </button>
          <button
            className={`mode-button ${uploadMode === 'text' ? 'active' : ''}`}
            onClick={() => setUploadMode('text')}
          >
            📝 Paste JSON
          </button>
        </div>

        {/* File Upload Mode */}
        {uploadMode === 'file' && (
          <div className="upload-section">
            <div
              className={`drop-zone ${file ? 'has-file' : ''}`}
              onDrop={handleFileDrop}
              onDragOver={handleDragOver}
            >
              {file ? (
                <div className="file-info">
                  <span className="file-icon">📄</span>
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">
                    {(file.size / 1024).toFixed(2)} KB
                  </span>
                  <button
                    className="remove-file"
                    onClick={() => setFile(null)}
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <div className="drop-prompt">
                  <span className="upload-icon">☁️</span>
                  <p>Drag & drop your JSON file here</p>
                  <p className="or-text">or</p>
                  <label className="file-input-label">
                    Choose File
                    <input
                      type="file"
                      accept=".json"
                      onChange={handleFileChange}
                      style={{ display: 'none' }}
                    />
                  </label>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Text Paste Mode */}
        {uploadMode === 'text' && (
          <div className="upload-section">
            <div className="json-input-container">
              <textarea
                className="json-input"
                value={jsonText}
                onChange={(e) => setJsonText(e.target.value)}
                placeholder='Paste your JSON data here...\n\nExample:\n{\n  "records": [\n    {\n      "id": "TXN001",\n      "date": "2024-01-15",\n      "amount": 1250.50,\n      "status": "reconciled"\n    }\n  ]\n}'
              />
            </div>
            <button className="sample-button" onClick={loadSampleData}>
              📋 Load Sample Data
            </button>
          </div>
        )}

        {/* Options */}
        <div className="upload-options">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={dropExisting}
              onChange={(e) => setDropExisting(e.target.checked)}
            />
            <span>Replace existing data</span>
          </label>
        </div>

        {/* Error Display */}
        {error && (
          <div className="upload-error">
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {/* Success Display */}
        {uploadResult && uploadResult.success && (
          <div className="upload-success">
            <h3>✅ Upload Successful!</h3>
            <div className="success-details">
              <p>📊 Records inserted: <strong>{uploadResult.records_inserted}</strong></p>
              <p>🔍 Indexes created: <strong>{uploadResult.indexes_created.length}</strong></p>
              {uploadResult.statistics && (
                <p>📁 Total records: <strong>{uploadResult.statistics.total_records}</strong></p>
              )}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="upload-actions">
          <button
            className="cancel-button"
            onClick={onCancel}
            disabled={uploading}
          >
            Cancel
          </button>
          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={uploading || (!file && !jsonText.trim())}
          >
            {uploading ? '⏳ Uploading...' : '🚀 Upload & Ingest'}
          </button>
        </div>

        {/* Info */}
        <div className="upload-info">
          <p className="info-text">
            ℹ️ Supported formats: JSON files with array of records or single record object
          </p>
          <details className="format-details">
            <summary>📖 See format examples</summary>
            <pre className="format-example">
{`// Array format:
[
  { "id": "1", "amount": 100, ... },
  { "id": "2", "amount": 200, ... }
]

// Object with records key:
{
  "records": [
    { "id": "1", "amount": 100, ... }
  ]
}

// Single record:
{ "id": "1", "amount": 100, ... }`}
            </pre>
          </details>
        </div>
      </div>
    </div>
  );
}

export default DataUpload;

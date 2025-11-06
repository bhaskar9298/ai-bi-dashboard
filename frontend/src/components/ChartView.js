import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import './ChartView.css';

function ChartView({ result }) {
  const [showPipeline, setShowPipeline] = useState(false);
  const [showData, setShowData] = useState(false);

  if (!result || !result.success) {
    return null;
  }

  const { query, pipeline, data, chart_config, plotly_figure, metadata } = result;

  return (
    <div className="chart-view">
      <div className="result-header">
        <div className="query-info">
          <h2>📊 Results for: "{query}"</h2>
          <div className="metadata">
            <span className="badge">📈 {metadata.chart_type}</span>
            <span className="badge">📝 {metadata.record_count} records</span>
          </div>
        </div>
      </div>

      {/* Main Visualization */}
      <div className="visualization-container">
        {plotly_figure && plotly_figure.data && plotly_figure.data.length > 0 ? (
          <Plot
            data={plotly_figure.data}
            layout={{
              ...plotly_figure.layout,
              autosize: true,
              paper_bgcolor: 'rgba(255,255,255,0)',
              plot_bgcolor: 'rgba(255,255,255,0)',
              font: {
                family: 'Arial, sans-serif',
                size: 12
              }
            }}
            config={{
              responsive: true,
              displayModeBar: true,
              displaylogo: false
            }}
            style={{ width: '100%', height: '500px' }}
          />
        ) : (
          <div className="no-chart">
            <p>No visualization available</p>
          </div>
        )}
      </div>

      {/* Chart Details */}
      {chart_config && chart_config.reasoning && (
        <div className="chart-reasoning">
          <h4>💡 Chart Selection Reasoning:</h4>
          <p>{chart_config.reasoning}</p>
        </div>
      )}

      {/* Toggle Sections */}
      <div className="toggle-sections">
        <button
          className="toggle-button"
          onClick={() => setShowPipeline(!showPipeline)}
        >
          {showPipeline ? '▼' : '▶'} MongoDB Query Pipeline
        </button>

        {showPipeline && (
          <div className="code-block">
            <pre>{JSON.stringify(pipeline, null, 2)}</pre>
            <button
              className="copy-button"
              onClick={() => {
                navigator.clipboard.writeText(JSON.stringify(pipeline, null, 2));
                alert('Pipeline copied to clipboard!');
              }}
            >
              📋 Copy
            </button>
          </div>
        )}

        <button
          className="toggle-button"
          onClick={() => setShowData(!showData)}
        >
          {showData ? '▼' : '▶'} Raw Data ({data.length} records)
        </button>

        {showData && (
          <div className="data-table-container">
            {data.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    {Object.keys(data[0]).map((key) => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((value, i) => (
                        <td key={i}>
                          {typeof value === 'object'
                            ? JSON.stringify(value)
                            : String(value)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No data available</p>
            )}
          </div>
        )}
      </div>

      {/* Export Options */}
      <div className="export-section">
        <h4>📥 Export Options:</h4>
        <div className="export-buttons">
          <button
            className="export-button"
            onClick={() => {
              const dataStr = JSON.stringify(data, null, 2);
              const dataBlob = new Blob([dataStr], { type: 'application/json' });
              const url = URL.createObjectURL(dataBlob);
              const link = document.createElement('a');
              link.href = url;
              link.download = 'query-results.json';
              link.click();
            }}
          >
            💾 Download JSON
          </button>
          <button
            className="export-button"
            onClick={() => {
              const csv = convertToCSV(data);
              const csvBlob = new Blob([csv], { type: 'text/csv' });
              const url = URL.createObjectURL(csvBlob);
              const link = document.createElement('a');
              link.href = url;
              link.download = 'query-results.csv';
              link.click();
            }}
          >
            📊 Download CSV
          </button>
        </div>
      </div>
    </div>
  );
}

// Helper function to convert data to CSV
function convertToCSV(data) {
  if (!data || data.length === 0) return '';

  const headers = Object.keys(data[0]);
  const csvRows = [];

  // Add headers
  csvRows.push(headers.join(','));

  // Add data rows
  for (const row of data) {
    const values = headers.map((header) => {
      const value = row[header];
      const escaped = String(value).replace(/"/g, '""');
      return `"${escaped}"`;
    });
    csvRows.push(values.join(','));
  }

  return csvRows.join('\n');
}

export default ChartView;

import pandas as pd
import numpy as np
import base64
import json
from datetime import datetime
from typing import Optional

def generate_html_report(df: pd.DataFrame, report_data: dict, output_path: str = "report.html"):
    """
    Generate a standalone HTML report with a premium design.
    """
    
    # Modern CSS for premium look
    css = """
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --bg: #0f172a;
        --card-bg: #1e293b;
        --text: #f8fafc;
        --text-dim: #94a3b8;
        --border: #334155;
        --accent: #22d3ee;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    body {
        font-family: 'Inter', -apple-system, sans-serif;
        background-color: var(--bg);
        color: var(--text);
        margin: 0;
        padding: 40px;
        line-height: 1.6;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
    }

    header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 40px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 20px;
    }

    h1 {
        margin: 0;
        font-size: 2.5rem;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .timestamp {
        color: var(--text-dim);
        font-size: 0.9rem;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 40px;
    }

    .card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    .card-title {
        color: var(--text-dim);
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 40px 0 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }

    th {
        color: var(--text-dim);
        font-weight: 600;
        font-size: 0.875rem;
    }

    .badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-dtype { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
    .badge-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
    .badge-success { background: rgba(16, 185, 129, 0.2); color: #34d399; }

    .chart-container {
        height: 100px;
        display: flex;
        align-items: flex-end;
        gap: 2px;
        margin-top: 10px;
    }

    .bar {
        background: var(--primary);
        flex: 1;
        border-radius: 2px 2px 0 0;
        min-height: 2px;
        transition: height 0.3s ease;
    }

    .bar:hover {
        background: var(--accent);
    }

    .scroll-x {
        overflow-x: auto;
    }
    """

    # Generate content
    rows, cols = report_data['shape']
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dfxpy Data Report</title>
        <style>{css}</style>
    </head>
    <body>
        <div class="container">
            <header>
                <div>
                    <h1>Dfxpy Analysis</h1>
                    <div class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                <div class="badge badge-success">v{report_data.get('version', '0.2.6')}</div>
            </header>

            <div class="grid">
                <div class="card">
                    <div class="card-title">Rows</div>
                    <div class="stat-value">{rows:,}</div>
                </div>
                <div class="card">
                    <div class="card-title">Columns</div>
                    <div class="stat-value">{cols:,}</div>
                </div>
                <div class="card">
                    <div class="card-title">Missing Cells</div>
                    <div class="stat-value">{sum(report_data['missing_values'].values()):,}</div>
                </div>
            </div>

            <div class="section-title">Column Overview</div>
            <div class="card scroll-x">
                <table>
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Type</th>
                            <th>Unique</th>
                            <th>Missing</th>
                            <th>Distribution</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for col in df.columns:
        dtype = str(df[col].dtype)
        unique = df[col].nunique()
        missing = df[col].isnull().sum()
        missing_pct = (missing / rows) * 100
        
        # Simple Histogram using DIVs
        chart_html = '<div class="chart-container">'
        if pd.api.types.is_numeric_dtype(df[col]) and not df[col].dropna().empty:
            counts, _ = np.histogram(df[col].dropna(), bins=20)
            max_count = max(counts) if len(counts) > 0 else 1
            for count in counts:
                height = (count / max_count) * 100 if max_count > 0 else 0
                chart_html += f'<div class="bar" style="height: {height}%" title="{count} values"></div>'
        else:
            chart_html += '<span style="color: var(--text-dim); font-size: 0.75rem;">N/A</span>'
        chart_html += '</div>'

        html += f"""
                        <tr>
                            <td><strong>{col}</strong></td>
                            <td><span class="badge badge-dtype">{dtype}</span></td>
                            <td>{unique:,}</td>
                            <td>
                                {missing:,} 
                                {f'<span class="badge badge-warning">{missing_pct:.1f}%</span>' if missing_pct > 0 else ''}
                            </td>
                            <td>{chart_html}</td>
                        </tr>
        """

    html += """
                    </tbody>
                </table>
            </div>

            <div class="section-title">Sample Data</div>
            <div class="card scroll-x">
                <table style="font-size: 0.8rem;">
                    <thead>
                        <tr>
    """
    
    # Sample Table Headers
    for col in df.columns:
        html += f"<th>{col}</th>"
    
    html += """
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Sample Table Body
    sample_df = df.head(10)
    for _, row in sample_df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{str(val)[:50]}{'...' if len(str(val)) > 50 else ''}</td>"
        html += "</tr>"

    html += """
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return output_path

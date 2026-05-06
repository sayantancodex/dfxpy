import pandas as pd
import numpy as np
import json
from datetime import datetime
from typing import Optional, Dict, Any

def generate_html_report(df: pd.DataFrame, report_data: dict, output_path: str = "report.html"):
    """
    Generate a standalone, interactive HTML report with a premium design.
    """
    
    # 1. Advanced Data Processing for the Report
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().fillna(0) if not numeric_df.empty else pd.DataFrame()
    
    # Missingness Heatmap Data (Downsampled for performance)
    msno_sample = df.isnull().astype(int)
    if len(df) > 100:
        msno_sample = msno_sample.iloc[np.linspace(0, len(df)-1, 100).astype(int)]
    
    # Column Details
    col_details = {}
    for col in df.columns:
        series = df[col]
        details = {
            "dtype": str(series.dtype),
            "missing": int(series.isnull().sum()),
            "unique": int(series.nunique()),
        }
        
        if pd.api.types.is_numeric_dtype(series):
            details["stats"] = {
                "Mean": f"{series.mean():.2f}",
                "Median": f"{series.median():.2f}",
                "Std": f"{series.std():.2f}",
                "Min": f"{series.min():.2f}",
                "Max": f"{series.max():.2f}",
                "Skew": f"{series.skew():.2f}" if hasattr(series, 'skew') else "N/A"
            }
            # Histogram
            if not series.dropna().empty:
                counts, bins = np.histogram(series.dropna(), bins=20)
                details["hist"] = {"counts": counts.tolist(), "bins": bins.tolist()}
        else:
            # Top Categories
            top_cats = series.value_counts().head(10)
            details["top_cats"] = {str(k): int(v) for k, v in top_cats.items()}
            
        col_details[col] = details

    # 2. Modern CSS (Premium, Glassmorphism, Responsive)
    css = """
    :root {
        --primary: #6366f1;
        --accent: #22d3ee;
        --bg: #0b0f1a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text: #f8fafc;
        --text-dim: #94a3b8;
        --border: rgba(51, 65, 85, 0.5);
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    body {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: radial-gradient(circle at top right, #1e1b4b, #0b0f1a);
        color: var(--text);
        margin: 0;
        min-height: 100vh;
        overflow-x: hidden;
    }

    .sidebar {
        width: 260px;
        position: fixed;
        top: 0;
        bottom: 0;
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(12px);
        border-right: 1px solid var(--border);
        padding: 30px 20px;
        z-index: 100;
    }

    .main-content {
        margin-left: 260px;
        padding: 40px;
    }

    .logo {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(to right, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 40px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .nav-item {
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
        color: var(--text-dim);
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .nav-item:hover, .nav-item.active {
        background: rgba(99, 102, 241, 0.15);
        color: var(--text);
    }

    .card {
        background: var(--card-bg);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .grid-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        text-align: center;
        padding: 20px;
    }

    .stat-label { color: var(--text-dim); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { font-size: 2rem; font-weight: 700; margin-top: 5px; }

    .tab-content { display: none; animation: fadeIn 0.4s ease; }
    .tab-content.active { display: block; }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* Heatmap Styles */
    .heatmap-grid {
        display: grid;
        gap: 2px;
    }

    .heatmap-cell {
        aspect-ratio: 1;
        border-radius: 2px;
        transition: transform 0.2s;
        cursor: pointer;
    }

    .heatmap-cell:hover {
        transform: scale(1.2);
        z-index: 10;
        outline: 2px solid var(--accent);
    }

    /* Charts */
    .svg-chart { width: 100%; height: 200px; }
    .bar { fill: var(--primary); rx: 4; transition: 0.3s; }
    .bar:hover { fill: var(--accent); }

    /* Table Styles */
    .table-container { overflow-x: auto; border-radius: 12px; }
    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th { text-align: left; padding: 16px; border-bottom: 1px solid var(--border); color: var(--text-dim); }
    td { padding: 16px; border-bottom: 1px solid var(--border); }
    tr:hover { background: rgba(255, 255, 255, 0.02); }

    .search-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        padding: 10px 16px;
        border-radius: 8px;
        color: white;
        width: 100%;
        max-width: 300px;
        margin-bottom: 20px;
    }

    .tooltip {
        position: fixed;
        background: #1e293b;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.2s;
        z-index: 1000;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    """

    # 3. HTML Content Construction
    rows, cols = report_data['shape']
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dfxpy Premium Report</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
        <style>{css}</style>
    </head>
    <body>
        <div class="tooltip" id="tooltip"></div>

        <div class="sidebar">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                DFXPY
            </div>
            <div class="nav-item active" onclick="showTab('overview', this)">Overview</div>
            <div class="nav-item" onclick="showTab('variables', this)">Variables</div>
            <div class="nav-item" onclick="showTab('correlations', this)">Correlations</div>
            <div class="nav-item" onclick="showTab('sample', this)">Data Preview</div>
            
            <div style="position: absolute; bottom: 30px; left: 20px; font-size: 0.8rem; color: var(--text-dim);">
                Version {report_data.get('version', '0.3.2')}<br>
                {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>

        <div class="main-content">
            <!-- TAB: OVERVIEW -->
            <div id="overview" class="tab-content active">
                <h2 style="margin-top: 0;">Dataset Summary</h2>
                <div class="grid-stats">
                    <div class="card stat-card">
                        <div class="stat-label">Total Rows</div>
                        <div class="stat-value">{rows:,}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-label">Total Columns</div>
                        <div class="stat-value">{cols:,}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-label">Missing Cells</div>
                        <div class="stat-value">{sum(report_data['missing_values'].values()):,}</div>
                    </div>
                    <div class="card stat-card">
                        <div class="stat-label">Numeric Ratio</div>
                        <div class="stat-value">{int(len(numeric_df.columns)/cols*100)}%</div>
                    </div>
                </div>

                <div class="card">
                    <h3>Missingness Map</h3>
                    <div class="heatmap-grid" style="grid-template-columns: repeat({cols}, 1fr); height: 150px;">
    """
    
    # Missingness Heatmap Cells
    for col_idx, col in enumerate(df.columns):
        missing_pattern = msno_sample[col].values
        html += f'<div style="display: grid; grid-template-rows: repeat({len(msno_sample)}, 1fr);">'
        for val in missing_pattern:
            color = "#1e293b" if val == 0 else "#ef4444"
            html += f'<div style="background: {color};"></div>'
        html += "</div>"
    
    html += """
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px; color: var(--text-dim); font-size: 0.7rem;">
                        <span>Start</span>
                        <span>Downsampled Sequence</span>
                        <span>End</span>
                    </div>
                </div>
            </div>

            <!-- TAB: VARIABLES -->
            <div id="variables" class="tab-content">
                <h2 style="margin-top: 0;">Detailed Column Analysis</h2>
    """
    
    for col, data in col_details.items():
        html += f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: var(--accent);">{col}</h3>
                        <span style="font-size: 0.8rem; padding: 4px 10px; background: rgba(99,102,241,0.2); border-radius: 20px;">{data['dtype']}</span>
                    </div>
                    
                    <div style="display: flex; gap: 30px; margin-top: 20px;">
                        <div style="flex: 1;">
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
        """
        
        # Stats List
        stats_to_show = {"Missing": f"{data['missing']:,} ({data['missing']/rows*100:.1f}%)", "Unique": f"{data['unique']:,}"}
        if "stats" in data:
            stats_to_show.update(data["stats"])
            
        for s_label, s_val in stats_to_show.items():
            html += f"""
                                <div>
                                    <div style="font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase;">{s_label}</div>
                                    <div style="font-size: 1.1rem; font-weight: 600;">{s_val}</div>
                                </div>
            """
            
        html += """
                            </div>
                        </div>
                        <div style="flex: 2; height: 180px;">
        """
        
        # Numeric Histogram (SVG)
        if "hist" in data:
            counts = data["hist"]["counts"]
            bins = data["hist"]["bins"]
            max_c = max(counts) if counts else 1
            html += f'<svg class="svg-chart" viewBox="0 0 1000 200" preserveAspectRatio="none">'
            bar_w = 1000 / len(counts)
            for i, c in enumerate(counts):
                h = (c / max_c) * 180
                x = i * bar_w
                y = 200 - h
                html += f'<rect x="{x}" y="{y}" width="{bar_w - 2}" height="{h}" class="bar" onmouseover="showTooltip(event, \'{c} values in bin [{bins[i]:.1f}, {bins[i+1]:.1f}]\')" onmouseout="hideTooltip()"></rect>'
            html += '</svg>'
        # Categorical Bar Chart (SVG)
        elif "top_cats" in data:
            cats = data["top_cats"]
            if cats:
                max_v = max(cats.values())
                html += f'<svg class="svg-chart" viewBox="0 0 1000 200" preserveAspectRatio="none">'
                bar_h = 200 / len(cats)
                for i, (cat, val) in enumerate(cats.items()):
                    w = (val / max_v) * 900
                    y = i * bar_h
                    html += f'<rect x="0" y="{y}" width="{w}" height="{bar_h - 4}" class="bar" onmouseover="showTooltip(event, \'{cat}: {val} times\')" onmouseout="hideTooltip()"></rect>'
                    html += f'<text x="{w + 10}" y="{y + bar_h/2 + 5}" fill="var(--text-dim)" style="font-size: 12px;">{cat}</text>'
                html += '</svg>'
        
        html += """
                        </div>
                    </div>
                </div>
        """

    # TAB: CORRELATIONS
    html += f"""
            </div>

            <div id="correlations" class="tab-content">
                <h2 style="margin-top: 0;">Feature Correlation Matrix</h2>
                <div class="card">
                    <div class="heatmap-grid" style="grid-template-columns: repeat({len(corr_matrix.columns)}, 1fr); max-width: 600px; margin: 0 auto;">
    """
    
    if not corr_matrix.empty:
        for i, row_label in enumerate(corr_matrix.index):
            for j, col_label in enumerate(corr_matrix.columns):
                val = corr_matrix.iloc[i, j]
                # Color scale: -1 (Blue) to 0 (Dark) to 1 (Red/Purple)
                opacity = abs(val)
                color = f"rgba(99, 102, 241, {opacity})" if val > 0 else f"rgba(239, 68, 68, {opacity})"
                html += f'<div class="heatmap-cell" style="background: {color};" onmouseover="showTooltip(event, \'{row_label} x {col_label}: {val:.3f}\')" onmouseout="hideTooltip()"></div>'
    else:
        html += "<p>Not enough numeric features for correlation analysis.</p>"
        
    html += """
                    </div>
                    <div style="text-align: center; margin-top: 20px; font-size: 0.8rem; color: var(--text-dim);">
                        Hover over cells to see exact correlation coefficients.
                    </div>
                </div>
            </div>

            <!-- TAB: SAMPLE DATA -->
            <div id="sample" class="tab-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 style="margin: 0;">Data Preview (Top 20)</h2>
                    <input type="text" id="sampleSearch" class="search-box" placeholder="Search rows..." onkeyup="filterTable()">
                </div>
                <div class="card table-container">
                    <table id="sampleTable">
                        <thead>
                            <tr>
    """
    for col in df.columns:
        html += f"<th>{col}</th>"
    
    html += "</tr></thead><tbody>"
    
    for _, row in df.head(20).iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{str(val)[:100]}{'...' if len(str(val)) > 100 else ''}</td>"
        html += "</tr>"
        
    html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            function showTab(tabId, el) {
                document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
                document.getElementById(tabId).classList.add('active');
                el.classList.add('active');
            }

            const tooltip = document.getElementById('tooltip');
            function showTooltip(e, text) {
                tooltip.innerHTML = text;
                tooltip.style.opacity = '1';
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
            }
            function hideTooltip() {
                tooltip.style.opacity = '0';
            }

            function filterTable() {
                const input = document.getElementById('sampleSearch');
                const filter = input.value.toLowerCase();
                const table = document.getElementById('sampleTable');
                const tr = table.getElementsByTagName('tr');

                for (let i = 1; i < tr.length; i++) {
                    let text = tr[i].textContent || tr[i].innerText;
                    tr[i].style.display = text.toLowerCase().indexOf(filter) > -1 ? "" : "none";
                }
            }
        </script>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return output_path

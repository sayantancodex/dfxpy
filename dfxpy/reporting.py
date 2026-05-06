import pandas as pd
import numpy as np
import json
from datetime import datetime
from typing import Optional, Dict, Any

def generate_html_report(df: pd.DataFrame, report_data: dict, output_path: str = "report.html"):
    """
    Generate a standalone, interactive HTML report with a professional Light/Dark theme toggle.
    """
    
    # 1. Advanced Data Processing
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().fillna(0) if not numeric_df.empty else pd.DataFrame()
    
    # Missingness Heatmap Data (Downsampled)
    msno_sample = df.isnull().astype(int)
    if len(df) > 100:
        msno_sample = msno_sample.iloc[np.linspace(0, len(df)-1, 100).astype(int)]
    
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
                "Max": f"{series.max():.2f}"
            }
            if not series.dropna().empty:
                counts, bins = np.histogram(series.dropna(), bins=20)
                details["hist"] = {"counts": counts.tolist(), "bins": bins.tolist()}
        else:
            top_cats = series.value_counts().head(10)
            details["top_cats"] = {str(k): int(v) for k, v in top_cats.items()}
        col_details[col] = details

    # 2. Dual-Theme CSS (Light default)
    css = """
    :root {
        --primary: #4f46e5;
        --accent: #06b6d4;
        --bg: #f8fafc;
        --sidebar-bg: #ffffff;
        --card-bg: #ffffff;
        --text: #1e293b;
        --text-dim: #64748b;
        --border: #e2e8f0;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --chart-bar: #4f46e5;
    }

    [data-theme="dark"] {
        --bg: #0f172a;
        --sidebar-bg: #1e293b;
        --card-bg: #1e293b;
        --text: #f8fafc;
        --text-dim: #94a3b8;
        --border: #334155;
        --chart-bar: #818cf8;
    }

    body {
        font-family: 'Inter', -apple-system, sans-serif;
        background-color: var(--bg);
        color: var(--text);
        margin: 0;
        transition: background-color 0.3s, color 0.3s;
    }

    .sidebar {
        width: 260px;
        position: fixed;
        top: 0;
        bottom: 0;
        background: var(--sidebar-bg);
        border-right: 1px solid var(--border);
        padding: 30px 20px;
        z-index: 100;
        transition: background-color 0.3s, border-color 0.3s;
    }

    .main-content {
        margin-left: 260px;
        padding: 40px;
    }

    .logo {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--primary);
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
        transition: 0.2s;
        color: var(--text-dim);
    }

    .nav-item:hover, .nav-item.active {
        background: rgba(79, 70, 229, 0.1);
        color: var(--primary);
        font-weight: 600;
    }

    .theme-toggle {
        position: absolute;
        bottom: 80px;
        left: 20px;
        padding: 10px 16px;
        border: 1px solid var(--border);
        border-radius: 8px;
        cursor: pointer;
        background: var(--card-bg);
        color: var(--text);
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: 0.3s;
    }

    .card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .grid-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card { text-align: center; }
    .stat-label { color: var(--text-dim); font-size: 0.75rem; text-transform: uppercase; font-weight: 600; }
    .stat-value { font-size: 1.8rem; font-weight: 700; margin-top: 4px; }

    .tab-content { display: none; }
    .tab-content.active { display: block; }

    .heatmap-grid { display: grid; gap: 2px; }
    .svg-chart { width: 100%; height: 180px; }
    .bar { fill: var(--chart-bar); rx: 4; }
    .bar:hover { fill: var(--accent); }

    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th { text-align: left; padding: 12px; border-bottom: 2px solid var(--border); color: var(--text-dim); font-weight: 600; }
    td { padding: 12px; border-bottom: 1px solid var(--border); }
    tr:hover { background: rgba(0,0,0,0.02); }
    [data-theme="dark"] tr:hover { background: rgba(255,255,255,0.02); }

    .search-box {
        background: var(--bg);
        border: 1px solid var(--border);
        padding: 8px 14px;
        border-radius: 6px;
        color: var(--text);
        width: 240px;
    }

    .tooltip {
        position: fixed;
        background: #1e293b;
        color: white;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        pointer-events: none;
        opacity: 0;
        z-index: 1000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    """

    # 3. HTML Structure
    rows, cols = report_data['shape']
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en" data-theme="light">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dfxpy Data Report</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <style>{css}</style>
    </head>
    <body>
        <div class="tooltip" id="tooltip"></div>

        <div class="sidebar">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                DFXPY
            </div>
            <div class="nav-item active" onclick="showTab('overview', this)">Overview</div>
            <div class="nav-item" onclick="showTab('variables', this)">Variables</div>
            <div class="nav-item" onclick="showTab('correlations', this)">Correlations</div>
            <div class="nav-item" onclick="showTab('sample', this)">Data Preview</div>
            
            <div class="theme-toggle" onclick="toggleTheme()">
                <span id="theme-icon">🌙</span> <span id="theme-text">Dark Mode</span>
            </div>

            <div style="position: absolute; bottom: 30px; left: 20px; font-size: 0.75rem; color: var(--text-dim);">
                Version {report_data.get('version', '0.3.4')}<br>
                {datetime.now().strftime('%Y-%m-%d %H:%M')}
            </div>
        </div>

        <div class="main-content">
            <div id="overview" class="tab-content active">
                <h2 style="margin-top: 0;">Dataset Summary</h2>
                <div class="grid-stats">
                    <div class="card stat-card"><div class="stat-label">Rows</div><div class="stat-value">{rows:,}</div></div>
                    <div class="card stat-card"><div class="stat-label">Columns</div><div class="stat-value">{cols:,}</div></div>
                    <div class="card stat-card"><div class="stat-label">Missing</div><div class="stat-value">{sum(report_data['missing_values'].values()):,}</div></div>
                    <div class="card stat-card"><div class="stat-label">Numeric</div><div class="stat-value">{len(numeric_df.columns)}</div></div>
                </div>

                <div class="card">
                    <h3 style="margin-top:0">Missingness Map</h3>
                    <div class="heatmap-grid" style="grid-template-columns: repeat({cols}, 1fr); height: 120px; background: var(--bg); border-radius: 8px; overflow: hidden;">
    """
    
    for col in df.columns:
        pattern = msno_sample[col].values
        html += '<div style="display: grid; grid-template-rows: repeat('+str(len(msno_sample))+', 1fr);">'
        for v in pattern:
            html += f'<div style="background: {"var(--border)" if v == 0 else "var(--danger)"};"></div>'
        html += "</div>"
    
    html += """
                    </div>
                </div>
            </div>

            <div id="variables" class="tab-content">
                <h2 style="margin-top:0">Variables</h2>
    """
    
    for col, data in col_details.items():
        html += f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center">
                        <h3 style="margin:0; color:var(--primary)">{col}</h3>
                        <span style="font-size:0.75rem; color:var(--text-dim)">{data['dtype']}</span>
                    </div>
                    <div style="display:flex; gap:40px; margin-top:20px">
                        <div style="width:200px">
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px">
        """
        stats = {"Missing": f"{data['missing']}", "Unique": f"{data['unique']}"}
        if "stats" in data: stats.update(data["stats"])
        for k,v in stats.items():
            html += f'<div><div class="stat-label" style="font-size:0.6rem">{k}</div><div style="font-weight:700">{v}</div></div>'
        
        html += '</div></div><div style="flex:1; height:180px">'
        if "hist" in data:
            c, b = data["hist"]["counts"], data["hist"]["bins"]
            max_c = max(c) if c else 1
            html += '<svg class="svg-chart" viewBox="0 0 1000 200" preserveAspectRatio="none">'
            w = 1000/len(c)
            for i, val in enumerate(c):
                h = (val/max_c)*180; x = i*w; y = 200-h
                html += f'<rect x="{x}" y="{y}" width="{w-2}" height="{h}" class="bar" onmouseover="showT(event,\'{val} values\')" onmouseout="hideT()"></rect>'
            html += '</svg>'
        elif "top_cats" in data:
            cats = data["top_cats"]
            if cats:
                max_v = max(cats.values())
                html += '<svg class="svg-chart" viewBox="0 0 1000 200" preserveAspectRatio="none">'
                h_b = 200/len(cats)
                for i, (k,v) in enumerate(cats.items()):
                    w_b = (v/max_v)*800; y_b = i*h_b
                    html += f'<rect x="0" y="{y_b}" width="{w_b}" height="{h_b-4}" class="bar" onmouseover="showT(event,\'{k}: {v}\')" onmouseout="hideT()"></rect>'
                    html += f'<text x="{w_b+10}" y="{y_b+h_b/2+5}" fill="var(--text-dim)" font-size="12">{k}</text>'
                html += '</svg>'
        html += '</div></div></div>'

    html += f"""
            </div>

            <div id="correlations" class="tab-content">
                <h2 style="margin-top:0">Correlations</h2>
                <div class="card">
                    <div class="heatmap-grid" style="grid-template-columns: repeat({len(corr_matrix.columns)}, 1fr); max-width: 500px; margin: 0 auto;">
    """
    if not corr_matrix.empty:
        for i, r in enumerate(corr_matrix.index):
            for j, c in enumerate(corr_matrix.columns):
                val = corr_matrix.iloc[i,j]
                op = abs(val)
                color = f"rgba(79, 70, 229, {op})" if val > 0 else f"rgba(239, 68, 68, {op})"
                html += f'<div style="aspect-ratio:1; background:{color}; border-radius:2px" onmouseover="showT(event,\'{r} x {c}: {val:.2f}\')" onmouseout="hideT()"></div>'
    else: html += "<p>No numeric data.</p>"

    html += """
                    </div>
                </div>
            </div>

            <div id="sample" class="tab-content">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px">
                    <h2 style="margin:0">Preview</h2>
                    <input type="text" id="q" class="search-box" placeholder="Search..." onkeyup="search()">
                </div>
                <div class="card" style="overflow-x:auto; padding:0">
                    <table id="t">
                        <thead><tr>
    """
    for col in df.columns: html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.head(20).iterrows():
        html += "<tr>"
        for v in row: html += f"<td>{str(v)[:50]}</td>"
        html += "</tr>"
    
    html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            function showTab(id, el) {
                document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
                document.getElementById(id).classList.add('active');
                el.classList.add('active');
            }

            function toggleTheme() {
                const b = document.documentElement;
                const isDark = b.getAttribute('data-theme') === 'dark';
                b.setAttribute('data-theme', isDark ? 'light' : 'dark');
                document.getElementById('theme-icon').innerText = isDark ? '🌙' : '☀️';
                document.getElementById('theme-text').innerText = isDark ? 'Dark Mode' : 'Light Mode';
            }

            const tt = document.getElementById('tooltip');
            function showT(e, txt) {
                tt.innerHTML = txt; tt.style.opacity = '1';
                tt.style.left = (e.clientX + 10) + 'px'; tt.style.top = (e.clientY + 10) + 'px';
            }
            function hideT() { tt.style.opacity = '0'; }

            function search() {
                const q = document.getElementById('q').value.toLowerCase();
                const rows = document.querySelectorAll('#t tbody tr');
                rows.forEach(r => {
                    r.style.display = r.innerText.toLowerCase().includes(q) ? '' : 'none';
                });
            }
        </script>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path

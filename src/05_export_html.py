import json
import os
import pandas as pd

def generar_dashboard():
    print("Generando Dashboard HTML estilo UI Oscura Avanzada (Corrigiendo Layout)...")
    
    with open("output/metricas.json", "r") as f:
        metricas = json.loads(f.read())
    with open("output/matrices.json", "r") as f:
        matrices = json.loads(f.read())
    with open("output/importancias.json", "r") as f:
        importancias = json.loads(f.read())

    df = pd.read_csv("data/data_processed.csv")
    total_malos = int(df['Mala_Calidad_Aire'].sum())
    total_buenos = int(len(df) - total_malos)
    pct_buenos = (total_buenos / len(df)) * 100

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analítico de Modelos</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@200;300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #030612;
            --blue: #0ea5e9;
            --green: #22c55e;
            --pink: #f43f5e;
            --text-main: #e2e8f0;
            --text-muted: #94a3b8;
            --border: rgba(255,255,255,0.05);
        }}
        
        * {{ box-sizing: border-box; }}
        
        body {{
            font-family: 'Montserrat', sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(14, 165, 233, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 50% 30%, rgba(34, 197, 94, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 80% 30%, rgba(244, 63, 94, 0.08) 0%, transparent 40%);
            color: var(--text-main);
            margin: 0;
            display: flex;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        .sidebar {{
            width: 70px;
            min-width: 70px;
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 30px 0;
            gap: 30px;
            background: rgba(3, 6, 18, 0.8);
            z-index: 10;
        }}
        .icon-btn {{
            width: 40px; height: 40px; border-radius: 50%;
            border: 1px solid var(--border);
            display: flex; align-items: center; justify-content: center;
            color: var(--text-muted); cursor: pointer; transition: 0.3s;
            font-size: 1.2rem;
        }}
        .icon-btn:hover, .icon-btn.active {{
            border-color: var(--blue); color: var(--blue);
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.3);
        }}

        .main-content {{
            flex: 1; 
            padding: 20px 40px;
            width: calc(100% - 70px);
        }}

        .header-title {{
            text-align: center; font-weight: 200; font-size: 1.8rem;
            letter-spacing: 12px; margin-bottom: 40px; color: #fff;
        }}

        /* GRID LAYOUTS */
        .grid-3-top {{
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 30px; 
            margin-bottom: 50px;
            width: 100%;
        }}
        .grid-3-bottom {{
            display: grid; 
            grid-template-columns: 1fr 1fr 1.5fr; 
            gap: 30px;
            width: 100%;
        }}

        /* KPI CARDS */
        .kpi-section {{ 
            display: flex; flex-direction: column; gap: 15px; 
            background: rgba(255,255,255,0.01);
            padding: 20px; border-radius: 12px;
            border: 1px solid var(--border);
        }}
        
        .kpi-card {{
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border); padding-bottom: 15px;
        }}
        .kpi-info {{ display: flex; align-items: center; gap: 15px; }}
        .kpi-icon {{
            width: 45px; height: 45px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.4rem;
        }}
        .kpi-icon.blue {{ background: rgba(14, 165, 233, 0.1); color: var(--blue); border: 1px solid var(--blue); box-shadow: 0 0 10px rgba(14, 165, 233, 0.3); }}
        .kpi-icon.green {{ background: rgba(34, 197, 94, 0.1); color: var(--green); border: 1px solid var(--green); box-shadow: 0 0 10px rgba(34, 197, 94, 0.3); }}
        .kpi-icon.pink {{ background: rgba(244, 63, 94, 0.1); color: var(--pink); border: 1px solid var(--pink); box-shadow: 0 0 10px rgba(244, 63, 94, 0.3); }}
        
        .kpi-text h2 {{ margin: 0; font-size: 2.2rem; font-weight: 300; }}
        .kpi-text p {{ margin: 5px 0 0 0; font-size: 0.75rem; color: var(--text-muted); letter-spacing: 1px; }}

        /* IMPORTANT: Chart wrappers constrain canvas size to prevent infinite growth */
        .sparkline-wrapper {{ width: 80px; height: 40px; position: relative; }}
        .chart-wrapper-top {{ width: 100%; height: 180px; position: relative; }}
        .chart-wrapper-bottom {{ width: 100%; height: 220px; position: relative; }}

        .panel-title {{
            font-size: 0.85rem; font-weight: 500; letter-spacing: 2px;
            margin-bottom: 20px; color: #fff; border-bottom: 1px solid var(--border); padding-bottom: 10px;
        }}

        /* TABLE */
        .custom-table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
        .custom-table th {{
            text-align: left; padding: 10px; color: var(--text-muted);
            border-bottom: 1px solid var(--border); font-weight: 400; font-size: 0.75rem;
        }}
        .custom-table td {{ padding: 15px 10px; border-bottom: 1px solid rgba(255,255,255,0.02); }}
        
        .data-bar-cell {{ display: flex; align-items: center; width: 100%; }}
        .data-bar-bg {{ width: 100%; background: rgba(255,255,255,0.05); height: 24px; position: relative; border-radius: 4px; overflow: hidden; }}
        .data-bar-fill {{ height: 100%; position: absolute; left: 0; top: 0; display: flex; align-items: center; padding-left: 8px; font-weight: 600; font-size: 0.75rem; color: #fff; }}
        .data-bar-fill.blue {{ background: linear-gradient(90deg, var(--blue), #38bdf8); }}
        .data-bar-fill.green {{ background: linear-gradient(90deg, var(--green), #4ade80); }}
        
        .pct-cell {{ background: rgba(244, 63, 94, 0.2); color: #fff; text-align: center; font-weight: 600; padding: 8px; border-radius: 4px; border: 1px solid rgba(244, 63, 94, 0.3); }}
    </style>
</head>
<body>

    <!-- SIDEBAR -->
    <div class="sidebar">
        <div class="icon-btn" style="border: none; font-size: 1.5rem; margin-bottom: 20px; cursor: default;">☰</div>
        <div class="icon-btn active" title="Dashboard">📊</div>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="header-title">RENDIMIENTO x PRECISIÓN x MODELOS</div>

        <!-- TOP SECTION -->
        <div class="grid-3-top">
            <!-- Col 1: XGBoost -->
            <div class="kpi-section">
                <div class="kpi-card" style="border-bottom-color: rgba(14, 165, 233, 0.3);">
                    <div class="kpi-info">
                        <div class="kpi-icon blue">X</div>
                        <div class="kpi-text">
                            <h2 id="xgb-auc">0%</h2>
                            <p>XGBOOST AUC-ROC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkBlue"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barBlue"></canvas></div>
            </div>

            <!-- Col 2: Random Forest -->
            <div class="kpi-section">
                <div class="kpi-card" style="border-bottom-color: rgba(34, 197, 94, 0.3);">
                    <div class="kpi-info">
                        <div class="kpi-icon green">R</div>
                        <div class="kpi-text">
                            <h2 id="rf-auc">0%</h2>
                            <p>RANDOM FOREST AUC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkGreen"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barGreen"></canvas></div>
            </div>

            <!-- Col 3: Red Neuronal -->
            <div class="kpi-section">
                <div class="kpi-card" style="border-bottom-color: rgba(244, 63, 94, 0.3);">
                    <div class="kpi-info">
                        <div class="kpi-icon pink">N</div>
                        <div class="kpi-text">
                            <h2 id="mlp-auc">0%</h2>
                            <p>RED NEURONAL AUC</p>
                        </div>
                    </div>
                    <div class="sparkline-wrapper"><canvas id="sparkPink"></canvas></div>
                </div>
                <div class="chart-wrapper-top"><canvas id="barPink"></canvas></div>
            </div>
        </div>

        <!-- BOTTOM SECTION -->
        <div class="grid-3-bottom">
            <!-- Donut -->
            <div class="kpi-section">
                <div class="panel-title">PROPORCIÓN DE CALIDAD DE AIRE</div>
                <div class="chart-wrapper-bottom">
                    <canvas id="donutChart"></canvas>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: var(--text-muted); font-size: 0.8rem;">
                        <span style="font-size: 1.8rem; color: #fff; display: block; font-weight:300;">{pct_buenos:.0f}%</span>
                        Aceptable
                    </div>
                </div>
            </div>

            <!-- Horizontal Bars -->
            <div class="kpi-section">
                <div class="panel-title">IMPORTANCIA POR VARIABLE</div>
                <div class="chart-wrapper-bottom">
                    <canvas id="horizBar"></canvas>
                </div>
            </div>

            <!-- Table -->
            <div class="kpi-section">
                <div class="panel-title">ANÁLISIS DETALLADO POR EQUIPO / MODELO</div>
                <table class="custom-table" id="modelsTable">
                    <thead>
                        <tr>
                            <th>MODELO</th>
                            <th style="width: 35%;">ACCURACY</th>
                            <th style="width: 35%;">F1-SCORE</th>
                            <th style="width: 15%; text-align: center;">RECALL</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Injected via JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const metricas = {json.dumps(metricas)};
        const importancias = {json.dumps(importancias)};

        document.getElementById('xgb-auc').innerText = (metricas["XGBoost"]["AUC_ROC"] * 100).toFixed(1) + "%";
        document.getElementById('rf-auc').innerText = (metricas["Random Forest"]["AUC_ROC"] * 100).toFixed(1) + "%";
        document.getElementById('mlp-auc').innerText = (metricas["Red Neuronal (MLP)"]["AUC_ROC"] * 100).toFixed(1) + "%";

        Chart.defaults.color = '#64748b';
        Chart.defaults.font.family = 'Montserrat';
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.responsive = true;

        const metricsLabels = ['Accuracy', 'Precision', 'Recall', 'F1', 'AUC'];

        function createSparkline(ctxId, color) {{
            new Chart(document.getElementById(ctxId).getContext('2d'), {{
                type: 'line',
                data: {{ labels: ['1','2','3','4','5'], datasets: [{{ data: [60, 65, 80, 75, 90], borderColor: color, borderWidth: 2, tension: 0.4, pointRadius: 0 }}] }},
                options: {{ 
                    plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }},
                    scales: {{ x: {{ display: false }}, y: {{ display: false }} }},
                    layout: {{ padding: 0 }} 
                }}
            }});
        }}
        createSparkline('sparkBlue', '#0ea5e9');
        createSparkline('sparkGreen', '#22c55e');
        createSparkline('sparkPink', '#f43f5e');

        function createTopBar(ctxId, color, dataVals) {{
            new Chart(document.getElementById(ctxId).getContext('2d'), {{
                type: 'bar',
                data: {{ labels: metricsLabels, datasets: [{{ data: dataVals, backgroundColor: color, borderRadius: 4 }}] }},
                options: {{ 
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{ 
                        y: {{ beginAtZero: true, max: 100, ticks: {{ stepSize: 25, callback: v => v+'%' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }}, 
                        x: {{ grid: {{ display: false }} }} 
                    }} 
                }}
            }});
        }}
        
        const mXgb = metricas["XGBoost"];
        const mRf = metricas["Random Forest"];
        const mMlp = metricas["Red Neuronal (MLP)"];
        
        createTopBar('barBlue', '#0ea5e9', [mXgb.Accuracy*100, mXgb.Precision*100, mXgb.Recall*100, mXgb.F1_Score*100, mXgb.AUC_ROC*100]);
        createTopBar('barGreen', '#22c55e', [mRf.Accuracy*100, mRf.Precision*100, mRf.Recall*100, mRf.F1_Score*100, mRf.AUC_ROC*100]);
        createTopBar('barPink', '#f43f5e', [mMlp.Accuracy*100, mMlp.Precision*100, mMlp.Recall*100, mMlp.F1_Score*100, mMlp.AUC_ROC*100]);

        new Chart(document.getElementById('donutChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Aceptable', 'Mala Calidad'],
                datasets: [{{ data: [{total_buenos}, {total_malos}], backgroundColor: ['#0ea5e9', 'rgba(14, 165, 233, 0.1)'], borderWidth: 0, hoverOffset: 4 }}]
            }},
            options: {{ cutout: '80%', plugins: {{ legend: {{ display: false }} }} }}
        }});

        const xgbImp = importancias["XGBoost"];
        const sortedImp = Object.keys(xgbImp).map(k => ({{k: k, v: xgbImp[k]}})).sort((a,b) => b.v - a.v).slice(0, 5);
        
        new Chart(document.getElementById('horizBar').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: sortedImp.map(i => i.k),
                datasets: [{{ data: sortedImp.map(i => i.v), backgroundColor: '#22c55e', borderRadius: 4 }}]
            }},
            options: {{ 
                indexAxis: 'y', 
                plugins: {{ legend: {{ display: false }} }},
                scales: {{ 
                    x: {{ display: false }}, 
                    y: {{ grid: {{ display: false }} }} 
                }} 
            }}
        }});

        const tbody = document.querySelector('#modelsTable tbody');
        for(const [name, mets] of Object.entries(metricas)) {{
            const acc = (mets.Accuracy*100).toFixed(1);
            const f1 = (mets.F1_Score*100).toFixed(1);
            const rec = (mets.Recall*100).toFixed(0);
            
            tbody.innerHTML += `
                <tr>
                    <td style="color:#fff; font-weight: 300;">${{name.replace(' (MLP)','')}}</td>
                    <td>
                        <div class="data-bar-cell">
                            <div class="data-bar-bg"><div class="data-bar-fill blue" style="width: ${{acc}}%;">${{acc}}%</div></div>
                        </div>
                    </td>
                    <td>
                        <div class="data-bar-cell">
                            <div class="data-bar-bg"><div class="data-bar-fill green" style="width: ${{f1}}%;">${{f1}}%</div></div>
                        </div>
                    </td>
                    <td><div class="pct-cell">${{rec}}%</div></td>
                </tr>
            `;
        }}
    </script>
</body>
</html>"""

    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("¡Dashboard de demostración corregido y generado exitosamente!")

if __name__ == "__main__":
    generar_dashboard()

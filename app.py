import dash
from dash import dcc, html, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import os

# 初始化 Dash 应用
app = dash.Dash(__name__, 
                title="Tesla Optimus & Financial Forecast Analysis",
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "Tesla Business Intelligence Dashboard"

# 基于提供的 Excel 数据创建数据集
def create_tesla_dataset():
    """创建 Tesla 财务预测数据集"""
    
    # 1. 各地区收入数据 (Sheet A)
    regional_data = pd.DataFrame({
        'Region': ['美国', '中国', '欧洲', '亚太', '中东', '其他'],
        '2022': [405.53, 181.45, 80, 40, 15, 92.64],
        '2023': [452.8, 251.01, 100.41, 55.78, 20.08, 87.82],
        '2024': [438, 250.24, 104.26, 62.56, 20.85, 101.15]
    })
    
    # 2. 各地区收入预测 2025-2030 (Sheet E)
    forecast_data = pd.DataFrame({
        'Region': ['美国', '中国', '欧洲', '亚太', '中东', '其他'],
        '2025': [455.52, 267.76, 116.77, 75.07, 23.98, 107.62],
        '2026': [473.74, 286.5, 130.78, 90.08, 27.58, 114.51],
        '2027': [492.69, 306.56, 146.47, 108.1, 31.72, 121.84],
        '2028': [512.4, 328.02, 164.05, 129.72, 36.48, 129.64],
        '2029': [532.9, 350.98, 183.74, 155.66, 41.95, 137.94],
        '2030': [554.22, 375.55, 205.79, 186.79, 48.24, 146.77]
    })
    
    # 3. 传统业务预测 (Sheet F)
    traditional_business = pd.DataFrame({
        'Year': ['2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E', '2029E', '2030E'],
        '汽车业务': [714.62, 824.19, 770.7, 800.02, 861.03, 941.62, 1029.43, 1124.95, 1228.7],
        '能源业务': [39.09, 60.35, 100.86, 144.23, 201.92, 282.69, 395.77, 554.08, 775.71],
        '服务业务': [60.91, 83.19, 105.34, 133, 167.58, 211.15, 266.05, 335.22, 422.38]
    })
    
    # 4. 新增业务预测 (Sheet G)
    new_business = pd.DataFrame({
        'Year': ['2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E', '2029E', '2030E'],
        'Optimus': [0, 0, 0, 0, 3, 20, 90, 200, 300],
        'Robotaxi': [0, 0, 0, 0, 0, 5, 80, 130, 200]
    })
    
    # 5. 最终合并预测 (Sheet H)
    total_forecast = pd.DataFrame({
        'Year': ['2022', '2023', '2024', '2025E', '2026E', '2027E', '2028E', '2029E', '2030E'],
        '传统业务': [814.62, 967.73, 976.9, 1077.25, 1230.53, 1435.46, 1691.25, 2014.25, 2426.79],
        '新增业务': [0, 0, 0, 0, 3, 25, 170, 330, 500],
        '总收入': [814.62, 967.73, 976.9, 1077.25, 1233.53, 1460.46, 1861.25, 2344.25, 2926.79],
        'YoY增长': ['-', '18.8%', '0.9%', '10.3%', '14.5%', '18.4%', '27.4%', '26.0%', '24.8%']
    })
    
    # 6. 2030业务结构 (Sheet I)
    business_structure_2030 = pd.DataFrame({
        '业务类型': ['汽车业务', '能源业务', '服务业务', 'Optimus', 'Robotaxi'],
        '收入_亿美元': [1228.7, 775.71, 422.38, 300, 200],
        '占比': [42.0, 26.5, 14.4, 10.3, 6.8]
    })
    
    return {
        'regional_data': regional_data,
        'forecast_data': forecast_data,
        'traditional_business': traditional_business,
        'new_business': new_business,
        'total_forecast': total_forecast,
        'business_structure_2030': business_structure_2030
    }

# 创建数据
data = create_tesla_dataset()

# 准备用于可视化的数据
def prepare_visualization_data():
    """准备图表数据"""
    
    # 1. 各地区收入历史+预测（长格式）
    regional_history = data['regional_data'].melt(id_vars=['Region'], 
                                                 value_vars=['2022', '2023', '2024'],
                                                 var_name='Year', 
                                                 value_name='Revenue')
    
    regional_forecast = data['forecast_data'].melt(id_vars=['Region'], 
                                                  value_vars=['2025', '2026', '2027', '2028', '2029', '2030'],
                                                  var_name='Year', 
                                                  value_name='Revenue')
    
    regional_complete = pd.concat([regional_history, regional_forecast])
    regional_complete['Year'] = pd.to_numeric(regional_complete['Year'])
    
    # 2. 业务组合数据
    business_mix = data['total_forecast'].copy()
    
    # 3. 新增业务增长趋势
    new_business_growth = data['new_business'].copy()
    
    return {
        'regional_complete': regional_complete,
        'business_mix': business_mix,
        'new_business_growth': new_business_growth
    }

viz_data = prepare_visualization_data()

# 应用布局
app.layout = html.Div([
    # 标题和导航
    html.Div([
        html.H1("🚀 Tesla 业务预测与 Optimus 分析仪表板", 
                style={'color': '#E82127', 'marginBottom': '10px'}),
        html.P("基于 Tesla 2022-2030 财务预测模型的数据分析与可视化", 
               style={'color': '#666', 'fontSize': '16px'})
    ], style={'textAlign': 'center', 'padding': '30px', 'background': '#f8f9fa', 
              'borderBottom': '2px solid #E82127'}),
    
    # 关键指标卡片
    html.Div([
        html.Div([
            html.H3("$2,926.79B", style={'color': '#E82127', 'margin': '0', 'fontSize': '28px'}),
            html.P("2030年预测总收入", style={'color': '#666', 'margin': '0'})
        ], style={'flex': 1, 'padding': '25px', 'background': 'white', 'margin': '10px', 
                  'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3("20.0%", style={'color': 'green', 'margin': '0', 'fontSize': '28px'}),
            html.P("2024-2030年复合增长率", style={'color': '#666', 'margin': '0'})
        ], style={'flex': 1, 'padding': '25px', 'background': 'white', 'margin': '10px', 
                  'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3("$500B", style={'color': '#1E3A8A', 'margin': '0', 'fontSize': '28px'}),
            html.P("2030年新增业务收入", style={'color': '#666', 'margin': '0'})
        ], style={'flex': 1, 'padding': '25px', 'background': 'white', 'margin': '10px', 
                  'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.H3("17.1%", style={'color': '#FF6B00', 'margin': '0', 'fontSize': '28px'}),
            html.P("新增业务收入占比 (2030)", style={'color': '#666', 'margin': '0'})
        ], style={'flex': 1, 'padding': '25px', 'background': 'white', 'margin': '10px', 
                  'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'})
    ], style={'display': 'flex', 'margin': '30px 20px', 'gap': '15px'}),
    
    # 第一行：收入趋势和地区分布
    html.Div([
        # 总收入趋势图
        html.Div([
            html.H3("📈 Tesla 总收入预测趋势 (2022-2030)", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dcc.Graph(
                id='total-revenue-trend',
                figure=px.line(viz_data['business_mix'], x='Year', y='总收入',
                              title='',
                              markers=True,
                              labels={'总收入': 'Revenue (亿美元)', 'Year': 'Year'})
                .update_layout(
                    plot_bgcolor='white',
                    height=400,
                    title_font_size=16,
                    yaxis_title="Revenue (亿美元)",
                    xaxis_title="Year"
                )
                .update_traces(line=dict(color='#E82127', width=3))
            )
        ], style={'flex': 2, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
        
        # 地区收入分布
        html.Div([
            html.H3("🌍 各地区收入分布 (2024)", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dcc.Graph(
                id='regional-distribution',
                figure=px.pie(data['regional_data'], values='2024', names='Region',
                             title='',
                             hole=0.4,
                             color_discrete_sequence=px.colors.sequential.RdBu)
                .update_layout(
                    plot_bgcolor='white',
                    height=400,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                .update_traces(textposition='inside', textinfo='percent+label')
            )
        ], style={'flex': 1, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'})
    ], style={'display': 'flex', 'margin': '20px', 'gap': '20px'}),
    
    # 第二行：业务构成和 Optimus 增长
    html.Div([
        # 业务构成堆叠面积图
        html.Div([
            html.H3("🏢 业务构成演变 (2022-2030)", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dcc.Graph(
                id='business-mix-evolution',
                figure=go.Figure(
                    data=[
                        go.Scatter(
                            name='传统业务',
                            x=data['total_forecast']['Year'],
                            y=data['total_forecast']['传统业务'],
                            mode='lines',
                            line=dict(width=0.5, color='rgb(184, 247, 212)'),
                            stackgroup='one',
                            fillcolor='rgba(184, 247, 212, 0.6)'
                        ),
                        go.Scatter(
                            name='新增业务',
                            x=data['total_forecast']['Year'],
                            y=data['total_forecast']['新增业务'],
                            mode='lines',
                            line=dict(width=0.5, color='rgb(111, 231, 219)'),
                            stackgroup='one',
                            fillcolor='rgba(111, 231, 219, 0.6)'
                        )
                    ]
                )
                .update_layout(
                    title='',
                    plot_bgcolor='white',
                    height=400,
                    xaxis_title="Year",
                    yaxis_title="Revenue (亿美元)",
                    showlegend=True,
                    hovermode='x unified'
                )
            )
        ], style={'flex': 2, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
        
        # Optimus 和 Robotaxi 增长
        html.Div([
            html.H3("🤖 Optimus & Robotaxi 业务增长", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dcc.Graph(
                id='new-business-growth',
                figure=px.bar(data['new_business'].melt(id_vars=['Year'], 
                                                       value_vars=['Optimus', 'Robotaxi'],
                                                       var_name='Business', 
                                                       value_name='Revenue'),
                             x='Year', y='Revenue', color='Business',
                             barmode='group',
                             title='',
                             color_discrete_map={'Optimus': '#1E3A8A', 'Robotaxi': '#FF6B00'})
                .update_layout(
                    plot_bgcolor='white',
                    height=400,
                    xaxis_title="Year",
                    yaxis_title="Revenue (亿美元)"
                )
            )
        ], style={'flex': 1, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'})
    ], style={'display': 'flex', 'margin': '20px', 'gap': '20px'}),
    
    # 第三行：数据表格和详细分析
    html.Div([
        # 详细数据表格
        html.Div([
            html.H3("📊 详细财务数据表", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dash_table.DataTable(
                id='detailed-table',
                columns=[{"name": i, "id": i} for i in data['total_forecast'].columns],
                data=data['total_forecast'].to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': '#f8f9fa',
                    'fontWeight': 'bold',
                    'border': '1px solid #dee2e6'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            )
        ], style={'flex': 1, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
        
        # 2030年业务结构
        html.Div([
            html.H3("🎯 2030年业务结构分析", 
                    style={'color': '#333', 'marginBottom': '20px'}),
            dcc.Graph(
                id='business-structure-2030',
                figure=px.bar(data['business_structure_2030'], 
                             x='业务类型', y='收入_亿美元',
                             text='占比',
                             title='',
                             color='业务类型',
                             color_discrete_sequence=px.colors.qualitative.Set3)
                .update_layout(
                    plot_bgcolor='white',
                    height=400,
                    xaxis_title="Business Type",
                    yaxis_title="Revenue (亿美元)",
                    showlegend=False
                )
                .update_traces(texttemplate='%{text}%', textposition='outside')
            )
        ], style={'flex': 1, 'padding': '20px', 'background': 'white', 
                  'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'})
    ], style={'display': 'flex', 'margin': '20px', 'gap': '20px'}),
    
    # 交互控制面板
    html.Div([
        html.H3("⚙️ 分析控制面板", 
                style={'color': '#333', 'marginBottom': '20px'}),
        html.Div([
            html.Label("选择分析维度:", style={'marginRight': '10px'}),
            dcc.RadioItems(
                id='analysis-dimension',
                options=[
                    {'label': '地区分析', 'value': 'regional'},
                    {'label': '业务分析', 'value': 'business'},
                    {'label': '时间趋势', 'value': 'trend'}
                ],
                value='business',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
        ], style={'marginBottom': '20px'}),
        
        html.Div([
            html.Label("选择年份范围:", style={'marginRight': '10px'}),
            dcc.RangeSlider(
                id='year-range-slider',
                min=2022,
                max=2030,
                step=1,
                marks={i: str(i) for i in range(2022, 2031)},
                value=[2022, 2030]
            )
        ])
    ], style={'padding': '30px', 'background': 'white', 'margin': '20px', 
              'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
    
    # 页脚
    html.Div([
        html.P("📊 Tesla 业务预测分析仪表板 | 数据来源: Tesla Financial Forecast Model.xlsx", 
               style={'color': '#666', 'textAlign': 'center', 'margin': '0'}),
        html.P("最后更新: 2024年1月 | 分析周期: 2022-2030", 
               style={'color': '#999', 'textAlign': 'center', 'margin': '10px 0 0 0'})
    ], style={'padding': '20px', 'background': '#f8f9fa', 'marginTop': '30px', 
              'borderTop': '1px solid #dee2e6'})
], style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh'})

# 回调函数
@app.callback(
    Output('regional-distribution', 'figure'),
    [Input('year-range-slider', 'value')]
)
def update_regional_distribution(year_range):
    selected_year = str(year_range[1])  # 使用结束年份
    if selected_year in ['2022', '2023', '2024']:
        values_col = selected_year
    else:
        # 对于预测年份，需要从 forecast_data 获取
        year_map = {'2025': '2025', '2026': '2026', '2027': '2027', 
                   '2028': '2028', '2029': '2029', '2030': '2030'}
        if selected_year in year_map:
            values_col = year_map[selected_year]
        else:
            values_col = '2024'
    
    fig = px.pie(data['regional_data'], values=values_col, names='Region',
                title=f'各地区收入分布 ({selected_year})',
                hole=0.4)
    fig.update_layout(plot_bgcolor='white')
    return fig

# 运行应用
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    print(f"🚀 Tesla Business Intelligence Dashboard starting on port {port}")
    print(f"📊 Access the dashboard at: http://localhost:{port}")
    app.run_server(host='0.0.0.0', port=port, debug=False)

# 导出 server
server = app.server

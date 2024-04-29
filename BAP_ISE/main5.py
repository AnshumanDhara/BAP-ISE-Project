import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Load each CSV file into a separate DataFrame
df_spcc_theory_a = pd.read_csv(r"Dataset/A_THEORY_SPCC.csv")
df_spcc_theory_b = pd.read_csv(r"Dataset/B_THEORY_SPCC.csv")
df_spcc_lab_a_group1 = pd.read_csv(r"Dataset/A_LAB_SPCC_1.csv")
df_spcc_lab_a_group2 = pd.read_csv(r"Dataset/A_LAB_SPCC_2.csv")
df_spcc_lab_a_group3 = pd.read_csv(r"Dataset/A_LAB_SPCC_3.csv")
df_spcc_lab_a_group4 = pd.read_csv(r"Dataset/A_LAB_SPCC_4.csv")
df_spcc_lab_b_group1 = pd.read_csv(r"Dataset/B_LAB_SPCC_1.csv")
df_spcc_lab_b_group2 = pd.read_csv(r"Dataset/B_LAB_SPCC_2.csv")
df_spcc_lab_b_group3 = pd.read_csv(r"Dataset/B_LAB_SPCC_3.csv")
df_spcc_lab_b_group4 = pd.read_csv(r"Dataset/B_LAB_SPCC_4.csv")

df_fosip_theory_a = pd.read_csv(r"Dataset/A_THEORY_FOSIP.csv")
df_fosip_theory_b = pd.read_csv(r"Dataset/B_THEORY_FOSIP.csv")
df_fosip_lab_a_group1 = pd.read_csv(r"Dataset/A_LAB_FOSIP_1.csv")
df_fosip_lab_a_group2 = pd.read_csv(r"Dataset/A_LAB_FOSIP_2.csv")
df_fosip_lab_a_group3 = pd.read_csv(r"Dataset/A_LAB_FOSIP_3.csv")
df_fosip_lab_a_group4 = pd.read_csv(r"Dataset/A_LAB_FOSIP_4.csv")
df_fosip_lab_b_group1 = pd.read_csv(r"Dataset/B_LAB_FOSIP_1.csv")
df_fosip_lab_b_group2 = pd.read_csv(r"Dataset/B_LAB_FOSIP_2.csv")
df_fosip_lab_b_group3 = pd.read_csv(r"Dataset/B_LAB_FOSIP_3.csv")
df_fosip_lab_b_group4 = pd.read_csv(r"Dataset/B_LAB_FOSIP_4.csv")

# Define Dash app
app = dash.Dash(__name__)

# Define Dash layout
app.layout = html.Div([
    html.H1("Attendance Analysis Dashboard", style={'textAlign': 'center', 'color': '#333333'}),
    html.Div([
        html.Label("Select Class:", style={'color': '#333333'}),
        dcc.Dropdown(
            id='class-dropdown',
            options=[
                {'label': 'A', 'value': 'A'},
                {'label': 'B', 'value': 'B'}
            ],
            value='A'
        ),
        html.Label("Select Subject:", style={'color': '#333333'}),
        dcc.Dropdown(
            id='subject-dropdown',
            options=[
                {'label': 'SPCC', 'value': 'SPCC'},
                {'label': 'FOSIP', 'value': 'FOSIP'}
            ],
            value='SPCC'
        ),
        html.Label("Select Type:", style={'color': '#333333'}),
        dcc.Dropdown(
            id='type-dropdown',
            options=[
                {'label': 'Theory', 'value': 'Theory'},
                {'label': 'Lab', 'value': 'Lab'}
            ],
            value='Theory'
        ),
        html.Div(
            id='division-dropdown-container',
            children=[
                html.Label("Select Batch", style={'color': '#333333'}),
                dcc.Dropdown(
                    id='division-dropdown',
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '2', 'value': '2'},
                        {'label': '3', 'value': '3'},
                        {'label': '4', 'value': '4'}
                    ],
                    value='1'
                )
            ],
            style={'display': 'none'}  # Initially hide the division dropdown
        )
    ], style={'background-color': 'rgba(240, 240, 240, 0.8)', 'padding': '20px', 'border-radius': '10px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='average-attendance-chart')
        ], style={'width': '100%', 'display': 'inline-block'}),
    ])
], style={'background-image': 'linear-gradient(to bottom, #f2f2f2, #dddddd)', 'padding': '20px'})

# Define callback function to update output based on dropdown selections
import numpy as np

# Define callback function to update output based on dropdown selections
@app.callback(
    Output('average-attendance-chart', 'figure'),
    [Input('class-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('type-dropdown', 'value'),
     Input('division-dropdown', 'value')]
)
def update_average_attendance(class_selected, subject_selected, type_selected, division_selected):
    # Get the selected DataFrame based on dropdown selections
    if subject_selected == 'SPCC':
        if type_selected == 'Lab':
            df = globals()[f'df_{subject_selected.lower()}_{type_selected.lower()}_{class_selected.lower()}_group{division_selected}']
        else:
            df = globals()[f'df_{subject_selected.lower()}_{type_selected.lower()}_{class_selected.lower()}']
    else:
        if type_selected == 'Lab':
            df = globals()[f'df_{subject_selected.lower()}_{type_selected.lower()}_{class_selected.lower()}_group{division_selected}']
        else:
            df = globals()[f'df_{subject_selected.lower()}_{type_selected.lower()}_{class_selected.lower()}']
            
    # Extract month from column names and group attendance data by month
    df_monthly = df.groupby(df.columns.str.split().str[0], axis=1).mean()

    # Create the line chart for average attendance per month for each subject
    line_fig = px.line(df_monthly, x=df_monthly.columns, y=df_monthly.mean(),
                       labels={'x': 'Month', 'y': 'Average Attendance'},
                       title='Average Attendance per Month for Each Subject')

    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)

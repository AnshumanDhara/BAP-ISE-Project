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
            dcc.Graph(id='attendance-chart')
        ], style={'width': '100%', 'display': 'inline-block'}),
    ])
], style={'background-image': 'linear-gradient(to bottom, #f2f2f2, #dddddd)', 'padding': '20px'})
# Define callback function to update output based on dropdown selections
# Define callback function to update output based on dropdown selections
@app.callback(
    [Output('division-dropdown-container', 'style'),
     Output('attendance-chart', 'figure')],
    [Input('class-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('type-dropdown', 'value'),
     Input('division-dropdown', 'value')]
)
def update_output(class_selected, subject_selected, type_selected, division_selected):
    # Update visibility of the division dropdown
    division_dropdown_style = {'display': 'block'} if type_selected == 'Lab' else {'display': 'none'}

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

    # Calculate total days present for each student
    df['Total Days Present'] = df.drop(columns=['UID No.', 'Student Name']).apply(lambda row: row.astype(str).str.contains('1').sum(), axis=1)

    # Filter out students with total attendance of 0
    df = df[df['Total Days Present'] > 0]

    # Calculate total classes for each student
    df['Total Classes'] = df.shape[1] - 2  # Subtracting 2 for 'UID No.' and 'Student Name' columns

    # Calculate attendance percentage for each student
    df['Attendance Percentage'] = ((df['Total Days Present'] / df['Total Classes']) * 100).round(2)

    # Calculate overall attendance percentage
    overall_attendance_percentage = df['Total Days Present'].sum() / df['Total Classes'].sum() * 100

    # Create the bar chart for overall attendance percentage
    overall_attendance_fig = px.bar(
        x=['Overall Attendance Percentage'],
        y=[overall_attendance_percentage],
        labels={'x': 'Overall Attendance Percentage', 'y': 'Percentage'},
        title='Overall Attendance Percentage'
    )

    # Create the bar chart for total days present vs. total classes
    bar_fig = px.bar(df, x='Student Name', y=['Total Days Present', 'Total Classes'],
                     title='Total Days Present vs. Total Classes', barmode='group')

    return division_dropdown_style, bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)

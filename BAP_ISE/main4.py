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
        ], style={'width': '50%', 'display': 'inline-block'})
    ])
], style={'background-image': 'linear-gradient(to bottom, #f2f2f2, #dddddd)', 'padding': '20px'})

# Define callback function to update output based on dropdown selections
@app.callback(
    Output('division-dropdown-container', 'style'),
    [Input('type-dropdown', 'value')]
)
def update_division_dropdown_visibility(type_selected):
    if type_selected == 'Lab':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('attendance-chart', 'figure'),
    [Input('class-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('type-dropdown', 'value'),
     Input('division-dropdown', 'value')]
)
def update_output(class_selected, subject_selected, type_selected, division_selected):
    if subject_selected == 'SPCC':
        if type_selected == 'Lab':
            df_selected = globals()[f'df_spcc_lab_{class_selected.lower()}_group{division_selected}']
        else:
            df_selected = globals()[f'df_spcc_theory_{class_selected.lower()}']
    else:
        if type_selected == 'Lab':
            df_selected = globals()[f'df_fosip_lab_{class_selected.lower()}_group{division_selected}']
        else:
            df_selected = globals()[f'df_fosip_theory_{class_selected.lower()}']

    # Drop unnecessary columns
    df_cleaned = df_selected.drop(columns=['UID No.', 'Student Name'])

    # Replace non-integer values with NaN in the attendance columns
    df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

    # Calculate total students
    total_students = len(df_cleaned)

    # Calculate total students present on each date
    total_students_present = df_cleaned.sum()

    # Calculate percentage of students present on each date
    percentage_present = (total_students_present / total_students) * 100

    # Create the bar chart for attendance percentage
    bar_fig = px.bar(x=percentage_present.index, y=percentage_present.values,
                     labels={'x': 'Date', 'y': 'Attendance Percentage'},
                     title='Attendance Percentage for Each Date')

    # Update y-axis range to ensure it shows absolute values
    bar_fig.update_layout(yaxis={'range': [0, 100]})

    return bar_fig

if __name__ == '__main__':
    app.run_server(debug=True)

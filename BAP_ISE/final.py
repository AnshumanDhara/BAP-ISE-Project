import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import numpy as np
import base64
from PIL import Image
from io import BytesIO

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
        ),
        html.Label("Filter Students:", style={'color': '#333333'}),
        dcc.Checklist(
            id='filter-checkbox',
            options=[
                {'label': 'Display only defaulters', 'value': 'filter'}
            ],
            value=[]
        )
    ], style={'background-color': 'rgba(240, 240, 240, 0.8)', 'padding': '20px', 'border-radius': '10px'}),
    html.Div(id='output-container', style={'margin-top': '20px'}),
    html.Div(id='defaulter-count', style={'margin-top': '20px', 'text-align': 'center'}),
    dcc.Graph(id='pie-chart'),
    html.Div([
        html.Div([
            dcc.Graph(id='attendance-chart1')
        ], style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '20px', 'margin-top': '30px'}),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='attendance-chart2')
        ], style={'width': '100%', 'height':'400px', 'display': 'inline-block', 'margin-bottom': '20px'}),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='attendance-chart3')
        ], style={'width': '75%', 'display': 'inline-block', 'margin-left': '12.5%', 'margin-top': '50px'})
    ])
], style={'background-image': 'linear-gradient(to bottom, #f2f2f2, #dddddd)', 'padding': '20px'})
    
# Define callback function to update output based on dropdown selections
# Define callback function to update output based on dropdown selections
@app.callback(
    [Output('output-container', 'children'),
     Output('defaulter-count', 'children'),
     Output('pie-chart', 'figure'),  # Update id to 'pie-chart'
     Output('attendance-chart1', 'figure'),
     Output('attendance-chart2', 'figure'),
     Output('attendance-chart3', 'figure')],
    [Input('class-dropdown', 'value'),
     Input('subject-dropdown', 'value'),
     Input('type-dropdown', 'value'),
     Input('division-dropdown', 'value'),
     Input('filter-checkbox', 'value')],
)
def update_output(class_selected, subject_selected, type_selected, division_selected, filter_value):
    
    # VISUALIZATION 1
    
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

    # Exclude the columns with "Intern"
    df = df.drop(columns=[col for col in df.columns if 'Intern' in col])

    # Calculate total days present for each student
    df['Total Days Present'] = df.drop(columns=['UID No.', 'Student Name']).apply(lambda row: row.astype(str).str.contains('1').sum(), axis=1)

    # Calculate total classes for each student
    df['Total Classes'] = df.shape[1] - 2  # Subtracting 2 for 'UID No.' and 'Student Name' columns

    # Calculate attendance percentage for each student
    df['Attendance Percentage'] = ((df['Total Days Present'] / df['Total Classes']) * 100).round(2)

    # Filter students with attendance less than 75%
    if 'filter' in filter_value:
        filtered_df = df[(df['Attendance Percentage'] < 75) & (df['Attendance Percentage'] != 0)]
    else:
        filtered_df = df[df['Attendance Percentage'] != 0]

    if filtered_df.empty:
        return "No students found.", "", {}  # Return empty figure for the pie chart

    # Select columns for display
    display_columns = ['UID No.', 'Student Name', 'Total Classes', 'Total Days Present', 'Attendance Percentage']
    filtered_df = filtered_df[display_columns]

    defaulter_text = "   "
    defaulter_count = 0  # Default value for defaulter_count
    defaulter_percentage = 0  # Default value for defaulter_percentage
    if 'filter' in filter_value:
        defaulter_count = len(filtered_df)
        defaulter_text = f"Total defaulters: {defaulter_count}"

        # Calculate the percentage of defaulters
        total_students = len(df)
        defaulter_percentage = round((defaulter_count / total_students) * 100, 2)

    # Create the pie chart figure
    pie_fig = {
        'data': [{
            'values': [defaulter_percentage, 100 - defaulter_percentage],
            'labels': ['Defaulters', 'Non-Defaulters'],
            'type': 'pie',
            'hole': 0.4,
            'hoverinfo': 'label+percent',
            'textinfo': 'value'
        }],
        'layout': {
            'title': 'Defaulter Percentage'
        }
    }
    
    # VISUALIZATION 2
    
    # Replace non-integer values with NaN in the attendance columns
    df_cleaned = df.drop(columns=['UID No.', 'Student Name', 'Total Classes', 'Total Days Present', 'Attendance Percentage']).apply(pd.to_numeric, errors='coerce')

    # Calculate total students present on each date
    total_students_present = df_cleaned.sum()

    # Create the line chart for total students present on each date
    line_fig = px.line(x=df_cleaned.columns, y=total_students_present,
                       labels={'x': 'Date', 'y': 'Total Students Present'},
                       title='Total Students Present on Each Date')

    # VISUALIZATION 3
    
    # Calculate total days present for each student
    df['Total Days Present'] = df.drop(columns=['UID No.', 'Student Name', 'Total Classes', 'Total Days Present', 'Attendance Percentage']).apply(lambda row: row.astype(str).str.contains('1').sum(), axis=1)

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
    bar_fig1 = px.bar(df, x='Student Name', y=['Total Days Present', 'Total Classes'],
                     title='Total Days Present vs. Total Classes', barmode='group')

    # VISUALIZATION 4
    
    # Drop unnecessary columns
    df_cleaned = df.drop(columns=['UID No.', 'Student Name', 'Total Classes', 'Total Days Present', 'Attendance Percentage'])

    # Replace non-integer values with NaN in the attendance columns
    df_cleaned = df_cleaned.apply(pd.to_numeric, errors='coerce')

    # Calculate total students
    total_students = len(df_cleaned)

    # Calculate total students present on each date
    total_students_present = df_cleaned.sum()

    # Calculate percentage of students present on each date
    percentage_present = (total_students_present / total_students) * 100

    # Create the bar chart for attendance percentage
    bar_fig2 = px.bar(x=percentage_present.index, y=percentage_present.values,
                     labels={'x': 'Date', 'y': 'Attendance Percentage'},
                     title='Attendance Percentage for Each Date')

    # Update y-axis range to ensure it shows absolute values
    bar_fig2.update_layout(yaxis={'range': [0, 100]})

    # RETURN ALL FIGURES
    
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={'background-color': '#f2f2f2', 'padding': '10px', 'text-align': 'center'}) for col in filtered_df.columns])] +

        # Body
        [html.Tr([
            html.Td(filtered_df.iloc[i][col], style={'padding': '10px', 'text-align': 'center'})
            for col in filtered_df.columns
        ]) for i in range(len(filtered_df))],

        style={'width': '100%', 'border-collapse': 'collapse', 'border': '1px solid #ddd', 'margin-top': '10px'}
    ), defaulter_text, pie_fig, line_fig, bar_fig1, bar_fig2

# Update the visibility of the division dropdown based on the type dropdown selection
@app.callback(
    Output('division-dropdown-container', 'style'),
    [Input('type-dropdown', 'value')],
)
def update_division_dropdown_visibility(type_selected):
    if type_selected == 'Lab':
        return {'display': 'block'}
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('pie-chart', 'style'),
    [Input('filter-checkbox', 'value')]
)
def update_pie_chart_visibility(filter_value):
    if 'filter' in filter_value:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
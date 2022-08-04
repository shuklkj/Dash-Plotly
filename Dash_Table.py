import pandas as pd
from dash import Dash, dash_table, dcc, html, dash
from dash.dependencies import Input, Output, State
import plotly.express as px

df = pd.read_csv('covid.csv')
df.sort_values('submission_date', inplace=True)

print(df['submission_date'])

df.columns = ['submission_date', 'state', 'tot_cases', 'conf_cases', 'prob_cases', 'new_case', 'pnew_case', 'tot_death',
              'conf_death', 'prob_death', 'new_death', 'pnew_death', 'created_at', 'consent_cases', 'consent_deaths']

app = dash.Dash(__name__, prevent_initial_callbacks=True)  # this was introduced in Dash version 1.12.0

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            if i == "iso_alpha3" or i == "year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=True,  # allow editing of data inside all cells
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        row_deletable=True,  # choose if user can delete a row (True) or not (False)
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=10,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        export_format="csv"
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div(id='choromap-container')
])


# -------------------------------------------------------------------------------------
# Create a chart
@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
def create_chart(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
                 order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    dff = pd.DataFrame(all_rows_data)
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    if "submission_date" in dff and "tot_cases" in dff:
        return [
            dcc.Graph(id='line-chart',
                      figure=px.line(
                          data_frame=dff,
                          x="submission_date",
                          y='tot_cases',
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors)
                      )
        ]

    if "submission_date" in dff and "new_case" in dff:
        return [
            dcc.Graph(id='line-chart',
                      figure=px.line(
                          data_frame=dff,
                          x="submission_date",
                          y='new_case',
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors)
                      )
        ]


if __name__ == "__main__":
    app.run_server(debug=True)

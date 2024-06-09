import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import datetime
import time

# Create the Dash app without specifying any external stylesheets
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ], suppress_callback_exceptions=True)

# Load the data from the CSV files
fiscal_file_path = "/Users/hannahjumilla/Desktop/Dashboard/ng_fiscal_modified.csv"
debt_file_path = "/Users/hannahjumilla/Desktop/Dashboard/NG_debt_modified2.csv"

df_fiscal = pd.read_csv(fiscal_file_path)
df_debt = pd.read_csv(debt_file_path)

# Define custom CSS for the dark blue header, dropdown menu, and animations
custom_css = """
.dark-blue-header {
    background-color: #00008B !important; /* Dark Blue Color */
}

/* Dropdown menu font color */
.Select-menu-outer {
    color: black !important;
}

/* Animation for Welcome text */
.welcome-text {
    font-size: 6em;
    color: white;
    text-align: center;
    margin-top: 1vh; /* Top margin 1vh */
    animation: fadeIn 2s ease-in-out;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Animation for background gradient */
@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.gradient-bg {
    background: linear-gradient(45deg, #ff1b6b, #45caff, #ff1b6b, #45caff, #ff1b6b); /* Aurora-like gradient */
    background-size: 400% 400%; /* Background size */
    animation: gradient 15s ease infinite; /* Animation */
    height: 100vh; /* Full height */
    display: flex; /* Flexbox */
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically */
    flex-direction: column; /* Align items vertically */
    padding-top: 60px; /* Ensure content starts below the navbar */
}

/* Animation for typewriter text */
@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: white }
}

.typewriter-text-container {
    background-color: rgba(0, 0, 0, 0.3); /* More transparent semi-transparent black background */
    padding: 20px; /* Padding around the text */
    border-radius: 0px; /* Sharp corners */
    max-width: 70%; /* Limit the width */
    margin: 0 auto; /* Center horizontally */
}

.typewriter-text {
    overflow: hidden; /* Hide overflow */
    white-space: nowrap; /* Don't wrap text */
    color: white;
    letter-spacing: .15em; /* Spacing between characters */
    animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    font-weight: bold; /* Make text bold */
    text-align: center; /* Center align text */
}

/* Navbar link hover effect */
.navbar-nav .nav-link {
    transition: background-color 0.3s, color 0.3s;
}

.navbar-nav .nav-link:hover {
    background-color: #0056b3; /* Change to a different shade of blue */
    color: #ffffff; /* Change text color on hover */
}

/* Navbar link click effect */
@keyframes clickEffect {
    0% { background-color: #0056b3; }
    50% { background-color: #00008B; }
    100% { background-color: #0056b3; }
}

.navbar-nav .nav-link:active {
    animation: clickEffect 0.3s;
}

/* Fade-in animation for the dashboard title */
.fade-in {
    animation: fadeInTitle 2s ease-in-out;
}

@keyframes fadeInTitle {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* Custom styles for date and time */
.date-time {
    font-size: 2em;
    color: white;
    text-align: center;
    margin-bottom: 1vh;
}

/* Styles for the information boxes */
.info-box {
    background-color: rgba(0, 0, 0, 0.3); /* Semi-transparent black background */
    padding: 20px; /* Padding around the text */
    border-radius: 5px; /* Rounded corners */
    color: white;
    font-size: 1.2em;
    text-align: center;
    margin: 10px;
    flex: 1; /* Make the boxes equal width */
    max-width: 45%; /* Limit the width */
    animation: fadeInBox 2s ease-in-out;
}

/* Animation for the fade-in effect */
@keyframes fadeInBox {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}
"""

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{custom_css}</style>
    </head>
    <body>
        {{%app_entry%}}
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </body>
</html>
"""

# Define the layout for the home page
home_layout = html.Div([
    # Navigation Bar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("2006-2023", href="/data")),
            dbc.NavItem(dbc.NavLink("2024", href="/2024")),
        ],
        brand="Financial Market Monitoring and Analysis Division",
        brand_href="#",
        className="dark-blue-header",  # Apply the custom dark blue class
        dark=True,
        fixed="top"  # Fix the navbar at the top
    ),
    html.Div(id="current-date-time", className="date-time"),  # Div to display date and time
    html.H1("Welcome!", className="welcome-text"),
    html.Div([
        html.P("This dashboard shows the Fiscal and Debt Indicators for the years 2006 to 2024.", className="typewriter-text"),
        html.P("Please click the buttons above to see the related charts.", className="typewriter-text")
    ], className="typewriter-text-container"),
    html.Div([
        html.Div([
            html.P("About the Fiscal Indicators"),
            html.P("The Fiscal Indicators show data about the revenue, expenses, amortization, among others.")
        ], className="info-box fade-in"),
        html.Div([
            html.P("About the Debt Indicators"),
            html.P("The Debt Indicators show data about the government's debt, gross domestic product, the USD/PHP exchange rate, etc.")
        ], className="info-box fade-in"),
    ], style={"display": "flex", "justify-content": "center", "max-width": "70%", "margin": "0 auto"}),
    dcc.Interval(
        id="interval-component",
        interval=1*1000,  # Update every second
        n_intervals=0
    )
], className="gradient-bg")

#Callback Time
@app.callback(
    Output("current-date-time", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_date_time(n):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Define the layout for the main page (2006-2023)
main_layout = html.Div([
    # Navigation Bar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("2006-2023", href="/data")),
            dbc.NavItem(dbc.NavLink("2024", href="/2024")),
        ],
        brand="Financial Market Monitoring and Analysis Division",
        brand_href="#",
        className="dark-blue-header",  # Apply the custom dark blue class
        dark=True,
    ),
    # Container for the content
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Fiscal and Debt Indicators Dashboard", className="text-center my-4 fade-in")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Select Fiscal Indicator", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='fiscal-indicator-dropdown',
                    options=[
                        {'label': indicator, 'value': indicator}
                        for indicator in df_fiscal['Fiscal Indicators'].unique()
                        if indicator not in ["BIR collections", "BOC collections", "BTr income",
                                             "Domestic financing 1", "External financing 1", 
                                             "Domestic financing  2", "External financing 2",
                                             "Domestic financing 3", "External financing 3",'Domestic amortization','External amortization','As share of revenues (percent)','As share of expenditures (percent)','As share of GDP (percent)']
                    ],
                    value='Revenues',
                    className="mb-4"
                )
            ], width=6),
            dbc.Col([
                html.Label("Select Debt Indicator", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='debt-indicator-dropdown',
                    options=[
                        {'label': indicator, 'value': indicator}
                        for indicator in df_debt['Debt Indicators'].unique()
                        if indicator not in ["Domestic debt", "External debt", "Domestic guarantees",
                                             "External guarantees", "On domestic debt", "On external debt", "Debt Indicators (continued)","Short-term debt, <1 year (type 1)",
            "Medium-term debt, 1 year to 5 years (type 1)","Long-term debt, >5 years (type 1)","Short-term debt, <1 year (type 2)",
            "Medium-term debt, 1 year to 5 years (type 2)",
            "Long-term debt, >5 years (type 2)","Philippine peso (PHP)",
            "US dollar (USD)",
            "Japanese yen (JPY)",
            "Euro (EUR)",
            "Chinese renminbi (CNY)",
            "Other currencies","PHP",
            "USD",
            "JPY",
            "EUR",
            "CNY","Memo items:"]
                    ],
                    value='Outstanding debt',
                    className="mb-4"
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Select Year", style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id='year-slider',
                    min=2006,
                    max=2023,
                    marks={year: {'label': str(year), 'style': {'color': 'black', 'font-weight': 'bold'}} for year in range(2006, 2024)},
                    value=[2006, 2023],
                    step=None,
                    className="mb-4"
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fiscal-chart')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='debt-chart')
            ], width=6)
        ])
    ])
])
# Define the layout for the 2024 page
layout_2024 = html.Div([
    # Navigation Bar
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("2006-2023", href="/data")),
            dbc.NavItem(dbc.NavLink("2024", href="/2024")),
        ],
        brand="Financial Market Monitoring and Analysis Division",
        brand_href="#",
        className="dark-blue-header",  # Apply the custom dark blue class
        dark=True,
    ),
    # Container for the content
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Fiscal and Debt Indicators Dashboard - 2024", className="text-center my-4 fade-in")
            ])
        ]),
        dbc.Row([
                        dbc.Col([
                html.Label("Select Fiscal Indicator", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='fiscal-indicator-dropdown-2024',
                    options=[
                        {'label': indicator, 'value': indicator}
                        for indicator in df_fiscal['Fiscal Indicators'].unique()
                        if indicator not in ["BIR collections", "BOC collections", "BTr income",
                                             "Domestic financing 1", "External financing 1", 
                                             "Domestic financing  2", "External financing 2",
                                             "Domestic financing 3", "External financing 3",'Domestic amortization','External amortization','As share of revenues (percent)','As share of expenditures (percent)','As share of GDP (percent)']
                    ],
                    value='Revenues',
                    className="mb-4"
                )
            ], width=6),
            dbc.Col([
                html.Label("Select Debt Indicator", style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='debt-indicator-dropdown-2024',
                    options=[
                        {'label': indicator, 'value': indicator}
                        for indicator in df_debt['Debt Indicators'].unique()
                        if indicator not in ["Domestic debt", "External debt", "Domestic guarantees",
                                             "External guarantees", "On domestic debt", "On external debt", "Debt Indicators (continued)","Short-term debt, <1 year (type 1)",
            "Medium-term debt, 1 year to 5 years (type 1)","Long-term debt, >5 years (type 1)","Short-term debt, <1 year (type 2)",
            "Medium-term debt, 1 year to 5 years (type 2)",
            "Long-term debt, >5 years (type 2)","Philippine peso (PHP)",
            "US dollar (USD)",
            "Japanese yen (JPY)",
            "Euro (EUR)",
            "Chinese renminbi (CNY)",
            "Other currencies","PHP",
            "USD",
            "JPY",
            "EUR",
            "CNY","Memo items:"]
                    ],
                    value='Outstanding debt',
                    className="mb-4"
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Select Time Period", style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id='period-slider-2024',
                    min=1,
                    max=4,
                    marks={
                        1: {'label': 'Jan-2024', 'style': {'color': 'black', 'font-weight': 'bold'}},
                        2: {'label': 'Feb-2024', 'style': {'color': 'black', 'font-weight': 'bold'}},
                        3: {'label': 'Mar-2024', 'style': {'color': 'black', 'font-weight': 'bold'}},
                        4: {'label': '1Q2024', 'style': {'color': 'black', 'font-weight': 'bold'}}
                    },
                    value=[1, 4],
                    step=None,
                    className="mb-4"
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fiscal-chart-2024')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='debt-chart-2024')
            ], width=6)
        ])
    ])
])

# Define the app layout to include the page container
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Update the page content based on the URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/data':
        return main_layout
    elif pathname == '/2024':
        return layout_2024
    else:
        return home_layout
    
# Define the callback to update the fiscal chart based on the selected year and indicator
@app.callback(
    Output('fiscal-chart', 'figure'),
    [
        Input('year-slider', 'value'),
        Input('fiscal-indicator-dropdown', 'value')
    ]
)
def update_fiscal_chart(selected_years, selected_indicator):
    start_year, end_year = selected_years
    df_selected = df_fiscal
    
    if selected_indicator == "Revenues":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "BIR collections",
            "BOC collections",
            "BTr income"
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Fiscal Indicators",
            title=f"Revenues for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
    elif selected_indicator == "Gross financing":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic financing 1",
            "External financing 1",
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df = selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Fiscal Indicators",
            title=f"Gross financing for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
    
    elif selected_indicator == "Amortization":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic amortization", "External amortization"
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df = selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Fiscal Indicators",
            title=f"Amortization for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
    elif selected_indicator == "Interest payments":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "As share of revenues (percent)",
            "As share of expenditures (percent)",            
            "As share of GDP (percent)",

        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
    
        fig = make_subplots(rows=1, cols=len(range(start_year, end_year + 1)), subplot_titles=[str(year) for year in range(start_year, end_year + 1)], specs=[[{'type': 'pie'}]*len(range(start_year, end_year + 1))])

        for i, year in enumerate(range(start_year, end_year + 1)):
            year_df = selected_year_df[selected_year_df["Year"] == str(year)]
            fig.add_trace(
                px.pie(
                    year_df,
                    names="Fiscal Indicators",
                    values="Value",
                    title=f"Interest payments for {year}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(title_text=f"Interest payments for {start_year}-{end_year}")
        return fig
    
    elif selected_indicator == "Financing mix (percent distribution of gross borrowing)":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic financing  2",
            "External financing 2",
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
    
        fig = make_subplots(rows=1, cols=len(range(start_year, end_year + 1)), subplot_titles=[str(year) for year in range(start_year, end_year + 1)], specs=[[{'type': 'pie'}]*len(range(start_year, end_year + 1))])

        for i, year in enumerate(range(start_year, end_year + 1)):
            year_df = selected_year_df[selected_year_df["Year"] == str(year)]
            fig.add_trace(
                px.pie(
                    year_df,
                    names="Fiscal Indicators",
                    values="Value",
                    title=f"Financing mix (percent distribution of gross borrowing) for {year}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(title_text=f"Financing mix (percent distribution of gross borrowing) {start_year}-{end_year}")
        return fig
    
    else:
        melted_df = df_selected.melt(id_vars=["Fiscal Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace('[^\d.-]', '', regex=True), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        selected_year_df = selected_year_df.sort_values(by="Year")
        fig = px.line(
            selected_year_df[selected_year_df["Fiscal Indicators"] == selected_indicator],
            x="Year",
            y="Value",
            title=f'{selected_indicator} over Time',
            markers=True
        )
        fig.update_yaxes(rangemode='tozero')

    return fig

#Define the callback for debt indicators 2006 to 2023
@app.callback(
    Output('debt-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('debt-indicator-dropdown', 'value')]
)
def update_debt_chart(selected_years, selected_indicator):
    start_year, end_year = selected_years
    df_selected = df_debt

    if selected_indicator == "Outstanding debt":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Domestic debt",
            "External debt"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        selected_year_df = selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Debt Indicators",
            title=f"Outstanding debt for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))

    elif selected_indicator == "Distribution by maturity type 3/":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Short-term debt, <1 year (type 1)",
            "Medium-term debt, 1 year to 5 years (type 1)",
            "Long-term debt, >5 years (type 1)"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        selected_year_df = selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Debt Indicators",
            title=f"Distribution by maturity type 3/ for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(
            yaxis=dict(type='linear'),
            legend=dict(
                font=dict(size=10),  # Adjust the size as needed
                title_font=dict(size=5)  # Adjust the size as needed
            )
        )

    elif selected_indicator == "Debt guaranteed by the NG":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Domestic guarantees",
            "External guarantees"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        selected_year_df = selected_year_df.groupby("Year").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        fig = px.bar(
            selected_year_df,
            x="Year",
            y="Value",
            color="Debt Indicators",
            title=f"Debt guaranteed by the NG for {start_year}-{end_year}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))

    elif selected_indicator == "Total debt by currency (in billion pesos)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Philippine peso (PHP)",
            "US dollar (USD)",
            "Japanese yen (JPY)",
            "Euro (EUR)",
            "Chinese renminbi (CNY)",
            "Other currencies"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        fig = px.line(
            selected_year_df,
            x="Year",
            y="Value",
            color="Debt Indicators",
            title=f"Total debt by currency (in billion pesos) for {start_year}-{end_year}",
            markers=True
        )
        fig.update_layout(yaxis=dict(type='linear'))
        fig.update_yaxes(rangemode='tozero')  # Set rangemode to 'tozero' for line charts

    elif selected_indicator == "Total debt by currency (percent of total)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "PHP",
            "USD",
            "JPY",
            "EUR",
            "CNY",
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])

        fig = make_subplots(
            rows=1,
            cols=len(range(start_year, end_year + 1)),
            subplot_titles=[str(year) for year in range(start_year, end_year + 1)],
            specs=[[{'type': 'pie'}] * len(range(start_year, end_year + 1))]
        )

        for i, year in enumerate(range(start_year, end_year + 1)):
            year_df = selected_year_df[selected_year_df["Year"] == str(year)]
            fig.add_trace(
                px.pie(
                    year_df,
                    names="Debt Indicators",
                    values="Value",
                    title=f"Debt by currency in {year}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(
            title_text=f"Total debt by currency (percent of total) for {start_year}-{end_year}"
        )

    elif selected_indicator == "Distribution by maturity type (percent of total)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Short-term debt, <1 year (type 2)",
            "Medium-term debt, 1 year to 5 years (type 2)",
            "Long-term debt, >5 years (type 2)"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace(',', ''), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])

        fig = make_subplots(
            rows=1,
            cols=len(range(start_year, end_year + 1)),
            subplot_titles=[str(year) for year in range(start_year, end_year + 1)],
            specs=[[{'type': 'pie'}] * len(range(start_year, end_year + 1))]
        )

        for i, year in enumerate(range(start_year, end_year + 1)):
            year_df = selected_year_df[selected_year_df["Year"] == str(year)]
            fig.add_trace(
                px.pie(
                    year_df,
                    names="Debt Indicators",
                    values="Value",
                    title=f"Distribution by maturity type (percent of total) for {year}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(
            title_text=f"Distribution by maturity type (percent of total) for {start_year}-{end_year}",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

    else:
        melted_df = df_selected.melt(id_vars=["Debt Indicators"], var_name="Year", value_name="Value")
        selected_year_df = melted_df[(melted_df["Year"] >= str(start_year)) & (melted_df["Year"] <= str(end_year))]
        selected_year_df["Value"] = pd.to_numeric(selected_year_df["Value"].str.replace('[^\d.-]', '', regex=True), errors='coerce')
        selected_year_df = selected_year_df.dropna(subset=["Value"])
        selected_year_df = selected_year_df.sort_values(by="Year")
        fig = px.line(
            selected_year_df[selected_year_df["Debt Indicators"] == selected_indicator],
            x="Year",
            y="Value",
            title=f'{selected_indicator} over Time',
            markers=True
        )
        fig.update_yaxes(rangemode='normal')

    return fig

# 2024 fiscal callback
@app.callback(
    Output('fiscal-chart-2024', 'figure'),
    [Input('period-slider-2024', 'value'),
     Input('fiscal-indicator-dropdown-2024', 'value')]
)
def update_fiscal_chart_2024(selected_period, selected_indicator):
    df_selected = df_fiscal

    # Determine the selected months based on the range of the slider
    period_map = {1: 'Jan-2024', 2: 'Feb-2024', 3: 'Mar-2024', 4: '1Q2024'}
    selected_months = [period_map[i] for i in range(selected_period[0], selected_period[1] + 1)]

    if selected_indicator == "Revenues":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "BIR collections",
            "BOC collections",
            "BTr income"
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Fiscal Indicators",
            title=f"Revenues for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
        
        return fig
    elif selected_indicator == "Gross financing":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic financing 1",
            "External financing 1",
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Fiscal Indicators",
            title=f"Gross financing for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))

        return fig
    elif selected_indicator == "Amortization":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic amortization", "External amortization"
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Fiscal Indicators",
            title=f"Amortization for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))

        return fig 
    elif selected_indicator == "Interest payments":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "As share of revenues (percent)",
            "As share of expenditures (percent)",            
            "As share of GDP (percent)",
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace(',', ''), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])

        fig = make_subplots(rows=1, cols=len(selected_months), subplot_titles=selected_months, specs=[[{'type': 'pie'}]*len(selected_months)])

        for i, month in enumerate(selected_months):
            month_df = selected_month_df[selected_month_df["Month"] == month]
            fig.add_trace(
                px.pie(
                    month_df,
                    names="Fiscal Indicators",
                    values="Value",
                    title=f"Interest payments for {month}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(title_text=f"Interest payments for {', '.join(selected_months)}")
        return fig

    elif selected_indicator == "Financing mix (percent distribution of gross borrowing)":
        sliced_df = df_selected[df_selected["Fiscal Indicators"].isin([
            "Domestic financing  2",
            "External financing 2",
        ])]
        melted_df = sliced_df.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace(',', ''), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])

        fig = make_subplots(rows=1, cols=len(selected_months), subplot_titles=selected_months, specs=[[{'type': 'pie'}]*len(selected_months)])

        for i, month in enumerate(selected_months):
            month_df = selected_month_df[selected_month_df["Month"] == month]
            fig.add_trace(
                px.pie(
                    month_df,
                    names="Fiscal Indicators",
                    values="Value",
                    title=f"Financing mix (percent distribution of gross borrowing) for {month}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(title_text=f"Financing mix (percent distribution of gross borrowing) {', '.join(selected_months)}")
        return fig
    else:
        melted_df = df_selected.melt(id_vars=["Fiscal Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace('[^\d.-]', '', regex=True), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered =True)
        selected_month_df = selected_month_df.sort_values(by="Month")
        fig = px.line(
            selected_month_df[selected_month_df["Fiscal Indicators"] == selected_indicator],
            x="Month",
            y="Value",
            title=f'{selected_indicator} over Time',
            markers=True
        )
        fig.update_yaxes(rangemode='tozero')

        return fig
    
# 2024 debt callback
@app.callback(
    Output('debt-chart-2024', 'figure'),
    [Input('period-slider-2024', 'value'),
     Input('debt-indicator-dropdown-2024', 'value')]
)
def update_debt_chart_2024(selected_period, selected_indicator):
    df_selected = df_debt

    # Determine the selected months based on the range of the slider
    period_map = {1: 'Jan-2024', 2: 'Feb-2024', 3: 'Mar-2024', 4: '1Q2024'}
    selected_months = [period_map[i] for i in range(selected_period[0], selected_period[1] + 1)]

    if selected_indicator == "Outstanding debt":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Domestic debt",
            "External debt",
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Debt Indicators",
            title=f"Outstanding debt for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
        return fig

    elif selected_indicator == "Distribution by maturity type 3/":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Short-term debt, <1 year (type 1)",
            "Medium-term debt, 1 year to 5 years (type 1)",
            "Long-term debt, >5 years (type 1)"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Debt Indicators",
            title=f"Distribution by maturity type for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
        return fig

    elif selected_indicator == "Debt guaranteed by the NG":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Domestic guarantees",
            "External guarantees"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.bar(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Debt Indicators",
            title=f"Debt guaranteed by the NG for {', '.join(selected_months)}",
            text_auto=True,
            barmode='stack'
        )
        fig.update_layout(yaxis=dict(type='linear'))
        return fig

    elif selected_indicator == "Total debt by currency (in billion pesos)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Philippine peso (PHP)",
            "US dollar (USD)",
            "Japanese yen (JPY)",
            "Euro (EUR)",
            "Chinese renminbi (CNY)",
            "Other currencies"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df = selected_month_df.groupby("Month").apply(lambda x: x.sort_values(by=["Value"], ascending=[False])).reset_index(drop=True)
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        fig = px.line(
            selected_month_df.sort_values(by="Month"),
            x="Month",
            y="Value",
            color="Debt Indicators",
            title=f"Total debt by currency (in billion pesos) for {', '.join(selected_months)}",
            markers=True
        )
        fig.update_layout(yaxis=dict(type='linear'))
        return fig

    elif selected_indicator == "Total debt by currency (percent of total)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "PHP",
            "USD",
            "JPY",
            "EUR",
            "CNY",
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace(',', ''), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])

        fig = make_subplots(rows=1, cols=len(selected_months), subplot_titles=selected_months, specs=[[{'type': 'pie'}]*len(selected_months)])

        for i, month in enumerate(selected_months):
            month_df = selected_month_df[selected_month_df["Month"] == month]
            fig.add_trace(
                px.pie(
                    month_df,
                    names="Debt Indicators",
                    values="Value",
                    title=f"Total debt by currency (percent of total) for {month}"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(title_text=f"Total debt by currency (percent of total) for {', '.join(selected_months)}")
        return fig

    elif selected_indicator == "Distribution by maturity type (percent of total)":
        sliced_df = df_selected[df_selected["Debt Indicators"].isin([
            "Short-term debt, <1 year (type 2)",
            "Medium-term debt, 1 year to 5 years (type 2)",
            "Long-term debt, >5 years (type 2)"
        ])]
        melted_df = sliced_df.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace(',', ''), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])

        fig = make_subplots(rows=1, cols=len(selected_months), subplot_titles=selected_months, specs=[[{'type': 'pie'}]*len(selected_months)])

        for i, month in enumerate(selected_months):
            month_df = selected_month_df[selected_month_df["Month"] == month]
            fig.add_trace(
                px.pie(
                    month_df,
                    names="Debt Indicators",
                    values="Value",
                    title=f"Distribution by maturity type (percent of total) over time"
                ).data[0],
                row=1, col=i+1
            )

        fig.update_layout(
            title_text=f"Distribution by maturity type (percent of total) for {', '.join(selected_months)}",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        return fig

    else:
        melted_df = df_selected.melt(id_vars=["Debt Indicators"], var_name="Month", value_name="Value")
        selected_month_df = melted_df[melted_df["Month"].isin(selected_months)]
        selected_month_df["Value"] = pd.to_numeric(selected_month_df["Value"].str.replace('[^\d.-]', '', regex=True), errors='coerce')
        selected_month_df = selected_month_df.dropna(subset=["Value"])
        selected_month_df["Month"] = pd.Categorical(selected_month_df["Month"], categories=selected_months, ordered=True)
        selected_month_df = selected_month_df.sort_values(by="Month")
        fig = px.line(
            selected_month_df[selected_month_df["Debt Indicators"] == selected_indicator],
            x="Month",
            y="Value",
            title=f'{selected_indicator} over Time',
            markers=True
        )
        fig.update_yaxes(rangemode='tozero')
        return fig


# Run the app on port 8051 instead of the default 8050
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)












































































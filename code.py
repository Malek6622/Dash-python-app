import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly 
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import requests
import dash_bootstrap_components as dbc
import dash_bootstrap_components.themes
import dash_table as dt

#external_stylesheets = [ 'https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/chriddyp/pen/brPBPO.css' ,[dbc.themes.BOOTSTRAP]]
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
app = dash.Dash(external_stylesheets=[BS])
#app = dash.Dash('project', external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = 'project'

tab1_stays = pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab1 csv/stays.csv", delimiter=';', skiprows=0, low_memory=False)
tab2_stays = pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab2 csv/stays.csv", delimiter=';', skiprows=0, low_memory=False)
tab2_in_cm_test = pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab2 csv/in-hospital-cm-test.csv", delimiter=';', skiprows=0, low_memory=False)
tab2_in_cm_test_report =pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab2 csv/in-hospital-cm-test-report.csv", delimiter=';', skiprows=0, low_memory=False)
tab2_in_cm_train_report = pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab2 csv/in-hospital-cm-train-report.csv", delimiter=';', skiprows=0, low_memory=False)
tab2_in_cm_train =pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab2 csv/in-hospital-cm-train.csv", delimiter=';', skiprows=0, low_memory=False)
tab3 = pd.read_csv("C:/Users/1692/Desktop/DashApp/Current code/tabs/tab3csv/length-of-stay-cm.csv", delimiter=';', skiprows=0, low_memory=False)

features = ['ETHNICITY', 'DIAGNOSIS', 'GENDER', 'AGE',  'MORTALITY_INUNIT', 'MORTALITY_INHOSPITAL']
opts = [{'label' : i, 'value' : i} for i in features]

white_button_style = {'background-color': 'white','color': 'Blue',}

tab2_in_cm_train_report["Precision"], tab2_in_cm_train_report["Recall"], tab2_in_cm_train_report["f1-score"],tab2_in_cm_train_report["Support"]= tab2_in_cm_train_report[",precision,recall,f1-score,support"].str.split(",", 3).str
tab2_in_cm_train_report = tab2_in_cm_train_report.drop([',precision,recall,f1-score,support'],axis = 1)

tab2_in_cm_test_report["Precision"], tab2_in_cm_test_report["Recall"], tab2_in_cm_test_report["f1-score"],tab2_in_cm_test_report["Support"]= tab2_in_cm_test_report[",precision,recall,f1-score,support"].str.split(",", 3).str
tab2_in_cm_test_report = tab2_in_cm_test_report.drop([',precision,recall,f1-score,support'],axis = 1)

app.layout =html.Div(children=[
	  dbc.Row(html.Div(children= [
      dbc.Col(html.Div(
      html.H1(children='Dashboard', 
           style={ 'color': '#0000A0','display': 'inline-block', 'float':'left','marginLeft':30 , 'marginRight':50,'backgroundColor':'aliceblue','font_family': 'Sans-Serif'})))],style={'width':'100%','backgroundColor':'aliceblue','max-width':50000})),
	  html.Div(children =[
		dbc.ButtonGroup(children =[
		dbc.Button('Tab1', id='btn-nclicks-1', n_clicks=0, color="primary", size='lg'),
	    dbc.Button('Tab2', id='btn-nclicks-2', n_clicks=0, color="primary",  size='lg'),
	    dbc.Button('Tab3', id='btn-nclicks-3', n_clicks=0, color="primary",  size='lg'),
	   
	    ],style={'width':'100%','marginRight':0,'marginLeft':0},className='row' )
	    ]),
	  dbc.Row(html.Div(children= [
      dbc.Col(html.Div(children =[  
        html.H1('Filters', style={ 'color': ' #0000A0','marginLeft':17,'font_family': 'Sans-Serif'}) , 
      dbc.Col(html.Div(children =[ 
      	dbc.DropdownMenu(
      			[
			    dbc.DropdownMenuItem('ETHNICITY', id ='ETHNICITY'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem("DIAGNOSIS", id ="DIAGNOSIS"),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('GENDER', id ='GENDER'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('AGE', id ='AGE'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INUNIT', id ='MORTALITY_INUNIT'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INHOSPITAL', id ='MORTALITY_INHOSPITAL'),
			],
      			id = 'opt', 
                label="Stays1 Columns",
                bs_size="sm",
                color="primary",
                )],style={'float':'left','marginLeft':0})),
         dbc.Col(html.Div(children =[ 
      	 dbc.DropdownMenu(
      			[
			    dbc.DropdownMenuItem('ETHNICITY', id ='ETHNICITY1'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem("DIAGNOSIS", id ="DIAGNOSIS1"),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('GENDER', id ='GENDER1'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('AGE', id ='AGE1'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INUNIT', id ='MORTALITY_INUNIT1'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INHOSPITAL', id ='MORTALITY_INHOSPITAL1'),
			],
      			id = 'opt1', 
                label="stays2 Columns",
                bs_size="sm",
                color="primary",
                )],style={'float':'left','marginLeft':0,'paddingTop':20})),
         dbc.Col(html.Div(children =[ 
      	 dbc.DropdownMenu(
      			[
			    dbc.DropdownMenuItem('ETHNICITY', id ='ETHNICITY2'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem("DIAGNOSIS", id ="DIAGNOSIS2"),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('GENDER', id ='GENDER2'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('AGE', id ='AGE2'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INUNIT', id ='MORTALITY_INUNIT2'),
			    dbc.DropdownMenuItem(divider=True),
			    dbc.DropdownMenuItem('MORTALITY_INHOSPITAL', id ='MORTALITY_INHOSPITAL2'),
			],
      			id = 'opt2', 
                label="stays3 Columns",
                bs_size="sm",
                color="primary",
                )],style={'float':'left','marginLeft':0,'paddingTop':20})),

      	],style={'width':'10%','marginRight':10,'marginLeft':0,'height':'100%','display': 'inline-block','backgroundColor':'aliceblue', 'float':'left'}, className="one column" )),

		dbc.Col(html.Div(children =[
		html.Div(children =[
			html.Div(id='container-button-timestamp'),
			])
		 ])),
		
      ],style={'width': '100%', 'marginRight':0, 'marginRight': 0 ,'max-width':50000},className='container')),
	  ])

@app.callback(Output('container-button-timestamp', 'children'),
              [Input('btn-nclicks-1', 'n_clicks'),
               Input('btn-nclicks-2', 'n_clicks'),
               Input('btn-nclicks-3', 'n_clicks'),
               Input('ETHNICITY', "n_clicks"),
               Input('DIAGNOSIS', "n_clicks"),
               Input('GENDER', "n_clicks"),
               Input( 'AGE', "n_clicks"),
               Input('MORTALITY_INUNIT', "n_clicks"),
               Input( 'MORTALITY_INHOSPITAL', "n_clicks"),
               Input('ETHNICITY1', "n_clicks"),
               Input('DIAGNOSIS1', "n_clicks"),
               Input('GENDER1', "n_clicks"),
               Input( 'AGE1', "n_clicks"),
               Input('MORTALITY_INUNIT1', "n_clicks"),
               Input( 'MORTALITY_INHOSPITAL1', "n_clicks"),
               Input('ETHNICITY2', "n_clicks"),
               Input('DIAGNOSIS2', "n_clicks"),
               Input('GENDER2', "n_clicks"),
               Input( 'AGE2', "n_clicks"),
               Input('MORTALITY_INUNIT2', "n_clicks"),
               Input( 'MORTALITY_INHOSPITAL2', "n_clicks")])

def displayClick(btn1, btn2, btn3,x1,x2,x3,x4,x5,x6,y1,y2,y3,y4,y5,y6,z1,z2,z3,z4,z5,z6):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	ctx = dash.callback_context
	if 'btn-nclicks-1' in changed_id:
		data = tab1_stays.to_dict('rows')
		columns =  [{"name": i, "id": i,} for i in (tab1_stays.columns)]
		return (html.Div(children=[ dt.DataTable(data=data, columns=columns,page_size=20,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '15px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0}))

	elif 'btn-nclicks-2' in changed_id:
		data0 = tab2_stays.to_dict('rows')
		data1 = tab2_in_cm_test_report.to_dict('rows') 
		data2 = tab2_in_cm_train_report.to_dict('rows')
		columns0 =  [{"name": i, "id": i,} for i in (tab2_stays.columns )]
		columns1 =  [{"name": i, "id": i,} for i in (tab2_in_cm_test_report.columns )]
		columns2 =  [{"name": i, "id": i,} for i in (tab2_in_cm_train_report.columns )]
		arr = tab2_stays.to_numpy()
		return(
		dbc.Row(
		html.Div(children=[ dt.DataTable(data=data0, columns=columns0,page_size=7,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '15px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		],)] ,style={'width':'20%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})),
		dbc.Row(html.Div(children=[dbc.Button("Model", color="primary", block=True, disabled=True),
			],style={'width':'100%'})),
		dbc.Row(
		html.Div(children=[
		html.Div(children=[
		dcc.Graph(
           figure={
           'data': [
             go.Heatmap(
                    x = ['Predicted 0', 'Predicted 1'],
                    y = ['Actual 1', 'Actual 0'],
                    z= [[.1, .4],
    				   [1.0, .07]],
    				colorscale='bugn',
    				text=[['241', '133'],
                          ['2772', '90']]
                     )],
            'layout': go.Layout(
             #hovermode="x unified",
             title = {
             'text': 'Test Score: 0.446',
             'font_family': 'Droid Sans',
             'font_size': 20,
              'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'},
             

            )})
		],style={ 'float':'left','display': 'inline-block','width': '42%','marginLeft':'10px' },className= 'three columns' ),
       html.Div(children=[
		dcc.Graph(
           figure={
           'data': [
             go.Heatmap(
                    x = ['Predicted 0', 'Predicted 1'],
                    y = ['Actual 1', 'Actual 0'],
                    z= [[.1, .4],
    				   [1.0, .07]],
    				colorscale = [[0, 'rgb(224, 243, 248)'],
              					 [1, 'rgb(12, 51, 131)']],
              		text=[['759', '1228'],
       				   ['12572', '122']]
              		
                     )],
            'layout': go.Layout(
             #hovermode="x unified",
             title = {'text':'Train Score: 0.736','font_family': 'Droid Sans',
                 'font_size': 20,
              'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'},
             xaxis = {'ticksuffix': ''},
             yaxis = {'title' : ''},
              #annotation=[['241', '133'],
               #            ['2772', '90']]


            )})
		],style={ 'float':'right','display': 'inline-block','width': '42%','marginLeft':'10px' },className= 'three columns' ),
        ],style={'width': '90%','max-width':50000},className='container')),

		dbc.Row(
		html.Div(children=[
		html.Div(children=[
		html.H4('Test', style={ 'color': ' #0000A0','font_family': 'Sans-Serif'}),
		dt.DataTable(data=data1, columns=columns1,page_size=20,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'80xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '20px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		])],style={ 'float':'left','display': 'inline-block','width': '42%','marginRight':100 },className= 'three columns'),
		html.Div(children=[
		html.H4('Train', style={ 'color': ' #0000A0','font_family': 'Sans-Serif'}),
		dt.DataTable(data=data2, columns=columns2,page_size=20,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'80xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '20px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		]),],style={ 'float':'right','display': 'inline-block','width': '42%','marginLeft':'10px' },className= 'three columns'),
		],style={'width': '90%','max-width':50000},className='container')),
		)

	elif 'btn-nclicks-3' in changed_id:
		data = tab1_stays.to_dict('rows')
		columns =  [{"name": i, "id": i,} for i in (tab3.columns)]
		data0 = tab2_stays.to_dict('rows')
		columns0 =  [{"name": i, "id": i,} for i in (tab2_stays.columns )]
		return (
		dbc.Row(
		html.Div(children=[dt.DataTable(data=data0, columns=columns0,page_size=10,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'80xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '15px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left' , 'marginRight':0,'marginBottom':5})),



		dbc.Row(html.Div(children=[dbc.Button("Title", color="primary", block=True, disabled=True),
			],style={'width':'100%'})),

		html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=10,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '15px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		],)],style={ 'float':'left','width': '42%' },className= 'three columns')
		)

	elif ctx.triggered:
		button_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if button_id in ['ETHNICITY'] :
			df = tab1_stays[['ETHNICITY']]
			data = tab1_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})


		elif button_id in ['DIAGNOSIS']:
			df = tab1_stays[['DIAGNOSIS']]
			data = tab1_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['GENDER']:
			df = tab1_stays[['GENDER']]
			data = tab1_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['AGE']:
			df = tab1_stays[['AGE']]
			data = tab1_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INUNIT']:
			df = tab1_stays[['MORTALITY_INUNIT']]
			data = tab1_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INHOSPITAL']:
			df = tab1_stays[['MORTALITY_INHOSPITAL']]
			data = tab1_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0}),
		elif button_id in ['ETHNICITY1'] :
			df = tab2_stays[['ETHNICITY']]
			data = tab2_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})


		elif button_id in ['DIAGNOSIS1']:
			df = tab2_stays[['DIAGNOSIS']]
			data = tab2_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['GENDER1']:
			df = tab2_stays[['GENDER']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['AGE1']:
			df = tab2_stays[['AGE']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INUNIT1']:
			df = tab2_stays[['MORTALITY_INUNIT']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INHOSPITAL1']:
			df = tab2_stays[['MORTALITY_INHOSPITAL']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})
		elif button_id in ['ETHNICITY2'] :
			df = tab2_stays[['ETHNICITY']]
			data = tab2_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})


		elif button_id in ['DIAGNOSIS2']:
			df = tab2_stays[['DIAGNOSIS']]
			data = tab2_stays.to_dict('rows')
			columns =  [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['GENDER2']:
			df = tab2_stays[['GENDER']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['AGE2']:
			df = tab2_stays[['AGE']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INUNIT2']:
			df = tab2_stays[['MORTALITY_INUNIT']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

		elif button_id in ['MORTALITY_INHOSPITAL2']:
			df = tab2_stays[['MORTALITY_INHOSPITAL']]
			data = tab2_stays.to_dict('rows')
			columns = [{"name": i, "id": i,} for i in (df)]

			return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
			style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
			'font_size': '15px'}
			, style_as_list_view=True,
			filter_action='native',
			style_header={
			'backgroundColor': 'aliceblue',
			'font_family': 'Sans-Serif',
			'font_size': '15px',
			'color':'#0000A0',
			'fontWeight': 'bold'},
			style_data_conditional=[
			{
			'if': {'row_index': 'odd'},
			'backgroundColor': 'rgb(248, 248, 248)'
			}
			],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

	else:

		data = tab1_stays.to_dict('rows')
		columns =  [{"name": i, "id": i,} for i in (tab1_stays.columns)]
		return html.Div(children=[dt.DataTable(data=data, columns=columns,page_size=20,
		style_cell={'textAlign': 'left','padding': '10px','marginLeft':'50xp','font_family': 'Sans-Serif',
		'font_size': '15px'}
		, style_as_list_view=True,
		filter_action='native',
		style_header={
		'backgroundColor': 'aliceblue',
		'font_family': 'Sans-Serif',
		'font_size': '15px',
		'color':'#0000A0',
		'fontWeight': 'bold'},
		style_data_conditional=[
		{
		'if': {'row_index': 'odd'},
		'backgroundColor': 'rgb(248, 248, 248)'
		}
		],)] ,style={'width':'20%','height':'30%' ,'marginLeft':0, 'float':'left','display': 'inline-block' , 'marginRight':0})

@app.callback(Output('btn-nclicks-1', 'style'), 
	[Input('btn-nclicks-1', 'n_clicks'),Input('btn-nclicks-2', 'n_clicks'),Input('btn-nclicks-3', 'n_clicks')])
def change_button_style(n_clicks,n_clicks1,n_clicks2):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'btn-nclicks-1' in changed_id:
		return white_button_style


@app.callback(Output('btn-nclicks-2', 'style'), 
	[Input('btn-nclicks-1', 'n_clicks'),Input('btn-nclicks-2', 'n_clicks'),Input('btn-nclicks-3', 'n_clicks')])
def change_button_style(n_clicks,n_clicks1,n_clicks2):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'btn-nclicks-2' in changed_id:
		return white_button_style

@app.callback(Output('btn-nclicks-3', 'style'), 
	[Input('btn-nclicks-1', 'n_clicks'),Input('btn-nclicks-2', 'n_clicks'),Input('btn-nclicks-3', 'n_clicks')])
def change_button_style(n_clicks,n_clicks1,n_clicks2):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'btn-nclicks-3' in changed_id:
		return white_button_style
if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
df = pd.read_csv("data/onlinedeliverydata.csv")


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    figures= []

# Does Income affect when food is ordered ?
    df_income_time = df.groupby('Monthly Income')['Order Time'].value_counts().unstack(fill_value=0)
    x = ['10001 to 25000','25001 to 50000','Below Rs.10000','More than 50000','No Income']
    data = []
    for income in list(df_income_time.columns):
        y = list(df_income_time[income].values)
        name = income
        data.append(go.Bar(name=name,x=x,y=y))
    fig = go.Figure(data=data, layout=go.Layout(
    title="Does income affect when food is ordered?",
    yaxis_title="Count",xaxis_title="Income range"))
    fig.update_layout(barmode='stack')
    #fig.show()
    figures.append(fig)

# How important is temperature in food, is it sufficient if its tasty, and in good quantity?
    x = ['Important','Very Important','Moderately Important','Slightly Important','Unimportant']
    y1 = list(df['q_Good Quantity'].value_counts())
    y2 = list(df['q_Good Taste '].value_counts())
    y3 = list(df['q_Temperature'].value_counts())

    fig = go.Figure(layout=go.Layout(
    title="Importance of temperature vs taste",
    yaxis_title="Count",
    xaxis_title="Level of importance given"))
    fig.add_trace(go.Bar(x = x,y = y1,
    name = 'Good Quantity',
    marker_color = '#2F1C9C'))
    fig.add_trace(go.Bar(x = x,y = y2,
    name = 'Good Taste',
    marker_color = '#00a375'))
    fig.add_trace(go.Bar(x = x,y = y3,
    name = 'Temperature',
    marker_color = '#ff5f5c'))
    fig.update_layout(barmode='group', xaxis_tickangle=45)
    figures.append(fig)


# Does politeness trump taste (experience over product?)?
    x = ['Important','Very Important','Moderately Important','Slightly Important','Unimportant']
    y1 = list(df['q_Politeness'].value_counts())
    y2 = list(df['q_High Quality of package'].value_counts())
    y3 = list(df['q_Number of calls'].value_counts())
    y4 = list(df['q_Good Taste '].value_counts())

    fig = go.Figure(layout=go.Layout(title="Does politeness trump taste",yaxis_title="Count",xaxis_title="Level of importance given"))
    fig.add_trace(go.Bar(x = x,y = y1,name = 'Politeness',marker_color = '#ADACB5'))
    fig.add_trace(go.Bar(x = x,y = y2,name = 'High Quality of package',marker_color = '#978CA6'))
    fig.add_trace(go.Bar(x = x,y = y3,name = 'Number of calls',marker_color = '#CCC8D0'))
    fig.add_trace(go.Bar(x = x,y = y4,name = 'Good Taste ',marker_color = '#ff5f5c'))
    fig.update_layout(barmode='group')#, xaxis_tickangle=0
    figures.append(fig)


# Distribution of customers
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",hover_name="Occupation", hover_data=["Monthly Income","Age","Output", 'Educational Qualifications','Family size'],color='Output', size=[1]*len(df), size_max=8,zoom=10, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    figures.append(fig)

# Customer feedback to improve
    data = {
    "Agree_yes":[108+45, 59+24,129+37,144+37],
    "Agree_no":[34+11,40+7,60+7,41+5],
    "Disagree_yes":[61+17,118+28,54+15,75+7],
    "Disagree_no":[7+1,25+2,7+1,33+0],
    "labels": [
    "Delay of delivery person getting assigned",
    "Bad past experience",
    "Delay of delivery person picking up food",
    "Long delivery time"]}

    fig = go.Figure(
    data = [
    go.Bar(name="Agree_yes",x=data['labels'],y = data['Agree_yes'],offsetgroup = 0,marker_color='#0F6B62'),
    go.Bar(name="Agree_no",x=data['labels'],y = data['Agree_no'],offsetgroup = 0,base=data["Agree_yes"],marker_color='#2D9F92'),
    go.Bar(name="Disagree_yes",x=data['labels'],y = data['Disagree_yes'],offsetgroup = 1,marker_color = "#9C212D"),
    go.Bar(name="Disagree_no",x=data['labels'],y = data['Disagree_no'],offsetgroup = 1,base=data["Disagree_yes"],marker_color = '#ED3147')
    ],
    layout=go.Layout(title="Customer feedback",yaxis_title="Count",xaxis_title="Question")
    )
    figures.append(fig)

    return figures

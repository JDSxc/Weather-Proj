import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
#import plotly.tools as tools
#from plotly.tools import mpl_to_plotly

def dict_creator(keys, values): ## assume that key and value have the same length
    data = {}
    counter = 0
    for key in keys:
        data[key] = values[counter]
        counter+=1

    return data

def average_data(arr1, arr2): ## assume that both have the same length
    data = []
    counter = 0
    for el in arr1:
        data.append((el + arr2[counter])/2)
        counter+=1
    return data

def convert_to_celsius(el):
    return (el - 32) * 5/9
    
def celsius_dict(dict):
    for key in dict.keys():
        dict[key] = convert_to_celsius(dict[key])
    return dict

def graph(average):
    x=list(average.keys())
    y=list(average.values())
    #plt.bar(x,y)
    plt.xlabel("Weekdays")
    plt.ylabel("Temperature (Celsius)")
    plt.plot(x, y)
    plt.title("Average Temperature")
    plt.savefig('./static/graph/graph.png')
    #plotly_fig = tools.mpl_to_plotly(plt.gcf())
    #plotly_fig.write_image('./templates/graph.png')
def graph_generator(average, high, low, tempType):
    x=list(average.keys())
    avgy=list(average.values())
    highy=list(high.values())
    lowy=list(low.values())

    plt.figure(figsize=(10, 6))
    #plt.bar(x,y)
    plt.xlabel("Weekdays")
    plt.ylabel(f"Temperature {tempType}°")
    
    plt.tight_layout()
    plt.margins(x=0)
    plt.plot(x,avgy, color="#c4c03f", label = "Average Temperature")
    plt.plot(x,highy, color="red", label = "High Temperature")
    plt.plot(x,lowy, color="#3f6bc4", label = "Low Temperature")
    plt.legend(['Average Temperature', 'High Temperature', 'Low Temperature'] )

    os.makedirs("/tmp/graph", exist_ok=True)
    plt.savefig(f'/tmp/graph/graph_{tempType}.png', bbox_inches="tight")
    print("executed")
    plt.close()


""" 
def graph_generator_interactive(average, high, low):
    x = list(average.keys())
    avgy = list(average.values())
    highy = list(high.values())
    lowy = list(low.values())

    trace_avg = go.Scatter(x=x, y=avgy, mode='lines+markers', name='Average Temperature', line=dict(color="#c4c03f"))
    trace_high = go.Scatter(x=x, y=highy, mode='lines+markers', name='High Temperature', line=dict(color="red"))
    trace_low = go.Scatter(x=x, y=lowy, mode='lines+markers', name='Low Temperature', line=dict(color="#3f6bc4"))

    layout = go.Layout(
        title='Next Week Temperature Forecast',
        xaxis=dict(title='Weekdays'),
        yaxis=dict(title='Temperature (°F)'),
        hovermode='closest'
    )

    fig = go.Figure(data=[trace_avg, trace_high, trace_low], layout=layout)
    os.makedirs(os.path.dirname("/tmp/graph/"), exist_ok=True)
    fig.write_html("/tmp/graph/graph.html")
"""
'''
average = {
    'Mon': 20,
    'Tues': 22,
    'Wed': 24,
    'Thurs': 21,
    'Fri': 23,
    'Sat': 26,
    'Sun': 25
}

high = {
    'Mon': 25,
    'Tues': 27,
    'Wed': 29,
    'Thurs': 26,
    'Fri': 28,
    'Sat': 31,
    'Sun': 30
}

low = {
    'Mon': 15,
    'Tues': 17,
    'Wed': 19,
    'Thurs': 16,
    'Fri': 18,
    'Sat': 21,
    'Sun': 20
}

graph_generator(average, high, low)
'''
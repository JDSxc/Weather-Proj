import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
#import plotly.tools as tools


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
def graph_generator(average, high, low):
    x=list(average.keys())
    avgy=list(average.values())
    highy=list(high.values())
    lowy=list(low.values())
    #plt.bar(x,y)
    plt.xlabel("Weekdays")
    plt.ylabel("Temperature (F)")
    #plt.figure(figsize=(8, 6))
    plt.margins(x=0)
    plt.plot(x,avgy, color="#c4c03f", label = "Average Temperature")
    plt.plot(x,highy, color="red", label = "High Temperature")
    plt.plot(x,lowy, color="#3f6bc4", label = "Low Temperature")
    plt.legend(['Average Temperature', 'High Temperature', 'Low Temperature'] )
    plt.title("Next week Temperature forecast")
    #os.makedirs('./static/graph', exist_ok=True)
    os.remove('./static/graph/graph.png')
    plt.savefig('./static/graph/graph.png')
    print("executed")
    plt.close()

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
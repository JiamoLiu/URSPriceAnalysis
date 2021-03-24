import pandas as pd
import matplotlib.pyplot as plt
file_in = r"C:\Users\27761\Desktop\Research\IMC2021\URSPriceAnalysis\urban_price_ISP - Data.tsv"
income_file_in = r"C:\Users\27761\Desktop\Research\IMC2021\URSPriceAnalysis\state_income.csv"
max_interested_mbps = 9999
min_interested_mbps = 0
min_quota_in_gb = 1000
from statistics import median

def get_mbps_and_cost_from_result(data):
    keys = data.keys()
    mbps = []
    cost = []
    for key in keys:
        mbps.append(key)
        cost.append(data[key][0])
    return mbps,cost

def plot_all_state(data,states):
    for state in states:
        plot_state(state,data)


def plot_state(state_name, data):
    data_temp = dict(sorted(data[state_name].items()))
    mbps,cost = get_mbps_and_cost_from_result(data_temp)
    plt.scatter(mbps,cost ,label = state_name)
    


def add_to_res_dict(dict,  up_down_value, cost,state_name):
    if state_name not in dict.keys():
        dict[state_name] = {}

    if up_down_value in dict[state_name].keys():
        cost_per_mbps = cost/up_down_value
        total = dict[state_name][up_down_value][0] * dict[state_name][up_down_value][1] + cost_per_mbps
        numbers = dict[state_name][up_down_value][1]+1
        dict[state_name][up_down_value] =  (total/numbers,numbers) 
    else:
        dict[state_name][up_down_value] = (cost/up_down_value,1)



def get_mbps_per_usd_for_state(state_data,state_name,download_res,upload_res):
    for index, row in state_data.iterrows():
        download = row["Download Bandwidth Mbps"]   
        upload = row["Upload Bandwidth Mbps"]
        charge = row["Monthly Charge"]
        add_to_res_dict(download_res, download,charge,state_name)
        add_to_res_dict(upload_res, upload,charge,state_name)
    return download_res, upload_res

def calculate_cost_metric_for_state(state_data, state_name, download_res, upload_res):
    if state_name not in download_res:
        download_res[state_name] = {}

    if state_name not in upload_res:
        upload_res[state_name] = {}

    down_res =[]
    up_res = []
    for index, row in state_data.iterrows():
        download = row["Download Bandwidth Mbps"]   
        upload = row["Upload Bandwidth Mbps"]
        charge = row["Monthly Charge"]
        down_cost_metric = charge/download
        up_cost_metric = charge/upload
        down_res.append(down_cost_metric)
        up_res.append(up_cost_metric)

    download_res[state_name] = down_res
    upload_res[state_name] = up_res
    return download_res,upload_res
    #print(state_data.index)

def find_median_of_all_states(data):
    res = {}
    for state in data.keys():
        res[state] = median(data[state])
    return res

#Find median of cost metric between 0-200
#Find 25->95 jump between price and speed

def unpack_dict(data):
    keys = []
    values = []
    for key,value in sorted(data.items(), key=lambda x: x[1]):
        keys.append(key)
        values.append(value)
    return keys,values
def plot_cost_metric_all(data,income_data):
    states, cost_metrics = unpack_dict(data)
    apply_weight(income_data,states,cost_metrics)
    #print(states)
    #print(cost_metrics)
    dictionary = dict(zip(states, cost_metrics))
    states, cost_metrics = unpack_dict(dictionary)
    plt.bar(states,cost_metrics) 

def apply_weight(income_data,states, cost_metrics):
    max_income = income_data["median_income_bgp"].max()
    for i in range(len(states)):
        state = states[i]
        weight = 1

        
        #print(income_data[income_data["State_y"].str.upper() == state].median_income_bgp.iat[0])


        if income_data["State_y"].str.upper().str.contains(state).any():
            weight = 1/((income_data[income_data["State_y"].str.upper() == state].median_income_bgp.iat[0])/max_income)
            cost_metrics[i] = cost_metrics[i] * weight
        print(weight)



def main():
    df = pd.read_csv(file_in, sep= "\t").dropna().replace("Inf", 9999).replace("Unlimited",9999)
    df = df.loc[(df["Usage Allowance GB"].astype(float) > min_quota_in_gb) & (df["Download Bandwidth Mbps"].astype(float) < max_interested_mbps) & (df["Download Bandwidth Mbps"].astype(float) > min_interested_mbps)]
    income_df = pd.read_csv(income_file_in)
    states = sorted(df["State"].unique())
    download_res = {}
    upload_res ={}

    download_cost_metric ={}
    upload_cost_metric={}
    for state in states:
        state_values = df.loc[df["State"] == state]
        get_mbps_per_usd_for_state(state_values, state,download_res,upload_res)
        calculate_cost_metric_for_state(state_values, state,download_cost_metric,upload_cost_metric)

    cost_metric = find_median_of_all_states(download_cost_metric)
    plot_cost_metric_all(cost_metric,income_df)
    #print(download_cost_metric)
    #print(download_res.keys())
    #plot_all_state(download_res,states)
    #plot_state("NEW JERSEY", download_res)
    #plot_state("ARIZONA", download_res)    
    #plot_state("GEORGIA", download_res) 
    #plot_state("MASSACHUSETTS", download_res) 
    #plt.xlim([0,200])
    plt.legend(loc="upper right")
    plt.xticks(rotation=90)
    #print(download_res["NEW JERSEY"])    
    #print(download_res["ARIZONA"])
    #print(download_res["MASSACHUSETTS"])       
    plt.show()



main()

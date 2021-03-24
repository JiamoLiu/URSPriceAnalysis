import pandas as pd
import matplotlib.pyplot as plt
file_in = r"C:\Users\27761\Desktop\Research\IMC2021\Price_Analysis\urban_price_ISP - Data.tsv"

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
    plt.plot(mbps,cost ,label = state_name)
    


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



    #print(state_data.index)


def main():
    df = pd.read_csv(file_in, sep= "\t").dropna().replace("Inf", 9999).replace("Unlimited",9999)
    df = df.loc[( df["Usage Allowance GB"].astype(float) > 1000)]
    states = sorted(df["State"].unique())
    download_res = {}
    upload_res ={}
    for state in states:
        state_values = df.loc[df["State"] == state]
        get_mbps_per_usd_for_state(state_values, state,download_res,upload_res)

    print(download_res.keys())
    #plot_all_state(download_res,states)
    plot_state("NEW JERSEY", download_res)
    plot_state("ARIZONA", download_res)    
    plot_state("GEORGIA", download_res) 
    plot_state("MASSACHUSETTS", download_res) 
    plt.xlim([0,200])
    plt.legend(loc="upper right")    
    plt.show()
main()

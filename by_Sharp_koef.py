

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from datetime import datetime
start = datetime.now()

file_1 = open("SP 500 347 2000-27.08.2020.txt", mode= "r")

raw_data = []
for i, line in enumerate(file_1):
    l = line.rstrip()
    a = l.split(",")
    raw_data.append(a)

file_1.close

raw_data = np.array(raw_data)
columns = raw_data[0]

data = np.delete(raw_data, 0, axis = 0)
data = np.delete(data, 0, axis = 1)

data = np.array(data, dtype=float)
#data = pd.DataFrame(raw_data, columns=columns)
#print(data.head())
#str_count, rows_count  = data.shape()
#for j in range(data:
#    std = np.std(item)
#    print(std)

#41275



#start_of_test_period = sharp_period    # Должен быть больше чем sharp_period

sharp_period = 200
end_of_test_period = 5386      # Похоже важна кратность диапазона end-start по step
start_of_test_period = end_of_test_period - sharp_period - 1
step = 100

max_stocks_to_portf = 10

columns_count = data.shape[1] # число акций
stocks_to_portf_list = []
overal_results = []
random_portf_list = []

for i in range(start_of_test_period,end_of_test_period,step):
#for i in range(sharp_period,sharp_period+step*10,step):        # Пересчитываем черзе период step коэфф Шарпа
    stocks_to_portf_list = []          
    counter = 1
    random_portf = np.mean(np.array(data[i-sharp_period:i,:]))
    random_portf_list.append(random_portf)
    for k in range(0, max_stocks_to_portf):
        sharp_ratio_list = []
        if counter == 1:                             # Выбираем первую акцию в портфель
            for j in range(0, columns_count):
                share_prices = np.array(data[i-sharp_period:i,j], dtype=float)
                income = np.sum(share_prices)
                std = np.std(share_prices)
                if std > 0:
                    sharp_ratio = income/std
                else:
                    sharp_ratio = 0
                sharp_ratio_list.append(sharp_ratio)
            
            max_sharp_ratio = max(sharp_ratio_list)
            indx_max_sharp_ratio = np.argmax(sharp_ratio_list)
            comulative_income = np.array(data[i-sharp_period:i,indx_max_sharp_ratio], dtype=float)   # Инициализируем доход портфеля
            stocks_to_portf_list.append(indx_max_sharp_ratio)
            counter = counter + 1
        else:
            for j in range(0, columns_count):
                if j in stocks_to_portf_list:    # Добавляю чтобы нельзя было повторно включать акции
                    sharp_ratio_list.append(0)
                else:
                    share_prices = np.array(data[i-sharp_period:i,j], dtype=float)
                    sub_sumpl_comulative_income = comulative_income + share_prices 
                    income = np.sum(sub_sumpl_comulative_income)
                    std = np.std(sub_sumpl_comulative_income)
                    if std > 0:
                        sharp_ratio = income/std
                    else:
                        sharp_ratio = 0
                    sharp_ratio_list.append(sharp_ratio)
            
            max_sharp_ratio = max(sharp_ratio_list)
            indx_max_sharp_ratio = np.argmax(sharp_ratio_list)
            comulative_income = comulative_income + np.array(data[i-sharp_period:i,indx_max_sharp_ratio], dtype=float)
            stocks_to_portf_list.append(indx_max_sharp_ratio)
            counter = counter + 1
    
    stocks_to_portf_list = np.array(stocks_to_portf_list)
    #print(stocks_to_portf_list)
    for j in range(0,max_stocks_to_portf):
        if j == 0:
            stock_ind = stocks_to_portf_list[j]
            results = np.array(data[i:i+step,stock_ind], dtype=float)
        else:
            stock_ind = stocks_to_portf_list[j]
            results = results + np.array(data[i:i+step,stock_ind], dtype=float) 
    results = np.array(results)
    overal_results.append(results)

#overal_results = pd.DataFrame(overal_results)
#print(overal_results)
overal_results = np.array(overal_results)    
print(overal_results.shape)
# Анализируем результаты
strings = overal_results.shape[0]
rows  = overal_results.shape[1]
print(strings, rows)

mean_profit_list = []
P_E_list = []

for i in range(0, overal_results.shape[0]):
    profit = 0
    loss = 0
    for j in range(0, overal_results.shape[1]):
        if overal_results[i][j] >= 0:
            profit = profit + overal_results[i][j]
        else:
            loss = loss + overal_results[i][j]
            
    mean_profit = (profit + loss)/max_stocks_to_portf
    P_E = -profit / loss
    mean_profit_list.append(mean_profit)
    P_E_list.append(P_E)

mean_profit_list = np.array(mean_profit_list)
P_E_list = np.array(P_E_list)
random_portf_list = np.array(random_portf_list)


print(max_sharp_ratio, indx_max_sharp_ratio)
print(stocks_to_portf_list)
print(mean_profit_list)
print('mean_annual_profit:', mean_profit_list.mean()*(250 / step))
print(P_E_list)
print('P_E_list.mean:', P_E_list.mean())

random_income = random_portf_list.mean() * 250
print('random_portf_mean_profit:', random_income)
#random_mean_profit = data.mean() * 250
#print('random_mean_profit:', random_mean_profit)


plt.plot(mean_profit_list)
plt.figure()
plt.plot(P_E_list)


finish = datetime.now()
print('start: ',start)
print('start: ',start)
print('finish: ',finish)
print('difference: ', finish-start)

for i  in range(0,stocks_to_portf_list.shape[0]):
    
    stock_ind = stocks_to_portf_list[i]
    name = columns[stock_ind]
    print(name)
    
    
    
    
    
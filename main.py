import numpy as np
import pandas as pd
import matplotlib as mpl
from pycaret.classification import *

data = pd.read_csv("ai4i2020.csv")
data.replace("?",np.nan,inplace=True)
for column in data.columns:
    try:
        data[column] = data[column].astype(float)
    except:
        pass
data.drop(['UDI', 'Product ID'],axis=1,inplace=True)
data['Machine failure']=0
data['Machine failure'][data['TWF']==1]=1
data['Machine failure'][data['HDF']==1]=2
data['Machine failure'][data['PWF']==1]=3
data['Machine failure'][data['OSF']==1]=4
data['Machine failure'][data['RNF']==1]=5
data.drop(['TWF','HDF','PWF','OSF','RNF'],axis=1,inplace=True)
data['Power'] = data['Rotational speed [rpm]'] * data['Torque [Nm]']
data['Temperature difference'] = data['Process temperature [K]'] - data['Air temperature [K]']
data = data[[
    'Machine failure',
    'Type',
    'Air temperature [K]',
    'Process temperature [K]',
    'Rotational speed [rpm]',
    'Torque [Nm]',
    'Tool wear [min]',
    'Power',
    'Temperature difference'
]]

s = setup(data, target = 'Machine failure', session_id = 42, data_split_stratify=True)
best_model = compare_models(sort = 'AUC')
save_model(best_model, "ai4i2020_pycaret_model")
calibrated_model = calibrate_model(best_model)
automl()

create_app(best_model)



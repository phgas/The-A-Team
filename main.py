import numpy as np
import pandas as pd
from pycaret.classification import *
from IPython.core.display_functions import display


def read_data(path):
    data = pd.read_csv(path)
    return data


def prepare_data(data):
    data.replace("?", np.nan, inplace=True)
    for column in data.columns:
        try:
            data[column] = data[column].astype(float)
        except:
            pass
    data.drop(['UDI', 'Product ID'], axis=1, inplace=True)
    data['Machine failure'] = 0
    data['Machine failure'][data['TWF'] == 1] = 1
    data['Machine failure'][data['HDF'] == 1] = 2
    data['Machine failure'][data['PWF'] == 1] = 3
    data['Machine failure'][data['OSF'] == 1] = 4
    data['Machine failure'][data['RNF'] == 1] = 5
    data.drop(['TWF', 'HDF', 'PWF', 'OSF', 'RNF'], axis=1, inplace=True)
    data['Power'] = data['Rotational speed [rpm]'] * data['Torque [Nm]']
    data['Temperature difference'] = data['Process temperature [K]'] - \
        data['Air temperature [K]']
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
    return data


def get_new_model(training_data):
    s = setup(training_data, target='Machine failure',
              session_id=42, data_split_stratify=True)
    best_model = compare_models(sort='AUC')
    calibrated_model = calibrate_model(model)
    automl()
    save_model(calibrated_model, "ai4i2020_pycaret_model")
    return best_model


def read_existing_model(path):
    model = load_model(path)
    return model


def get_prediction(model, unseen_data):
    prediction = predict_model(model, data=unseen_data)
    return prediction

if __name__ == "__main__":
    #training_data_raw = read_data("ai4i2020.csv")
    #training_data_prepared = prepare_data(training_data_raw)
    #model = get_new_model(training_data_prepared)

    model = read_existing_model("ai4i2020_pycaret_model")
    #create_app(model)

    unseen_data_raw = read_data("ai4i2020_test.csv")
    unseen_data_prepared = prepare_data(unseen_data_raw)
    prediction = get_prediction(model, unseen_data_prepared)
    display(prediction)

import numpy as np
import pandas as pd
from pycaret.classification import *


def read_prediction_data(path):
    data = pd.read_csv(path)

    expected_headers = [
        'UDI', 'Product ID', 'Type', 'Air temperature [K]', 'Process temperature [K]',
        'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]'
    ]

    if not all(col in data.columns for col in expected_headers):
        return False, data
    return True, data


def read_training_data(path):
    data = pd.read_csv(path)

    expected_headers = [
        'UDI', 'Product ID', 'Type', 'Air temperature [K]', 'Process temperature [K]',
        'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'Machine failure',
        'TWF', 'HDF', 'PWF', 'OSF', 'RNF'
    ]

    if not all(col in data.columns for col in expected_headers):
        return False, data
    return True, data


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


def create_new_model(training_data, model_path):
    setup_data = setup(training_data, target='Machine failure',
                       session_id=42, data_split_stratify=True)
    best_mode = compare_models(sort='AUC')
    calibrated_model_failure = calibrate_model(best_mode)
    save_model(calibrated_model_failure, model_path)
    return best_mode


def read_existing_model(path):
    model = load_model(path)
    return model


def get_prediction(model, unseen_data):
    prediction = predict_model(model, data=unseen_data, raw_score=True)
    predictions = []

    for index, row in prediction.iterrows():
        pred_dict = {
            'Type': unseen_data['Type'][index],
            'Air temperature [K]': unseen_data['Air temperature [K]'][index],
            'Process temperature [K]': unseen_data['Process temperature [K]'][index],
            'Rotational speed [rpm]': unseen_data['Rotational speed [rpm]'][index],
            'Torque [Nm]': unseen_data['Torque [Nm]'][index],
            'Tool wear [min]': unseen_data['Tool wear [min]'][index],
            'Power': f"{unseen_data['Power'][index]:.1f}",
            'Temperature difference': f"{unseen_data['Temperature difference'][index]:.1f}",
            'No_FAILURE': row['prediction_score_0'],
            'Toolwear_FAILURE': row['prediction_score_1'],
            'Heat-Dissipation_FAILURE': row['prediction_score_2'],
            'Power_FAILURE': row['prediction_score_3'],
            'Overstrain_FAILURE': row['prediction_score_4'],
            'Random_FAILURE': row['prediction_score_5']
        }
        predictions.append(pred_dict)

    return predictions


if __name__ == "__main__":

    is_valid_training_data, training_data_raw = read_training_data(
        "ai4i2020.csv")
    if is_valid_training_data:
        training_data_prepared = prepare_data(training_data_raw)
        model_failure = create_new_model(
            training_data_prepared, "ai4i2020_pycaret_model")

    is_valid_prediction_data, prediction_data_raw = read_prediction_data(
        "prediction_data.csv")
    if is_valid_prediction_data:
        prediction_data_prepared = prepare_data(prediction_data_raw)

        model = read_existing_model("ai4i2020_pycaret_model")
        prediction = get_prediction(
            model, prediction_data_prepared)

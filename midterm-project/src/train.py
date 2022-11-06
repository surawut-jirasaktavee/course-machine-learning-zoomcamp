import logging
import pandas as pd
from pathlib import Path
import pickle
import xgboost as xgb


def runcmd(cmd, verbose = False, *args, **kwargs):

    import subprocess

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


def getDataset(dataUrl: str) ->pd.DataFrame:    
        
    data_path = Path('../dataset/')
    data_path.mkdir(parents=True, exist_ok=True)
    
    
    if Path.is_file(Path('../dataset/dataset_31_credit-g.arff')):
        print('File exists')
    else:
        runcmd(f"wget {dataUrl}", verbose=True)
        runcmd("mv dataset_31_credit-g.arff ../dataset/dataset_31_credit-g.arff")
        print('Downloaded dataset successfully')        
    
    dataPath = f'{data_path}/dataset_31_credit-g.arff'
    
    logging.info('Get dataset')
    print("Get Dataset is complete...")
    
    return dataPath
    
def getDataFrame(dataPath: str) ->pd.DataFrame:
     
    from scipy.io import arff 
     
    data = arff.loadarff(dataPath)
    df_data = pd.DataFrame(data[0])
    df_col = pd.DataFrame(data[1])
    
    logging.info('Get dataframe')
    print("Get DataFrame is complete...")
        
    return df_data, df_col

def getColumnName(df_cols: pd.DataFrame) ->list():

    col_name = list()

    for col in df_col[0]:
        col_name.append(col)
    
    logging.info('Get column name from dataframe')
    print("Get all column name is complete...")    
        
    return col_name

def cleanString(df_data: pd.DataFrame, col_name: list(), numeric_cols: list()) ->pd.DataFrame:
    
    for col in col_name:
        if col not in numeric_cols:
            df_data[col] = df_data[col].apply(lambda x: str(x).replace("b", ''))
            df_data[col] = df_data[col].apply(lambda x: str(x).replace("'", ''))
            df_data[col] = df_data[col].apply(lambda x: str(x).replace(" ", "_"))    
     
    logging.info('Cleaning data with string values') 
    print("Cleansing String values is complete...")        
                    
    return df_data

def cleanClass(df_data: pd.DataFrame, col_target: str) -> pd.DataFrame:
    
    df_data[col_target] = df_data[col_target].apply(lambda x: 'good' if x == 'good' else 'bad')
    
    logging.info('Clean target column')
    print("Cleansing target column is complete...")
    
    return df_data

def prepareData(df: pd.DataFrame) ->pd.DataFrame:
    
    status_values = {
        'good': 'ok',
        'bad': 'default'
    }

    df['class'] = df['class'].map(status_values)

    # modify values in own_telephone column
    own_telephone_values = {
        'yes': 'yes',
        'none': 'no'
    }

    df.own_telephone = df.own_telephone.map(own_telephone_values)

    # modify values in other_payment_plans column
    payment_values = {
        'none': 'no',
        'ank': 'ank',
        'stores': 'stores'
    }

    df.other_payment_plans = df.other_payment_plans.map(payment_values)


    # modify values in property_values column
    property_values = {
        'no_known_property': 'unknown',
        'life_insurance': 'life_insurance',
        'real_estate': 'real_estate',
        'car': 'car'
    }

    df.property_magnitude = df.property_magnitude.map(property_values)

    # modify values in other_parties_values column
    other_parties_values = {
        'none': 'no',
        'guarantor': 'guarantor',
        'co_applicant': 'co_applicant'
    }

    df.other_parties = df.other_parties.map(other_parties_values)

    saving_status_values = {
        'no_known_savings': 'unknown',
        '<100': '<100',
        '100<=X<500': '100<=X<500',
        '500<=X<1000': '500<=X<1000',
        '>=1000': '>=1000'
        
    }

    df.savings_status = df.savings_status.map(saving_status_values)

    # split personal_status column into sex and personal_status columns
    sex = df.personal_status.apply(lambda x: x.split("_")[0])
    df.insert(9, 'sex', sex)
    df.personal_status = df.personal_status.apply(lambda x: x.split("_")[1])
    df = df.rename(columns={"class": "status"})
    
    logging.info('Preparing data')
    print("Preparing Data already complete...")
    
    return df

def splitDataset(df: pd.DataFrame, test_size: float, 
                 random_state: int, enable_shuffle: bool) ->pd.DataFrame:
    
    from sklearn.model_selection import train_test_split
    
    df_train, df_val = train_test_split(df, test_size=test_size, random_state=random_state, shuffle=enable_shuffle)
    
    logging.info('Spliting dataset')
    print("Spliting Dataset is complete...")
    
    return df_train, df_val

def getTrainingDataset(df_train: pd.DataFrame, df_val: pd.DataFrame):
    
    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)

    y_train = (df_train["status"] == 'default').astype('int').values
    y_val = (df_val["status"] == 'default').astype('int').values

    del df_train["status"]
    del df_val["status"]
    
    
    logging.info('Get training dataset')
    print("Training dataset is ready...")
    
    return df_train, df_val, y_train, y_val


def prepareFeatures(df_train: pd.DataFrame, df_val: pd.DataFrame):
    
    from sklearn.feature_extraction import DictVectorizer
   
    train_dict = df_train.to_dict(orient='records')
    val_dict = df_val.to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(train_dict)
    X_val = dv.transform(val_dict)
   
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    
    
    logging.info('Preparing features')
    print("Features preparing is complete...")
    
    return dtrain, dval, dv


def model_training(dtrain, params: dict, num_boost_round):
    
    model = xgb.train(params, dtrain, num_boost_round=num_boost_round)
   
    logging.info('Start model training')
    print("The model training session is successfully...")
    
    return model


def model_prediction(model, dval):
    
    y_pred = model.predict(dval)
    
    logging.info('Get prediction')
    print("Get model prediction...")
    
    return y_pred


def model_evaluation(y_val, y_pred):
    
    from sklearn.metrics import roc_auc_score

    score = roc_auc_score(y_val, y_pred)
    
    logging.info('Evaluate model...')
    print(f"Get ROC_AUC_SCORE of model: {score}")
    
    return score
    
  
def saveModel(model_name: str, enableBatch: None, model, dv):
    
    import bentoml
    
    if enableBatch:
        bentoml.xgboost.save_model(model_name, model,
                                   custom_objects={
                                       'dictVectorizer': dv
                                   },
                                   signatures={
                                       "predict": {
                                           "batchable": True,
                                           "batch_dim": 0
                                       }
                                   })
    else:
        bentoml.xgboost.save_model(model_name, model,
                               custom_objects={
                                   'dictVectorizer': dv
                               })
    
    logging.info('Saved model')
    
    print("Save model successfully...")

############################################################################################################
######################################## PARAMETERS ########################################################
############################################################################################################
n_splits = 5
# dataPath = '../dataset/dataset_31_credit-g.arff'
dataUrl = 'https://www.openml.org/data/download/31/dataset_31_credit-g.arff'

categorical_cols = ['checking_status', 'credit_history', 'purpose', 'savings_status', 'employment', 
                    'personal_status', 'other_parties', 'property_magnitude', 'other_payment_plans', 
                    'housing', 'job', 'own_telephone', 'foreign_worker']
numeric_cols = ['duration', 'credit_amount', 'installment_commitment', 'residence_since', 'age', 
                'existing_credits', 'num_dependents']
target_col = 'class'
enable_shuffle = True
test_size = 0.2
val_size = 0.25
random_state = 42

params = {
    'eta': 0.08,
    'max_depth': 8,
    'min_child_weight': 8,
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'nthread': 8,
    'seed': 42,
    'verbosity': 1,
}

num_boost_round = 200

############################################################################################################
######################################## PARAMETERS ########################################################
############################################################################################################


if __name__ == "__main__":
    
    dataPath = getDataset(dataUrl)
    df_data, df_col = getDataFrame(dataPath)
    col_name = getColumnName(df_col)
    df = cleanString(df_data, col_name, numeric_cols)
    df = cleanClass(df, target_col)
    df = prepareData(df)
    df_train, df_val = splitDataset(df, test_size, enable_shuffle, random_state)
    df_train, df_val, y_train, y_val = getTrainingDataset(df_train, df_val)
    dtrain, dval, dv = prepareFeatures(df_train, df_val)

    print("Start training session...")
    model = model_training(dtrain, params, num_boost_round)
    y_pred = model_prediction(model, dval)
    score = model_evaluation(y_val, y_pred)

    model_name = 'credit_risk_model'
    enableBatch = True
    saveModel(model_name, enableBatch, model, dv)

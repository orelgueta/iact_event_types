import argparse
from pathlib import Path
import event_classes

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=(
            'Train event classes models.'
            'Results are saved in the models directory.'
        )
    )

    args = parser.parse_args()

    # dl2_file_name = '/lustre/fs21/group/cta/users/maierg/analysis/AnalysisData/uploadDL2/Paranal_20deg/gamma_cone.S.3HB9-FD_ID0.eff-0.root'
    dl2_file_name = '/lustre/fs21/group/cta/users/maierg/analysis/AnalysisData/uploadDL2/Paranal_20deg/gamma_onSource.S.3HB9-FD_ID0.eff-0.root'
    dtf = event_classes.extract_df_from_dl2(dl2_file_name)
    dtf_e = event_classes.bin_data_in_energy(dtf)

    dtf_e_train, dtf_e_test = event_classes.split_data_train_test(dtf_e)

    labels, train_features = event_classes.nominal_labels_train_features()

    all_models = event_classes.define_regressors()
    models_to_train = {
        # 'linear_regression': all_models['linear_regression'],
        # 'random_forest': all_models['random_forest'], # Do not use, performs bad and takes lots of disk space
        # 'MLP': all_models['MLP'],
        # 'MLP_relu': all_models['MLP_relu'],
        # 'MLP_logistic': all_models['MLP_logistic'],
        # 'MLP_uniform': all_models['MLP_uniform'],
        # 'MLP_small': all_models['MLP_small'],
        # 'MLP_lbfgs': all_models['MLP_lbfgs'],
        # 'BDT': all_models['BDT'], # Do not use, performs bad and takes lots of disk space
        # 'ridge': all_models['ridge'],
        # 'SVR': all_models['SVR'], # Do not use, performs bad and takes forever to apply
        # 'linear_SVR': all_models['linear_SVR'],
        # 'SGD': all_models['SGD'],
    }

    for this_model in models_to_train.values():
        this_model['train_features'] = train_features
        this_model['labels'] = labels

    trained_models = event_classes.train_models(
        dtf_e_train,
        models_to_train
    )
    event_classes.save_models(trained_models)
    event_classes.save_test_dtf(dtf_e_test)

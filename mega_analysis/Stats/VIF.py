# Multicollinearity solution using VIF  26/6/19

def calculate_vif_(X, thresh=5.0):
    """
    Linear variational inflation factor for multi-colinearity solutions
    Removes colinear features with messages

    X is patients by features DataFrame
    Good idea to inspect the VIFs for all data and consider threshold changes?

    Returns remaining X without the omitted features and list of VIFs
    """

    features = list(range(X.shape[1]))
    dropped = True
    while dropped:
        dropped = False
        vif = [variance_inflation_factor(X.iloc[:, features].values, ix)
               for ix in range(X.iloc[:, features].shape[1])]

        maxloc = vif.index(max(vif))
        if max(vif) > thresh:
            print('dropping \'' + X.iloc[:, features].columns[maxloc] +
                  '\' at index: ' + str(maxloc))
            print('VIF = ', vif[maxloc])
            print('\n\n all VIFs = ', vif)
            del features[maxloc]
            dropped = True

    print('Remaining features:')
    print(X.columns[features])
    return X.iloc[:, features], vif
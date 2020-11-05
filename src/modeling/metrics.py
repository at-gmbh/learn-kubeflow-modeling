from sklearn.metrics import f1_score, roc_auc_score, average_precision_score

def average_precision(targets, predictions) -> float:
    return average_precision_score(
        y_true=targets.astype("float"),
        y_score=predictions.astype("float"),
        average="macro",
    ).item()


def auc(targets, predictions) -> float:
    return roc_auc_score(
        y_true=targets.astype("float"),
        y_score=predictions.astype("float"),
        average="macro",
    ).item()


def weighted_f1(targets, predictions) -> float:
    return f1_score(
        y_true=targets.astype("float").argmax(axis=1),
        y_pred=predictions.astype("float").argmax(axis=1),
        average='weighted',
    ).item()


def macro_f1(targets, predictions) -> float:

    return f1_score(
        y_true=targets.astype("float").argmax(axis=1),
        y_pred=predictions.astype("float").argmax(axis=1),
        average='macro',
    ).item()


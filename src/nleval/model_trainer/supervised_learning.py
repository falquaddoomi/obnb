from nleval.model_trainer.base import BaseTrainer
from nleval.typing import Any, Dict, LogLevel, Optional


class SupervisedLearningTrainer(BaseTrainer):
    """Trainer for supervised learning model.

    Example:
        Given a dictionary ``metrics`` of metric functions, and a ``features``
        that contains the features for each data point, we can train a
        logistic regression model as follows.

        >>> from sklearn.linear_model import LogisticRegression
        >>> trainer = SupervisedLearningTrainer(metrics, features)
        >>> results = trainer.train(LogisticRegression(), y, masks)

        See the ``split`` method in ``label.collection.LabelsetCollection`` for
        generating ``y`` and ``masks``.

    """

    def __init__(
        self,
        metrics,
        train_on="train",
        log_level: LogLevel = "WARNING",
    ):
        """Initialize SupervisedLearningTrainer.

        Note:
            Only takes features as input. However, one could pass the graph
            object as features to use the rows of the adjaceny matrix as the
            node features.

        """
        super().__init__(
            metrics,
            train_on=train_on,
            log_level=log_level,
        )

    def train(
        self,
        model: Any,
        dataset,
        split_idx: int = 0,
    ) -> Dict[str, float]:
        """Train a supervised learning model.

        The ``model`` in this case is a  upervised learning model that has a
        ``fit`` method for training the model, and a ``decision_function`` that
        returns the predict confidence scores given some features. See
        ``sklearn.linear_model.LogisticRegression`` for example.

        """
        # TODO: log time and other useful stats (maybe use the decorator?)
        model.fit(*dataset.get_split(self.train_on, split_idx))

        # Evaluate the trained model using the specified metrics
        results = {}
        for metric_name, metric_func in self.metrics.items():
            for mask_name, (x, y) in dataset.splits(split_idx):
                y_pred = model.decision_function(x)
                score = metric_func(y, y_pred)
                results[f"{mask_name}_{metric_name}"] = score

        return results


class MultiSupervisedLearningTrainer(SupervisedLearningTrainer):
    """Supervised learning model trainer with multiple feature sets.

    Used primarily for auto hyperparameter selection.

    """

    def __init__(
        self,
        metrics,
        train_on="train",
        val_on: str = "val",
        metric_best: Optional[str] = None,
        log_level: LogLevel = "WARNING",
    ):
        """Initialize MultiSupervisedLearningTrainer."""
        super().__init__(
            metrics,
            train_on=train_on,
            log_level=log_level,
        )

        self.val_on = val_on
        if metric_best is None:
            self.metric_best = list(metrics)[0]
        else:
            self.metric_best = metric_best

    def train(self, model, dataset, y, masks, split_idx=0):
        """Train a supervised learning mode and select based on validation."""
        best_results = None
        best_val_score = 0
        val_mask_name = f"{self.val_on}_{self.metric_best}"

        val_scores = []
        for fset_name in dataset.feature.fset_idmap.lst:
            self._curr_fset_name = fset_name
            results = super().train(model, y, masks, split_idx)
            val_score = results[val_mask_name]
            val_scores.append(val_score)

            if val_score > best_val_score:
                best_results = results
                best_val_score = val_score
                best_fset_name = self._curr_fset_name

        score_str = ", ".join([f"{i:.3f}" for i in val_scores])
        self.logger.info(
            f"Best val score: {best_val_score:.3f} (via {best_fset_name}) "
            f"Other val scores: [{score_str}]",
        )

        return best_results
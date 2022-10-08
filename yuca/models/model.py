from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from typing import Any

from yuca.dataset import Dataset, DatasetSlice
from yuca.models.evaluation import Evaluation


def _mark_trained(func):
    def wrapper(self: Model, *args, **kwargs):
        logging.info("Training %s model", self.name)
        val = func(self, *args, **kwargs)
        self.trained = True
        return val

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


class Model(ABC):

    """Abstract class for models."""

    def __init__(self, name: str):
        self.name = name
        self.summary = {"name": self.name}
        self.trained = False

    @abstractmethod
    @_mark_trained
    def train(self, data: Dataset | DatasetSlice, cross_validation: int = 0):
        """Train the model using a given dataset"""

    @abstractmethod
    def predict(self, data: Dataset | DatasetSlice) -> list[Any]:
        """Predict the labels of a given set of trajectories"""

    def save(self, path: str):
        """Save the model to a given path"""
        raise NotImplementedError

    def _predict(self, data: Dataset | DatasetSlice) -> list[Any]:
        # TODO: check mark trained decorator
        # if not self.trained:
        #     raise Exception("Model is not trained yet.")

        return self.predict(data)

    def evaluate(self, data: Dataset | DatasetSlice) -> Evaluation:
        """Evaluate the trained model"""

        logging.info("Evaluating the %s model", self.name)
        predictions = self._predict(data)
        return Evaluation(self.summary, data, predictions)

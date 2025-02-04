"""Module for housing postprocessing operations."""

from datetime import datetime

from monty.json import MSONable


class Operator(MSONable):
    """Base operator class. Tracks everything required through a combination
    of the MSONable base class and by using an additional datetime key to track
    when the operator was logged into the metadata of a new node.

    .. important::

        The __call__ method must be derived for every operator. In particular,
        this operator should take as arguments at least one other data point
        (node).
    """

    def as_dict(self):
        d = super().as_dict()
        d["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return d

    @classmethod
    def from_dict(cls, d):
        if "datetime" in d.keys():
            d.pop("datetime")
        return super().from_dict(d)

    def __call__(self):
        raise NotImplementedError


class Identity(Operator):
    """The identity operation. Does nothing. Used for testing purposes."""

    def __call__(self, x):
        """
        Parameters
        ----------
        x : tiled.client.dataframe.DataFrameClient
        """

        # Note this will throw a TypeError, as setting attributes is not
        # allowed!
        x.metadata["derived"] = {**self.as_dict(), "parents": [x.uri]}

        return x

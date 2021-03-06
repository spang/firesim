import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


class FixtureInfoListModel(QtCore.QAbstractListModel):
    COLUMNS = ('key','value',)

    def __init__(self, data):
        QtCore.QAbstractListModel.__init__(self)
        self._data = data
        self.setRoleNames(dict(enumerate(FixtureInfoListModel.COLUMNS)))

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        if index.isValid() and role == FixtureInfoListModel.COLUMNS.index('key'):
            return self._data[index.row()]
        return None
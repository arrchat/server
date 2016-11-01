from Contact import Contact
from copy import copy

__author__ = 'JuniorJPDJ'

class GroupContact(Contact):
    def update_group_memberlist(self):
        self._memberlist = []
        return True

    @property
    def memberlist(self):
        if self.update_group_memberlist():
            return copy(self._memberlist)
        return False

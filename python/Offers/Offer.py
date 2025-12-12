from abc import abstractmethod


class Offer:
    @abstractmethod
    def get_message(self):
        pass

class range:
    def __init__(self, begin, end):
        if begin > end:
            raise ValueError('The begin range value cannot be greater than the end range value.')
        self.begin = begin
        self.end = end

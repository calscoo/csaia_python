class range:

    def __init__(self, begin, end):
        if begin is None or end is None:
            raise ValueError('begin or end cannot be None')
        self.check_range(begin, end)
        self._set_begin(begin)
        self._set_end(end)

    def _get_begin(self):
        return self.begin

    def _set_begin(self, begin):
        if begin is None:
            raise ValueError('begin cannot be None')
        end = None
        try:
            end = self._get_end()
        except: AttributeError
        self.check_range(begin, end)
        self.begin = begin

    def _get_end(self):
        return self.end

    def _set_end(self, end):
        if end is None:
            raise ValueError('end cannot be None')
        begin = None
        try:
            begin = self._get_begin()
        except: AttributeError
        self.check_range(begin, end)
        self.end = end

    @staticmethod
    def check_range(begin, end):
        if begin is not None and end is not None and begin > end:
            raise ValueError('The begin range value cannot be greater than the end range value.')

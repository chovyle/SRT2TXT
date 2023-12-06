from pathlib import PurePath

class SRT_Line:
    def __init__(self):
        self._order = 0
        self._sTime = ''
        self._eTime = ''
        self._text = ''

    def __repr__(self):
        return f'Line {self.order} : "{self.text}"'

    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, file):
        self._file = file

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        try:
            self._order = int(order)
        except ValueError:
            self._order = int(order.encode('ascii', 'ignore').decode())

    @property
    def sTime(self):
        return self._sTime

    @sTime.setter
    def sTime(self, sTime):
        self._sTime = sTime

    @property
    def eTime(self):
        return self._eTime

    @eTime.setter
    def eTime(self, eTime):
        self._eTime = eTime

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, text):
        self._text = text

    def get_timestamp(self, timestamp):
        self.sTime, self.eTime = timestamp.split(' --> ')

    def get_text_list(self, text_list):
        self.text = ' '.join([text.strip() for text in text_list])

    def properties(self):
        return (self.order, self.sTime, self.eTime, self.text)
        
class SRT_List(list):

    def __init__(self):
        super().__init__()
        self._name = ''

    def merge_text(self):
        return ' '.join([line.text for line in self])
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        try:
            self._name = PurePath(name).stem
        except TypeError:
            self._name = name.name
    
    def read_srt(self, src):
        self.name = src
        with open(src, 'r', encoding='utf-8') as file:
            BUFFER = list()
            for line in file.read().split('\n'):
                BUFFER.append(line)
                if line.strip() == '':
                    SRT_INFO = SRT_Line()
                    SRT_INFO.order = BUFFER[0]
                    SRT_INFO.get_timestamp(BUFFER[1])
                    SRT_INFO.get_text_list(BUFFER[2:])
                    self.append(SRT_INFO)
                    BUFFER.clear()

    def read_srt_streamlit(self, src):
        self.name = src
        BUFFER = list()
        for line in src.readlines():

            line = line.decode()
            if line.strip() == '':
                SRT_INFO = SRT_Line()
                SRT_INFO.order = BUFFER[0]
                SRT_INFO.get_timestamp(BUFFER[1])
                SRT_INFO.get_text_list(BUFFER[2:])
                self.append(SRT_INFO)
                BUFFER.clear()
            else:
                BUFFER.append(line.strip())

    
    def export_streamlit(self):
        return f'{PurePath(self.name).stem}\n{self.merge_text()}'

    def export(self):
        with open(f'{self._name}.txt', 'w', encoding='utf-8') as file:
            file.write(f'{self.name}\n{self.merge_text()}')
    
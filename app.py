import streamlit as st

st.set_page_config(page_title='SRT2TXT',
                   page_icon=':train:')

from SRT2TXT import *
from io import BytesIO

class App:
    def __init__(self):
        if 'files' not in st.session_state:
            st.session_state.files = []
        if 'text' not in st.session_state:
            st.session_state.text = []

    def main(self):


        TITLE = st.title('SRT2TXT')

        st.session_state.files = st.file_uploader(label='SRT 파일을 업로드하세요.',
                                                  type='.srt',
                                                  accept_multiple_files=True,
                                                  on_change=self.load_files())
        
        REFRESH = st.button(label="새로고침")

        SHOW_TEXT = st.text_area(label='출력 텍스트 (CTRL + A로 전체 선택 후 복사하여 사용하세요.)', 
                                 value=self.output(),
                                 height=500)
    
    def output(self):
        if len(st.session_state.text) > 0:
            return '\n\n'.join(st.session_state.text)
        else:
            return ''

    def load_files(self):
        st.session_state.text = [self.read_file(file) 
                                 for file in st.session_state.files]

    def read_file(self, file):
        SRT = SRT_List()
        SRT.read_srt_streamlit(file)
        return SRT.export_streamlit()
            
if __name__ == "__main__":
    app = App()
    app.main()
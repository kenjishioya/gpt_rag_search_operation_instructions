from pathlib import Path
import streamlit as st
from st_aggrid import AgGrid

import pandas as pd

from services.chat_bot import create_vector

def show_layout():
    st.title('登録')
    st.write('---')
    if st.session_state['regist_screen_mode'] == 'list':
        _show_list()
    else:
        _show_regist()


def _toggle_screen_mode():
    sm = 'regist' if st.session_state['regist_screen_mode'] == 'list' else 'list'
    st.session_state['regist_screen_mode'] = sm
    st.rerun()

def _show_list():
    if st.button('登録'):
        _toggle_screen_mode()
    AgGrid(st.session_state['oi_list'])

def _show_regist():
    st.text_input('名前', key='name')
    st.text_input('型番', key='model_number')
    st.file_uploader('取扱説明書', key='file')
    col1, col2 = st.columns(2)
    with col1:
        is_valid = _validate_input()
        submit = st.button('確定', disabled=not is_valid)
        if submit:
            _regist()
    with col2:
        if st.button('キャンセル'):
            _toggle_screen_mode()

def _validate_input():
    # 名前がからでない
    if st.session_state['name'] is None or st.session_state['name'].strip() == '':
        return False
    # 型番がからでない
    if st.session_state['model_number'] is None or st.session_state['model_number'].strip() == '':
        return False
    # ファイル
    if st.session_state['file'] is None:
        return False
    file_name = st.session_state['file'].name.split('.')
    extention = file_name[-1]
    if extention not in ['pdf', 'PDF']:
        return False
    return True

def _regist():
    if st.session_state['file'] is not None:
        name = st.session_state['file'].name
        byte = st.session_state['file'].getvalue()
        with open(f'./assets/{name}', mode='wb') as f:
            f.write(byte)
        new_row = {'name': st.session_state['name'], 'model_number': st.session_state['model_number'], 'file_name': name}
        _df = pd.DataFrame([new_row])
        _df = pd.concat([st.session_state['oi_list'],_df], ignore_index=True)

        _df.to_json('./assets/operation_instructions.json', orient='records')

        create_vector(name)

        _toggle_screen_mode()
        st.rerun()

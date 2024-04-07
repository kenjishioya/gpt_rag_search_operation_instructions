import streamlit as st
from services.chat_bot import init_gpt, search

def show_layout():
    st.title('チャット')
    st.selectbox(
        '取扱説明書',
        options=st.session_state['oi_list'].to_dict(orient='records'),
        format_func=lambda x: x['name'],
        key='chat_oi',
        index=None
    )
    if 'chat_oi' not in st.session_state or st.session_state['chat_oi'] is None:
        st.info('取扱説明書を選択してください。')
    else:
        _show_chat()


def _show_chat():
    file_name = st.session_state['chat_oi']['file_name']
    if file_name not in st.session_state['conversation_list']:
        st.session_state['conversation_list'][file_name] = []
    retrieval_chain = init_gpt(file_name)
    prompt = st.chat_input('質問してください。')
    if prompt:
        answer = search(prompt, retrieval_chain)
        conversation = dict(question=prompt, answer=answer)
        st.session_state['conversation_list'][file_name].append(conversation)
        for c in st.session_state['conversation_list'][file_name]:
            with st.chat_message("user"):
                st.write(c['question'])
            with st.chat_message("AI"):
                st.write(c['answer'])
        

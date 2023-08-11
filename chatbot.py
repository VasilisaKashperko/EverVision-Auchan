import openai
import streamlit as st
from search import langchain_load_db, langchain_find_docs, \
    langchain_parse_docs


CONFIG = {
    'gpt_model': 'gpt-3.5-turbo',
    'bot_name': 'Чат-бот АШАН',
    'placeholder_msg': 'Чем я могу помочь?',
    'add_context_every_n': 20,
    'user_avatar': '🍀',
    'assistant_avatar': './images/favicon.ico',
    'help_context': './docs/help.txt',
    'logo': './images/auchan-logo.png',
    'page_icon': './images/favicon.ico'
}

st.set_page_config(
    page_title=CONFIG['bot_name'],
    page_icon=CONFIG['page_icon'],
)

with open(CONFIG['help_context']) as f:
    help_lines = f.readlines()
    HELP_CONTEXT = ''.join(help_lines)


def add_context(prompt, context, start=True):
    if start:
        prompt = context + prompt
    else:
        prompt = prompt + context
    return prompt


def main():
    # chatbot name, appear at the top of page
    st.image(CONFIG['logo'], caption=CONFIG['bot_name'], width=200)

    # add openai api key from secrets
    openai.api_key = st.secrets['OPENAI_API_KEY']

    # load vectorized documents
    vector_db = langchain_load_db()

    # choose openai model
    model_key = 'openai_model'
    if model_key not in st.session_state:
        st.session_state[model_key] = CONFIG['gpt_model']

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message['role'] == 'user':
            avatar = CONFIG['user_avatar']
        elif message['role'] == 'assistant':
            avatar = CONFIG['assistant_avatar']
        with st.chat_message(message['role'], avatar=avatar):
            st.markdown(message['show_content'])

    # phrase locates in the user input placeholder at each query
    if show_prompt := st.chat_input(CONFIG['placeholder_msg']):
        # show message on screen
        with st.chat_message('user', avatar=CONFIG['user_avatar']):
            st.markdown(show_prompt)

        # find documents using prompt
        docs = langchain_find_docs(vector_db, show_prompt)

        # parse docs into singe context line
        context_str = langchain_parse_docs(docs)

        # add context
        prompt = add_context(
            show_prompt,
            HELP_CONTEXT + context_str,
            start=True
        )

        # append message from the user in a session state
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
            'show_content': show_prompt
        })

        with st.chat_message('assistant', avatar=CONFIG['assistant_avatar']):
            message_placeholder = st.empty()
            full_response = ''

            gpt_chars = 0
            messages_gpt = []
            for m in st.session_state.messages[::-1]:
                gpt_chars += len(m['content'])

                if gpt_chars > 4000:
                    break

                messages_gpt += [m]

            messages_gpt = messages_gpt[::-1]

            # messages - list of history, role - user or assistant
            responses = openai.ChatCompletion.create(
                model=st.session_state[model_key],
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in messages_gpt
                ],
                stream=True,
            )

            # iterate over each response
            for response in responses:
                # response parts
                full_response += response.choices[0].delta.get('content', '')

                # words appear continiously
                message_placeholder.markdown(full_response + '▌')

            # show full response
            message_placeholder.markdown(full_response)

        # append messages to history
        st.session_state.messages.append(
            {
                'role': 'assistant',
                'content': full_response,
                'show_content': full_response
            }
        )


if __name__ == '__main__':
    main()

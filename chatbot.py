import openai
import streamlit as st


st.set_page_config(
    page_title="Чат-бот АШАН",
    page_icon="./images/favicon.ico",
)


CONFIG = {
    'gpt_model': 'gpt-3.5-turbo',
    'bot_name': 'Чат-бот АШАН',
    'placeholder_msg': 'Чем я могу помочь?',
    'add_context_every_n': 20,
    'user_avatar': '🍀',
    'assistant_avatar': './images/favicon.ico'
}

HELP_CONTEXT = 'Ты - консультант магазина АШАН. Если тебе написали "здравствуйте", ответь так же.\n'
HELP_CONTEXT += 'Если разговор приобрел тему политики, отвечай вежливым отказом.\n'
HELP_CONTEXT += 'Используй "Ассортимент магазина АШАН:" для ответа на вопросы.\n'
HELP_CONTEXT += '"Ассортимент АШАН":\n'
HELP_CONTEXT += '- молоко "Буренка" - 100 рублей, 1 литр.\n'
HELP_CONTEXT += '- молоко "Простаквашино" - 200 рублей, 1.5 литра.\n'
HELP_CONTEXT += '- сыр "Пармезан" - 150 рублей, 200 грамм.\n'


def add_context(prompt, context, start=True):
    if start:
        prompt = context + prompt
    else:
        prompt = prompt + context
    return prompt


def main():
    # chatbot name, appear at the top of page
    # st.title(CONFIG['bot_name'])
    st.image('./images/auchan-logo.png', caption='Чат-бот АШАН', width=200)

    # add openai api key from secrets
    openai.api_key = st.secrets['OPENAI_API_KEY']

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

        # help with products
        if len(st.session_state.messages) % CONFIG['add_context_every_n'] == 0:
            prompt = add_context(show_prompt, HELP_CONTEXT, start=True)
        else:
            prompt = show_prompt

        # append message from the user in a session state
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
            'show_content': show_prompt
        })

        with st.chat_message('assistant', avatar=CONFIG['assistant_avatar']):
            message_placeholder = st.empty()
            full_response = ''

            # messages - list of history, role - user or assistant
            responses = openai.ChatCompletion.create(
                model=st.session_state[model_key],
                messages=[
                    {'role': m['role'], 'content': m['content']}
                    for m in st.session_state.messages
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

import openai
import streamlit as st


CONFIG = {
    'gpt_model': 'gpt-3.5-turbo',
    'bot_name': 'Ашанчик',
    'placeholder_msg': 'Чем могу помочь?',
}


def main():
    # chatbot name, appear at the top of page
    st.title(CONFIG['bot_name'])

    # add openai api key from secrets
    openai.api_key = st.secrets['OPENAI_API_KEY']

    # choose openai model
    model_key = 'openai_model'
    if model_key not in st.session_state:
        st.session_state[model_key] = CONFIG['gpt_model']

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # phrase locates in the user input placeholder at each query
    if prompt := st.chat_input(CONFIG['placeholder_msg']):
        # append message from the user in a session state
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        # show message on screen
        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
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
                'content': full_response
            }
        )


if __name__ == '__main__':
    main()

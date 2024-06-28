import pytest
from unittest.mock import MagicMock, patch
from chatbot import generate_response, main

# Mocking Streamlit components
@patch('chatbot.st.chat_message')
@patch('chatbot.st.chat_input')
@patch('chatbot.st.spinner')
@patch('chatbot.st.write')
@patch('chatbot.st.session_state', new_callable=MagicMock)
@patch('chatbot.st.sidebar')
@patch('chatbot.st.title')
@patch('chatbot.st.text_input')
@patch('chatbot.st.warning')
@patch('chatbot.st.success')
@patch('chatbot.Login')
@patch('chatbot.hugchat.ChatBot')
def test_generate_response(mock_chatbot, mock_login, mock_success, mock_warning, mock_text_input, mock_title, mock_sidebar, mock_session_state, mock_write, mock_spinner, mock_chat_input, mock_chat_message):
    # Mocking session state
    mock_session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Setting up mock objects
    mock_login_instance = MagicMock()
    mock_chatbot_instance = MagicMock()

    mock_login.return_value = mock_login_instance
    mock_login_instance.login.return_value.get_dict.return_value = {'fake': 'cookies'}

    mock_chatbot.return_value = mock_chatbot_instance
    mock_chatbot_instance.chat.return_value = "Mocked response"

    # Test case: valid credentials
    prompt_input = "Hello!"
    email = "test@example.com"
    passwd = "password"

    # Test case: missing email
    response = generate_response(prompt_input, "", passwd)
    assert response[0:5] == "Error"

    # Test case: missing password
    response = generate_response(prompt_input, email, "")
    assert response[0:5] == "Error"

    main()

    # Verify if the prompt was added correctly
    assert mock_session_state.messages[-2]["role"] == "user"
    assert mock_session_state.messages[-1]["role"] == "assistant"

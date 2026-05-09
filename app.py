import streamlit as st
from apis import note_generator, create_audio, create_quiz
from PIL import Image
from gtts import gTTS
import io

# title
st.title('Note summarizer and Quiz Generator')
st.markdown('Upload upto 3 images to generate no summary and quizzes')
st.divider()

with st.sidebar:
    st.header('Controls')
    images = st.file_uploader(
        "Upload the photos of your notes",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True
    )

    if images:
        if (len(images) > 3):
            st.error('Upload 3 images max.')
        else:
            st.subheader('Your uploaded images')
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img)
    
    # difficulty
    selected_option = st.selectbox(
        'Enter the difficulty of your quiz',
        ('Easy', 'Medium', 'Hard'),
        index=None
    )


    # button
    pressed = st.button(
        'Click the button to initiate AI',
        type='primary'
        )


if pressed:
    if not images:
        st.error('You must upload at least 1 image')
    if not selected_option:
        st.error('You must select a difficulty')
    
    if images and selected_option:

        pil_images = []
        for img in images:
            pil_images.append(Image.open(img))
        
        # your notes
        with st.container(border=True):
            st.subheader('Your notes')
            with st.spinner('AI is generating a response for you..'):
                generated_notes = note_generator(pil_images)
                st.markdown(generated_notes)


        # audio transcript
        with st.container(border=True):
            st.subheader('Audio transcript')
            with st.spinner('Audio is being produced..'):
                    generated_audio = create_audio(generated_notes)
                    st.audio(generated_audio)
        
        # quiz
        with st.container(border=True):
            st.subheader(f"Quiz, difficulty level - {selected_option}")
            with st.spinner('AI is creating quiz for you..'):
                generated_quiz = create_quiz(pil_images, selected_option)
                st.markdown(generated_quiz)

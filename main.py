import os

from dotenv import load_dotenv
import streamlit as st

from api_utils import BuildBook
from deep_lake_utils import SaveToDeepLake
from pdf_gen_utils import build_pdf

STYLES = {
            'Impressionism': 'Monet, impressionist art style, loose brushstrokes, vibrant colors, painted, painted light',
            'Cubism': 'Cubist art style, Picasso, fragmented forms, geometric shapes, angular lines, limited color palette, artistic',
            'Surrealism': 'Surrealist art style, dreamlike, abstract art, dream-like artwork, Salvador Dalí, art',
            'Japanese Ukiyo-e': 'Ukiyo-e art style, Hokusai, woodblock prints, flat areas of color, outlines, nature, Japanese culture',
            'Art Nouveau': 'Art Nouveau style, Mucha, curving lines, natural forms, ornamental, elegant, stylized',
            'Folk Art': 'Folk art style, naive art, simple shapes, bright colors, childlike, intuitive, traditional',
            'Expressionism': 'Expressionist art style, Edvard Munch, distorted forms, dramatic colors, emotional impact, subjective'
          }

load_dotenv('keys.env')
dataset_path = os.getenv('DATASET_PATH')


def main():
    st.title("Hamzah's Story Book Generator")
    user_input = st.text_input("Enter a prompt and Hamzah's AI will generate a picture book ... just for you!", max_chars=70)
    style = st.selectbox("Pick a style, any style!", [key for key in STYLES.keys()])
    model = st.radio("Which OpenAI model would you prefer?", ['gpt-3.5-turbo-0613', 'gpt-4-0613'])
    deep_lake = st.checkbox("Save to Deep Lake?")
    if 'not_saving' not in st.session_state:
        st.session_state['not_saving'] = True
    if st.button('Generate!') and user_input and st.session_state['not_saving']:
        with st.spinner('Hamzah The Genuis is at work on your book...'):
            build_book = BuildBook(model, user_input, f'{STYLES[style]}')
            pages = build_book.list_of_tuples
            finished_pdf = build_pdf(pages, 'result.pdf')
            file_bytes = open(finished_pdf, 'rb').read()
            st.download_button(label='Download Book', data=file_bytes, file_name='picture_book.pdf',
                               key='download_button')
            st.write('Hamzahs AI has written your book! Click the download button to download it!')
        if deep_lake and st.session_state['not_saving']:
            st.session_state['not_saving'] = False
            with st.spinner('Saving to DeepLake...'):
                try:
                    SaveToDeepLake(build_book, dataset_path=dataset_path).fill_dataset()
                    st.markdown(
                        f'Your images aved too')
                    st.session_state['not_saving'] = True

                except:
                    st.write('There was an error saving to Deep Lake. Ensure your API key and dataset path are correct, then try again.')
                    st.session_state['not_saving'] = True


if __name__ == '__main__':
    main()

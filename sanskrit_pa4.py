import pandas as pd
import json
import streamlit as st
import openai

user_api_key = st.sidebar.text_input('OpenAI API key', type='password')

client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as a Sanskrit professor.
            You will be given a Sanskrit text containing at least one noun. Your task is to 
            list all nouns in the text in a JSON array with the following fields:
                • Word in the Text: The word as it appears in the Sanskrit sentence (e.g. बालः)
                • Before Applying External Sandhi Form: The form of the word before applying external Sandhi (e.g. बालस्)
                • Original Form: The dictionary/original form of the word (e.g. बाल)
                • Meaning: The meaning of the word in English.
                • Case: The grammatical case of the word in the text (choose from [Nominative, Accusative, Instrumental, Dative, Ablative, Genitive, Locative, Vocative]).
                • Number: The number of the word in the text (choose from [Singular, Dual, Plural]).
                • Gender: The gender of the word based on its usage in the text (choose from [Masculine, Neuter, Feminine]).
                • The analyze form: The form abbreviated form a word's case, gender, and number respectively (e.g. बालस् is Nominative, Singular, Masculine. Its analyze form is NomSM.)
            
            If the text contains no nouns, do not execute any tasks and inform the user that the text must include at least one noun.
            
            Do not respond or take any action until the text is provided.
            """

st.title(':orange[Sanskrit] Noun Finder')

st.divider()

st.header(':orange[Sanskrit 101]: What you should know')
st.subheader('What is an external :orange[Sandhi]?')
st.markdown('The external Sandhi is the term for the set of sound changes between words in a sentence. This process makes pronunciation more natural and easier.')
st.subheader('The :orange[analyzed form] of a Sanskrit word you should know')
st.markdown('In Sanskrit academic field, when you have to analyze each word in a sentence/text, there is a universal form of an analyze form abbreviated with the properties of each part of speech. \
            \nFor nouns, there are three categories: :orange[case], :orange[number], and :orange[gender]')
major = st.selectbox('Select a category you want to know about',['Case','Number','Gender'],index=None,placeholder="Select the category...")
if major == 'Case':
    Case = {'Nom':':orange[Nominative] - subject',
            'Acc':':orange[Accusative] - direct object',
            'Ins':':orange[Instrumental] - "with" someone or something',
            'Dat':':orange[Dative] - "to", "for"',
            'Abl':':orange[Ablative] - "from", "since", "because of"',
            'Gen':':orange[Genitive] - possession or belonging',
            'Loc':':orange[Locative] - location',
            'Voc':':orange[Vocative] - address someone'}
    Case_type = st.segmented_control(
        'Choose the case for the further explanation',
        list(Case.keys()),
        selection_mode="single")
    st.write(f'You selected _{Case_type}_: {Case.get(Case_type, "You haven't selected any case...")}')
    st.write(':orange[Note]: This is the :orange[brief] definition of cases, Some cases might have additional functions beyond the ones mentioned above.')

elif major == 'Number':
    Number = {'S':':orange[Singular]','D':':orange[Dual]','P':':orange[Plural]'}
    Number_type = st.segmented_control(
        'Choose the number for the further explanation',
        list(Number.keys()),
        selection_mode="single")
    st.write(f'You selected _{Number_type}_: {Number.get(Number_type, "You haven't selected any number...")}')
    
elif major == 'Gender':
    Gender = {'M':':orange[Masculine]','N':':orange[Neuter]','F':':orange[Feminine]'}
    Gender_type = st.segmented_control(
        'Choose the gender for the further explanation',
        list(Gender.keys()),
        selection_mode="single")
    st.write(f'You selected _{Gender_type}_: {Gender.get(Gender_type, "You haven't selected any gender...")}')
st.markdown('Once you understand about these abbreviated properties, you can write an analyze form of a noun by conbining its **case**, **number**, and **gender** respectively. :orange[For instance], **देवस्** (a deity) is **nominative**, **singular**, **masculine**. Its analyze form is **NomSM**.')

st.divider()

st.header("Let's get :orange[started]!")


st.markdown('Input the Sanskrit text and the AI will provide you \n\
            the table of nouns, listing their properties as used in the text.')

user_input = st.text_area("Enter your text below:","Your text here")

if st.button('Submit'):
    message_so_far = [
        {'role':'system','content':prompt},
        {'role':'user','content':user_input}
        ]
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messases=message_so_far
        )

    st.markdown('Here is the result')
    noun_dictionary = response.choices[0].message.content
    sanskritjson = json.load(noun_dictionary)
    sanskrit_df = pd.DataFrame.from_dict(sanskritjson)
    print("Noun(s) in the text:")
    st.table(sanskrit_df)
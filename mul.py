import streamlit as st

st.set_page_config(page_title="Ancient Names Translator", page_icon="📜")
st.title("📜 Ancient Names Translator")

st.markdown("""
Translate **names or words** between:
- English ↔ Brahmi  
- English ↔ Kharosthi  
- English ↔ Tamil  
- English ↔ Hebrew  
- English ↔ Aramaic  
- English ↔ Greek  
- English ↔ Latin (Old Roman)
""")

# ---------------- BRAHMI ----------------
brahmi_cons = {
    "k":"𑀓","g":"𑀕","c":"𑀘","j":"𑀚",
    "t":"𑀢","d":"𑀤","n":"𑀦",
    "p":"𑀧","m":"𑀫","y":"𑀬",
    "r":"𑀭","l":"𑀮","v":"𑀯",
    "s":"𑀲","h":"𑀳"
}
brahmi_indep_vowels = {
    "a":"𑀅","ā":"𑀆","i":"𑀇","ī":"𑀈",
    "u":"𑀉","ū":"𑀊","e":"𑀏","ai":"𑀐",
    "o":"𑀑","au":"𑀒"
}
brahmi_dep_vowels = {
    "a":"","ā":"𑀸","i":"𑀺","ī":"𑀻",
    "u":"𑀼","ū":"𑀽","e":"𑀾","ai":"𑀿",
    "o":"𑁀","au":"𑁁"
}

# ---------------- TAMIL ----------------
tamil = {"a":"அ","i":"இ","u":"உ","e":"எ","o":"ஒ",
         "k":"க","c":"ச","t":"த","n":"ந","p":"ப","m":"ம",
         "y":"ய","r":"ர","l":"ல","v":"வ","s":"ஸ","h":"ஹ"}
tamil_rev = {v:k for k,v in tamil.items()}

# ---------------- HEBREW ----------------
hebrew = {"a":"א","b":"ב","g":"ג","d":"ד","h":"ה",
          "k":"כ","l":"ל","m":"מ","n":"נ","r":"ר","s":"ש","t":"ת","y":"י","v":"ו"}
hebrew_rev = {v:k for k,v in hebrew.items()}

# ---------------- ARAMAIC ----------------
aramaic = {"a":"𐡀","b":"𐡁","g":"𐡂","d":"𐡃","h":"𐡄",
           "k":"𐡊","l":"𐡋","m":"𐡌","n":"𐡍","r":"𐡓","s":"𐡔","t":"𐡕"}
aramaic_rev = {v:k for k,v in aramaic.items()}

# ---------------- GREEK ----------------
greek = {"a":"Α","b":"Β","g":"Γ","d":"Δ","e":"Ε","z":"Ζ","i":"Ι","k":"Κ","l":"Λ",
         "m":"Μ","n":"Ν","o":"Ο","p":"Π","r":"Ρ","s":"Σ","t":"Τ","u":"Υ"}
greek_rev = {v:k for k,v in greek.items()}

# ---------------- LATIN ----------------
latin = {chr(i): chr(i).upper() for i in range(97,123)}
latin_rev = {v:k for k,v in latin.items()}

# ---------------- FUNCTIONS ----------------
def english_to_brahmi(word):
    result = ""
    i = 0
    word = word.lower()
    while i < len(word):
        # two-letter vowels first
        if i+1 < len(word) and word[i:i+2] in brahmi_indep_vowels:
            result += brahmi_indep_vowels[word[i:i+2]]
            i += 2
        elif word[i] in brahmi_indep_vowels:
            result += brahmi_indep_vowels[word[i]]
            i += 1
        elif word[i] in brahmi_cons:
            cons = brahmi_cons[word[i]]
            vowel = ""
            # check next 2 letters for dependent vowel
            if i+2 <= len(word) and word[i+1:i+3] in brahmi_dep_vowels:
                vowel = brahmi_dep_vowels[word[i+1:i+3]]
                i += 2
            elif i+1 < len(word) and word[i+1] in brahmi_dep_vowels:
                vowel = brahmi_dep_vowels[word[i+1]]
                i += 1
            result += cons + vowel
            i += 1
        else:
            result += word[i]
            i += 1
    return result

def to_script(text, mapping):
    return "".join(mapping.get(c.lower(), c) for c in text)

def to_english(text, reverse_map):
    return "".join(reverse_map.get(c, c) for c in text)

# ---------------- UI ----------------
mode = st.selectbox("Choose Translation Mode", ["English → Ancient", "Ancient → English"])
text = st.text_input("Enter text:")

if text:
    if mode == "English → Ancient":
        st.subheader("Translations")
        st.write("Brahmi:", english_to_brahmi(text))
        st.write("Tamil:", to_script(text, tamil))
        st.write("Hebrew:", to_script(text, hebrew))
        st.write("Aramaic:", to_script(text, aramaic))
        st.write("Greek:", to_script(text, greek))
        st.write("Latin:", to_script(text, latin))
    else:
        st.subheader("English (phonetic)")
        st.write("From Brahmi:", to_english(text, {v:k for k,v in {**brahmi_cons, **brahmi_indep_vowels}.items()}))
        st.write("From Tamil:", to_english(text, tamil_rev))
        st.write("From Hebrew:", to_english(text, hebrew_rev))
        st.write("From Aramaic:", to_english(text, aramaic_rev))
        st.write("From Greek:", to_english(text, greek_rev))
        st.write("From Latin:", to_english(text, latin_rev))

import pytesseract
from PIL import Image

# Example: extract text from image
def extract_text_from_image(image):
    text = pytesseract.image_to_string(Image.open(image), lang='eng') # we start with English
    return text

uploaded_file = st.file_uploader("Upload an image of the inscription:", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    extracted_text = extract_text_from_image(uploaded_file)
    st.subheader("📖 Extracted Text")
    st.write(extracted_text)
if uploaded_file:
    # Extract text
    extracted_text = extract_text_from_image(uploaded_file)

    st.subheader("Translations of Extracted Text")
    st.write("Brahmi:", english_to_brahmi(extracted_text))
    st.write("Tamil:", to_script(extracted_text, tamil))
    st.write("Hebrew:", to_script(extracted_text, hebrew))
    st.write("Aramaic:", to_script(extracted_text, aramaic))
    st.write("Greek:", to_script(extracted_text, greek))
    st.write("Latin:", to_script(extracted_text, latin))

st.markdown("""
<style>
body {
    background-color: #fdf6e3;
    color: #073642;
    font-family: 'Times New Roman', serif;
}
h1, h2, h3 {
    color: #b58900;
}
.stButton>button {
    background-color: #268bd2;
    color: white;
    font-size: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

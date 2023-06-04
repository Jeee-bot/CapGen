import streamlit as st
from PIL import Image
from generate_caption import generate_caption_for_img

def main():
    # Set the title of the web app
    st.title("Image Caption Generator")

    # Create a file uploader widget to allow the user to choose an image file
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    # Check if an image file is uploaded
    if uploaded_file is not None:
        # Open the uploaded image file using PIL
        image = Image.open(uploaded_file)
        
        # Display the uploaded image on the web app
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Check if the "Generate Caption" button is clicked
        if st.button("Generate Caption"):
            # Generate a caption for the uploaded image
            caption = generate_caption_for_img(image)
            
            # Display the generated caption on the web app with bigger and bold font
            st.markdown(f"<p style='font-size: 20px; font-weight: bold;'>Generated Caption: {caption}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

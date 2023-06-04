from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize the Blip image captioning model
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Initialize the T5 text-to-text transfer model and tokenizer
t5_tokenizer = AutoTokenizer.from_pretrained('prasanthsagirala/text-to-social-media-captions')
t5_model = AutoModelForSeq2SeqLM.from_pretrained('prasanthsagirala/text-to-social-media-captions')

def generate_desc(image, text):
    """
    Generates image description using the Blip image captioning model.

    Parameters:
    - image: Image object or URL of the image.
    - text: Additional text to condition the image captioning model.

    Returns:
    - Generated image description.
    """
    if text != "":
        # Conditional image captioning
        inputs = blip_processor(image, text, return_tensors="pt")
        out = blip_model.generate(**inputs)
        return blip_processor.decode(out[0], skip_special_tokens=True)
    else:
        # Unconditional image captioning
        inputs = blip_processor(image, return_tensors="pt")
        out = blip_model.generate(**inputs)
        return blip_processor.decode(out[0], skip_special_tokens=True)

def generate_caption(text="a woman playing soccer"):
    """
    Generates a caption for the given text using the T5 text-to-text transfer model.

    Parameters:
    - text: Text for which the caption needs to be generated.

    Returns:
    - Generated caption.
    """
    inputs = ["captionize: " + text]
    inputs = t5_tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt")
    output = t5_model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=64)
    decoded_output = t5_tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    return decoded_output

def generate_caption_for_img(image_path):
    """
    Generates a caption for the given image.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - Generated caption.
    """
    img_desc = generate_desc(image_path, "")
    caption = generate_caption(img_desc)
    return caption
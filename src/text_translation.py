import argostranslate.package
import argostranslate.translate
import os

def setup_translation_model(from_lang="en", to_lang="hi", model_dir="./models/argos/translate"):
    """
    Install the Argos Translate model for the specified language pair.
    """
    # Define model file path
    model_file = f"translate-{from_lang}_{to_lang}.argosmodel"
    model_path = os.path.join(model_dir, model_file)

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file '{model_file}' not found in {model_dir}. "
            "Please download it manually from https://www.argosopentech.com/argospm/"
        )

    # Install the language model
    print(f"Installing translation model from {model_path}...")
    argostranslate.package.install_from_path(model_path)
    print("Model installed successfully.")

def translate_text(input_text, from_lang="en", to_lang="hi"):
    """
    Translate text from the source language to the target language.
    """
    installed_languages = argostranslate.translate.get_installed_languages()
    source_lang = next((lang for lang in installed_languages if lang.code == from_lang), None)
    target_lang = next((lang for lang in installed_languages if lang.code == to_lang), None)

    if not source_lang or not target_lang:
        raise ValueError("Required language pair is not installed.")

    # Get translation object
    translation = source_lang.get_translation(target_lang)
    if not translation:
        raise ValueError("Translation between the selected languages is not available.")

    # Perform translation
    return translation.translate(input_text)

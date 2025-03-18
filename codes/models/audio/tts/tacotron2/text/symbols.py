""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from models.audio.tts.tacotron2.text import cmudict



_pad        = '_'
_punctuation = '!\'(),.:;? '
_special = '-'
_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzäöüßÄÖÜ'


# Path to your Yoruba transcription file
file_path = 'yoruba_transcription.txt'

try:
    # Read the Yoruba transcription file
    with open(file_path, 'r', encoding='utf-8') as file:
        yoruba_text = file.read()
    
    # Extract unique characters from the Yoruba text
    yoruba_chars = set(yoruba_text)
    
    # Filter out characters that are already in _letters, _punctuation, or _special
    existing_chars = set(_letters + _punctuation + _special + _pad)
    new_yoruba_chars = yoruba_chars - existing_chars
    
    # Sort the new characters for consistency
    sorted_new_chars = sorted(list(new_yoruba_chars))
    
    # Update _letters with new Yoruba characters
    _letters = _letters + ''.join(sorted_new_chars)
except:
    pass


# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in cmudict.valid_symbols]

# Export all symbols:
symbols = [_pad] + list(_special) + list(_punctuation) + list(_letters) + _arpabet


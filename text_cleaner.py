import re

def text_cleaner(text):

    # Removes special characters
    text = re.sub(r'[*a-zA-Z0-9 ]', '', text)

    # Replaces multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)

    # Trims unnecessary whitespaces
    text = text.strip()
    text = ' '.join(text.split()) 
    
    # Removes HTML tags
    text = re.sub(r'<[*>]*?>', '', text)
    
    # Removes URLs
    text = re.sub(r'http[s]?://(?: [a-zA-Z] | [0-9] | [$—_@. &+] | [!*\\(\\) , ] | (2% [0-9a-fA-F] [0-9a-fA-F]))+', '', text)

    return text
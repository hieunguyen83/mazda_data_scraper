# CODING TOOLS FOR DATA PROCESSING

import requests


def download_file_from_google_drive(file_id, destination):
    """ A function to download a shareable file from Google Drive. """
    URL = "https://docs.google.com/uc?export=download&confirm=1"
    session = requests.Session()
    response = session.get(URL, params={"id": file_id}, stream=True)

    def get_confirm_token():
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    def save_response_content():
        chunk_size = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    token = get_confirm_token()
    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content()


# FUNCTIONS TO SUPPORT PROCESSING DATA
def transform_text(text):
    """ In index page, there are many dot(.), remove this when for readable. """
    text = text.replace('.page ', ' page ')  # make sure a space before page
    # loop through
    while '..' in text:
        text = text.replace('..', '')

    # replace hyphen + break line. e.g. "Seating posi-\ntion" --> "Seating position"
    text = text.replace('-\n', '')

    return text


def format_text_data(text_to_process):  # using for rendering data later.
    # there are many unicode icon in each page,
    # when present data, but them back in file instead of the confusing unicode text.
    unicode_icon = ['▼', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
                    '⑪', '⑫','⑬', '⑭', '⑮', '⑯', '⑰', '⑱', '⑲', '⑳']
    unicode_text = ['\u25bc', '\u2460', '\u2461', '\u2462', '\u2463', '\u2464', '\u2465', '\u2466', '\u2467', '\u2468', '\u2469',
                    '\u246a', '\u246b','\u246c', '\u246d', '\u246e', '\u246f', '\u2470', '\u2471', '\u2472', '\u2473']

    final_text = text_to_process
    for text, icon in zip(unicode_text, unicode_icon):
        final_text = final_text.replace(text, icon)
    return final_text



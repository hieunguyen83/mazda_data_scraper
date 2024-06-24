#MAZDA DATA SCRAPER
"""
- to extract all data from the pdf file
- data to extract from each page:
    + text
    + table
    + detail small images
    + overview image
"""

# importing python packages
import pdfplumber
from pypdf import PdfReader
import urllib.request as get_image  # this package to scrape whole page image from web in each pdf page
import json  # storing scraped data to a JSON file
import os  # delete a file if existed

# delete this file if existed, will generate a brand new one.
if os.path.exists('mazda_data.jsonl'):
    os.remove('mazda_data.jsonl')

# create images folder, if not existed.
if not os.path.exists('images'):
    os.makedirs('images')

# pdf file to scrape data
pdf_file = '3_2020.pdf'


# FUNCTIONS TO SUPPORT PROCESSING DATA
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


# creating a class to structure data
class PageData:
    page_number: int = 0
    table_data: list = []
    text_data: str = ''
    small_image_names: list = []  # there maybe many small images in each page, get all names
    overview_image_name: str = ''  # and a whole & big image if any, download it, get name
    scraper_notes: list = []  # any note while collecting data, store here

    def scrape_data(self, pdf_page_number):
        self.page_number = pdf_page_number  # store page number
        print(self.page_number)

        with pdfplumber.open(pdf_file) as pdf:
            selected_page = pdf.pages[pdf_page_number - 1]

            # Extract table
            tables = selected_page.extract_tables(table_settings={"text_tolerance": 5})
            self.table_data = tables  # store tables data

            # Extract text
            pdf_text = selected_page.extract_text()
            self.text_data = pdf_text  # store text data
            print(self.text_data)

        # Extract every single image, store files to a folder(Images), save names accordingly
        reader = PdfReader(pdf_file)
        selected_page = reader.pages[pdf_page_number - 1]  # reader started from 0, so -1

        try:  # in case the image not qualified to process
            images = selected_page.images  # getting all images in page
            for image in images:  # loop through
                image_name = f'page{pdf_page_number}_' + image.name  # naming the image with page number
                with open(f'images/{image_name}', 'wb') as f:  # saving image to local folder
                    f.write(image.data)
                self.small_image_names.append(image_name)  # store image name
        except:
            self.scraper_notes.append('Not processed all small images.')

        # Extract Overview Image, which is a big image with numbers and guidance.
        # This will be scraped directly from the web page instead.
        overview_image = f'page{pdf_page_number}_overview.jpg'
        image_url = f'https://static-data2.manualslib.com/storage/pdf39/191/19024/1902335/images/3_2020_{pdf_page_number}_bg.jpg'

        try:
            get_image.urlretrieve(image_url, f'images/{overview_image}')
            self.overview_image_name = overview_image

        except:
            self.scraper_notes.append('Not processed overview image.')

        # Save data to JSON file
        data_to_save = {'page_number': self.page_number,
                        'table_data': self.table_data,
                        'text_data': self.text_data,
                        'small_image_names': self.small_image_names,
                        'overview_image_name': self.overview_image_name,
                        'scraper_notes': self.scraper_notes
                        }

        with open('mazda_data.jsonl', 'a', encoding='utf-8') as f:
            f.writelines(f'{json.dumps(data_to_save)}\n')


for page_number in range(8, 10):  # process 720 pages in the pdf file
    mazda_data = PageData()
    mazda_data.scrape_data(page_number)

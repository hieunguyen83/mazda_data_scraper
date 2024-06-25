#MAZDA DATA SCRAPER
"""
ETL all data from a pdf file
- Extract data from each page, taking 3 seconds to extract one page. for 720 pages will take 36 minutes.
    Data type:
    + text
    + table
    + detail small images
    + overview image
- Transform data:
    + remove dot line in each index page for readable

- Load add extracted data to JSON file: mazda_data.jsonl
    & all extracted images saved to images folder

"""
# importing python packages
import pdfplumber
from pypdf import PdfReader
import urllib.request as get_image  # this package to scrape whole page image from web in each pdf page
import json  # storing scraped data to a JSON file
import os  # check file if existed for delete, download
from data_tools import transform_text  #
import shutil # to remove non-empty folder

# pdf file to scrape data
pdf_file = 'mazda_manual.pdf'

# first, download the mazda manual pdf file, save to current folder
# in this case, the file get it from Google Drive.
if not os.path.exists(pdf_file):  # if the file existed, skip this step
    from data_tools import download_file_from_google_drive

    print('Downloading a 34Mb-sized pdf file. This takes 1 - 2 minutes.')

    google_file_id = '1-3v_4cGdMFuTH_X5wzrDnAyYwImYw3qE'
    file_name = 'mazda_manual.pdf'
    download_file_from_google_drive(google_file_id, pdf_file)

# delete file, folder if existed, will generate brand new space.
if os.path.exists('mazda_data.jsonl'):
    os.remove('mazda_data.jsonl')
if os.path.exists('images'):
    shutil.rmtree('images')

# create images folder.
if not os.path.exists('images'):
    os.makedirs('images')


# creating a class to structure data
class PageData:
    def __init__(self):
        self.page_number: int = 0
        self.table_data: list = []
        self.text_data: str = ''
        self.small_image_names: list = []  # there maybe many small images in each pdf page, get all names here
        self.overview_image_name: str = ''  # a whole big image if any, download it, get name here

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

        try:  # try, in case the image not qualified to process
            images = selected_page.images  # getting all images in page
            for image in images:  # loop through
                image_name = f'page{pdf_page_number}_' + image.name  # naming the image with page number
                with open(f'images/{image_name}', 'wb') as f:  # saving image to local folder
                    f.write(image.data)
                    self.small_image_names.append(image_name)  # store image name
        except:
            print('No small image found.')

        # Extract Overview Image, which is a big image with numbers and guidance.
        # This will be scraped directly from the web page instead.
        overview_image = f'page{pdf_page_number}_overview.jpg'
        image_url = f'https://static-data2.manualslib.com/storage/pdf39/191/19024/1902335/images/3_2020_{pdf_page_number}_bg.jpg'

        try:
            get_image.urlretrieve(image_url, f'images/{overview_image}')
            self.overview_image_name = overview_image

        except:
            print('No overview image found.')

        # Save data to JSON file
        data_to_save = {'page_number': self.page_number,
                        'table_data': self.table_data,
                        'text_data': transform_text(self.text_data),
                        'small_image_names': self.small_image_names,
                        'overview_image_name': self.overview_image_name
                        }

        with open('mazda_data.jsonl', 'a', encoding='utf-8') as f:
            f.writelines(f'{json.dumps(data_to_save)}\n')


# for page_number in range(1, 720):  # process all 720 pages, taking 36 minutes. extracting 1830 images.

# I select some pages to demonstrate:
# page 6 : many small images
# page 8: 'no table, Pictorial Index, text, with small images, overview image'
# page 22: only text
# page 54: 'Table data, text, no image'
# page 60: 'Big Table data, little text, no image'
# page 61: '2 Table data, little text, no image'

for page_number in [6, 8, 22, 54, 60, 61]:
    mazda_data = PageData()
    mazda_data.scrape_data(page_number)

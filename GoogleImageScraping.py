import argparse
from selenium import webdriver
import time
import requests
import io
from PIL import Image
import os
import hashlib
import sys


# create path for save donwloded image
def create_save_path(search_keyword: str, path: str):

    if os.path.exists(path):
        save_path = os.path.join(path + '/' + search_keyword + '/')

        # create a directory with search keyword
        if os.path.exists(save_path) != True:
            os.mkdir(path + '/' + search_keyword)
            print('Create new directory', save_path)

        print('Success: Create save path', save_path)
        return save_path
    else:
        # exit if path doesn't exist
        print('Error: Not found path')
        sys.exit()


# fetch image urls for download
def fetch_image_urls(search_keyword: str, download_number: int, wd: webdriver):
    print('------------------------------------------------')
    print('Start getting thumnails')

    fetch_thumbnail_count = 0
    thumbnails = None
    # fetch thumbnails up to number of images to download
    while fetch_thumbnail_count < download_number:
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        thumbnails = wd.find_elements_by_css_selector('img.Q4LuWd')
        fetch_thumbnail_count = len(thumbnails)

        # break if fetched thumbnails number exceed number of images to download
        if len(thumbnails) >= download_number:
            print('Success: Fetched thumbnails count', download_number)
            break
        else:
            # load more thumbnails when load_more_button appears
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # brek when end_text appears ( this is the limit of thumbnails that can be fetched )
        end_text = wd.find_element_by_class_name('OuJzKb')
        if end_text and end_text.text == 'Looks like you\'ve reached the end':
            print('Success: Fetched maximum thumbnails count', len(thumbnails))
            break

    print('Start getting image urls')
    image_urls = []
    # extract the image url from the elements displayed by clicking the thumbnails
    for thumbnail in thumbnails[:download_number]:
        try:
            thumbnail.click()
            time.sleep(1)
        except Exception:
            continue

        # extract only the original image url because there are some urls
        thumbnail_alt = thumbnail.get_attribute('alt')
        images = wd.find_elements_by_css_selector('img.n3VNCb')
        for image in images:
            image_alt = image.get_attribute('alt')
            if thumbnail_alt == image_alt and 'http' in image.get_attribute('src'):
                image_urls.append(image.get_attribute('src'))

    print('Success: Fetched image urls count', len(image_urls))
    return image_urls


# download and save from image url in save path
def save_images(image_urls: [str], dir_path: str):
    print('------------------------------------------------')
    print('Start downloading and saving images')

    success_count = 0
    for url in image_urls:
        # download image data from url
        try:
            image_content = requests.get(url, timeout=3.5).content
        except requests.exceptions.RequestException as error:
            print('Error: Filed download image', error)
            continue

        # generate JPG image form data
        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
        except IOError as error:
            print('Error: Failed convert image to JPG:', error)
            continue

        # save image
        try:
            image_name = hashlib.sha1(image_content).hexdigest()[:15] + '.jpg'
            file_path = os.path.join(dir_path, image_name)
            image.save(file_path, quality=90)
        except IOError as error:
            print('Error: Failed save image:', error)
            continue

        print('Success: Save image', image_name)
        success_count += 1

    print('------------------------------------------------')
    print('Comlplete !!', success_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='A keyword for image search')
    parser.add_argument('-n', '--number', help='Number of downloads')
    parser.add_argument(
        '-p', '--path', help="Path to save the downloaded image")
    args = parser.parse_args()

    # create save path
    save_path = create_save_path(args.keyword, args.path)

    # open Google Chrome and go to Google image page
    DRIVER_PATH = ""  # DRIVER_PATH = "Your Goolge Driver Path"
    wd = webdriver.Chrome(executable_path=DRIVER_PATH)
    wd.get('https://google.com')
    serch_box = wd.find_element_by_css_selector('input.gsfi')
    serch_box.send_keys(args.keyword)
    url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(url.format(q=args.keyword))

    # fetch image urls
    image_urls = fetch_image_urls(args.keyword, int(args.number), wd)
    # download and save image
    save_images(image_urls, save_path)
    # close Google Chrome
    wd.quit()

# library imports
import requests
from PIL import Image
from json import load

# file imports
import selectors
from constants import HREF, WB
from functions import initiate_driver, adjust_image_name


# TODO print progress bar
# TODO Create default data.json and add data to it (try tk)


if __name__ == '__main__':

    # extract data from data.json
    download_path, show_browser, subreddit_links, max_images_in_subreddit, minimum_width, minimum_height = load(
        open('./data.json')
    ).values()

    # initiate chrome driver
    driver = initiate_driver(not show_browser, False, False)

    # walk through subreddits
    for subreddit_link in subreddit_links:

        driver.get(subreddit_link)

        # get max post links
        posts_links = [
            post_link.get_attribute(HREF) for post_link in driver.find_elements_by_css_selector(selectors.post)
        ][:max_images_in_subreddit]

        for post_link in posts_links:

            driver.get(post_link)

            # get image name and link from image post
            image_name, image_link = [
                adjust_image_name(
                    driver.find_element_by_css_selector(
                        selectors.image_name
                    ).text
                ).strip(),
                driver.find_element_by_css_selector(
                    selectors.image_link
                ).get_attribute(HREF)
            ]

            image_path = f'{download_path}/{image_name}.png'

            # download image from image link
            image = open(image_path, WB)
            image.write(requests.get(image_link).content)
            image.close()

            # delete image with less than minimum resolution
            width, height = Image.open(image_path).size
            if width < minimum_width or height < minimum_height:
                print(image_name)
                # remove(image_path)

    # quit driver
    driver.quit()

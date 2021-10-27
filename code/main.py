# library imports
import requests
from os import remove
from PIL import Image
from json import load

# file imports
import selectors
from constants import HREF, WB
from functions import initiate_driver, adjust_image_name, print_progress_bar, styled


# TODO Create default data.json and add data to it (try tk)
# TODO print grey █ instead of white █


if __name__ == '__main__':
    # extract data from data.json
    download_path, show_browser, subreddit_links, max_images_in_subreddit, minimum_width, minimum_height = load(
        open('./data.json')
    ).values()

    print(styled(f'Downloading wallpapers to {download_path}', 'green'))

    # initiate chrome driver
    driver = initiate_driver(not show_browser, False, False)
    if not show_browser:
        print(styled('Driver running in the background', 'yellow'))

    # walk through subreddits
    for subreddit_link in subreddit_links:
        driver.get(subreddit_link)

        # get max post links
        posts_links = [
            post_link.get_attribute(HREF) for post_link in driver.find_elements_by_css_selector(selectors.post)
        ][:max_images_in_subreddit]

        print(styled(
            f'\nCollected {len(posts_links)} wallpapers from {subreddit_link}', 'green'
        ))

        for post_link in posts_links:
            print_progress_bar(
                2, 10, '', 'Opening image in driver', 1, 10,
                styled('█')
            )
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

            styled_image_name = styled(f"'{image_name[:10]}...'", 'Cyan')
            print_progress_bar(
                4, 10, '', f'Downloading {styled_image_name}       ', 1, 10,
                styled('█')
            )

            image_path = f'{download_path}/{image_name}.png'

            # download image from image link
            image = open(image_path, WB)
            image.write(requests.get(image_link).content)
            image.close()

            print_progress_bar(
                6, 10, '', f'Checking {styled_image_name} resolution', 1, 10,
                styled('█')
            )

            # delete image with less than minimum resolution
            width, height = Image.open(image_path).size
            if width < minimum_width or height < minimum_height:
                remove(image_path)
                print_progress_bar(
                    8, 10, '', f'{styled_image_name} doesn\'t meet minimum resolution', 1, 10,
                    styled('█')
                )
                print_progress_bar(
                    10, 10, '', f'Successfully deleted {styled_image_name}', 1, 10,
                    styled('█')
                )

            else:
                print_progress_bar(
                    8, 10, '', f'{styled_image_name} meets minimum resolution', 1, 10,
                    styled('█')
                )
                print_progress_bar(
                    10, 10, '', f'Successfully downloaded {styled_image_name}', 1, 10,
                    styled('█')
                )

    # quit driver
    driver.quit()

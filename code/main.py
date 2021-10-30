# library imports
import requests
from os import remove
from PIL import Image

# file imports
import selectors
from constants import HREF, RED, WB, GREEN, YELLOW, CYAN
from functions import initiate_driver, adjust_image_name, print_progress_bar, styled, get_json_data


# TODO print grey █ instead of white █


if __name__ == '__main__':
    # extract data from data.json
    download_path, show_browser, subreddits, max_images_in_subreddit, minimum_width, minimum_height = get_json_data()

    print(styled(f'Downloading wallpapers to {download_path}', GREEN))

    # initiate chrome driver
    driver = initiate_driver(not show_browser, False, False)
    if not show_browser:
        print(styled('Driver running in the background', YELLOW))

    # walk through subreddits
    for subreddit in subreddits:
        driver.get(f'https://reddit.com/r/{subreddit}/top/')

        # get max post links
        posts_links = [
            post_link.get_attribute(HREF) for post_link in driver.find_elements_by_css_selector(selectors.post)
        ][:max_images_in_subreddit]

        print(styled(
            f'\nCollected {len(posts_links)} wallpapers from r/{subreddit}', GREEN
        ))

        for post_link in posts_links:

            print_progress_bar(2, 10, '', 'Opening image in driver', 1, 10)
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

            styled_image_name = styled(f"'{image_name[:10]}...'", CYAN)
            print_progress_bar(
                4, 10, '', f'Downloading {styled_image_name}       ', 1, 10
            )

            image_path = f'{download_path}/{image_name}.png'

            # download image from image link
            image = open(image_path, WB)
            image.write(requests.get(image_link).content)
            image.close()

            print_progress_bar(
                6, 10, '', f'Checking {styled_image_name} resolution', 1, 10,
            )

            # delete image with less than minimum resolution
            width, height = Image.open(image_path).size
            if width < minimum_width or height < minimum_height:
                remove(image_path)
                print_progress_bar(
                    8, 10, '', f'{styled_image_name} doesn\'t meet minimum resolution', 1, 10
                )
                print_progress_bar(
                    10, 10, '', f"{styled('Successfully deleted', RED)} {styled_image_name} {styled(f'({width}x{height})', RED)}", 1, 10
                )

            else:
                print_progress_bar(
                    8, 10, '', f'{styled_image_name} meets minimum resolution', 1, 10
                )
                print_progress_bar(
                    10, 10, '', f"{styled('Successfully downloaded', GREEN)} {styled_image_name} {styled(f'({minimum_width}x{height})', GREEN)}", 1, 10
                )

    # quit driver
    driver.quit()

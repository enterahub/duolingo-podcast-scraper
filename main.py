"""
A Python mini-project for downloading(i.e. scraping) transcript of Duolingo Podcast.
"""

import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re

import threading  # for IO-intensive pthon tasks
import time

"""
翻页式的，但是有规律
"""
# Get parent directory
parent_directory = Path(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))


def timing_val(func):
    """
    Timing decorator.
    :param func:
    :return:
    """

    def wrapper(*arg, **kw):
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        return (t2 - t1), res, func.__name__

    return wrapper


def grasp_one_webpage(link, folder_abs_path):
    domain = "https://podcast.duolingo.com/"

    # Your previous code to get the list of h2 elements
    html = requests.get(link).content
    soup = BeautifulSoup(html, "html.parser")
    h2_elements = soup.find_all("h2", {"class": "entry-title"})

    # Extract the URLs from the href attributes
    urls = [h2.find("a")["href"] for h2 in h2_elements]

    # Now, you can loop through the URLs and send requests to each URL
    for u in urls:
        subpage_full_url = domain + u  # Replace "https://example.com" with your base URL
        html = requests.get(subpage_full_url).content

        soup = BeautifulSoup(html, "html.parser")

        # Set directory for one episode
        # title=Permalink to Episode 95: La championne du fromage (Cheese Champion) - Revisited
        title = soup.find("h1", {"class": "entry-title"}).find('a')['title']
        pattern = r"Permalink to Episode (\d+): (.+)"
        match = re.search(pattern, title)
        if match:
            podcast_no = match.group(1)
            title = match.group(2)
            script_file_name = f'{podcast_no}. {title} (Duolingo French Podcast)'

            # Get script
            p_elements = soup.find_all("p")
            text = "\n\n".join(p.get_text() for p in p_elements)
            if not os.path.exists(f"{folder_abs_path}/{podcast_no}. {title}.txt"):
                with open(f"{folder_abs_path}/{script_file_name}.txt", 'w+') as f:
                    f.writelines(f"Audio Link:\n{subpage_full_url}\n\n")
                    f.write(text)
                    print(f"{subpage_full_url} Finish writing.")


@timing_val
def without_multithreading():
    print("1) spanish\n"
          "2) french\n"
          "3) ingles-espanol\n"
          "4) ingles-portugues\n")

    # Create a parent folder for containing the resources downloaded
    subject = input("Subject: ").lower().strip()
    folder_abs_path = parent_directory / f"{subject}_downloaded_script"
    if not os.path.exists(folder_abs_path):
        os.makedirs(folder_abs_path)

    url = f"https://podcast.duolingo.com/{subject}"
    grasp_one_webpage(url, folder_abs_path)

    for no in range(21):
        url = f"https://podcast.duolingo.com/{subject}{no}.html"
        grasp_one_webpage(url, folder_abs_path)


@timing_val
def with_multithreading():
    print("1) spanish\n"
          "2) french\n"
          "3) ingles-espanol\n"
          "4) ingles-portugues\n")

    # Create a parent folder for containing the resources downloaded
    subject = input("Subject: ").lower().strip()
    folder_abs_path = parent_directory / f"{subject}_downloaded_script"
    if not os.path.exists(folder_abs_path):
        os.makedirs(folder_abs_path)

    url = f"https://podcast.duolingo.com/{subject}"
    grasp_one_webpage(url, folder_abs_path)

    threads = []
    for no in range(21):
        url = f"https://podcast.duolingo.com/{subject}{no}.html"
        T = threading.Thread(target=grasp_one_webpage, args=[url, folder_abs_path])  # Establish threads
        threads.append(T)
        T.run()  # Run thread
        time.sleep(1)

    for thread in threads:
        thread.join()


with_multithreading()

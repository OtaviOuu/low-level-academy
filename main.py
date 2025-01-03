import requests
from yt_dlp import YoutubeDL
import os
from pprint import pp
import markdown

headers = {
    "cookie": "_fbp=fb.1.1735846173942.19722123836071597; X-CSRFToken=6ggxL9TErQduQkOtVlqlmDEsdO0HwAfk; sessionid=r3xx0qnc5qcgzwb3o3zg30a9z05m2h6e; ph_phc_WKFUWupqkrfoAEQlFqCdCLeddHiDZ6r81mZ0CMaVe0l_posthog=%7B%22distinct_id%22%3A%220194287e-9367-735e-ab2b-9ec58ce1a588%22%2C%22%24sesid%22%3A%5B1735846700774%2C%220194287e-9366-763f-9040-840014fcb2d0%22%2C1735846171494%5D%7D",
    "referer": "https://lowlevel.academy/player/3",
}


def download(url, path):
    ydl_opts = {
        "outtmpl": os.path.join(path, "video.mp4"),
        "http_headers": {
            "Referer": "https://lowlevel.academy/",
        },
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def scrape(course_id):
    site_name = "low-level-academy"
    url = f"https://lowlevel.academy/api/courses/{course_id}/"
    response = requests.get(url, headers=headers).json()
    if not response == [[], []]:
        course_data = {
            "title": response[0]["title"],
            "description": response[0]["description"],
            "image": response[0]["image_path"],
        }

        sorted_data = sorted(response[1], key=lambda x: (x["section"], x["number"]))

        module_path = None
        for content in sorted_data:
            if content["mod"] == "header":
                module_index = content["section"]
                module_title = f"{module_index} - {content['title']}"
                module_path = os.path.join(
                    site_name,
                    course_data["title"],
                    module_title,
                )
                os.makedirs(module_path, exist_ok=True)
                continue

            video_data = {
                "title": content["title"],
                "index": content["number"],
                "description": content["content"],
                "url": content["video_url"],
            }
            video_title_formated = f"{video_data['index']} - {video_data['title']}"

            path = os.path.join(
                module_path,
                video_title_formated,
            )

            os.makedirs(path, exist_ok=True)

            html_output = markdown.markdown(video_data["description"])
            template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="referrer" content="origin">
                <title>{video_data['title']}</title>
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-50 min-h-screen">
                <div class="container mx-auto px-4 py-8 max-w-4xl">
                    <!-- Video Container -->
                    <div class="mb-8">
                        <iframe 
                            src="{video_data['url']}"
                            class="w-full aspect-video bg-black rounded-lg shadow-lg"
                            frameborder="0" 
                            allow="autoplay; fullscreen; picture-in-picture; clipboard-write"
                            title="{video_data['title']}"
                        ></iframe>
                    </div>

                    <!-- Content Container -->
                    <div class="bg-white rounded-lg shadow-lg p-6 md:p-8">
                        <!-- Title -->
                        <h1 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                            {video_data['title']}
                        </h1>

                        <!-- Module Info -->
                        <div class="flex items-center space-x-2 text-sm text-gray-600 mb-6">
                            <span class="font-medium">Module {module_index}</span>
                            <span>•</span>
                            <span>Video {video_data['index']}</span>
                        </div>

                        <!-- Description -->
                        <div class="prose max-w-none">
                            <div class="whitespace-pre-wrap text-gray-700">
                                {html_output}
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            try:
                # download(video_data["url"], path)

                with open(os.path.join(path, "index.html"), "w") as f:
                    f.write(template)
            except Exception as e:
                print("Error: ", video_data["url"])


def teste():
    url = "https://lowlevel.academy/api/courses/2/"
    response = requests.get(url, headers=headers).json()
    sorted_data = sorted(response[1], key=lambda x: (x["section"], x["number"]))

    pp(sorted_data[0])


if __name__ == "__main__":
    for i in range(1, 9):
        scrape(i)

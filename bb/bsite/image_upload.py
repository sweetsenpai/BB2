from imagekitio import ImageKit
import os
from dotenv import load_dotenv
load_dotenv()

storage = ImageKit(
    private_key=os.environ.get("PRIVATE"),
    public_key=os.environ.get("PUBLIC"),
    url_endpoint=os.environ.get("IMGURL")
)


def upload_image(image_data, file_name):

    image = storage.upload_file(file_name=file_name, file=image_data)

    return [image.url, image.file_id]


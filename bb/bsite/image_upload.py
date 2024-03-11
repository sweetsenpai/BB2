from imagekitio import ImageKit
storage = ImageKit(
    private_key='private_6yiSo7pou41zMsOWBQf4RLLeYG0=',
    public_key='public_FMSOmBrnFs/cvjqr5KgTtBwrOtQ=',
    url_endpoint='https://ik.imagekit.io/sweetsenpai'
)


def upload_image(image_data, file_name):

    image = storage.upload_file(file_name=file_name, file=image_data)  # Сохраняем изображение с указанными параметрами
    return image.url


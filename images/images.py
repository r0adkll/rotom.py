

class ImageDownloader:
    """
    Base image downloader
    """

    def download(self, set_code, numbers):
        raise NotImplementedError('You must implement the download() method yourself!')

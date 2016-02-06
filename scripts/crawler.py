import os, re, requests, json, threading, urllib, time

def url_cleanup(url):
    return json.loads('"'+ url + '"')

class urlfile():
    def __init__(self, url):
        self.url = url
        self.clean_url = url_cleanup(self.url)
        self.downloaded = 0
        self.size = None
        self.initThread = threading.Thread(
            name='urlfile_init',
            target=self.init
            )
        self.initThread.start()
    def init(self):
        site = urllib.urlopen(self.clean_url)
        meta = site.info()
        self.size = meta.getheaders("Content-Length")[0]
        site.close()
    def download(self, *args):
        local_filename = self.clean_url.split('/')[-1]
        r = requests.get(self.clean_url, stream=True)
	if len(args) == 1:
		local_filename = args[0] + local_filename
        with open(local_filename, 'wb') as f:
            self.downloaded=0;
            chunk_size = 1024;
            for chunk in r.iter_content(chunk_size=chunk_size): 
                if chunk: 
                    f.write(chunk)
                    f.flush()
                    self.downloaded+=chunk_size;
        return local_filename
    def threaded_download(self):
        self.thread = threading.Thread(
            name='downloader', 
            target=self.download,
            )
        self.thread.start()

class urlcrawl():
    def __init__(self, url, fileformat):
        self.url = url
        self.fileformat = fileformat
        self.thread = None
        self.crawlResults = None
    def crawl(self):
        urlrequest = requests.get(url_cleanup(self.url))
        urlRequestResult = ''.join([y for y in urlrequest])
        format_url = '(http[^\"|^\']+.' \
            + self.fileformat \
            + '([^\"|^\'|^\b]+)?)'
        self.crawlResults = re.findall(format_url , urlRequestResult)
        return [x[0] for x in self.crawlResults]
    def threaded_crawl(self):
        self.thread = threading.Thread(
            name='crawl', 
            target=self.crawl, 
            )
        self.thread.start()
        while(self.thread.is_alive()):
            x = None
        return [x[0] for x in self.crawlResults]



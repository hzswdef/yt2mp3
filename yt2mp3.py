from youtube_dl import YoutubeDL
from requests import get

from sys import stdout
from os.path import exists, join
from os import getcwd, mkdir


YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
    

class yt2mp3:
    
    prefix = '[ yt2mp3 ]'
    
    def reset(self):
        self.songs = []
    
    
    def search(self, query):
        hr = lambda s: '0' + s if not bool(len(s) - 1) else s
        format_duration = lambda d: ':'.join([
            hr(str(d // 60)),
            hr(str(d % 60))
        ])
        
        print(f'{self.prefix} Searching media...')
        
        with YoutubeDL(YTDL_OPTIONS) as ytdl:
            results = ytdl.extract_info(f'ytsearch5:{query}', download=False)['entries']
            
            print()
            
            for i, ytdl_info in enumerate(results):
                mp3_info = {
                    'title': ytdl_info['title'],
                    'url': ytdl_info['url'],
                    'duration': format_duration(ytdl_info['duration']),
                    'filesize': round(float(ytdl_info['filesize'] / 1000000), 2), # filesize in Mb
                    'filesize_raw': ytdl_info['filesize']
                }
                
                print(f'{i + 1}. {mp3_info["duration"]} | {mp3_info["filesize"]}Mb | {mp3_info["title"]}')
                
                self.songs.append(mp3_info)
        print()
    
    
    def choose_song(self):
        song_index = int(input(f'{self.prefix} Select: ')) - 1
        
        self.save_song(song_index)
    
    
    def start(self):
        self.reset()
        
        self.search(input(f'{self.prefix} Search: '))
        self.choose_song()
    
    
    def save_song(self, song_index):
        def output_progress(cn, fs, prefix):
            cfs = round(float((1000 * cn) / 1000000), 2)
            stdout.write(f'\r{prefix} {cfs}Mb / {fs}Mb  ')
            stdout.flush()
        
        song = self.songs[song_index]
        url = get(song['url'], stream=True)
        
        if not exists(getcwd() + '/mp3'):
            mkdir(getcwd() + '/mp3')
        
        with open(f'{getcwd()}/mp3/{song["title"]}.mp3', 'wb') as f:
            for _, data in enumerate(url.iter_content(chunk_size=1024)):
                f.write(data)
                
                output_progress(_, song['filesize'], self.prefix)
        
        print(f'Saved in "{getcwd()}/mp3/"')
        
        self.start()


if __name__ == '__main__':
    worker = yt2mp3()
    worker.start()
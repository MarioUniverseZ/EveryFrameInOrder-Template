# %%
import pandas as pd
import subprocess
import os
import shutil
import glob

# %% 
df = pd.read_csv('../playlist.csv')

# %%
df['title'] = df['youtube_title'].apply(lambda x: x.split('｜')[0])
df['title'] = df['title'].apply(lambda x: x.split(' | ')[0])

# %%
for index, row in df.iterrows():
    if row['done'] == False:
        season, episode = row['season_episode'][:3], row['season_episode'][3:]
        cmd = f'yt-dlp -o - "https://www.youtube.com/watch?v={row['video_id']}" -f 136 | ffmpeg -i pipe:0 -vf fps=2 -q:v 5 Frames/{season}{episode}_%d.jpg'
        subprocess.run(cmd, check=True, shell=True)
        directory = f'Frames/{season}{episode}'
        os.makedirs(directory, exist_ok=True)
        for f in glob.glob('Frames/*.jpg'):
            shutil.move(f, directory)
        df.loc[df.index[index], 'done'] = True

# %%
df.to_csv('../playlist.csv', index=False)



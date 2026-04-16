# %%
import pandas as pd
from pathlib import Path

# %%
d = []
for path in Path('.././Frames').rglob('*.jpg'):
    if path.is_file():
        p = str(path).split('\\')
        d.append({
            'episode': p[2],
            'filename': p[-1],
        })

# %%
title = pd.read_csv('../playlist.csv')
title = title[['season_episode', 'title']]
df = pd.DataFrame(d)
df['num'] = df['filename'].str[7:-4].astype(int)
new_df = []
for i in df['episode'].unique().tolist():
    temp = pd.concat([df.loc[df['episode'] == i].sort_values(by='num')], ignore_index=True)
    new_df.append(temp)
new_df = pd.concat(new_df, ignore_index=True)
# df = df.drop(columns='num')

# %%
df1 = new_df[new_df['episode'].str[:3].isin(['S01', 'S02', 'S03'])]
df2 = new_df[new_df['episode'].str[:3].isin(['S04', 'S05'])]
df3 = new_df[new_df['episode'].str[:3].isin(['A01'])]
new_df = pd.concat([df1, df3, df2], ignore_index=True)

# %%
for i in df['episode'].unique().tolist():
    new_df.loc[new_df['episode'] == i, 'frame_end'] = new_df.loc[new_df['episode'] == i, 'num'].max()
new_df['frame_end'] = new_df['frame_end'].astype(int)
new_df['frame_start'] = new_df['filename'].apply(lambda x: x[x.find("_")+1 :x.find(".")])

# %%
new_df = new_df[['episode', 'frame_start', 'frame_end', 'filename']]
new_df['filename'] = 'Frames/' + new_df['episode'] + '/' + new_df['filename']
new_df = new_df.merge(title, left_on='episode', right_on='season_episode')
new_df = new_df[['episode', 'title', 'frame_start', 'frame_end', 'filename']]
new_df.to_csv('../df.csv', index=False)



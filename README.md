# EveryFrameInOrder-Template
This is the every-frame-in-order bot template that you can deploy anywhere, currently it's run as [Every Danmachi Frame in Order](https://www.facebook.com/every.danmachi.fio)

## Requirements
### Tools
- yt-dlp
- ffmpeg
- Python 3.12 (this environment uses 3.12.10)
- DBMS (MySQL for this template)
- ~15GB disk space (this is based on the number of frames)

### Frame Preprocess and Environment Preparation
1. Try to find your favorite anime included in a YouTube playlist
2. Extract the video titles and their video ids like:

    ```bash
    yt-dlp --flat-playlist --print "%(playlist_index)s - %(title)s: %(id)s" "youtube_playlist_url" > output.txt
    ```
3. Pack these information into a csv with the following columns:

    | video_id | youtube_title | index             | season_episode | title | done  |
    | -------- | ------------- | ----------------- | -------------- | ----- | ----- |
    | id       | youtube_title | playlist_index    | S01E01         | title | False |
    | ...      | ...           | ...               | S01E02         | ...   | ...   |
4. Create an environment for the .py scripts using the command:<br>(For Linux users, jump to [Deploy on Ubuntu Linux](#deploy-on-ubuntu-linux) section for step 4-5 and 8-9)

    ```bash
    python -m venv .venv
    ```
    If using VSCode, the venv will automatically activate for you
5. Install packages for venv

    ```bash
    pip install -r requirements.txt
    ```
6. Run [e.py](preprocess/e.py)
    - you probably need a different rule for extracting `anime` - `episode` : `title` from youtube_title if the current method doesn't fit
    - the example fps is 2 frames per second and having a jpg quality of 5, feel free to adjust
    - the frames will be stored in Frames directory
7. Once `playlist.csv` is created, run [writedb.py](preprocess/writedb.py)
    - the df1 df2 df3 code block is for rearranging episode order, you can ignore if not needed
8. Create a database and a table from your DB choice. For the table (storing posting information), you can have the schema like this:

    ```sql
    DROP TABLE IF EXISTS db.anime_name;
    /*!40101 SET @saved_cs_client     = @@character_set_client */;
    /*!50503 SET character_set_client = utf8mb4 */;
    CREATE TABLE db.anime_name (
    `id` int NOT NULL AUTO_INCREMENT,
    `episode` varchar(10) NOT NULL,
    `title` varchar(200) NOT NULL,
    `frame_start` int NOT NULL,
    `frame_end` int NOT NULL,
    `filename` varchar(100) NOT NULL,
    `post_time` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uniq_episode_frame` (`filename`)
    ) ENGINE=InnoDB AUTO_INCREMENT=262141 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    ```
9. Import `df.csv` into the table

### Get Meta Graph API Page Access Token
1. Create an app in [Facebook Developer](https://developers.facebook.com/apps)
2. Add use cases for facebook page, at least `pages_show_list`, `pages_read_engagement` and `pages_manage_posts` are required
3. Go to [Meta Business Suite](https://business.facebook.com/). Click the cog icon in the bottom left and then click pages from account, link your facebook page and grant yourself total control
4. Create a system user granting him full control for both app and page
5. Generate a system user access token: choose the app linking to your page, token expiration never, grant necessary use cases and finally copy the token
6. Go to [Graph API Test Tool](https://developers.facebook.com/tools/explorer/) then GET ... me/accounts, this shows up the pages that this system user has a role on. Locate `access_token` inside the curly brackets, check the name is the dedicated facebook page and then copy `access_token`
7. Paste the access token into [Graph API Access Token Debug Tool](https://developers.facebook.com/tools/debug/accesstoken/) and check if the token type is Page and the expiration date is Never. The never-expired access token, page id and app id are needed for bot setup

### Get Sentry DSN
1. Sign up for [Sentry.io](https://sentry.io/)
2. Get Sentry DSN from [the instruction](https://docs.sentry.io/concepts/key-terms/dsn-explainer/#where-to-find-your-data-source-name-dsn). The DSN is needed for the bot setup

### Bot Setup
1. Copy and paste SQL connection information  facebook-related token, id and sentry dsn into .env (`HOST`, `USER`,...), (`PAGE_ACCESS_TOKEN`, `PAGE_ID`, `APP_ID`), (`SENTRY_DSN`)<br>if you are deploying this on Ubuntu Linux, keep `HOST` empty
2. Adjust post interval (in seconds) in config.py if needed, the default is 600

## Run Bot on Windows
```bash
python job_scheduler.py
```

## Deploy on Ubuntu Linux
MySQL server (or any other DBMS) should be installed directly on the machine
1. install python3.12, pip3, venv and activate venv

    ```bash
    sudo apt update
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.12 python3-pip python3-venv

    python3 -m venv .venv
    ```
2. install packages for venv

    ```bash
    pip3 install -r requirements.txt
    ```
3. do step 6-7 at [Frame Preprocess and Environment Preparation](#frame-preprocess-and-environment-preparation) section
4. install mysql server

    ```bash
    sudo apt update
    sudo apt install mysql-server
    ```
5. set root password and secure installation

    ```bash
    sudo mysql_secure_installation
    ```
6. start service and login

    ```bash
    sudo systemctl start mysql
    sudo mysql
    ```
7. import df.csv into the table

    ```sql
    LOAD DATA INFILE 'df.csv'
    INTO TABLE db.table
    FIELDS TERMINATED BY ',' 
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
    ```
8. have your access tokens and sentry DSN from [Get Meta Graph API Page Access Token](#get-meta-graph-api-page-access-token) and [Get Sentry DSN](#get-sentry-dsn) sections and put them in .env file
9. run ```python3 job_scheduler.py```

## Deploy on Docker
Make sure you have finished step 1-8 [above](#deploy-on-ubuntu-linux)

1. allow connection from container

    ```sql
    CREATE USER 'your_user'@'172.17.0.%' IDENTIFIED BY 'your_password';
    GRANT ALL PRIVILEGES ON your_db.* TO 'your_user'@'172.17.0.%';
    FLUSH PRIVILEGES;
    ```
2. exit mysql and run ```sudo ufw allow 3306/tcp``` to allow connection from outside, ```hostname -I``` to get your machine IP address and change `HOST` value with the address in .env file
3. change `bind-address` to `0.0.0.0` in `/etc/mysql/mysql.conf.d/mysqld.cnf`

### Set up Docker
1. [install docker](https://docs.docker.com/engine/install/ubuntu/)
2. build and wait for container to be built (check cd path)

    ```bash
    docker build -t anime-bot .
    ```
3. run container

    ```bash
    docker run -d --name anime-bot -v $PWD/Frames:/app/Frames anime-bot
    ```

#### Optional but helpful commands for Docker
- check recent posts
    ```bash
    docker logs --tail 20 anime-bot
    ```
- check if posts get published with HTTP 500 (yes, meta graph API is really untrustable)
    ```bash
    docker logs anime-bot 2>&1 | grep -A 1 -B 1 Recovered
    ```

## Example stdout
```
Bot started...
Posting Episode S01E01, File: Frames/S01E01/S01E01_1.jpg
Success: 1: File: Frames/S01E01/S01E01_1.jpg
Posting Episode S01E01, File: Frames/S01E01/S01E01_2.jpg
...
```

## Notes
- If error occurred or you want to stop the bot, hit Ctrl + C in the terminal

## Special Thanks
- [ESFIO](https://www.facebook.com/EverySpongeInOrder)
- [每一個BanG Dream Its Mygo幀](https://www.facebook.com/profile.php?id=61557479721069)
- ChatGPT

## License
[MIT](LICENSE)
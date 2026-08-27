import sentry_sdk
import time
from config import ANIME
from db_function import get_next_frames, mark_posted
from fb_post import post_to_facebook, check_post_if_error

MAX_RETRIES = 3

def job():
    frames = get_next_frames(ANIME, 2)

    if not frames:
        print("All frames posted.")
        return "DONE"

    for frame in frames:
        title = frame["title"]
        episode = frame["episode"]
        frame_num = frame['frame_start']
        total_frames = frame["frame_end"]
        id = frame["id"]
        filename = frame["filename"].rstrip('\r')

        retries = 0

        while retries < MAX_RETRIES:

            try:
                caption = f"{title}\nFrame {frame_num} out of {total_frames}"

                print(f"Posting Episode {episode}, File: {filename}")

                post_to_facebook(filename, caption)

                mark_posted(ANIME, id)

                print(f"Success: {id}: File: {filename}")
                retries = 0
                break
            except Exception as e:
                print(f"ERROR at File: {filename}:", e)

                if check_post_if_error(caption):
                    print("Recovered: Post actually succeeded despite error.")

                    mark_posted(ANIME, id)
                    print(f"Success: {id}: File: {filename}")
                    retries = 0
                    break

                retries += 1

                if retries >= MAX_RETRIES:

                    sentry_sdk.capture_exception(e)

                    print("Scheduler paused due to real error, and retry exhausted")
                    return "ERROR"

                wait_time = 2 ** retries
                print(f"Retrying in {wait_time} seconds")
                time.sleep(wait_time)

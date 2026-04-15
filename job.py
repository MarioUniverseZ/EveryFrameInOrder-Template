import sentry_sdk
from config import ANIME
from db_function import get_next_frames, mark_posted
from fb_post import post_to_facebook

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

        try:
            caption = f"(BOT試營運)\n{title}\nFrame {frame_num} out of {total_frames}"

            print(f"Posting Episode {episode}, File: {filename}")

            post_to_facebook(filename, caption)

            mark_posted(ANIME, id)

            print(f"Success: {id}: File: {filename}")

        except Exception as e:
            print(f"ERROR at File: {filename}:", e)

            sentry_sdk.capture_exception(e)

            print("Scheduler paused due to error.")

            return "ERROR" # 🚨 stop processing remaining frames
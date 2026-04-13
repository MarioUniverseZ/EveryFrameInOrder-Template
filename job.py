import sentry_sdk
from scheduler import scheduler
from db_function import get_next_frame, get_total_frames_for_episode, mark_posted
from fb_post import post_to_facebook

def job():
    frame = get_next_frame()

    if not frame:
        print("All frames posted.")
        scheduler.shutdown()
        return

    episode = frame["episode"]
    frame_num = frame["frame_start"]
    total_frames = get_total_frames_for_episode(episode)

    caption = f"S{episode:02d}E?? - Frame {frame_num} of {total_frames}"
    # ↑ If you want real episode formatting like S01E07,
    # you should store season separately in DB.

    try:
        print(f"Posting Episode {episode}, Frame {frame_num}")

        post_to_facebook(frame["shareable_url"], caption)

        mark_posted(frame["id"])

        print("Success")

    except Exception as e:
        print("ERROR:", e)

        sentry_sdk.capture_exception(e)

        # Pause scheduler on failure
        scheduler.pause()
        print("Scheduler paused due to error.")
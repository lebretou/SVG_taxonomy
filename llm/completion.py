import asyncio
import aiohttp
import time
import gen_prompt
from gen_prompt import generate_prompts
from post_process import save_svg_files, save_csv_files, save_value_files
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

OPENAI_API_KEY = "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"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

class ProgressLog:
    def __init__(self, total):
        self.total = total
        self.done = 0
    
    def increment(self):
        self.done = self.done + 1
    
    def __repr__(self):
        return f"Done runs {self.done}/{self.total}."

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5), before_sleep=print, retry_error_callback=lambda _: None)
async def get_completion(content, session, semaphore, progress_log, index):
    async with semaphore:
        print(f"Processing: {progress_log.done + 1}/{progress_log.total}.")
        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
            # "model": "gpt-3.5-turbo",
            "model": "gpt-4-turbo-preview",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0
        }) as resp:
            if resp.status != 200:
                error_message = await resp.text()
                print(f"Error from API: {error_message}")
                raise Exception(f"Error with status code {resp.status} from API.")
                # return None
            response_json = await resp.json()
            progress_log.increment()
            print(progress_log)
            return (index, response_json["choices"][0]["message"]["content"])

async def get_completion_list(content_list, max_parallel_calls, timeout=100):
    semaphore = asyncio.Semaphore(value=max_parallel_calls)
    progress_log = ProgressLog(len(content_list))
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(timeout)) as session:
        completion_dict = await asyncio.gather(*[get_completion(content, session, semaphore, progress_log, index) for index, content in enumerate(content_list)])
        completion_dict = dict(completion_dict)
        return [completion_dict[i] for i in range(len(content_list))]

async def main():
    prompt_list = generate_prompts("Bar Plot", "Find Anomalies", "unlabeled", "../images/bar/easy_unlabeled")
    start_time = time.perf_counter()
    # completion_list = await get_completion_list(["Ping", "Pong"], 100, 1000)

    completion_list = await get_completion_list(prompt_list, 100, 1000)
    print("Time elapsed: ", time.perf_counter() - start_time, "seconds.")


    # Save the files
    save_svg_files(completion_list, "../results/bar/anomaly/easy_unlabeled", "bar_anomaly")
    # save_csv_files(completion_list, "../results/bar/filter/easy_unlabeled", "bar_filter")
    # save_value_files(completion_list, "../results/bar/range/easy_labeled", "bar_range.txt")


if __name__ == '__main__':
    asyncio.run(main())

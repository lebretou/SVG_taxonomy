import asyncio
import aiohttp
import time
import gen_prompt
from gen_prompt import generate_prompts
from post_process import save_svg_files

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
async def get_completion(content, session, semaphore, progress_log):
    async with semaphore:

        print(f"Processing: {progress_log.done + 1}/{progress_log.total}.")

        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
            # "model": "gpt-3.5-turbo",
            "model": "gpt-4-0125-preview",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0
        }) as resp:
            if resp.status != 200:
                # Log the error or handle it accordingly
                error_message = await resp.text()  # Get the text of the response
                print(f"Error from API: {error_message}")
                return None  # Or handle the error as appropriate for your application

            response_json = await resp.json()

            progress_log.increment()
            print(progress_log)

            return response_json["choices"][0]["message"]["content"]

async def get_completion_list(content_list, max_parallel_calls, timeout=100):
    semaphore = asyncio.Semaphore(value=max_parallel_calls)
    progress_log = ProgressLog(len(content_list))

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(timeout)) as session:
        return await asyncio.gather(*[get_completion(content, session, semaphore, progress_log) for content in content_list])

async def main():

    # Generate the prompts
    prompt_list = generate_prompts("Scatter Plot", "Clustering", "./images/scatter")
    # print(prompt_list)


    start_time = time.perf_counter()
    completion_list = await get_completion_list(prompt_list, 100, 1000)  # Adding a timeout value, which was missing
    print("Time elapsed: ", time.perf_counter() - start_time, "seconds.")
    # print(completion_list)

    # Save the SVG files
    save_svg_files(completion_list, "./results/scatter/cluster", "scatter_clustering")

if __name__ == '__main__':
    asyncio.run(main())

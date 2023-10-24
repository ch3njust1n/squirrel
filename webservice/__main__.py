import os
import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
from .assistant import review_pull_request

routes = web.RouteTableDef()

router = routing.Router()


@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register("pull_request", action="synchronize")
async def pull_request_synchronize_event(event, gh, *args, **kwargs):
    base_url = event.data["pull_request"]["url"]
    repo_url = "/".join(base_url.split("/")[:-2])
    pull_number = event.data["pull_request"]["number"]
    url = f"{repo_url}/pulls/{pull_number}/files"

    headers = {
        "Authorization": f"token {os.getenv('GH_AUTH')}",
        "Accept": "application/vnd.github.v3+json",
    }

    comment = {"body": "", "event": "COMMENT"}

    # Get files from PR
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        files = await response.json()

        if response.status == 200:
            for file in files:
                filename = file["filename"]
                comment["body"] += f"{filename}\n" + await review_pull_request(
                    filename, file["patch"]
                )
        else:
            print(f"Failed to get files. Response: {files}")

    # Post comment on PR
    async with aiohttp.ClientSession() as session:
        post_url = f"{repo_url}/pulls/{pull_number}/reviews"
        response = await session.post(post_url, headers=headers, json=comment)

        if response.status == 201:
            print("Comment posted successfully")
        else:
            print(f"Failed to post comment.")


@routes.post("/")
async def main(request):
    """
    This function is triggered whenever a pull request is updated.
    It fetches the updated files and prints out the file name and the changes made.
    """
    body = await request.read()

    secret = os.environ.get("GH_WEBHOOK_SECRET")
    oauth_token = os.environ.get("GH_AUTH")
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "ch3njust1n", oauth_token=oauth_token)
        await router.dispatch(event, gh)

    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = int(os.getenv("PORT"))
    if port is not None:
        port = int(port)

    web.run_app(app, host="0.0.0.0", port=port)

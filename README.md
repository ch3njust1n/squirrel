<p align="center">
    <img src="/assets/logo.jpeg" width="200" height="200" align="left"> 
    <h1>SQUIRREL: Software Quality Under Integrated Review, Revision, Evaluation, and Learning</h1>
</p>
<br/>
<br/>


## Setup
1. Generate a GitHub access token.
2. Create your LLM api key with your prefered service. For development, this repo uses Anthropic's Claude.
3. If not already in the repo, add `Procfile` to the root of the repo, which is require for Heroku.
    - The file should contain `web: python3 -m webservice`.
4. Create a Heroku account.
    - Under `Deploy/Deployment Method`, connect your GitHub repo.
    - Under `Settings/Config Vars`, click `Reveal Config Vars` and add your envrionment variables: 
        - `GH_AUTH` - GitHub access token.
        - `GH_WEBHOOK_SECRET`: A random string. You can generate a random string offline with a tool like [cuddly-succotash](https://github.com/ch3njust1n/cuddly-succotash).
        - `ANTHROPIC_API_KEY`: Anthropic key
    - In the top-right corner of the dashboard, click `Open app` and copy the Payload URL.
5. Create a GitHub Webhook. In your repo, go to `Settings/Webhook` and click `Add webhook`.
    - Under `Payload URL`, add your Heroku Payload URL.
    - Under `Content type`, select `application/json`.
    - Under the `Which events would you like to trigger this webhook?`, select `Let me select individual events.` and select the functionalities you want to enable.
6. Head back to Heroku.
    - Under `Manual deploy`, select the branch you want to deploy and click `Deploy Branch`.


![system-diagram](/assets/github.png)


## Current Capabilities
- Reviewing Pull Requests - On each commit, the bot will review the code patch and give feedback on the pull request.
- Automatic reply to issues - When an issue is opened, it will reply with a comment.

## Extending the system

**Using other LLMS**
Add your LLM generation call to `assistant.py` by extending `get_completion()`.

**Extending the GitHub Capabilities**
1. Add new functionality to `assistant.py`.
2. Your new function must be `async`.
3. Prompt the model appropriately for the given task.
4. End the function with `return await get_completion(prompt)`.
5. When calling your new function, remember to `await` the call.


## References
1. [GitHub REST API documentation](https://docs.github.com/en/rest?apiVersion=2022-11-28)
2. [Webhooks documentation](https://docs.github.com/en/webhooks#events)
3. [Gitgethub](https://gidgethub.readthedocs.io/en/latest/index.html)
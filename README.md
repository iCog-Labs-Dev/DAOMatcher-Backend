# DAOMatcher project's backend

## Project setup

- Makesure you have python 3.8 or above installed
- Makesure you have python venv installed
- Makesure you have set `.env` in the same format given in the `.env.example`
- Run the script `./setup` and that's it
- Make a post request to http://localhost:5000 with the following format
- The `depth` field is used to increase the relevance of the results, but this would increase the time it takes to process the users.
```
{
      "query":"Politics",
      "user_list":["@example@server", "{LinkedIn public identifier}"],
      "user_limit":5,
      "depth": 10
}
```

- Use the `@example@server.subserver` for Mastodon
   > Example mastodon handle:  `@MarkRuffalo@mastodon.social`
- LinkedIn public identifier is the last part of the profile url for LinkedIn example:

  > LinkedIn Profile url: `https://www.linkedin.com/in/yeabsesra-ic-4859b5287/`
  >
  > LinkedIn Public Identifier: `yeabsesra-ic-4859b5287`

## WSS

- You can either wait for the server to finish with the process or connect to websocket on the `update` event from your client to get live updates from the server. To get updates from the `wss` web socket you must initiate the request using the `get_users` event on the websocket server in the first place.

## Docker

- You can also use Docker to setup everything locally and run the application.
  **Docker build and tag**

  ```
  docker  build -t daomatcher:latest .
  ```

  **Docker run**

  ```
   docker run -it daomatcher:latest
  ```

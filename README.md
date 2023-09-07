# DAOMatcher project's backend

## Project setup

- Makesure you have python 3.8 or above installed
- Makesure you have python venv installed
- Makesure you have set `.env` in the same format given in the `.env.example`
- Run the script ./setup and that's it
- If you are not mac or debian user, install `redis-server` and run the ./setup server
- Make a post request to http://localhost:5000 with the following format
  > ```
  >
  > ```
      {
      "query":"Politics",
      "user_list":["@example@server", "https://www.linkedin.com/in/{linkedIn public identifier}/"],
      "user_limit":5
  }```

## SSE

- You can either wait for the server to finish with the process or register SSE on your client at `http://localhost:5000/stream` to get live updates from the server

# DAOMatcher Backend

This is the backend server for the DAOMatcher project. Follow the instructions below to set up and run the server locally.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Python](https://www.python.org/downloads/) (version 3.11)
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency management and virtual environments)
- [Python venv](https://docs.python.org/3/library/venv.html) (virtual environment module)

## Getting Started

1. **Clone the Repository**

   Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/your-username/DAOMatcher-backend.git
   ```

2. **Navigate to the Project Directory**

   Change to the project directory:

   ```bash
   cd DAOMatcher-backend
   ```

3. **Install Dependencies**

   Install the project dependencies using Poetry:

   ```bash
   poetry install
   ```

4. **Activate the Virtual Environment**

   Activate the virtual environment:

   ```bash
   poetry shell
   ```

5. **Set Up Environment Variables**

   Copy the `.env.example` file to `.env` and update the values as needed:

   ```bash
   cp .env.example .env
   ```

   Open the `.env` file and set the appropriate values for your environment.

6. **Run the Setup Script**

   Run the setup script to initialize the project and run the server:

   ```bash
   ./setup
   ```

## WebSocket Support (WSS)

You can either wait for the server to finish processing or connect to the WebSocket on the `update` event from your client to get live updates from the server. To get updates from the WebSocket, you must initiate the request using the `get_users` event on the WebSocket server first.

## Running Tests

The project includes model-based evaluation tests to assess prompt efficiency. To run the tests, follow these steps:

1. **Activate the Virtual Environment** (if not already activated):

   ```bash
   poetry shell
   ```

2. **Run the Tests**

   Run the tests using pytest:

   ```bash
   pytest test_model_graded_eval.py
   ```

   To see more detailed output, use:

   ```bash
   pytest test_model_graded_eval.py -s
   ```

## Docker

You can also use Docker to set up everything locally and run the application.

**Docker build and tag**

```bash
docker build -t daomatcher:latest .
```

**Docker run**

```bash
docker run -it daomatcher:latest
```

---

Feel free to reach out if you have any questions or encounter any issues.

Happy coding!

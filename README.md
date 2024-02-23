# Chaturbate API Integration

This project provides an integration with the Chaturbate API, allowing for the polling of various events such as broadcast starts, user entries, and more. It uses async for event handling.

## Features

- Polling Chaturbate API for real-time events
- Handling of various event types, including broadcast starts/stops, user entries/exits, follows/unfollows, chat messages, and tips
- Extensible event handling system

## Installation

Ensure you have Python 3.8+ installed on your machine. Then, you can install the package and its dependencies using the following command:

```
pip install -r requirements.txt
```

## Usage

To use this integration, you'll need to set up your environment with the necessary API URL. Create a `.env` file in the root directory with the following content:

```
EVENTS_API_URL=your_chaturbate_api_url_here
```

Replace `your_chaturbate_api_url_here` with the actual API URL provided by Chaturbate.

To start the application, run:

```
python runner.py
```

This will initiate the polling process, and you'll begin receiving events based on the configured handlers.

## Development

To contribute to this project or modify it for your needs, clone the repository and install the development dependencies:

```
pip install -e .
```

Run tests to ensure your modifications don't break existing functionality:

```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.


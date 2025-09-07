# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Intervals-mcp-server is a Model Context Protocol (MCP) server for connecting Claude with the Intervals.icu API. It provides tools for authentication and data retrieval for athlete activities, events, and wellness data.

## Development Commands

### Environment Setup

```bash
# Create and activate virtual environment
uv venv --python 3.12
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows

# Install dependencies
uv sync --all-extras  # Includes development dependencies
```

### Running the Server

```bash
# Run the server manually (for development)
uv run mcp run src/intervals_mcp_server/server.py

# Install the server for Claude Desktop
uv run mcp install src/intervals_mcp_server/server.py --name "Intervals.icu" --with-editable . --env-file .env
```

### Testing

```bash
# Run all tests
uv run pytest -v tests

# Run a specific test file
uv run pytest -v tests/test_server.py

# Run a specific test
uv run pytest -v tests/test_server.py::test_function_name
```

### Code Quality

```bash
# Linting
uv run ruff .

# Type checking
uv run mypy src tests
```

## Project Structure

- `src/intervals_mcp_server/server.py`: Main entry point containing the FastMCP server implementation with all MCP tools
- `src/intervals_mcp_server/utils/formatting.py`: Utilities for formatting API responses
- `src/intervals_mcp_server/utils/types.py`: Type definitions for workout steps and related data
- `tests/`: Unit tests for the server and utility functions

## Architecture

The intervals-mcp-server follows a straightforward architecture:

1. **FastMCP Server**: The main entry point that defines MCP tools as async functions
2. **API Communication**: All requests to Intervals.icu API go through the `make_intervals_request()` function
3. **Data Formatting**: Utility functions in `formatting.py` convert API responses to user-friendly text
4. **Error Handling**: Comprehensive error handling with user-friendly messages
5. **Environment Configuration**: Configuration via environment variables with validation on startup

## MCP Tools

The server exposes the following MCP tools:

- `get_activities`: Retrieve a list of activities
- `get_activity_details`: Get detailed information for a specific activity
- `get_activity_intervals`: Get detailed interval data for a specific activity
- `get_wellness_data`: Fetch wellness data
- `get_events`: Retrieve upcoming events (workouts, races, etc.)
- `get_event_by_id`: Get detailed information for a specific event
- `add_or_update_event`: Create or update an event
- `delete_event`: Delete a specific event
- `delete_events_by_date_range`: Delete events within a date range

## Development Guidelines

1. **API Communication**: All API requests should go through the `make_intervals_request()` function
2. **Error Handling**: Handle errors consistently using the established patterns
3. **Formatting**: Use the formatting utilities for consistent outputs
4. **Testing**: Add unit tests for new functionality
5. **Type Hints**: Use proper type hints for all functions and variables
6. **Documentation**: Add comprehensive docstrings for all functions

## Environment Variables

- `API_KEY`: Intervals.icu API key (required)
- `ATHLETE_ID`: Athlete ID (required, can be numeric or i-prefixed)
- `INTERVALS_API_BASE_URL`: API base URL (optional, defaults to "https://intervals.icu/api/v1")
- `LOG_LEVEL`: Logging level (optional, defaults to INFO)
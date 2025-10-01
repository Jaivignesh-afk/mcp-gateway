Overview
This repository contains a Dockerized MCP Gateway configured to proxy a NASDAQ Data Link MCP server, along with a Python async client that initializes an MCP session, enumerates available tools, and calls an example tool via Server-Sent Events (SSE).
The client connects to the gateway at http://localhost:8080/nasdaq/sse and demonstrates a sample call to a tool named list_stock_stat_fields with empty arguments.

Architecture
The docker-compose.yml defines two services: mcp-gateway (exposed on host port 8080) and nasdaq-mcp (exposed on host port 8081, mapping to the container’s 8080), forming a simple gateway-to-backend topology.
gateway.yaml configures a server entry nasdaq-data-link pointing to http://nasdaq-mcp:8080/sse with transport type sse and signature verification enabled, enabling the gateway to route SSE traffic to the backend MCP server over the internal Docker network.

File structure
test.py — Async Python example client using mcp.ClientSession over SSE to initialize a session, list tools, and call an example tool.

docker-compose.yml — Orchestrates mcp-gateway and nasdaq-mcp services, ports, environment, command flags, volumes, and secrets.

gateway.yaml — Gateway server configuration binding nasdaq-data-link to the nasdaq-mcp service via SSE with signature verification.

Prerequisites
Docker and Docker Compose are required since orchestration and service configuration are defined in docker-compose.yml.
Python with a module providing the mcp package is required to run the example client in test.py that imports mcp and mcp.client.sse.
A NASDAQ Data Link API key must be supplied either via NASDAQ_API_KEY environment variable or the nasdaq_data_link_api_key.txt secret described in the compose configuration.

Setup
Place gateway.yaml under a local ./config directory so it mounts into the gateway container at /config/gateway.yaml, matching the mcp-gateway command flag and volume mapping in docker-compose.yml.
Create a nasdaq_data_link_api_key.txt file containing the NASDAQ Data Link API key to back the my_secret secret declared in the compose file if using the provided secret workflow.

Run with Docker
Start the stack with docker compose up -d to launch mcp-gateway on host port 8080 and nasdaq-mcp on host port 8081 as defined by the ports section.

The gateway will route /nasdaq over SSE to nasdaq-mcp using the server name nasdaq-data-link and the configuration provided via --servers and /config/gateway.yaml.

NASDAQ_DATA_LINK_API_KEY is passed to both gateway and backend via environment, with an optional secret my_secret defined for file-based key provisioning.

Run the Python client
Install dependencies so that the mcp module and mcp.client.sse are importable, since test.py imports these symbols to establish an SSE client and MCP session.
Run python test.py to initialize the session, list available tools, and call the example tool list_stock_stat_fields with empty arguments against http://localhost:8080/nasdaq/sse.
The script prints tool metadata from the list_tools response and then prints the result content of the example tool call for quick verification.

Configuration details
mcp-gateway uses the image docker/mcp-gateway:latest, binds 8080:8080, mounts ./config:/config, and is started with flags including --transport=sse, --servers=nasdaq-data-link, --port=8080, --verbose=true, and --config=/config/gateway.yaml.
nasdaq-mcp uses the image mcp/nasdaq-data-link:latest, maps 8081:8080, and also expects NASDAQ_DATA_LINK_API_KEY from the environment for backend access to the data service.
gateway.yaml enables verify_signatures: true to enforce signature checks while routing SSE traffic to http://nasdaq-mcp:8080/sse under the nasdaq-data-link server entry.

Troubleshooting
If list_tools returns no entries or tool calls fail, verify that NASDAQ_DATA_LINK_API_KEY is available via NASDAQ_API_KEY env mapping or backed by the nasdaq_data_link_api_key.txt secret as configured in Docker Compose.
Ensure the gateway config is accessible at /config/gateway.yaml inside the gateway container by confirming the ./config mount and the --config flag alignment in the compose file.
Confirm the client target URL is http://localhost:8080/nasdaq/sse and that both containers are running and listening on the expected ports defined in docker-compose.yml.

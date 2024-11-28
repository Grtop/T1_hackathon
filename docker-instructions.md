# Docker Setup Instructions

To run this application using Docker, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your system.

2. Open a terminal in the project root directory.

3. Build and start the container:
```bash
docker-compose up --build
```

4. The application will be available at `http://localhost:5000`

5. To stop the application:
```bash
docker-compose down
```

Note: The application is configured to:
- Run on port 5000
- Automatically restart if it crashes
- Use a volume mount to reflect code changes without rebuilding
- Include all necessary Python dependencies
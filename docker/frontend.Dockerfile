FROM node:20-alpine

WORKDIR /app/frontend

# Install dependencies only (no build). Source code will be bind-mounted in compose.
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

EXPOSE 3000

# Default environment; can be overridden at runtime (e.g. APP_ENV=production)
ENV APP_ENV=development

COPY frontend/entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Default command delegates to entrypoint, which chooses dev or prod based on APP_ENV.
CMD ["./entrypoint.sh"]

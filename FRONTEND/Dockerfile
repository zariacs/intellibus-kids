# 1️⃣ Build Stage: Build the Next.js app
FROM node:23.10.0 AS builder

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first (to leverage Docker caching)
COPY package.json ./

# Install dependencies
RUN npm install

# Copy the rest of the project files
COPY . .

# ✅ Set environment variables at build time
ARG NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
ENV NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}

# Clear Next.js cache before building
RUN rm -rf .next node_modules/.cache

# Build the Next.js app
RUN npm run build

# 2️⃣ Production Stage: Run the built app in a lightweight image
FROM node:23.10.0-slim

# Set working directory
WORKDIR /app

# Copy built files from the previous stage
COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/.next /app/.next
COPY --from=builder /app/node_modules /app/node_modules

# Expose Next.js default port
EXPOSE 3000

# Start Next.js in production mode
CMD ["npm", "run", "start"]
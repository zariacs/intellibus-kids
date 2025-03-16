# 1️⃣ Build Stage: Build the Next.js app
FROM node:23.10.0-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first (to leverage Docker caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --frozen-lockfile

# Copy the rest of the project files
COPY . .

# Build the Next.js app
RUN npm run build

# 2️⃣ Production Stage: Run the built app in a lightweight image
FROM node:23.10.0-alpine

# Set working directory
WORKDIR /app

# Set environment to production for optimization
ENV NODE_ENV=production

# Copy only necessary files from builder stage
COPY --from=builder /app/package.json /app/package-lock.json ./
COPY --from=builder /app/.next /app/.next

# Install only production dependencies
RUN npm install --frozen-lockfile --production

# Expose Next.js default port
EXPOSE 3000

# Start Next.js in production mode
CMD ["npm", "run", "start"]

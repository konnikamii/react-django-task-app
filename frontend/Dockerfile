FROM node:latest
 
# Set working directory
WORKDIR /app

# this will allow us to run vite and other tools directly
ENV PATH /app/node_modules/.bin:$PATH

# Install debug tools
RUN apt-get update && apt-get install -y \
  curl \
  wget \
  net-tools \
  vim \
  bash\
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY package*.json ./

# Remove cached or broken node_modules if they exist (Optional)
# RUN rm -rf node_modules package-lock.json 

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose port and start the application
EXPOSE 3000 24678 
EXPOSE 80
EXPOSE 443

CMD ["npm", "run", "dev", "--host"]
# CMD ["npm", "run", "dev", "--host"]
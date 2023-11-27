FROM python:3.10.10-alpine

# Switch working directory
WORKDIR /app

# Copy the requirements file for Python
COPY ./requirements.txt /app/requirements.txt

# Copy the entire application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js 18 and Yarn
RUN apk add --no-cache nodejs-current npm yarn

# Install Node.js dependencies using Yarn
RUN yarn install

# Set the default command to run the application with yarn server
CMD ["yarn", "server"]

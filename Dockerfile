# Use Apify's Python actor base image
FROM apify/actor-python:3.11

# Copy source code
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run actor
CMD ["python", "src/actor.py"]

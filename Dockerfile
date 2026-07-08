# ប្រើប្រាស់ Python 3.11 ជំនាន់ស្រាល (slim) ធ្វើជាមូលដ្ឋាន
FROM python:3.11-slim

# កំណត់ទីតាំងធ្វើការងារ (Working Directory)
WORKDIR /app

# ដំឡើង System Dependencies ដែលត្រូវការមួយចំនួន
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ចម្លងឯកសារ requirements.txt ចូល
COPY requirements.txt .

# ដំឡើង Python Libraries ទាំងអស់
RUN pip install --no-cache-dir -r requirements.txt

# ដំឡើង Playwright Browser (Chromium) និង Dependencies ដែលពាក់ព័ន្ធរបស់វា
RUN playwright install chromium
RUN playwright install-deps chromium

# ចម្លងកូដ Bot ទាំងស្រុងចូលទៅក្នុង Container
COPY bot.py .

# បញ្ជាឲ្យដំណើរការកូដ
CMD ["python", "bot.py"]

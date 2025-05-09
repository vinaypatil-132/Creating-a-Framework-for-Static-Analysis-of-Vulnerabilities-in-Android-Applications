FROM python:3.11-slim

WORKDIR /app

COPY analyzer.py app.py ./
COPY templates/ templates/
COPY uploads/ uploads/
COPY reports/ reports/
COPY results/ results/
COPY permissions_pie_chart.png permissions_pie_chart.png

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# run the application
CMD ["python","app.py"]

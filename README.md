A Flask-based web application that aggregates and displays research papers from multiple sources (like arXiv, IEEE, Springer etc. via APIs or scraping). It allows users to search, filter, and explore papers easily through a clean web interface.
🚀 Features
•	🔍 Search by keyword – find papers by title, abstract, or author.
•	🏷️ Filter results – by year, category, or source.
•	📑 View paper details – title, authors, abstract, publication year, and links to the full text.
•	🌐 Lightweight backend – built with Flask.
•	🎨 Simple UI – powered by HTML, CSS, and templates.
🛠️ Tech Stack
•	Backend: Flask (Python 3.11)
•	Frontend: HTML, CSS
•	Data: Requests, BeautifulSoup, Feedparser, NLTK, PyPDF2, NetworkX
•	Environment: Virtualenv
📂 Project Structure
Research_Paper_Aggregator/
│── backend/
│   │── app.py              # Flask app entry point
│   │── scraper.py          # Fetch & parse papers (APIs/web scraping)
│   │── requirements.txt    # Dependencies
│   │── templates/          # HTML templates (index.html, results.html)
│   │── static/             # CSS, JS, images
│── README.md               # Project documentation
⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/AnushkaGoswami-tech/Research_Paper_Aggregator.git
cd Research_Paper_Aggregator/backend

👉 Or just click here: https://github.com/AnushkaGoswami-tech/Research_Paper_Aggregator
2. Create a virtual environment
python3.11 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
4. Run the application
python app.py
5. Open in browser
👉 Visit: http://127.0.0.1:5000/
📦 Requirements (requirements.txt)
Flask==3.0.3
Werkzeug==3.0.3
flask-cors==4.0.1
requests==2.32.3
feedparser==6.0.11
nltk==3.9.1
networkx==3.3
PyPDF2==3.0.1
🔮 Future Enhancements
•	🔑 User authentication (save & bookmark papers)
•	🤖 ML-based recommendation system
•	📊 Visualization of research trends
•	☁️ Deployment on Heroku / AWS / Azure
👨‍💻 Author
Anushka Goswami
GitHub: https://github.com/AnushkaGoswami-tech
![Uploading image.png…]()

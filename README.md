# 🧳 Weekend Getaway Ranker

A Python-based recommendation system that ranks tourist destinations for short trips based on **distance (approximated), rating, and popularity**, using India’s *Must-See Places* dataset.

This project is implemented as a **Data Engineering assignment**, focusing on data preprocessing, feature engineering, and ranking logic.

---

## 📌 Project Objective

The goal of this project is to recommend the **top weekend getaway destinations** for a given **source city** by analyzing:

- ⭐ Google review ratings  
- 🔥 Popularity (number of Google reviews)  
- 📍 Distance approximation using administrative hierarchy  

---

## 📂 Dataset Description

The dataset contains information about popular tourist places across India.

### Important Columns Used
- `Name` – Tourist place name  
- `City` – City where the place is located  
- `State` – State  
- `Zone` – Geographic zone of India  
- `Google review rating` – Rating (scale: 1–5)  
- `Number of google review in lakhs` – Popularity indicator  

⚠️ The dataset does **not** include latitude and longitude values.

---

## 🧠 Algorithm Details

### Distance Approximation Logic

Since the dataset does not contain geospatial coordinates, **distance is approximated using administrative hierarchy**.

| Condition | Approx. Distance |
|---------|------------------|
| Same City | ~10 km (Local exploration) |
| Same State | ~150 km (Ideal weekend trip) |
| Same Zone | ~500 km (Extended weekend trip) |
| Different Zone | ~1500 km (Long-distance travel) |

This heuristic provides a practical and explainable proxy for distance.

---

### Ranking Strategy

Each destination is assigned a ranking score based on the following weighted factors:

- **Distance (heuristic): 40%**
- **Google Review Rating: 40%**
- **Popularity: 20%**

#### Popularity Normalization
Popularity values are log-normalized to reduce bias from extremely popular places:
```python
log_reviews = log(1 + number_of_reviews)
```
This ensures balanced influence in the ranking.

---

## 🛠️ Technologies Used

- Python 3  
- Pandas  
- NumPy  

---

## 📁 Project Structure

Weekend-Getaway-Ranker/
│
├── data/
│   └── travel_places.csv
│
├── weekend_getaway_ranker.py
│
├── README.md
│
├── sample_output.txt
│
└── requirements.txt

---

## ⚙️ Installation & Execution

Follow the steps below to run the project locally.

### Step 1: Clone the Repository
```bash
git clone [ github repo link of this project ](https://github.com/purkait03/Weekend-Getaway-Ranker.git)
cd weekend-getaway-ranker
pip install -r requirements.txt
python weekend_ranker.py
```

---

The script runs with predefined test cities:
```python
    test_cities = ['Kolkata', 'New Delhi', 'Bengaluru']
```
To test with different cities, open weekend_ranker.py in a text editor and modify the test_cities list at the bottom of the file:
```python
    test_cities = ['Puri', 'Chennai', 'Jaipur'] 
```

---

## 👤 Author

Sougata Purkait
Final Year Computer Science Engineering Student
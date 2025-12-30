import pandas as pd
import numpy as np
import sys

class WeekendGetawayRanker:
    def __init__(self, data_path):
        """
        Initialize the ranker with the dataset.
        """
        try:
            self.df = pd.read_csv(data_path)
        except FileNotFoundError:
            print(f"Error: File {data_path} not found.")
            sys.exit(1)
            
        self.preprocess()
        self.max_log_reviews = self.df['log_reviews'].max()

    def preprocess(self):
        """
        Clean and prepare the data:
        - Standardize city names (e.g., Bangalore -> Bengaluru).
        - Convert numeric columns to appropriate types.
        - Create normalized popularity metrics.
        """
        # Standardize City Names to handle common variations
        city_map = {
            'Delhi': 'New Delhi',
            'Bangalore': 'Bengaluru',
            'Gurgaon': 'Gurugram',
            'Bombay': 'Mumbai',
            'Calcutta': 'Kolkata',
            'Madras': 'Chennai'
        }
        self.df['City'] = self.df['City'].replace(city_map)
        
        # specific fix for 'New Delhi' logic if needed (dataset has 'Delhi' and 'New Delhi')
        # We merge them to 'New Delhi'
        self.df.loc[self.df['City'] == 'Delhi', 'City'] = 'New Delhi'

        # Ensure numeric types and handle missing values
        self.df['Google review rating'] = pd.to_numeric(self.df['Google review rating'], errors='coerce').fillna(0)
        self.df['Number of google review in lakhs'] = pd.to_numeric(self.df['Number of google review in lakhs'], errors='coerce').fillna(0)
        
        # Calculate Log Popularity to reduce skew from very popular places
        # We use log(x+1) to handle zeros
        self.df['log_reviews'] = np.log1p(self.df['Number of google review in lakhs'])

    def calculate_heuristic_distance(self, row, source_city, source_state, source_zone):
        """
        Estimate distance based on administrative hierarchy since 
        lat/long coordinates are not available.
        """
        if row['City'] == source_city:
            return 10  # Local (Same City)
        elif row['State'] == source_state:
            return 150 # Weekend Trip (Same State)
        elif row['Zone'] == source_zone:
            return 500 # Extended Trip (Same Zone)
        else:
            return 1500 # Long Distance (Different Zone)

    def get_recommendations(self, source_city, k=5):
        """
        Rank top k weekend destinations.
        Ranking Score = w1*Rating + w2*Popularity + w3*Proximity
        """
        # specific normalization for input
        input_city = source_city.title()
        city_map = {'Delhi': 'New Delhi', 'Bangalore': 'Bengaluru', 'Bombay': 'Mumbai'}
        input_city = city_map.get(input_city, input_city)

        # Get Source Context
        source_row = self.df[self.df['City'] == input_city]
        if source_row.empty:
            return None, f"Source City '{source_city}' not found in the dataset."
        
        # Use the first match to determine State and Zone
        source_state = source_row.iloc[0]['State']
        source_zone = source_row.iloc[0]['Zone']

        # Calculate Distance Heuristic
        self.df['est_distance_km'] = self.df.apply(
            lambda row: self.calculate_heuristic_distance(row, input_city, source_state, source_zone), 
            axis=1
        )

        # Ranking Algorithm
        # Weights: 
        # - Distance: 40% (We want weekend getaways, so closer is better)
        # - Rating: 40% (Quality matters)
        # - Popularity: 20% (Social proof)
        
        # Normalize Distance (0 to 1, where 1 is closest)
        # Assuming max practical distance is ~2000km for this scale
        norm_distance = 1 - (self.df['est_distance_km'] / 2000)
        
        # Normalize Rating (0 to 1)
        norm_rating = self.df['Google review rating'] / 5.0
        
        # Normalize Popularity (0 to 1)
        norm_popularity = self.df['log_reviews'] / self.max_log_reviews

        # Calculate Final Score
        self.df['rank_score'] = (0.4 * norm_distance) + (0.4 * norm_rating) + (0.2 * norm_popularity)

        # Sort by Score
        recommendations = self.df.sort_values(by='rank_score', ascending=False).head(k)
        
        return recommendations[['Name', 'City', 'State', 'est_distance_km', 'Google review rating', 'rank_score']], None

if __name__ == "__main__":
    # Example usage
    file_path = 'data/travel_places.csv'
    ranker = WeekendGetawayRanker(file_path)
    
    test_cities = ['Kolkata', 'New Delhi', 'Bengaluru']
    
    print("=== Weekend Getaway Ranker Output ===\n")
    for city in test_cities:
        print(f"--- Top Recommendations for {city} ---")
        recs, error = ranker.get_recommendations(city)
        if error:
            print(error)
        else:
            # Formatting output for readability
            print(recs.to_string(index=False))
        print("\n")
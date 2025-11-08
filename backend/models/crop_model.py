"""
Crop prediction model using rule-based logic.
For demonstration purposes - can be replaced with trained ML models.
"""
from typing import Dict, List, Tuple
import random


class CropPredictor:
    """
    Rule-based crop prediction system.
    Uses agricultural domain knowledge for recommendations.
    """
    
    # Crop requirements database (simplified)
    CROP_REQUIREMENTS = {
        'Rice': {
            'soil_types': ['Alluvial Soil', 'Clay Soil'],
            'n_range': (80, 120),
            'p_range': (40, 60),
            'k_range': (40, 60),
            'ph_range': (5.5, 7.0),
            'temp_range': (20, 30),
            'humidity_range': (60, 80),
            'rainfall_range': (100, 200),
            'regions': ['North India', 'East India', 'South India']
        },
        'Wheat': {
            'soil_types': ['Alluvial Soil', 'Clay Soil', 'Black Soil'],
            'n_range': (80, 120),
            'p_range': (40, 60),
            'k_range': (40, 60),
            'ph_range': (6.0, 7.5),
            'temp_range': (12, 25),
            'humidity_range': (50, 70),
            'rainfall_range': (50, 100),
            'regions': ['North India', 'Central India']
        },
        'Maize': {
            'soil_types': ['Alluvial Soil', 'Red Soil', 'Black Soil'],
            'n_range': (90, 130),
            'p_range': (50, 80),
            'k_range': (50, 80),
            'ph_range': (5.5, 7.5),
            'temp_range': (21, 30),
            'humidity_range': (60, 75),
            'rainfall_range': (60, 120),
            'regions': ['North India', 'South India', 'Central India']
        },
        'Sugarcane': {
            'soil_types': ['Black Soil', 'Alluvial Soil'],
            'n_range': (100, 150),
            'p_range': (50, 90),
            'k_range': (60, 100),
            'ph_range': (6.0, 8.0),
            'temp_range': (21, 27),
            'humidity_range': (70, 90),
            'rainfall_range': (150, 250),
            'regions': ['South India', 'West India']
        },
        'Cotton': {
            'soil_types': ['Black Soil', 'Red Soil'],
            'n_range': (60, 120),
            'p_range': (30, 60),
            'k_range': (30, 60),
            'ph_range': (6.0, 8.0),
            'temp_range': (21, 30),
            'humidity_range': (50, 80),
            'rainfall_range': (50, 100),
            'regions': ['Central India', 'South India', 'West India']
        },
        'Soybean': {
            'soil_types': ['Black Soil', 'Red Soil', 'Alluvial Soil'],
            'n_range': (20, 40),
            'p_range': (40, 80),
            'k_range': (30, 70),
            'ph_range': (6.0, 7.5),
            'temp_range': (20, 30),
            'humidity_range': (60, 80),
            'rainfall_range': (60, 100),
            'regions': ['Central India', 'North India']
        },
        'Peanut': {
            'soil_types': ['Red Soil', 'Laterite Soil'],
            'n_range': (20, 40),
            'p_range': (40, 70),
            'k_range': (30, 60),
            'ph_range': (6.0, 7.0),
            'temp_range': (20, 30),
            'humidity_range': (50, 70),
            'rainfall_range': (50, 100),
            'regions': ['South India', 'West India']
        },
        'Coconut': {
            'soil_types': ['Laterite Soil', 'Alluvial Soil'],
            'n_range': (50, 100),
            'p_range': (30, 60),
            'k_range': (60, 120),
            'ph_range': (5.5, 7.0),
            'temp_range': (22, 32),
            'humidity_range': (70, 90),
            'rainfall_range': (150, 250),
            'regions': ['South India']
        },
        'Lentil': {
            'soil_types': ['Clay Soil', 'Black Soil'],
            'n_range': (20, 40),
            'p_range': (30, 60),
            'k_range': (20, 50),
            'ph_range': (6.0, 7.5),
            'temp_range': (15, 25),
            'humidity_range': (50, 70),
            'rainfall_range': (40, 80),
            'regions': ['North India', 'Central India']
        },
        'Chickpea': {
            'soil_types': ['Clay Soil', 'Black Soil'],
            'n_range': (20, 40),
            'p_range': (30, 60),
            'k_range': (20, 50),
            'ph_range': (6.0, 8.0),
            'temp_range': (20, 30),
            'humidity_range': (50, 70),
            'rainfall_range': (60, 100),
            'regions': ['Central India', 'North India']
        }
    }
    
    def calculate_suitability_score(
        self,
        crop_name: str,
        soil_type: str,
        n_level: float,
        p_level: float,
        k_level: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph_level: float,
        region: str
    ) -> float:
        """Calculate how suitable a crop is for given conditions (0-100)."""
        
        requirements = self.CROP_REQUIREMENTS[crop_name]
        score = 0
        max_score = 8  # Number of factors
        
        # Soil type match (critical factor - worth 2 points)
        if soil_type in requirements['soil_types']:
            score += 2
        
        # NPK levels match (1 point each)
        if requirements['n_range'][0] <= n_level <= requirements['n_range'][1]:
            score += 1
        if requirements['p_range'][0] <= p_level <= requirements['p_range'][1]:
            score += 1
        if requirements['k_range'][0] <= k_level <= requirements['k_range'][1]:
            score += 1
        
        # pH level match
        if requirements['ph_range'][0] <= ph_level <= requirements['ph_range'][1]:
            score += 1
        
        # Temperature match
        if requirements['temp_range'][0] <= temperature <= requirements['temp_range'][1]:
            score += 1
        
        # Humidity match
        if requirements['humidity_range'][0] <= humidity <= requirements['humidity_range'][1]:
            score += 1
        
        # Rainfall match
        if requirements['rainfall_range'][0] <= rainfall <= requirements['rainfall_range'][1]:
            score += 1
        
        # Region match (bonus)
        if region in requirements['regions']:
            score += 1
            max_score += 1
        
        # Convert to percentage and add slight randomness for realism
        percentage = (score / max_score) * 100
        randomness = random.uniform(-2, 2)
        return max(0, min(100, percentage + randomness))
    
    def predict(
        self,
        soil_type: str,
        n_level: float,
        p_level: float,
        k_level: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        ph_level: float,
        region: str
    ) -> Tuple[str, float, List[Dict[str, float]]]:
        """
        Predict the best crop for given conditions.
        
        Returns:
            Tuple of (predicted_crop, confidence_score, alternative_crops)
        """
        
        # Calculate suitability score for each crop
        crop_scores = {}
        for crop_name in self.CROP_REQUIREMENTS.keys():
            score = self.calculate_suitability_score(
                crop_name, soil_type, n_level, p_level, k_level,
                temperature, humidity, rainfall, ph_level, region
            )
            crop_scores[crop_name] = round(score, 1)
        
        # Sort by score
        sorted_crops = sorted(
            crop_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top prediction
        predicted_crop = sorted_crops[0][0]
        confidence_score = sorted_crops[0][1]
        
        # Get alternative crops (top 2-3 alternatives)
        alternative_crops = [
            {"crop": crop, "score": score}
            for crop, score in sorted_crops[1:4]
            if score > 50  # Only include reasonable alternatives
        ]
        
        return predicted_crop, confidence_score, alternative_crops


# Global instance
crop_predictor = CropPredictor()


def predict_crop(
    soil_type: str,
    n_level: float,
    p_level: float,
    k_level: float,
    temperature: float,
    humidity: float,
    rainfall: float,
    ph_level: float,
    region: str
) -> Tuple[str, float, List[Dict[str, float]]]:
    """
    Main prediction function to be called by API endpoint.
    
    Returns:
        Tuple of (predicted_crop, confidence_score, alternative_crops)
    """
    return crop_predictor.predict(
        soil_type, n_level, p_level, k_level,
        temperature, humidity, rainfall, ph_level, region
    )

"""
Yield estimation model using rule-based calculations.
"""
from typing import Dict, Tuple
import random


class YieldEstimator:
    """
    Rule-based yield estimation system.
    Uses environmental and soil parameters to estimate crop yield.
    """
    
    # Base yield potential for each crop (tonnes/hectare)
    BASE_YIELDS = {
        'Rice': 6.0,
        'Wheat': 5.5,
        'Maize': 7.0,
        'Cotton': 2.2,  # Bales
        'Sugarcane': 70.0,
        'Soybean': 2.8,
        'Peanut': 2.5,
        'Coconut': 80.0,  # Nuts per tree (different scale)
        'Lentil': 1.5,
        'Chickpea': 2.0
    }
    
    # Regional average yields (% of base)
    REGIONAL_FACTORS = {
        'North India': 0.85,
        'South India': 0.90,
        'East India': 0.82,
        'West India': 0.80,
        'Central India': 0.88
    }
    
    # Seasonal factors
    SEASONAL_FACTORS = {
        'Kharif': 1.0,   # Monsoon season - best for most crops
        'Rabi': 0.95,    # Winter season
        'Zaid': 0.85     # Summer season
    }
    
    def calculate_climate_factor(
        self,
        crop_type: str,
        temperature: float,
        humidity: float,
        rainfall: float
    ) -> float:
        """Calculate yield factor based on climate conditions (0-1.2)."""
        
        factor = 1.0
        
        # Temperature effects
        if crop_type in ['Rice', 'Maize', 'Sugarcane']:
            # Warm season crops
            if 22 <= temperature <= 30:
                factor += 0.1
            elif temperature < 18 or temperature > 35:
                factor -= 0.2
        elif crop_type in ['Wheat', 'Chickpea', 'Lentil']:
            # Cool season crops
            if 18 <= temperature <= 25:
                factor += 0.1
            elif temperature < 12 or temperature > 30:
                factor -= 0.2
        
        # Humidity effects
        if crop_type == 'Rice':
            if humidity > 70:
                factor += 0.05
        elif crop_type in ['Wheat', 'Chickpea']:
            if 50 <= humidity <= 70:
                factor += 0.05
        
        # Rainfall effects
        if crop_type == 'Rice':
            if rainfall > 100:
                factor += 0.1
            elif rainfall < 80:
                factor -= 0.15
        elif crop_type in ['Wheat', 'Maize']:
            if 60 <= rainfall <= 100:
                factor += 0.1
            elif rainfall < 40 or rainfall > 150:
                factor -= 0.1
        
        return max(0.5, min(1.2, factor))
    
    def calculate_soil_factor(
        self,
        soil_type: str,
        soil_ph: float,
        n_level: float,
        p_level: float,
        k_level: float
    ) -> float:
        """Calculate yield factor based on soil conditions (0-1.2)."""
        
        factor = 1.0
        
        # Soil type factor
        if soil_type in ['Alluvial Soil', 'Black Soil']:
            factor += 0.1
        elif soil_type in ['Laterite Soil', 'Red Soil']:
            factor += 0.05
        
        # pH factor
        if 6.0 <= soil_ph <= 7.5:
            factor += 0.05
        elif soil_ph < 5.5 or soil_ph > 8.5:
            factor -= 0.1
        
        # NPK factor (check if levels are adequate)
        npk_score = 0
        if n_level >= 60:
            npk_score += 1
        if p_level >= 30:
            npk_score += 1
        if k_level >= 40:
            npk_score += 1
        
        factor += (npk_score / 3) * 0.15
        
        return max(0.6, min(1.2, factor))
    
    def calculate_confidence_interval(
        self,
        estimated_yield: float,
        climate_factor: float,
        soil_factor: float
    ) -> Tuple[float, float]:
        """Calculate confidence interval for the estimate."""
        
        # Calculate uncertainty based on factors
        avg_factor = (climate_factor + soil_factor) / 2
        
        if avg_factor > 1.1:
            # High confidence
            margin = estimated_yield * 0.08
        elif avg_factor > 0.95:
            # Medium confidence
            margin = estimated_yield * 0.12
        else:
            # Lower confidence
            margin = estimated_yield * 0.18
        
        lower = round(estimated_yield - margin, 1)
        upper = round(estimated_yield + margin, 1)
        
        return lower, upper
    
    def estimate(
        self,
        crop_type: str,
        season: str,
        temperature: float,
        humidity: float,
        rainfall: float,
        soil_type: str,
        soil_ph: float,
        n_level: float,
        p_level: float,
        k_level: float,
        region: str = 'Central India'
    ) -> Dict:
        """
        Estimate crop yield based on all parameters.
        
        Returns:
            Dictionary with yield estimation details
        """
        
        if crop_type not in self.BASE_YIELDS:
            raise ValueError(f"No yield data available for {crop_type}")
        
        # Get base yield
        base_yield = self.BASE_YIELDS[crop_type]
        
        # Calculate factors
        climate_factor = self.calculate_climate_factor(
            crop_type, temperature, humidity, rainfall
        )
        
        soil_factor = self.calculate_soil_factor(
            soil_type, soil_ph, n_level, p_level, k_level
        )
        
        seasonal_factor = self.SEASONAL_FACTORS.get(season, 1.0)
        
        # Calculate estimated yield
        estimated_yield = base_yield * climate_factor * soil_factor * seasonal_factor
        
        # Add slight randomness for realism
        randomness = random.uniform(0.95, 1.05)
        estimated_yield = round(estimated_yield * randomness, 1)
        
        # Calculate confidence interval
        lower, upper = self.calculate_confidence_interval(
            estimated_yield, climate_factor, soil_factor
        )
        
        # Calculate regional average (slightly lower than optimal)
        regional_factor = self.REGIONAL_FACTORS.get(region, 0.85)
        regional_average = round(base_yield * regional_factor * seasonal_factor, 1)
        
        # Optimal yield (under perfect conditions)
        optimal_yield = round(base_yield * 1.15 * seasonal_factor, 1)
        
        return {
            'estimated_yield': estimated_yield,
            'confidence_interval': {'lower': lower, 'upper': upper},
            'regional_average': regional_average,
            'optimal_yield': optimal_yield
        }


# Global instance
yield_estimator = YieldEstimator()


def estimate_yield(
    crop_type: str,
    season: str,
    temperature: float,
    humidity: float,
    rainfall: float,
    soil_type: str,
    soil_ph: float,
    n_level: float,
    p_level: float,
    k_level: float
) -> Dict:
    """
    Main estimation function to be called by API endpoint.
    
    Returns:
        Dictionary with yield estimation details
    """
    return yield_estimator.estimate(
        crop_type, season, temperature, humidity, rainfall,
        soil_type, soil_ph, n_level, p_level, k_level
    )

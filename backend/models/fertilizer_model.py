"""
Fertilizer recommendation model using rule-based agricultural knowledge.
"""
from typing import Dict, Tuple


class FertilizerRecommender:
    """
    Rule-based fertilizer recommendation system.
    Based on crop requirements and current soil nutrient levels.
    """
    
    # Fertilizer recommendations for each crop
    FERTILIZER_DATA = {
        'Rice': {
            'fertilizer': 'Urea + DAP',
            'target_npk': {'n': 120, 'p': 60, 'k': 40},
            'quantity': 220,
            'timing': 'Two split applications - 50% at planting, 50% at tillering',
            'notes': 'Apply with adequate water. Avoid excess nitrogen in waterlogged conditions.'
        },
        'Wheat': {
            'fertilizer': 'Urea + SSP',
            'target_npk': {'n': 100, 'p': 50, 'k': 50},
            'quantity': 200,
            'timing': 'Half at sowing, half at tillering stage',
            'notes': 'Ensure proper moisture for nutrient uptake.'
        },
        'Maize': {
            'fertilizer': 'DAP + Urea',
            'target_npk': {'n': 110, 'p': 70, 'k': 60},
            'quantity': 240,
            'timing': 'Basal + first weeding + second weeding',
            'notes': 'Apply potash only if K level is very low.'
        },
        'Cotton': {
            'fertilizer': 'Urea + SSP + MOP',
            'target_npk': {'n': 100, 'p': 50, 'k': 50},
            'quantity': 200,
            'timing': 'Split into 3 doses at 30, 60, 90 days',
            'notes': 'Cotton is sensitive to excess nitrogen during flowering.'
        },
        'Sugarcane': {
            'fertilizer': 'Urea + DAP + MOP',
            'target_npk': {'n': 150, 'p': 75, 'k': 75},
            'quantity': 300,
            'timing': '4-6 weeks after planting',
            'notes': 'High nutrient requirement. Apply in split doses.'
        },
        'Soybean': {
            'fertilizer': 'DAP',
            'target_npk': {'n': 20, 'p': 60, 'k': 40},
            'quantity': 120,
            'timing': 'At sowing time',
            'notes': 'Soybean fixes atmospheric nitrogen, reduce N application.'
        },
        'Peanut': {
            'fertilizer': 'SSP + MOP',
            'target_npk': {'n': 25, 'p': 50, 'k': 75},
            'quantity': 150,
            'timing': 'Basal application at sowing',
            'notes': 'Legume crop - minimal nitrogen required. Focus on P and K.'
        },
        'Coconut': {
            'fertilizer': 'Urea + SSP + MOP',
            'target_npk': {'n': 100, 'p': 50, 'k': 140},
            'quantity': 290,
            'timing': 'Apply in 3-4 split doses throughout the year',
            'notes': 'High potassium requirement. Apply adequate organic matter.'
        },
        'Lentil': {
            'fertilizer': 'DAP',
            'target_npk': {'n': 20, 'p': 40, 'k': 20},
            'quantity': 80,
            'timing': 'Basal application at sowing',
            'notes': 'Pulse crop with nitrogen fixation. Minimal fertilizer needed.'
        },
        'Chickpea': {
            'fertilizer': 'DAP',
            'target_npk': {'n': 20, 'p': 40, 'k': 20},
            'quantity': 80,
            'timing': 'Basal application',
            'notes': 'Legume crop. Use rhizobium culture for better nitrogen fixation.'
        }
    }
    
    def adjust_for_current_levels(
        self,
        target_npk: Dict[str, float],
        current_n: float,
        current_p: float,
        current_k: float
    ) -> Dict[str, float]:
        """Adjust NPK recommendations based on current soil levels."""
        
        adjusted = {
            'n': max(0, target_npk['n'] - current_n),
            'p': max(0, target_npk['p'] - current_p),
            'k': max(0, target_npk['k'] - current_k)
        }
        
        return adjusted
    
    def adjust_for_ph(
        self,
        fertilizer: str,
        soil_ph: float
    ) -> Tuple[str, str]:
        """Adjust fertilizer recommendation based on soil pH."""
        
        notes_addition = ""
        
        if soil_ph < 6.0:
            notes_addition = " Soil is acidic - consider lime application before fertilizer."
            if 'DAP' in fertilizer:
                fertilizer = fertilizer  # DAP is suitable for acidic soils
        elif soil_ph > 8.0:
            notes_addition = " Soil is alkaline - use acidic fertilizers. Consider sulfur application."
            if 'Urea' in fertilizer:
                fertilizer = fertilizer.replace('Urea', 'Ammonium Sulfate')
        
        return fertilizer, notes_addition
    
    def calculate_quantity(
        self,
        base_quantity: float,
        adjusted_npk: Dict[str, float],
        target_npk: Dict[str, float]
    ) -> float:
        """Calculate adjusted fertilizer quantity."""
        
        # Calculate reduction factor based on existing nutrients
        total_target = sum(target_npk.values())
        total_needed = sum(adjusted_npk.values())
        
        if total_target == 0:
            return base_quantity
        
        reduction_factor = total_needed / total_target
        adjusted_quantity = base_quantity * reduction_factor
        
        return round(adjusted_quantity, 0)
    
    def recommend(
        self,
        crop_type: str,
        current_n: float,
        current_p: float,
        current_k: float,
        soil_ph: float,
        soil_type: str
    ) -> Dict:
        """
        Generate fertilizer recommendation.
        
        Returns:
            Dictionary with fertilizer details
        """
        
        if crop_type not in self.FERTILIZER_DATA:
            raise ValueError(f"No fertilizer data available for {crop_type}")
        
        # Get base recommendation
        base_data = self.FERTILIZER_DATA[crop_type]
        
        # Adjust for current nutrient levels
        adjusted_npk = self.adjust_for_current_levels(
            base_data['target_npk'],
            current_n,
            current_p,
            current_k
        )
        
        # Adjust for pH
        fertilizer, ph_note = self.adjust_for_ph(
            base_data['fertilizer'],
            soil_ph
        )
        
        # Calculate adjusted quantity
        quantity = self.calculate_quantity(
            base_data['quantity'],
            adjusted_npk,
            base_data['target_npk']
        )
        
        # Adjust notes for soil type
        soil_note = ""
        if 'Clay' in soil_type:
            soil_note = " Clay soil retains nutrients well - split applications recommended."
        elif 'Sandy' in soil_type or 'Laterite' in soil_type:
            soil_note = " Sandy/Laterite soil - apply in smaller, frequent doses to prevent leaching."
        
        return {
            'recommended_fertilizer': fertilizer,
            'npk_ratio': adjusted_npk,
            'quantity_per_hectare': quantity,
            'application_timing': base_data['timing'],
            'notes': base_data['notes'] + ph_note + soil_note
        }


# Global instance
fertilizer_recommender = FertilizerRecommender()


def recommend_fertilizer(
    crop_type: str,
    current_n: float,
    current_p: float,
    current_k: float,
    soil_ph: float,
    soil_type: str
) -> Dict:
    """
    Main recommendation function to be called by API endpoint.
    
    Returns:
        Dictionary with fertilizer recommendation details
    """
    return fertilizer_recommender.recommend(
        crop_type, current_n, current_p, current_k, soil_ph, soil_type
    )

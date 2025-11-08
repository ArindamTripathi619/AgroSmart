import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Sprout, AlertCircle } from 'lucide-react';
import { Button, Card, FormField, LoadingSpinner } from '../components/ui';
import * as api from '../services/api';

interface CropPredictionResult {
  predicted_crop: string;
  confidence_score: number;
  alternative_crops: { crop: string; score: number }[];
}

export function CropPrediction() {
  const [formData, setFormData] = useState({
    soil_type: 'Black Soil',
    n_level: 50,
    p_level: 50,
    k_level: 50,
    temperature: 25,
    humidity: 60,
    rainfall: 100,
    ph_level: 7,
    region: 'North India',
  });

  const [result, setResult] = useState<CropPredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const soilTypes = ['Black Soil', 'Red Soil', 'Laterite Soil', 'Alluvial Soil', 'Clay Soil'];
  const regions = [
    'North India',
    'South India',
    'East India',
    'West India',
    'Central India',
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: ['n_level', 'p_level', 'k_level', 'temperature', 'humidity', 'rainfall', 'ph_level'].includes(
        name
      )
        ? parseFloat(value)
        : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Call the real API endpoint
      const prediction = await api.predictCrop({
        soil_type: formData.soil_type,
        n_level: formData.n_level,
        p_level: formData.p_level,
        k_level: formData.k_level,
        temperature: formData.temperature,
        humidity: formData.humidity,
        rainfall: formData.rainfall,
        ph_level: formData.ph_level,
        region: formData.region,
      });

      // Convert confidence scores from decimal to percentage
      const formattedResult = {
        ...prediction,
        confidence_score: prediction.confidence_score * 100,
        alternative_crops: prediction.alternative_crops.map(crop => ({
          ...crop,
          score: crop.score * 100
        }))
      };

      setResult(formattedResult);
    } catch (err) {
      setError('Failed to generate prediction. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-2xl px-md">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-2xl"
        >
          <h1 className="text-h1 font-poppins font-bold text-neutral-900 dark:text-white mb-md">
            Crop Prediction
          </h1>
          <p className="text-body text-neutral-600 dark:text-neutral-300">
            Discover the ideal crop for your soil and climate conditions
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-2xl">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="p-lg">
              <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-lg">
                Enter Your Data
              </h2>

              <form onSubmit={handleSubmit} className="space-y-md">
                <FormField
                  label="Soil Type"
                  tooltip="Select the primary soil type of your farm"
                >
                  <select
                    name="soil_type"
                    value={formData.soil_type}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    {soilTypes.map((soil) => (
                      <option key={soil} value={soil}>
                        {soil}
                      </option>
                    ))}
                  </select>
                </FormField>

                <FormField
                  label="Nitrogen (N) Level (ppm)"
                  tooltip="Parts per million of nitrogen in soil"
                >
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="n_level"
                      min="0"
                      max="200"
                      value={formData.n_level}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.n_level}</span>
                      <span>200</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Phosphorus (P) Level (ppm)">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="p_level"
                      min="0"
                      max="100"
                      value={formData.p_level}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.p_level}</span>
                      <span>100</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Potassium (K) Level (ppm)">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="k_level"
                      min="0"
                      max="200"
                      value={formData.k_level}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.k_level}</span>
                      <span>200</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Temperature (°C)">
                  <input
                    type="number"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleInputChange}
                    className="input-field"
                    step="0.1"
                  />
                </FormField>

                <FormField label="Humidity (%)">
                  <input
                    type="number"
                    name="humidity"
                    value={formData.humidity}
                    onChange={handleInputChange}
                    className="input-field"
                    min="0"
                    max="100"
                    step="0.1"
                  />
                </FormField>

                <FormField label="Rainfall (mm)">
                  <input
                    type="number"
                    name="rainfall"
                    value={formData.rainfall}
                    onChange={handleInputChange}
                    className="input-field"
                    step="0.1"
                  />
                </FormField>

                <FormField label="Soil pH Level">
                  <input
                    type="number"
                    name="ph_level"
                    value={formData.ph_level}
                    onChange={handleInputChange}
                    className="input-field"
                    min="0"
                    max="14"
                    step="0.1"
                  />
                </FormField>

                <FormField label="Region">
                  <select
                    name="region"
                    value={formData.region}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    {regions.map((region) => (
                      <option key={region} value={region}>
                        {region}
                      </option>
                    ))}
                  </select>
                </FormField>

                {error && (
                  <div className="p-md bg-error/10 border border-error rounded-lg flex gap-md text-error">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-xs" />
                    <p>{error}</p>
                  </div>
                )}

                <Button type="submit" isLoading={loading} className="w-full">
                  Predict Crop
                </Button>
              </form>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <AnimatePresence>
              {result ? (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="space-y-lg"
                >
                  <Card className="p-lg bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-900/10">
                    <div className="text-center">
                      <div className="mb-md p-lg bg-white dark:bg-dark-surface rounded-lg inline-block">
                        <Sprout className="w-12 h-12 text-primary-600" />
                      </div>
                      <h3 className="text-h2 font-poppins font-bold text-primary-700 dark:text-primary-300 mb-md">
                        {result.predicted_crop}
                      </h3>
                      <div className="flex items-center justify-center gap-md mb-lg">
                        <div className="relative w-24 h-24">
                          <svg
                            className="w-full h-full transform -rotate-90"
                            viewBox="0 0 100 100"
                          >
                            <circle
                              cx="50"
                              cy="50"
                              r="45"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="4"
                              className="text-neutral-200 dark:text-neutral-700"
                            />
                            <circle
                              cx="50"
                              cy="50"
                              r="45"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="4"
                              strokeDasharray={`${(result.confidence_score / 100) * 282.7} 282.7`}
                              className="text-success transition-all duration-500"
                            />
                          </svg>
                          <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-2xl font-poppins font-bold text-primary-600 dark:text-primary-300">
                              {result.confidence_score.toFixed(1)}%
                            </span>
                          </div>
                        </div>
                      </div>
                      <p className="text-body text-neutral-600 dark:text-neutral-300">
                        Confidence Score
                      </p>
                    </div>
                  </Card>

                  {result.alternative_crops && result.alternative_crops.length > 0 && (
                    <Card className="p-lg">
                      <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                        Alternative Crops
                      </h4>
                      <div className="space-y-md">
                        {result.alternative_crops.map((alt, idx) => (
                          <div key={idx} className="flex items-center justify-between p-md bg-neutral-50 dark:bg-dark-bg rounded-lg">
                            <span className="font-medium text-neutral-900 dark:text-white">
                              {alt.crop}
                            </span>
                            <span className="text-sm font-semibold text-primary-600 dark:text-primary-300">
                              {alt.score.toFixed(1)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </Card>
                  )}

                  <Card className="p-lg">
                    <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                      Suitability Scores
                    </h4>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={[
                        { name: result.predicted_crop, score: result.confidence_score },
                        ...result.alternative_crops.map(crop => ({
                          name: crop.crop,
                          score: crop.score
                        }))
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="score" fill="#2E7D32" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Card>
                </motion.div>
              ) : (
                <Card className="p-lg h-full flex items-center justify-center">
                  <div className="text-center">
                    <div className="mb-md p-lg bg-primary-50 dark:bg-primary-900/20 rounded-lg inline-block">
                      <Sprout className="w-12 h-12 text-primary-400" />
                    </div>
                    <p className="text-body text-neutral-600 dark:text-neutral-400">
                      {loading ? 'Analyzing your soil data...' : 'Fill in your farm data and click "Predict Crop" to get started'}
                    </p>
                    {loading && (
                      <div className="mt-lg">
                        <LoadingSpinner />
                      </div>
                    )}
                  </div>
                </Card>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

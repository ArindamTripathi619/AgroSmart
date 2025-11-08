import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Droplets, AlertCircle } from 'lucide-react';
import { Button, Card, FormField, LoadingSpinner } from '../components/ui';
import * as api from '../services/api';

interface FertilizerResult {
  recommended_fertilizer: string;
  npk_ratio: { n: number; p: number; k: number };
  quantity_per_hectare: number;
  application_timing: string;
  notes: string;
}

export function FertilizerRecommendation() {
  const [formData, setFormData] = useState({
    crop_type: 'Rice',
    current_n: 50,
    current_p: 30,
    current_k: 40,
    soil_ph: 7,
    soil_type: 'Alluvial Soil',
  });

  const [result, setResult] = useState<FertilizerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean'];
  const soilTypes = ['Black Soil', 'Red Soil', 'Laterite Soil', 'Alluvial Soil', 'Clay Soil'];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: ['current_n', 'current_p', 'current_k', 'soil_ph'].includes(name)
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
      const recommendation = await api.recommendFertilizer({
        crop_type: formData.crop_type,
        current_n: formData.current_n,
        current_p: formData.current_p,
        current_k: formData.current_k,
        soil_ph: formData.soil_ph,
        soil_type: formData.soil_type,
      });

      setResult(recommendation);
    } catch (err) {
      setError('Failed to generate recommendation. Please try again.');
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
            Fertilizer Recommendation
          </h1>
          <p className="text-body text-neutral-600 dark:text-neutral-300">
            Get personalized fertilizer suggestions for optimal crop growth
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
                Soil Analysis
              </h2>

              <form onSubmit={handleSubmit} className="space-y-md">
                <FormField
                  label="Crop Type"
                  tooltip="Select your primary crop"
                >
                  <select
                    name="crop_type"
                    value={formData.crop_type}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    {crops.map((crop) => (
                      <option key={crop} value={crop}>
                        {crop}
                      </option>
                    ))}
                  </select>
                </FormField>

                <FormField
                  label="Current Nitrogen (N) Level"
                  tooltip="Current N content in ppm"
                >
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="current_n"
                      min="0"
                      max="200"
                      value={formData.current_n}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.current_n}</span>
                      <span>200</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Current Phosphorus (P) Level">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="current_p"
                      min="0"
                      max="100"
                      value={formData.current_p}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.current_p}</span>
                      <span>100</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Current Potassium (K) Level">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="current_k"
                      min="0"
                      max="200"
                      value={formData.current_k}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0</span>
                      <span className="font-semibold text-primary-600">{formData.current_k}</span>
                      <span>200</span>
                    </div>
                  </div>
                </FormField>

                <FormField
                  label="Soil pH Level"
                  tooltip="Measure acidity/alkalinity (7 is neutral)"
                >
                  <input
                    type="number"
                    name="soil_ph"
                    value={formData.soil_ph}
                    onChange={handleInputChange}
                    className="input-field"
                    min="0"
                    max="14"
                    step="0.1"
                  />
                </FormField>

                <FormField label="Soil Type">
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

                {error && (
                  <div className="p-md bg-error/10 border border-error rounded-lg flex gap-md text-error">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-xs" />
                    <p>{error}</p>
                  </div>
                )}

                <Button type="submit" isLoading={loading} className="w-full">
                  Get Recommendation
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
                  <Card className="p-lg bg-gradient-to-br from-secondary-50 to-secondary-100 dark:from-secondary-900/20 dark:to-secondary-900/10">
                    <div className="text-center">
                      <div className="mb-md p-lg bg-white dark:bg-dark-surface rounded-lg inline-block">
                        <Droplets className="w-12 h-12 text-secondary-600" />
                      </div>
                      <h3 className="text-h2 font-poppins font-bold text-secondary-700 dark:text-secondary-300 mb-md">
                        {result.recommended_fertilizer}
                      </h3>
                      <p className="text-body text-neutral-600 dark:text-neutral-300 mb-md">
                        Quantity: <span className="font-semibold">{result.quantity_per_hectare} kg/ha</span>
                      </p>
                      <p className="text-small text-neutral-500 dark:text-neutral-400">
                        {result.application_timing}
                      </p>
                    </div>
                  </Card>

                  <Card className="p-lg">
                    <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
                      NPK Ratio Comparison
                    </h4>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={[
                        {
                          name: 'Nutrient',
                          Current: formData.current_n,
                          Recommended: result.npk_ratio.n,
                        },
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Current" fill="#FDD835" />
                        <Bar dataKey="Recommended" fill="#2E7D32" />
                      </BarChart>
                    </ResponsiveContainer>
                    <div className="mt-lg grid grid-cols-3 gap-md">
                      <div className="text-center p-md bg-neutral-50 dark:bg-dark-bg rounded-lg">
                        <p className="text-small text-neutral-600 dark:text-neutral-400 mb-xs">Nitrogen</p>
                        <p className="text-h3 font-poppins font-bold text-neutral-900 dark:text-white">
                          {result.npk_ratio.n}
                        </p>
                      </div>
                      <div className="text-center p-md bg-neutral-50 dark:bg-dark-bg rounded-lg">
                        <p className="text-small text-neutral-600 dark:text-neutral-400 mb-xs">Phosphorus</p>
                        <p className="text-h3 font-poppins font-bold text-neutral-900 dark:text-white">
                          {result.npk_ratio.p}
                        </p>
                      </div>
                      <div className="text-center p-md bg-neutral-50 dark:bg-dark-bg rounded-lg">
                        <p className="text-small text-neutral-600 dark:text-neutral-400 mb-xs">Potassium</p>
                        <p className="text-h3 font-poppins font-bold text-neutral-900 dark:text-white">
                          {result.npk_ratio.k}
                        </p>
                      </div>
                    </div>
                  </Card>

                  <Card className="p-lg border-l-4 border-l-warning">
                    <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                      Important Notes
                    </h4>
                    <p className="text-body text-neutral-600 dark:text-neutral-300">
                      {result.notes}
                    </p>
                  </Card>
                </motion.div>
              ) : (
                <Card className="p-lg h-full flex items-center justify-center">
                  <div className="text-center">
                    <div className="mb-md p-lg bg-secondary-50 dark:bg-secondary-900/20 rounded-lg inline-block">
                      <Droplets className="w-12 h-12 text-secondary-400" />
                    </div>
                    <p className="text-body text-neutral-600 dark:text-neutral-400">
                      {loading ? 'Analyzing your soil data...' : 'Enter your soil data to get a personalized recommendation'}
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

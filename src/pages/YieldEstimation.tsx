import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ComposedChart, LineChart, Line } from 'recharts';
import { TrendingUp, AlertCircle } from 'lucide-react';
import { Button, Card, FormField, LoadingSpinner } from '../components/ui';
import * as api from '../services/api';

interface YieldResult {
  estimated_yield: number;
  confidence_interval: { lower: number; upper: number };
  regional_average: number;
  optimal_yield: number;
}

export function YieldEstimation() {
  const [formData, setFormData] = useState({
    crop_type: 'Rice',
    area_hectares: 1.0,
    season: 'Kharif',
    temperature: 25,
    humidity: 70,
    rainfall: 100,
    soil_type: 'Alluvial Soil',
    soil_ph: 7,
    n_level: 80,
    p_level: 40,
    k_level: 50,
  });

  const [result, setResult] = useState<YieldResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane'];
  const seasons = ['Kharif', 'Rabi', 'Zaid'];
  const soilTypes = ['Black Soil', 'Red Soil', 'Laterite Soil', 'Alluvial Soil', 'Clay Soil'];

  const seasonalData = [
    { month: 'Month 1', yield: 0 },
    { month: 'Month 2', yield: 0.8 },
    { month: 'Month 3', yield: 1.8 },
    { month: 'Month 4', yield: 3.2 },
    { month: 'Month 5', yield: 4.5 },
    { month: 'Month 6', yield: 5.2 },
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: [
        'temperature',
        'humidity',
        'rainfall',
        'soil_ph',
        'n_level',
        'p_level',
        'k_level',
      ].includes(name)
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
      const yieldData = await api.estimateYield({
        crop_type: formData.crop_type,
        area_hectares: formData.area_hectares,
        season: formData.season,
        temperature: formData.temperature,
        humidity: formData.humidity,
        rainfall: formData.rainfall,
        soil_type: formData.soil_type,
        soil_ph: formData.soil_ph,
        n_level: formData.n_level,
        p_level: formData.p_level,
        k_level: formData.k_level,
      });

      // Round yield values to 2 decimal places for cleaner display
      const formattedResult = {
        ...yieldData,
        estimated_yield: Math.round(yieldData.estimated_yield * 100) / 100,
        confidence_interval: {
          lower: Math.round(yieldData.confidence_interval.lower * 100) / 100,
          upper: Math.round(yieldData.confidence_interval.upper * 100) / 100
        },
        regional_average: Math.round(yieldData.regional_average * 100) / 100,
        optimal_yield: Math.round(yieldData.optimal_yield * 100) / 100
      };

      setResult(formattedResult);
    } catch (err) {
      setError('Failed to generate estimate. Please try again.');
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
            Yield Estimation
          </h1>
          <p className="text-body text-neutral-600 dark:text-neutral-300">
            Predict your harvest yield using environmental and soil parameters
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
                Farm Parameters
              </h2>

              <form onSubmit={handleSubmit} className="space-y-md">
                <FormField label="Crop Type">
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

                <FormField label="Season">
                  <select
                    name="season"
                    value={formData.season}
                    onChange={handleInputChange}
                    className="input-field"
                  >
                    {seasons.map((season) => (
                      <option key={season} value={season}>
                        {season}
                      </option>
                    ))}
                  </select>
                </FormField>

                <FormField label="Temperature (°C)">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="temperature"
                      min="0"
                      max="50"
                      value={formData.temperature}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0°</span>
                      <span className="font-semibold text-accent-600">{formData.temperature}°C</span>
                      <span>50°</span>
                    </div>
                  </div>
                </FormField>

                <FormField label="Humidity (%)">
                  <div className="space-y-2">
                    <input
                      type="range"
                      name="humidity"
                      min="0"
                      max="100"
                      value={formData.humidity}
                      onChange={handleInputChange}
                      className="w-full"
                    />
                    <div className="flex justify-between text-small text-neutral-600 dark:text-neutral-400">
                      <span>0%</span>
                      <span className="font-semibold text-accent-600">{formData.humidity}%</span>
                      <span>100%</span>
                    </div>
                  </div>
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

                <FormField label="Soil pH">
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

                <FormField label="Nitrogen (N) Level">
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

                <FormField label="Phosphorus (P) Level">
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

                <FormField label="Potassium (K) Level">
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

                {error && (
                  <div className="p-md bg-error/10 border border-error rounded-lg flex gap-md text-error">
                    <AlertCircle className="w-5 h-5 flex-shrink-0 mt-xs" />
                    <p>{error}</p>
                  </div>
                )}

                <Button type="submit" isLoading={loading} className="w-full">
                  Estimate Yield
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
                  <Card className="p-lg bg-gradient-to-br from-accent-50 to-accent-100 dark:from-accent-900/20 dark:to-accent-900/10">
                    <div className="text-center">
                      <div className="mb-md p-lg bg-white dark:bg-dark-surface rounded-lg inline-block">
                        <TrendingUp className="w-12 h-12 text-accent-600" />
                      </div>
                      <p className="text-small text-neutral-600 dark:text-neutral-400 mb-sm">
                        Estimated Yield
                      </p>
                      <h3 className="text-4xl font-poppins font-bold text-accent-700 dark:text-accent-300">
                        {result.estimated_yield}{' '}
                        <span className="text-lg text-neutral-600 dark:text-neutral-400">
                          {formData.crop_type === 'Sugarcane' ? 'tonnes/ha' : 'tonnes/ha'}
                        </span>
                      </h3>
                      <p className="text-small text-neutral-500 dark:text-neutral-400 mt-md">
                        Range: {result.confidence_interval.lower} - {result.confidence_interval.upper} tonnes/ha
                      </p>
                    </div>
                  </Card>

                  <Card className="p-lg">
                    <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
                      Yield Comparison
                    </h4>
                    <ResponsiveContainer width="100%" height={300}>
                      <ComposedChart data={[
                        {
                          name: 'Your Farm',
                          yield: result.estimated_yield,
                          regional: result.regional_average,
                          optimal: result.optimal_yield,
                        },
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="yield" fill="#4FC3F7" name="Your Yield" />
                        <Bar dataKey="regional" fill="#FDD835" name="Regional Avg" />
                        <Bar dataKey="optimal" fill="#2E7D32" name="Optimal" />
                      </ComposedChart>
                    </ResponsiveContainer>
                  </Card>

                  <Card className="p-lg">
                    <h4 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
                      Seasonal Growth Projection
                    </h4>
                    <ResponsiveContainer width="100%" height={250}>
                      <LineChart data={seasonalData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Line
                          type="monotone"
                          dataKey="yield"
                          stroke="#2E7D32"
                          strokeWidth={3}
                          dot={{ fill: '#2E7D32', r: 5 }}
                          activeDot={{ r: 7 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </Card>

                  <Card className="p-lg border-l-4 border-l-success">
                    <div className="flex items-start gap-md">
                      <div className="text-success">✓</div>
                      <div>
                        <h4 className="font-semibold text-neutral-900 dark:text-white mb-sm">
                          Performance Analysis
                        </h4>
                        <p className="text-body text-neutral-600 dark:text-neutral-300">
                          Your estimated yield is{' '}
                          <span className="font-semibold">
                            {(((result.estimated_yield - result.regional_average) / result.regional_average) * 100).toFixed(1)}%
                          </span>
                          {result.estimated_yield > result.regional_average ? ' above' : ' below'} the regional average.
                        </p>
                      </div>
                    </div>
                  </Card>
                </motion.div>
              ) : (
                <Card className="p-lg h-full flex items-center justify-center">
                  <div className="text-center">
                    <div className="mb-md p-lg bg-accent-50 dark:bg-accent-900/20 rounded-lg inline-block">
                      <TrendingUp className="w-12 h-12 text-accent-400" />
                    </div>
                    <p className="text-body text-neutral-600 dark:text-neutral-400">
                      {loading ? 'Calculating yield estimate...' : 'Enter your farm parameters to estimate yield'}
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

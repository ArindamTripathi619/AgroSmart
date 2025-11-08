import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { BarChart3, TrendingUp, Calendar } from 'lucide-react';
import { Button, Card, LoadingSpinner } from '../components/ui';

interface DashboardStats {
  totalPredictions: number;
  averageConfidence: number;
  topCrop: string;
  topRegion: string;
}

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalPredictions: 0,
    averageConfidence: 0,
    topCrop: 'N/A',
    topRegion: 'N/A',
  });

  const [cropData, setCropData] = useState<any[]>([]);
  const [timeSeriesData, setTimeSeriesData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('week');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Mock dashboard data for now - can be replaced with real API call later
        const mockPredictions = [
          { predicted_crop: 'Rice', region: 'North India', confidence_score: 92, created_at: new Date().toISOString() },
          { predicted_crop: 'Wheat', region: 'North India', confidence_score: 88, created_at: new Date().toISOString() },
          { predicted_crop: 'Maize', region: 'South India', confidence_score: 85, created_at: new Date().toISOString() },
          { predicted_crop: 'Rice', region: 'East India', confidence_score: 90, created_at: new Date().toISOString() },
          { predicted_crop: 'Cotton', region: 'West India', confidence_score: 87, created_at: new Date().toISOString() },
        ];

        const predictions = mockPredictions;

        if (predictions && predictions.length > 0) {
          const cropCounts = predictions.reduce(
            (acc, pred) => {
              const crop = pred.predicted_crop;
              acc[crop] = (acc[crop] || 0) + 1;
              return acc;
            },
            {} as Record<string, number>
          );

          const cropChartData = Object.entries(cropCounts)
            .map(([crop, count]) => ({
              name: crop,
              count,
            }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 5);

          setCropData(cropChartData);

          const avgConfidence = (
            predictions.reduce((sum, p) => sum + p.confidence_score, 0) / predictions.length
          ).toFixed(1);

          setStats({
            totalPredictions: predictions.length,
            averageConfidence: parseFloat(avgConfidence),
            topCrop: predictions[0].predicted_crop,
            topRegion: predictions[0].region,
          });

          const last7Days = predictions.slice(0, 7).reverse();
          const timeData = last7Days.map((pred, idx) => ({
            day: `Day ${idx + 1}`,
            confidence: pred.confidence_score,
            timestamp: pred.created_at,
          }));
          setTimeSeriesData(timeData);
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [dateRange]);

  const COLORS = ['#2E7D32', '#66BB6A', '#FDD835', '#4FC3F7', '#FFA726'];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  if (loading) {
    return (
      <div className="min-h-screen py-2xl px-md flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-2xl px-md">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-2xl"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-md">
            <div>
              <h1 className="text-h1 font-poppins font-bold text-neutral-900 dark:text-white mb-md">
                Analytics Dashboard
              </h1>
              <p className="text-body text-neutral-600 dark:text-neutral-300">
                View predictions history and system performance metrics
              </p>
            </div>
            <div className="flex gap-sm">
              {['week', 'month', 'all'].map((range) => (
                <Button
                  key={range}
                  variant={dateRange === range ? 'primary' : 'secondary'}
                  size="sm"
                  onClick={() => setDateRange(range)}
                >
                  {range.charAt(0).toUpperCase() + range.slice(1)}
                </Button>
              ))}
            </div>
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-lg mb-2xl"
        >
          {[
            {
              icon: BarChart3,
              label: 'Total Predictions',
              value: stats.totalPredictions,
              color: 'text-primary-600',
            },
            {
              icon: TrendingUp,
              label: 'Avg Confidence',
              value: `${stats.averageConfidence}%`,
              color: 'text-accent-600',
            },
            {
              icon: BarChart3,
              label: 'Top Crop',
              value: stats.topCrop,
              color: 'text-secondary-600',
            },
            {
              icon: Calendar,
              label: 'Top Region',
              value: stats.topRegion,
              color: 'text-success',
            },
          ].map((stat, idx) => {
            const Icon = stat.icon;
            return (
              <motion.div key={idx} variants={itemVariants}>
                <Card className="p-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-small text-neutral-600 dark:text-neutral-400 mb-md">
                        {stat.label}
                      </p>
                      <p className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white">
                        {stat.value}
                      </p>
                    </div>
                    <div className={`p-md bg-neutral-100 dark:bg-neutral-700 rounded-lg ${stat.color}`}>
                      <Icon className="w-6 h-6" />
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 lg:grid-cols-2 gap-2xl mb-2xl"
        >
          <motion.div variants={itemVariants}>
            <Card className="p-lg">
              <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
                Top Predicted Crops
              </h3>
              {cropData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={cropData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#2E7D32" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-72 flex items-center justify-center text-neutral-500">
                  No data available
                </div>
              )}
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-lg">
              <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
                Prediction Distribution
              </h3>
              {cropData.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={cropData}
                      dataKey="count"
                      nameKey="name"
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      label
                    >
                      {cropData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-72 flex items-center justify-center text-neutral-500">
                  No data available
                </div>
              )}
            </Card>
          </motion.div>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="p-lg">
            <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-lg">
              Confidence Trend
            </h3>
            {timeSeriesData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" />
                  <XAxis dataKey="day" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="confidence"
                    stroke="#2E7D32"
                    strokeWidth={2}
                    dot={{ fill: '#2E7D32', r: 5 }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-72 flex items-center justify-center text-neutral-500">
                No data available
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </div>
  );
}

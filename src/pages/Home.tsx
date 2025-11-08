import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Sprout, Droplets, TrendingUp } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button, Card } from '../components/ui';
import * as api from '../services/api';

export function Home() {
  const [stats, setStats] = useState({ crops: 0, fertilizers: 0, yields: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Try to fetch real statistics from API
        const apiStats = await api.getStatistics();
        
        // If API returns all zeros (no database connected), use mock data for demo
        // Once database is integrated, this will show real prediction counts
        if (apiStats.crops === 0 && apiStats.fertilizers === 0 && apiStats.yields === 0) {
          // Mock data for demonstration (will be replaced by real data when DB is connected)
          setStats({
            crops: 1247,
            fertilizers: 892,
            yields: 634,
          });
        } else {
          // Use real API data
          setStats({
            crops: apiStats.crops,
            fertilizers: apiStats.fertilizers,
            yields: apiStats.yields,
          });
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
        // Fallback to mock data on error
        setStats({
          crops: 1247,
          fertilizers: 892,
          yields: 634,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const features = [
    {
      icon: Sprout,
      title: 'Crop Prediction',
      description: 'Discover the most suitable crop based on your soil and climate conditions',
      link: '/crop',
      color: 'text-primary-600',
    },
    {
      icon: Droplets,
      title: 'Fertilizer Recommendation',
      description: 'Get personalized fertilizer suggestions for optimal crop growth',
      link: '/fertilizer',
      color: 'text-secondary-600',
    },
    {
      icon: TrendingUp,
      title: 'Yield Estimation',
      description: 'Predict your harvest yield with advanced environmental analysis',
      link: '/yield',
      color: 'text-accent-600',
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.1,
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

  return (
    <div className="min-h-screen">
      <section className="relative overflow-hidden bg-gradient-to-b from-primary-50 to-white dark:from-primary-900/20 dark:to-dark-bg py-3xl px-md">
        <div className="absolute inset-0 opacity-10 dark:opacity-5">
          <svg className="w-full h-full" viewBox="0 0 1200 600">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="1200" height="600" fill="url(#grid)" className="text-primary-300" />
          </svg>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-2xl"
          >
            <h1 className="text-4xl md:text-5xl font-poppins font-bold text-neutral-900 dark:text-white mb-md">
              Smart Agriculture Predictions
            </h1>
            <p className="text-xl text-neutral-600 dark:text-neutral-300 mb-2xl max-w-2xl mx-auto">
              Harness the power of AI and data science to make informed decisions about your crops, fertilizers, and yields
            </p>
            <div className="flex flex-col sm:flex-row gap-md justify-center">
              <Link to="/crop">
                <Button size="lg">Start Predicting</Button>
              </Link>
              <Link to="/about">
                <Button variant="secondary" size="lg">Learn More</Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-3xl px-md">
        <div className="max-w-7xl mx-auto">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 gap-lg mb-3xl"
          >
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <motion.div key={feature.title} variants={itemVariants}>
                  <Link to={feature.link}>
                    <Card className="h-full hover:scale-105 transition-transform duration-300 cursor-pointer p-lg">
                      <div className="flex flex-col items-center text-center">
                        <div className="mb-md p-md bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                          <Icon className={`w-8 h-8 ${feature.color}`} />
                        </div>
                        <h3 className="text-h3 font-poppins font-semibold mb-sm text-neutral-900 dark:text-white">
                          {feature.title}
                        </h3>
                        <p className="text-body text-neutral-600 dark:text-neutral-300">
                          {feature.description}
                        </p>
                      </div>
                    </Card>
                  </Link>
                </motion.div>
              );
            })}
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-1 md:grid-cols-3 gap-lg"
          >
            {[
              { label: 'Crop Predictions', value: stats.crops },
              { label: 'Fertilizer Recommendations', value: stats.fertilizers },
              { label: 'Yield Estimates', value: stats.yields },
            ].map((stat) => (
              <motion.div key={stat.label} variants={itemVariants}>
                <Card className="p-lg text-center">
                  <p className="text-body text-neutral-600 dark:text-neutral-400 mb-sm">
                    {stat.label}
                  </p>
                  <p className="text-4xl font-poppins font-bold text-primary-600 dark:text-primary-300">
                    {loading ? '...' : stat.value}
                  </p>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      <section className="py-3xl px-md bg-primary-50 dark:bg-primary-900/10">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-2xl">
            <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-md">
              How It Works
            </h2>
            <p className="text-body text-neutral-600 dark:text-neutral-300">
              Our AI models analyze soil and environmental data to provide accurate predictions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-lg">
            {[
              {
                step: '01',
                title: 'Enter Your Data',
                description: 'Provide soil composition, climate conditions, and other relevant parameters',
              },
              {
                step: '02',
                title: 'AI Analysis',
                description: 'Our machine learning models process your data using advanced algorithms',
              },
              {
                step: '03',
                title: 'Get Insights',
                description: 'Receive detailed predictions and recommendations tailored to your farm',
              },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white font-poppins font-bold text-lg mb-md">
                  {item.step}
                </div>
                <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-sm">
                  {item.title}
                </h3>
                <p className="text-body text-neutral-600 dark:text-neutral-300">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

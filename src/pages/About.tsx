import React from 'react';
import { motion } from 'framer-motion';
import { Leaf, Code2, Database, Zap, Github, Mail } from 'lucide-react';
import { Card } from '../components/ui';

export function About() {
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

  return (
    <div className="min-h-screen py-2xl px-md">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-3xl"
        >
          <h1 className="text-h1 font-poppins font-bold text-neutral-900 dark:text-white mb-md">
            About AgroSmart
          </h1>
          <p className="text-body text-neutral-600 dark:text-neutral-300 max-w-2xl mx-auto">
            Empowering farmers with AI-driven insights for smarter, more sustainable agriculture
          </p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 lg:grid-cols-2 gap-2xl mb-3xl"
        >
          <motion.div variants={itemVariants}>
            <Card className="p-lg h-full">
              <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-md">
                Our Mission
              </h2>
              <p className="text-body text-neutral-600 dark:text-neutral-300 leading-relaxed mb-md">
                AgroSmart is dedicated to revolutionizing agriculture by making advanced AI predictions accessible to farmers of all backgrounds. We believe that data-driven decision making should be simple, intuitive, and actionable.
              </p>
              <p className="text-body text-neutral-600 dark:text-neutral-300 leading-relaxed">
                Our platform analyzes soil composition, climate conditions, and environmental factors to provide personalized recommendations for crop selection, fertilizer application, and yield optimization.
              </p>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-lg h-full bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-900/10">
              <h2 className="text-h2 font-poppins font-bold text-primary-700 dark:text-primary-300 mb-lg">
                Key Features
              </h2>
              <ul className="space-y-md">
                {[
                  'Crop Prediction based on soil and climate',
                  'Fertilizer Recommendations optimized for yield',
                  'Yield Estimation with confidence intervals',
                  'Real-time Analytics Dashboard',
                  'Historical prediction tracking',
                  'User-friendly interface design',
                ].map((feature, idx) => (
                  <li key={idx} className="flex items-start gap-md">
                    <span className="text-primary-600 dark:text-primary-300 mt-1">✓</span>
                    <span className="text-body text-neutral-700 dark:text-neutral-300">{feature}</span>
                  </li>
                ))}
              </ul>
            </Card>
          </motion.div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mb-3xl"
        >
          <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-lg text-center">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-lg">
            {[
              {
                step: 1,
                title: 'Data Input',
                description: 'Enter your soil composition, climate data, and farm parameters through our intuitive interface',
              },
              {
                step: 2,
                title: 'AI Analysis',
                description: 'Our machine learning models trained on agricultural datasets analyze your inputs',
              },
              {
                step: 3,
                title: 'Insights & Recommendations',
                description: 'Receive actionable predictions with confidence scores and detailed explanations',
              },
            ].map((item, idx) => (
              <motion.div key={idx} variants={itemVariants}>
                <Card className="p-lg text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-300 font-poppins font-bold mb-md">
                    {item.step}
                  </div>
                  <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                    {item.title}
                  </h3>
                  <p className="text-body text-neutral-600 dark:text-neutral-300">
                    {item.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mb-3xl"
        >
          <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-lg text-center">
            Technology Stack
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-lg">
            {[
              { icon: Code2, name: 'React + TypeScript', description: 'Interactive UI' },
              { icon: Database, name: 'FastAPI + Python', description: 'ML Backend' },
              { icon: Zap, name: 'Scikit-learn', description: 'ML Models' },
              { icon: Leaf, name: 'Tailwind CSS', description: 'Modern Styling' },
            ].map((tech, idx) => {
              const Icon = tech.icon;
              return (
                <motion.div key={idx} variants={itemVariants}>
                  <Card className="p-lg text-center">
                    <Icon className="w-8 h-8 mx-auto mb-md text-primary-600 dark:text-primary-300" />
                    <h4 className="font-poppins font-semibold text-neutral-900 dark:text-white mb-xs">
                      {tech.name}
                    </h4>
                    <p className="text-small text-neutral-600 dark:text-neutral-400">
                      {tech.description}
                    </p>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mb-3xl"
        >
          <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-lg text-center">
            Project Methodology
          </h2>
          <Card className="p-lg">
            <div className="space-y-md">
              <div>
                <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                  Data Collection & Preprocessing
                </h3>
                <p className="text-body text-neutral-600 dark:text-neutral-300">
                  Our models are trained on comprehensive agricultural datasets including historical crop yields, soil compositions, weather patterns, and farming practices from multiple regions.
                </p>
              </div>
              <div>
                <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                  Machine Learning Models
                </h3>
                <p className="text-body text-neutral-600 dark:text-neutral-300">
                  We employ state-of-the-art algorithms including Random Forests, Gradient Boosting, and Neural Networks to provide accurate predictions with confidence intervals.
                </p>
              </div>
              <div>
                <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md">
                  Validation & Testing
                </h3>
                <p className="text-body text-neutral-600 dark:text-neutral-300">
                  All predictions are validated against real-world agricultural outcomes with rigorous cross-validation and performance metrics tracking.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="mb-3xl"
        >
          <h2 className="text-h2 font-poppins font-bold text-neutral-900 dark:text-white mb-lg text-center">
            Team
          </h2>
          <Card className="p-lg">
            <p className="text-body text-neutral-600 dark:text-neutral-300 mb-lg">
              AgroSmart is developed as part of the IND4 initiative - a collaborative effort combining expertise in agriculture, data science, and software engineering to tackle real-world farming challenges.
            </p>
            <p className="text-body text-neutral-600 dark:text-neutral-300">
              Our diverse team brings together researchers, developers, and agricultural experts working towards sustainable farming practices through technological innovation.
            </p>
          </Card>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 md:grid-cols-2 gap-lg"
        >
          <motion.div variants={itemVariants}>
            <Card className="p-lg">
              <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md flex items-center gap-md">
                <Github className="w-6 h-6 text-neutral-700 dark:text-neutral-300" />
                Open Source
              </h3>
              <p className="text-body text-neutral-600 dark:text-neutral-300 mb-md">
                AgroSmart is built with open-source technologies and contributes to the agricultural tech community.
              </p>
              <a
                href="https://github.com"
                className="text-primary-600 dark:text-primary-300 font-semibold hover:underline"
              >
                View on GitHub →
              </a>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-lg">
              <h3 className="text-h3 font-poppins font-semibold text-neutral-900 dark:text-white mb-md flex items-center gap-md">
                <Mail className="w-6 h-6 text-neutral-700 dark:text-neutral-300" />
                Get in Touch
              </h3>
              <p className="text-body text-neutral-600 dark:text-neutral-300 mb-md">
                Have questions or feedback? We'd love to hear from you!
              </p>
              <a
                href="mailto:info@agrosmart.com"
                className="text-primary-600 dark:text-primary-300 font-semibold hover:underline"
              >
                info@agrosmart.com
              </a>
            </Card>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-3xl pt-lg border-t border-neutral-200 dark:border-neutral-700"
        >
          <p className="text-small text-neutral-600 dark:text-neutral-400">
            © 2024 AgroSmart. Built with ❤️ for sustainable agriculture.
          </p>
        </motion.div>
      </div>
    </div>
  );
}

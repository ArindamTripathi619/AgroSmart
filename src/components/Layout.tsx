import React from 'react';
import { Navigation } from './Navigation';

interface LayoutProps {
  children: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-neutral-50 dark:bg-dark-bg">
      <Navigation />
      <main className="flex-1">
        {children}
      </main>
      <footer className="bg-primary-50 dark:bg-dark-surface border-t border-neutral-200 dark:border-neutral-700 mt-3xl py-3xl px-md">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2xl mb-2xl">
            <div>
              <h3 className="text-h3 font-poppins font-bold text-primary-600 dark:text-primary-300 mb-md">AgroSmart</h3>
              <p className="text-small text-neutral-600 dark:text-neutral-400">
                Intelligent predictions for smarter farming
              </p>
            </div>
            <div>
              <h4 className="font-poppins font-semibold text-neutral-900 dark:text-white mb-md">Features</h4>
              <ul className="space-y-sm text-small text-neutral-600 dark:text-neutral-400">
                <li>Crop Prediction</li>
                <li>Fertilizer Recommendation</li>
                <li>Yield Estimation</li>
              </ul>
            </div>
            <div>
              <h4 className="font-poppins font-semibold text-neutral-900 dark:text-white mb-md">Project</h4>
              <p className="text-small text-neutral-600 dark:text-neutral-400 mb-md">
                Built with React, TypeScript, FastAPI, and Scikit-learn
              </p>
            </div>
          </div>
          <div className="border-t border-neutral-300 dark:border-neutral-600 pt-lg">
            <p className="text-center text-small text-neutral-600 dark:text-neutral-400">
              © 2024 AgroSmart. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

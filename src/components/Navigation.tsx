import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Leaf, Moon, Sun, Menu, X } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './ui';

export function Navigation() {
  const { isDark, toggleTheme } = useTheme();
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const navLinks = [
    { label: 'Home', path: '/' },
    { label: 'Crop Prediction', path: '/crop' },
    { label: 'Fertilizer', path: '/fertilizer' },
    { label: 'Yield Estimation', path: '/yield' },
    { label: 'Dashboard', path: '/dashboard' },
    { label: 'About', path: '/about' },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-white dark:bg-dark-surface border-b border-neutral-200 dark:border-neutral-700 shadow-sm">
      <div className="max-w-7xl mx-auto px-md py-md">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-md hover:opacity-80 transition-opacity">
            <div className="gradient-primary p-2 rounded-lg">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <span className="text-h3 font-poppins font-bold text-primary-600 dark:text-primary-300 hidden sm:inline">
              AgroSmart
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-lg">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`text-small font-medium transition-colors ${
                  isActive(link.path)
                    ? 'text-primary-600 dark:text-primary-300'
                    : 'text-neutral-600 dark:text-neutral-400 hover:text-primary-600 dark:hover:text-primary-300'
                }`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-sm">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              aria-label="Toggle theme"
            >
              {isDark ? (
                <Sun className="w-5 h-5 text-yellow-400" />
              ) : (
                <Moon className="w-5 h-5 text-neutral-600" />
              )}
            </button>

            <Link to="/crop" className="hidden sm:inline">
              <Button size="sm">Predict Now</Button>
            </Link>

            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {mobileOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden mt-md pt-md border-t border-neutral-200 dark:border-neutral-700"
            >
              <div className="flex flex-col gap-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={() => setMobileOpen(false)}
                    className={`px-md py-sm rounded-lg transition-colors ${
                      isActive(link.path)
                        ? 'bg-primary-50 dark:bg-primary-900 text-primary-600 dark:text-primary-300'
                        : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-700'
                    }`}
                  >
                    {link.label}
                  </Link>
                ))}
                <Button onClick={() => setMobileOpen(false)} className="w-full mt-sm">
                  Predict Now
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </nav>
  );
}

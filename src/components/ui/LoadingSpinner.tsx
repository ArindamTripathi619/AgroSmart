import React from 'react';
import { Leaf } from 'lucide-react';
import { motion } from 'framer-motion';

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
      >
        <Leaf className="w-8 h-8 text-primary-500" />
      </motion.div>
    </div>
  );
}

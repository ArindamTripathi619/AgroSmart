import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  hover?: boolean;
}

export function Card({ children, hover = true, className = '', ...props }: CardProps) {
  return (
    <div
      className={`card ${hover ? 'hover:shadow-lg' : ''} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

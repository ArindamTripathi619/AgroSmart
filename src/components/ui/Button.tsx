import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className = '',
  children,
  ...props
}: ButtonProps) {
  const baseClass = 'font-poppins font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed';

  const variantClass = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    ghost: 'btn-ghost',
  }[variant];

  const sizeClass = {
    sm: 'px-3 py-1 text-small',
    md: 'px-md py-sm text-body',
    lg: 'px-lg py-md text-body',
  }[size];

  return (
    <button
      disabled={disabled || isLoading}
      className={`${baseClass} ${variantClass} ${sizeClass} ${className}`}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <span className="w-4 h-4 rounded-full border-2 border-current border-t-transparent animate-spin" />
          Loading...
        </span>
      ) : (
        children
      )}
    </button>
  );
}

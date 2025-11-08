import React from 'react';

interface FormFieldProps {
  label: string;
  error?: string;
  tooltip?: string;
  required?: boolean;
  children: React.ReactNode;
}

export function FormField({ label, error, tooltip, required, children }: FormFieldProps) {
  return (
    <div className="mb-md">
      <div className="flex items-center gap-xs mb-xs">
        <label className="form-label">
          {label}
          {required && <span className="text-error ml-xs">*</span>}
        </label>
        {tooltip && (
          <div className="group relative cursor-help">
            <span className="text-neutral-400 text-xs">ⓘ</span>
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 bg-neutral-900 text-white text-xs rounded-lg p-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 pointer-events-none z-10">
              {tooltip}
            </div>
          </div>
        )}
      </div>
      {children}
      {error && <p className="text-error text-small mt-xs">{error}</p>}
    </div>
  );
}

/**
 * Button UI Component
 * 
 * A reusable button component with various styles and states.
 */

import React from 'react';
import './Button.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  className?: string;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  fullWidth?: boolean;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  className = '',
  icon,
  iconPosition = 'left',
  fullWidth = false
}) => {
  const buttonClasses = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    loading && 'btn--loading',
    disabled && 'btn--disabled',
    fullWidth && 'btn--full-width',
    className
  ].filter(Boolean).join(' ');

  const handleClick = () => {
    if (!disabled && !loading && onClick) {
      onClick();
    }
  };

  const renderIcon = () => {
    if (!icon) return null;
    
    return (
      <span className={`btn__icon btn__icon--${iconPosition}`}>
        {icon}
      </span>
    );
  };

  const renderContent = () => {
    if (loading) {
      return (
        <>
          <span className="btn__spinner" />
          <span className="btn__text">Loading...</span>
        </>
      );
    }

    return (
      <>
        {icon && iconPosition === 'left' && renderIcon()}
        <span className="btn__text">{children}</span>
        {icon && iconPosition === 'right' && renderIcon()}
      </>
    );
  };

  return (
    <button
      type={type}
      className={buttonClasses}
      onClick={handleClick}
      disabled={disabled || loading}
    >
      {renderContent()}
    </button>
  );
};

export default Button;

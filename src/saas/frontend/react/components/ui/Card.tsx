/**
 * Card UI Component
 * 
 * A reusable card component with header, content, and footer sections.
 */

import React from 'react';
import './Card.css';

// ============================================================================
// INTERFACES
// ============================================================================

interface CardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outlined';
  padding?: 'none' | 'small' | 'medium' | 'large';
}

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

interface CardTitleProps {
  children: React.ReactNode;
  className?: string;
  level?: 1 | 2 | 3 | 4 | 5 | 6;
}

// ============================================================================
// MAIN COMPONENT
// ============================================================================

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  variant = 'default',
  padding = 'medium'
}) => {
  const cardClasses = [
    'card',
    `card--${variant}`,
    `card--padding-${padding}`,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={cardClasses}>
      {children}
    </div>
  );
};

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  className = ''
}) => {
  const headerClasses = [
    'card__header',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={headerClasses}>
      {children}
    </div>
  );
};

export const CardContent: React.FC<CardContentProps> = ({
  children,
  className = ''
}) => {
  const contentClasses = [
    'card__content',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={contentClasses}>
      {children}
    </div>
  );
};

export const CardFooter: React.FC<CardFooterProps> = ({
  children,
  className = ''
}) => {
  const footerClasses = [
    'card__footer',
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={footerClasses}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<CardTitleProps> = ({
  children,
  className = '',
  level = 3
}) => {
  const titleClasses = [
    'card__title',
    `card__title--h${level}`,
    className
  ].filter(Boolean).join(' ');

  const Tag = `h${level}` as keyof JSX.IntrinsicElements;

  return (
    <Tag className={titleClasses}>
      {children}
    </Tag>
  );
};

export default Card;

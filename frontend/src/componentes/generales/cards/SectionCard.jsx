import React from 'react';
import './SectionCard.css';

export const SectionCard = ({ titulo, children, className = "" }) => {
    return (
        <div className={`section-card ${className}`}>
            {titulo && <h3 className="section-card-title">{titulo}</h3>}
            <div className="section-card-content">
                {children}
            </div>
        </div>
    );
};

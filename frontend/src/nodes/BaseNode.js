import { useState } from 'react';
import { Handle } from 'reactflow';

export const BaseNode = ({
  id,
  data,
  nodeType,
  fields = [],
  handles = [],
  style = {},
  className = '',
  children
}) => {
  const [fieldValues, setFieldValues] = useState(() => {
    const initial = {};
    fields.forEach(field => {
      initial[field.name] =
        data?.[field.name] ?? field.defaultValue ?? '';
    });
    return initial;
  });

  const handleFieldChange = (fieldName, value) => {
    setFieldValues(prev => ({
      ...prev,
      [fieldName]: value
    }));
    if (data?.onChange) {
      data.onChange(id, fieldName, value);
    }
  };

  const renderField = (field) => {
    const value = fieldValues[field.name];
    if (!field.type) return null;
    return (
      <label key={field.name} className="node-field">
        {field.label}
        {field.type === 'select' ? (
          <select
            value={value}
            onChange={(e) =>
              handleFieldChange(field.name, e.target.value)
            }
          >
            {field.options?.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        ) : field.type === 'textarea' ? (
          <textarea
            value={value}
            onChange={(e) =>
              handleFieldChange(field.name, e.target.value)
            }
            placeholder={field.placeholder}
            rows={field.rows || 3}
          />
        ) : (
          <input
            type="text"
            value={value}
            onChange={(e) =>
              handleFieldChange(field.name, e.target.value)
            }
            placeholder={field.placeholder}
          />
        )}
      </label>
    );
  };

  const renderHandles = () =>
    handles.map(handle => (
      <Handle
        key={handle.name}
        type={handle.type}
        position={handle.position}
        id={handle.id || `${id}-${handle.name}`}
        style={handle.style || {}}
      />
    ));

  const baseStyle = {
    width: 220,
    border: '2px solid #e9ecef',
    borderRadius: 12,
    background: '#ffffff',
    padding: 12,
    boxShadow: '0 4px 10px rgba(0,0,0,0.08)',
    fontFamily: "'Segoe UI', sans-serif",
    transition: 'all 0.2s ease',
    ...style
  };

  return (
    <div className={`base-node ${className}`} style={baseStyle}>
      {renderHandles()}
      <div className="node-header">
        <strong className="node-title">{nodeType}</strong>
      </div>
      <div className="node-content">
        {fields.map(renderField)}
        {children}
      </div>
    </div>
  );
};
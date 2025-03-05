// src/components/MessageNode.jsx
import React, { memo } from 'react';
import { Handle, Position } from 'reactflow';

function MessageNode({ data }) {
  const { message_id, text, command, buttons, input_handler, button_width } = data;

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 border-2 border-gray-200 min-w-[200px]">
      <Handle type="target" position={Position.Top} />

      {/* Message ID and Command */}
      <div className="flex justify-between items-center mb-2">
        <span className="font-bold text-sm">ID: {message_id}</span>
        {command && (
          <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
            {command}
          </span>
        )}
      </div>

      {/* Message Text */}
      <p className="text-sm mb-3">{text}</p>

      {/* Buttons */}
      {buttons && buttons.length > 0 && (
        <div className="space-y-2">
          <div className="text-xs font-semibold text-gray-500">Buttons:</div>
          <div className={`grid grid-cols-${button_width || 1} gap-3 relative pb-8`}>
            {buttons.map((button, index) => (
              <div
                key={index}
                className="relative bg-gray-100 text-xs px-3 py-1.5 rounded inline-flex items-center"
                style={{ 
                  color: button.color,
                  width: 'fit-content'
                }}
              >
                {button.text}
                <Handle
                  type="source"
                  position={Position.Right}
                  id={`button-${index}`}
                  style={{
                    right: -10,
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: button.color,
                    width: '8px',
                    height: '8px'
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input Handler */}
      {input_handler && (
        <div className="mt-2">
          <div className="text-xs font-semibold text-gray-500">Input Handler:</div>
          <div className="text-xs text-purple-600">
            Key: {input_handler.key}
            <Handle
              type="source"
              position={Position.Bottom}
              id="input-handler"
              style={{ bottom: -10, background: '#9333ea' }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default memo(MessageNode);
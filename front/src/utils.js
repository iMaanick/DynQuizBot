// src/utils.js
const BUTTON_COLORS = [
  '#ff6b6b', // Red
  '#4ecdc4', // Teal
  '#45b7d1', // Blue
  '#96ceb4', // Green
  '#ffeead', // Yellow
  '#ff9999', // Pink
];

export const validateJSON = (jsonString) => {
  if (!jsonString.trim()) {
    return { isValid: false, error: 'JSON input is empty' };
  }

  try {
    const parsed = JSON.parse(jsonString);
    
    if (!Array.isArray(parsed)) {
      return { isValid: false, error: 'JSON must be an array of messages' };
    }

    for (const message of parsed) {
      if (!message.message_id || !message.text) {
        return { isValid: false, error: 'Each message must have message_id and text' };
      }
    }

    return { isValid: true, error: null };
  } catch (err) {
    return { isValid: false, error: 'Invalid JSON format: ' + err.message };
  }
};

export const processMessages = (messages) => {
  const nodes = [];
  const edges = [];
  const usedColors = new Map(); // Track used colors for consistent button colors

  messages.forEach((message, index) => {
    // Create node
    nodes.push({
      id: message.message_id.toString(),
      type: 'messageNode',
      position: { x: index * 300, y: index * 100 }, // Initial positioning
      data: {
        ...message,
        button_width: message.button_width || 1,
        buttons: message.buttons?.map((button, buttonIndex) => ({
          ...button,
          color: getButtonColor(button.text, usedColors),
        })),
      },
    });

    // Create edges from buttons
    if (message.buttons) {
      message.buttons.forEach((button, buttonIndex) => {
        const buttonColor = getButtonColor(button.text, usedColors);
        edges.push({
          id: `edge-${message.message_id}-${button.target_message_id}-${buttonIndex}`,
          source: message.message_id.toString(),
          target: button.target_message_id.toString(),
          sourceHandle: `button-${buttonIndex}`,
          style: { stroke: buttonColor },
          type: 'smoothstep',
        });
      });
    }

    // Create edge from input handler
    if (message.input_handler) {
      edges.push({
        id: `edge-${message.message_id}-${message.input_handler.target_message_id}-input`,
        source: message.message_id.toString(),
        target: message.input_handler.target_message_id.toString(),
        sourceHandle: 'input-handler',
        style: { stroke: '#9333ea' },
        type: 'smoothstep',
      });
    }
  });

  return { nodes, edges };
};

const getButtonColor = (buttonText, usedColors) => {
  if (usedColors.has(buttonText)) {
    return usedColors.get(buttonText);
  }
  const color = BUTTON_COLORS[usedColors.size % BUTTON_COLORS.length];
  usedColors.set(buttonText, color);
  return color;
};

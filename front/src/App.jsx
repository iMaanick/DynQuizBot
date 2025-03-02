// src/App.jsx
import React, { useState, useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  ReactFlowProvider,
  useNodesState,
  useEdgesState
} from 'reactflow';
import 'reactflow/dist/style.css';
import MessageNode from './components/MessageNode';
import { validateJSON, processMessages } from './utils';

const nodeTypes = {
  messageNode: MessageNode,
};

function App() {
  const [jsonInput, setJsonInput] = useState('');
  const [error, setError] = useState('');
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const handleJsonChange = (e) => {
    setJsonInput(e.target.value);
    setError('');
  };

  const handleVisualize = useCallback(() => {
    try {
      const validationResult = validateJSON(jsonInput);
      if (!validationResult.isValid) {
        setError(validationResult.error);
        return;
      }

      const { nodes: newNodes, edges: newEdges } = processMessages(JSON.parse(jsonInput));
      setNodes(newNodes);
      setEdges(newEdges);
      setError('');
    } catch (err) {
      setError('Failed to process the JSON data: ' + err.message);
    }
  }, [jsonInput, setNodes, setEdges]);

  const handleSend = async () => {
    try {
      const response = await fetch('/res', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonInput,
      });
      
      if (!response.ok) {
        throw new Error('Failed to send data');
      }
      
      alert('Data sent successfully!');
    } catch (err) {
      setError('Failed to send data: ' + err.message);
    }
  };

  return (
    <div className="flex h-screen">
      {/* Left Panel - JSON Input */}
      <div className="w-1/3 p-4 bg-gray-100 flex flex-col">
        <h2 className="text-xl font-bold mb-4">Message Flow Visualizer</h2>
        <textarea
          className="flex-1 p-2 border rounded-md mb-4 font-mono text-sm resize-none"
          value={jsonInput}
          onChange={handleJsonChange}
          placeholder="Paste your JSON here..."
        />
        {error && (
          <div className="text-red-500 mb-4 text-sm">
            {error}
          </div>
        )}
        <div className="flex gap-2">
          <button
            onClick={handleVisualize}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Visualize
          </button>
          <button
            onClick={handleSend}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Send
          </button>
        </div>
      </div>

      {/* Right Panel - Flow Visualization */}
      <div className="w-2/3 h-full">
        <ReactFlowProvider>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </ReactFlowProvider>
      </div>
    </div>
  );
}

export default App;
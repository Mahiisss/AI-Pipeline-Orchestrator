import { BaseNode } from './BaseNode';
import { Position } from 'reactflow';

export const InputNode = ({ id, data }) => {
  const fields = [
    {
      name: 'inputName',
      type: 'text',
      label: 'Name',
      defaultValue: id.replace('customInput-', 'input_')
    },
    {
      name: 'inputType',
      type: 'select',
      label: 'Type',
      defaultValue: 'Text',
      options: [
        { value: 'Text', label: 'Text' },
        { value: 'File', label: 'File' }
      ]
    },
    {
      name: 'value',
      type: 'text',
      label: 'Value',
      defaultValue: 'hello kintsugi',
      placeholder: 'Enter input value'
    }
  ];

  const handles = [
    {
      name: 'value',
      type: 'source',
      position: Position.Right
    }
  ];

  return (
    <BaseNode
      id={id}
      data={data}
      nodeType="Input"
      fields={fields}
      handles={handles}
      className="input-node"
      style={{
        backgroundColor: '#e3f2fd'
      }}
    />
  );
};